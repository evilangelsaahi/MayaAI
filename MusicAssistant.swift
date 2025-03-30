import Foundation
import PythonKit

class MusicAssistant: ObservableObject {
    @Published var messages: [Message] = []
    @Published var isProcessing = false
    private var pythonAssistant: PythonObject?
    
    struct Message: Identifiable {
        let id = UUID()
        let text: String
        let isUser: Bool
        let timestamp: Date
    }
    
    init() {
        setupPythonEnvironment()
    }
    
    private func setupPythonEnvironment() {
        // Set up Python environment
        let sys = Python.import("sys")
        let os = Python.import("os")
        
        // Add the current directory to Python path
        if let currentPath = FileManager.default.currentDirectoryPath as? String {
            sys.path.append(currentPath)
        }
        
        // Import the Python module
        do {
            let agent = Python.import("agent")
            pythonAssistant = agent.MusicAssistant()
        } catch {
            print("Error importing Python module: \(error)")
        }
    }
    
    @MainActor
    func startNewChat() async {
        guard let assistant = pythonAssistant else { return }
        
        do {
            let greeting = try await assistant.start_new_chat().string
            messages.append(Message(text: greeting, isUser: false, timestamp: Date()))
        } catch {
            print("Error starting new chat: \(error)")
            messages.append(Message(text: "Error starting new chat. Please try again.", isUser: false, timestamp: Date()))
        }
    }
    
    @MainActor
    func sendMessage(_ text: String) async {
        guard let assistant = pythonAssistant else { return }
        
        // Add user message to the chat
        messages.append(Message(text: text, isUser: true, timestamp: Date()))
        isProcessing = true
        
        do {
            let response = try await assistant.process_message(text).string
            messages.append(Message(text: response, isUser: false, timestamp: Date()))
        } catch {
            print("Error processing message: \(error)")
            messages.append(Message(text: "Error processing message. Please try again.", isUser: false, timestamp: Date()))
        }
        
        isProcessing = false
    }
    
    func clearChat() {
        guard let assistant = pythonAssistant else { return }
        
        do {
            try assistant.clear_conversation()
            messages.removeAll()
        } catch {
            print("Error clearing chat: \(error)")
        }
    }
    
    func getConversationHistory() -> [[String: Any]] {
        guard let assistant = pythonAssistant else { return [] }
        
        do {
            return try assistant.get_conversation_history().array
        } catch {
            print("Error getting conversation history: \(error)")
            return []
        }
    }
} 