//
//  main.swift
//  MayaUI
//
//  Created by Sahil Bohot on 2025-03-29.
//

import Foundation
import PythonKit
import PythonCodable

// Set up Python virtual environment
let venvPath = "/Users/sahilbohot/xcode projects/MayaAI/WatsonxCrewAI/venv"
let pythonPath = "\(venvPath)/bin/python"
let pythonLibPath = "/Library/Frameworks/Python.framework/Versions/3.10/lib/libpython3.10.dylib"

// Set environment variables
setenv("PYTHON_LIBRARY", pythonLibPath, 1)
setenv("PYTHON_HOME", "/Library/Frameworks/Python.framework/Versions/3.10", 1)
setenv("PYTHONPATH", "\(venvPath)/lib/python3.10/site-packages:/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages", 1)
setenv("DYLD_LIBRARY_PATH", "/Library/Frameworks/Python.framework/Versions/3.10/lib", 1)
setenv("DYLD_FRAMEWORK_PATH", "/Library/Frameworks/Python.framework/Versions/3.10", 1)

// Initialize Python environment
PythonLibrary.useVersion(3)
let sys = Python.import("sys")

// Add the path to your Python project
sys.path.append("/Users/sahilbohot/xcode projects/MayaAI/WatsonxCrewAI")

// Import your agent interface module
let pythonModule = Python.import("agent")
let agentInterface = pythonModule.AgentInterface()

// Function to send a message to the Python script
func sendMessage(_ text: String) {
    // Call Python agent
    let response = agentInterface.process_query(text)
    
    // Convert Python response to Swift string
    let responseText = String(response) ?? "Error processing request"
    
    // Print the response
    print("Response from Python script: \(responseText)")
}

// Example usage
let message = "Your input data here"
sendMessage(message)

print("Hello, World!")

