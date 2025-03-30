from crewai import Crew, Task, Agent
from crewai_tools import SerperDevTool
from langchain_ibm import WatsonxLLM
import os
from config import WATSONX_APIKEY, WATSONX_PROJECT_ID, WATSONX_URL, WATSONX_PLATFORM_URL, WATSONX_MODEL_ID, SERPER_API_KEY, OPENWEATHERMAP_API_KEY
import sys
from datetime import datetime
import logging
import requests
from langchain_core.tools import Tool

"""
# Set all required environment variables
os.environ["WATSONX_APIKEY"] = WATSONX_APIKEY
os.environ["WATSONX_PROJECT_ID"] = WATSONX_PROJECT_ID
os.environ["WATSONX_URL"] = WATSONX_URL
os.environ["WATSONX_PLATFORM_URL"] = WATSONX_PLATFORM_URL
os.environ["WATSONX_MODEL_ID"] = WATSONX_MODEL_ID
os.environ["SERPER_API_KEY"] = SERPER_API_KEY
os.environ["OPENWEATHERMAP_API_KEY"] = OPENWEATHERMAP_API_KEY
"""

class OpenWeatherMapTool:
    """Tool to fetch weather data from OpenWeatherMap API."""
    
    def __init__(self):
        self.api_key = OPENWEATHERMAP_API_KEY

    def fetch_weather(self, city: str) -> str:
        """Fetch weather data for a specified city."""
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
        
        try:
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                weather_description = data['weather'][0]['description']
                temperature = data['main']['temp']
                return f"The current weather in {city} is {weather_description} with a temperature of {temperature}°C."
            else:
                return f"Error fetching weather data: {data.get('message', 'Unknown error')}"
        except Exception as e:
            logging.error(f"Error fetching weather: {str(e)}")
            return "Unable to fetch weather data at this time."

