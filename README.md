# MayaAI - Music Industry Assistant
## AI Agent Hackathon with IBM watsonx.ai

MayaAI is an intelligent music industry assistant powered by CrewAI, featuring three specialized agents working together to provide comprehensive music industry insights and creative assistance.

under 3 minute demo of the project:


[![Video Demo](http://img.youtube.com/vi/sPpk7xr73II/0.jpg)](https://youtu.be/sPpk7xr73II)


## Features

### 1. MAYA (Senior Artist Manager)
- Develops comprehensive career development plans
- Creates 6-month career roadmaps
- Identifies potential collaboration opportunities
- Provides brand positioning strategies
- Analyzes target audience demographics
- Plans media and performance engagements

**Technical Configuration:**
- Tools: SerperDevTool (for web search), OpenWeatherMapTool (configured manually for weather data)
- Max Iterations: 1
- Max Time: 200 seconds
- Allows Delegation: True
- Temperature: 0.5
- Model: WatsonX (granite-3-8b-instruct)

### 2. Music Researcher
- Conducts data-driven music market research
- Analyzes current genre popularity trends
- Identifies emerging music styles
- Provides demographic listening preferences
- Suggests potential collaborations
- Recommends cover songs based on audience data

**Technical Configuration:**
- Tools: SerperDevTool (for market research and trend analysis)
- Max Iterations: 1
- Max Time: 200 seconds
- Temperature: 0.5
- Specialized in data-driven analysis

### 3. Musician & Lyricist Assistant
- Generates original musical compositions
- Creates lyrical content matching specified themes
- Provides chord progression recommendations
- Analyzes rhyme schemes
- Suggests musical genre adaptations
- Creates demo lyrics and chord structures

**Technical Configuration:**
- Tools: None (focused on creative generation)
- Max Iterations: 1
- Max Time: 200 seconds
- Temperature: 0.5
- Outputs saved in structured format with markers:
  - 🎵 MUSICAL CONTENT START 🎵
  - 🎵 MUSICAL CONTENT END 🎵

**Global Model Parameters:**
- Decoding Method: Sample
- Max New Tokens: 250
- Top K: 50
- Top P: 0.95
- Model: WatsonX LLM
- Project Integration: CrewAI Framework

## Setup

1. Clone the repository:
```bash
git clone https://github.com/evilangelsaahi/MayaAI.git
cd MayaAI
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API keys:
Create `.env` file in directory, an empty template is present save your API keys there and remove `_template` so that `config.py` file can map with your API keys:

```python
# WatsonX Configuration
WATSONX_APIKEY="PUT-YOUR-API-KEY-HERE"
WATSONX_PROJECT_ID="PUT-YOUR-API-KEY-HERE"
WATSONX_URL="PUT-YOUR-API-KEY-HERE"
WATSONX_PLATFORM_URL="PUT-YOUR-API-KEY-HERE"
WATSONX_MODEL_ID="PUT-YOUR-API-KEY-HERE"

# Model Parameters are hardcoded in code but can be put here as well
DECODING_METHOD=sample
MAX_NEW_TOKENS=200
MIN_NEW_TOKENS=0
TEMPERATURE=0
TOP_K=1
TOP_P=1

# Serper Configuration
SERPER_API_KEY="PUT-YOUR-API-KEY-HERE"

# NewsAPIWrapper
NEWS_API_KEY="not-using-this-tool"

# OpenWeatherMap
OPENWEATHERMAP_API_KEY="PUT-YOUR-API-KEY-HERE"

```

## Usage

Run the main application:
```bash
python agent.py
```
or
```bash
python3 agent.py
```

The application provides an interactive menu with options to:
1. Get career development advice
2. Research music trends
3. Generate creative content
4. Save conversation history
5. Exit the application


## Language Model Parameters: Quick Reference

- **Decoding Method: "sample"**
  * Randomly selects next tokens based on their probability distribution
  * Provides more varied output than "greedy" decoding (which always selects most likely token)

- **Max New Tokens: 250**
  * Limits output length to 250 new tokens (roughly 800 characters in English)
  * Prevents excessively long responses and controls computation time

- **Temperature: 0.4**
  * Controls randomness in output (scale 0-1)
  * Lower setting (0.5) favors consistency and predictability over creativity
  * Creates more focused, deterministic responses

- **Top-k: 50**
  * Restricts token selection to only the 50 most probable options
  * Filters out unlikely or nonsensical choices
  * Balances output diversity with quality

- **Top-p: 0.95**
  * Uses "nucleus sampling" to dynamically select tokens
  * Considers only tokens whose cumulative probability reaches 95%
  * More adaptable than top-k, adjusts based on probability distribution

This configuration creates reliable, consistent outputs with moderate creativity and reasonable length constraints.

**Note: There's always a tradeoff between creativity and being right, these params are chosen to suit the best case for this project.**
**Sometimes I noticed right answer in the thought process of Agent, but again in final answer it apologizes for being wrong.**

## Outputs

All generated content (lyrics, chords, etc.) is automatically saved to the `outputs` directory with timestamped filenames in the format:
`save` text need to be prompted to AI agent to save upto last two conversations 
```
outputs/creative_output_YYYYMMDD_HHMMSS.txt
```

## Project Structure

```
MayaAI/
├── agent.py              # Main application file
├── config.py            # Configuration and API keys
├── requirements.txt     # Project dependencies
├── outputs/            # Generated content directory
└── README.md           # Project documentation
```

## Dependencies

- crewai
- crewai-tools
- langchain-ibm
- langchain-core
- requests
- python-dotenv

## License

This project is licensed under the MIT License - see the LICENSE file for details.


## Acknowledgments

* [Nicholas Renotte](https://github.com/nicknochnack) - Data Science professional at IBM, whose work and tutorials have been foundation for this project
* [Maya Murad](https://www.linkedin.com/in/maya-murad/) for the inspiration behind the MAYA (Senior Artist Manager) name whose tutorials have been inspirational for this project

# Other References 🔗

<p>-<a href="https://python.langchain.com/docs/integrations/llms/ibm_watsonx/">Watsonx Langchain</a>:WatsonxLLM is a wrapper for IBM watsonx.ai foundation models.</p>
<p>-<a href="https://docs.crewai.com/">CrewAI</a>:Cutting-edge framework for orchestrating role-playing, autonomous AI agents. By fostering collaborative intelligence, CrewAI empowers agents to work together seamlessly, tackling complex tasks.</p>

# Github repo developed by

👨🏾‍💻 Project developed by [Sahil Bohot](https://www.linkedin.com/in/sahilbohot/) - Mainframe Systems Programmer and AI enthusiast<br />
📜 License: This project is licensed under the MIT License </br>