class MusicAssistant:
    def __init__(self):
        self.llm = WatsonxLLM(
            model_id=WATSONX_MODEL_ID,
            url=WATSONX_URL,
            params={
                "decoding_method": "sample",
                "max_new_tokens": 250,
                "temperature": 0.5,
                "top_k": 50,
                "top_p": 0.95
            },
            project_id=WATSONX_PROJECT_ID,
        )
        self.search = SerperDevTool()
        self.weather_tool = OpenWeatherMapTool()
        self.setup_agents()
        self.conversation_history = []
        self.current_context = None
        self.logger = logging.getLogger(__name__)

    def setup_agents(self):
        # MAYA - Main Conversational Agent with weather tool
        self.maya = Agent(
            llm=self.llm,
            role="Senior Music Industry Advisor",
            goal="Help users navigate the music industry and develop their musical skills, ask other agents for help and call tools when needed",
            backstory="I'm MAYA, your dedicated music industry advisor with expertise in trends, artist development, and creative direction",
            tools=[self.search, Tool(
                name="weather_search",
                description="Fetch current weather information for a specified city.",
                func=self.weather_tool.fetch_weather
            )],
            allow_delegation=True,
            verbose=1,
            max_iterations=1,
            max_time=200
        )

        # Trend Analyst with enhanced search capabilities
        self.trend_analyst = Agent(
            llm=self.llm,
            role="Music Trend Analyst",
            goal="Provide data-driven insights into music market trends and audience preferences",
            backstory="Expert in music analytics and market trends with access to real-time industry data",
            tools=[self.search],
            verbose=1,
            max_iterations=1,
            max_time=200
        )

        # Creative Assistant
        self.creative = Agent(
            llm=self.llm,
            role="Creative Music Assistant",
            goal="Generate original musical compositions and lyrical content.",
            backstory="Experienced in songwriting and music theory, stays updated with current trends.",
            tools=[],
            verbose=1,
            max_iterations=1,
            max_time=200
        )

    def start_new_chat(self) -> dict:
        """Start a new chat session"""
        self.conversation_history = []
        self.current_context = None
        greeting = self.get_greeting()
        return {
            "message": greeting,
            "timestamp": datetime.now().isoformat()
        }

    def get_greeting(self) -> str:
        """Get the initial greeting message"""
        greeting_task = Task(
            description="""
            Create a warm, engaging welcome message for a new user.
            Include:
            1. A friendly introduction as MAYA (Music Assistant for Your Activities)
            2. A small explanation of your capabilities
            3. An invitation to start the conversation
            Keep it short and sweet with artistic flair.
            """,
            expected_output="A welcoming greeting message",
            agent=self.maya
        )
        
        try:
            return greeting_task.execute()
        except Exception as e:
            self.logger.error(f"Error generating greeting: {str(e)}")
            return """
            👋 Welcome! I'm MAYA, your Music Assistant.
            I'm here to help you with anything music-related.
            How can I assist you today?
            """

    def run_interaction(self, user_input: str) -> dict:
        """Run interaction with delegation to specialized agents"""
        try:
            if not user_input.strip():
                return {
                    "message": self.show_menu(),
                    "timestamp": datetime.now().isoformat()
                }

            # Handle menu options
            if user_input.lower() == 'new':
                return {
                    "message": self.start_new_chat(),
                    "timestamp": datetime.now().isoformat()
                }
            elif user_input.lower() == 'exit':
                return {
                    "message": "Thank you for using MAYA! Have a musical day! 🎵",
                    "timestamp": datetime.now().isoformat()
                }
            elif user_input.lower() == 'menu':
                return {
                    "message": self.show_menu(),
                    "timestamp": datetime.now().isoformat()
                }
            elif user_input.lower() == 'save':
                return {
                    "message": self.save_last_conversation(),
                    "timestamp": datetime.now().isoformat()
                }

            context = self._get_conversation_context()
            
            # First, perform a search to gather relevant information
            search_task = Task(
                description=f"""
                Perform an initial search to gather relevant information about:
                Query: {user_input}
                Context: {context}
                
                Focus on finding the most recent and relevant information.
                Return the search results in a clear, structured format.
                """,
                expected_output="Initial search results",
                agent=self.maya,
                max_iterations=1,
                max_time=60
            )
            
            initial_search_results = search_task.execute()
            
            # Use search results to inform the analysis
            analysis_task = Task(
                description=f"""
                Analyze this query and determine which specialists should handle it:
                Query: {user_input}
                Context: {context}
                Initial Search Results: {initial_search_results}
                
                If the query involves:
                - Music industry news, trends, market analysis -> Delegate to Trend Analyst
                - Creative aspects (composition, chords, scale modes, lyrics, artistic direction) -> Delegate to Creative Assistant
                - If the query requires an internet search, indicate that a search should be performed.
                - Multiple aspects -> Coordinate responses from relevant agents
                
                Return the decision as: "TREND", "CREATIVE", "SEARCH", or "BOTH"
                """,
                expected_output="Analysis decision for delegation",
                agent=self.maya,
                max_iterations=1,
                max_time=60
            )
            
            delegation_decision = analysis_task.execute().strip().upper()
            responses = []
            
            if delegation_decision in ["TREND", "BOTH"]:
                trend_task = Task(
                    description=f"""
                    Analyze the following query from a music industry trend perspective:
                    Query: {user_input}
                    Context: {context}
                    Initial Search Results: {initial_search_results}
                    
                    Provide insights on current trends, market analysis, and industry patterns.
                    Focus on delivering clear, concise, and accurate information in a single response.
                    Use the search results to support your analysis.
                    """,
                    expected_output="Trend analysis and insights",
                    agent=self.trend_analyst,
                    max_iterations=1,
                    max_time=180
                )
                responses.append(f"📊 Industry Analysis:\n{trend_task.execute()}")

            if delegation_decision in ["CREATIVE", "BOTH"]:
                creative_task = Task(
                    description=f"""
                    Address the following query from a creative and artistic perspective:
                    Query: {user_input}
                    Context: {context}
                    Initial Search Results: {initial_search_results}
                    
                    Provide creative insights, musical suggestions, or artistic direction.
                    Include detailed chord progressions, scales, and lyrical content if applicable.
                    
                    IMPORTANT: When generating musical content:
                    1. For chord progressions, format them clearly with:
                       - Chord names (e.g., Am, F, C, G)
                       - Time signature
                       - Any specific voicings or variations
                    2. For lyrics, format them with:
                       - Clear verse/chorus structure
                       - Line breaks
                       - Rhyme scheme indicators if applicable
                    3. Always mark the start of musical content with "🎵 MUSICAL CONTENT START 🎵"
                    4. Always mark the end of musical content with "🎵 MUSICAL CONTENT END 🎵"
                    
                    Focus on delivering complete, well-structured content in a single response.
                    Use the search results to inform your creative suggestions.
                    """,
                    expected_output="Creative insights and suggestions",
                    agent=self.creative,
                    max_iterations=1,
                    max_time=180
                )
                creative_response = creative_task.execute()
                responses.append(f"🎵 Creative Input:\n{creative_response}")
                
                if "🎵 MUSICAL CONTENT START 🎵" in creative_response:
                    self.save_creative_output(creative_response)

            if responses:
                synthesis_task = Task(
                    description=f"""
                    Synthesize these specialist insights into a coherent response:
                    Initial Search Results: {initial_search_results}
                    Specialist Responses: {' '.join(responses)}
                    
                    Create a clear, unified response that incorporates all relevant insights.
                    Focus on delivering a well-structured, complete response in a single iteration.
                    Use the search results to support and validate the specialist insights.
                    """,
                    expected_output="Synthesized response",
                    agent=self.maya,
                    max_iterations=1,
                    max_time=120
                )
                final_response = synthesis_task.execute()
            else:
                final_response = Task(
                    description=f"""
                    Provide a direct response to:
                    Query: {user_input}
                    Context: {context}
                    Initial Search Results: {initial_search_results}
                    
                    Focus on delivering a clear, complete response in a single iteration.
                    Use the search results to support your response.
                    """,
                    expected_output="Direct response",
                    agent=self.maya,
                    max_iterations=1,
                    max_time=60
                ).execute()

            self.conversation_history.append({
                'input': user_input,
                'output': final_response,
                'timestamp': datetime.now().isoformat()
            })

            return {
                "message": final_response,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error in interaction: {str(e)}")
            return {
                "message": f"I apologize, but I encountered an error. Please try again. Error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    def _get_conversation_context(self) -> str:
        """Get context from the last 5 conversations"""
        if not self.conversation_history:
            return "No previous conversation context."
        
        recent_conversations = self.conversation_history[-1:]
        context = "\n".join([
            f"User: {conv['input']}\nMAYA: {conv['output']}"
            for conv in recent_conversations
        ])
        
        return context

    def get_conversation_history(self):
        """Get the current conversation history"""
        return self.conversation_history

    def clear_conversation(self):
        """Clear the conversation history"""
        self.conversation_history = []
        self.current_context = None

    def show_menu(self) -> str:
        """Show menu options when user sends empty input"""
        menu = """
        👋 Welcome! Here are your options:
        
        1. Start a new chat (type 'new')
        2. Show menu options (type 'menu')
        3. Save last conversation (type 'save')
        4. Exit (type 'exit')
        5. Continue current conversation (just type your question)
        
        What would you like to do?
        """
        return menu

    def save_last_conversation(self) -> str:
        """Save the last conversation to a text file"""
        if not self.conversation_history:
            return "No conversation to save. Start a new chat first!"
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"outputs/conversation_{timestamp}.txt"
            
            # Create outputs directory if it doesn't exist
            os.makedirs("outputs", exist_ok=True)
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"MAYA AI Conversation - {timestamp}\n")
                f.write("=" * 50 + "\n\n")
                
                for conv in self.conversation_history:
                    f.write(f"User: {conv['input']}\n")
                    f.write(f"MAYA: {conv['output']}\n")
                    f.write("-" * 30 + "\n")
            
            return f"Conversation saved successfully to {filename}"
        except Exception as e:
            self.logger.error(f"Error saving conversation: {str(e)}")
            return f"Error saving conversation: {str(e)}"

    def save_creative_output(self, creative_output: str):
        """Save creative output to a file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"outputs/creative_output_{timestamp}.txt"
            
            # Create outputs directory if it doesn't exist
            os.makedirs("outputs", exist_ok=True)
            
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"MAYA AI Creative Output - {timestamp}\n")
                f.write("=" * 50 + "\n\n")
                f.write(creative_output)
            
            return f"Creative output saved successfully to {filename}"
        except Exception as e:
            self.logger.error(f"Error saving creative output: {str(e)}")
            return f"Error saving creative output: {str(e)}"

def main():
    """Main function to run the music assistant"""
    try:
        assistant = MusicAssistant()
        print("\n" + assistant.get_greeting())
        print("\nPress Enter for menu options at any time.")
        
        while True:
            user_input = input("\nYour input: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nThank you for using MAYA! Have a musical day! 🎵")
                break
            
            response = assistant.run_interaction(user_input)
            print(f"\nMAYA: {response['message']}")
            
            # Show menu again if response was menu-related
            if "Welcome!" in response['message']:
                continue
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logging.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()
