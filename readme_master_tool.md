MCP-SRE: Multi-agent Collaborative Platform for SRE Incident Analysis

This project is a complete simulation and analysis platform designed to mimic a real-world Site Reliability Engineering (SRE) workflow. It uses a crew of AI agents, powered by CrewAI, to perform root cause analysis (RCA), suggest remediation plans, and write postmortem reports for simulated application failures.

The core innovation of this project is its novel approach to Retrieval-Augmented Generation (RAG). Instead of traditional vector search, it uses a Code Intelligence Graph, which maps the application's source code, functions, and potential errors into a structured knowledge base. This allows the AI agents to perform more precise, context-aware analysis.

📂 Project Structure

Here is an overview of all the files in this project and their roles:

/mcp_approach
├── 📄 README.md                 # This guide
├── 📄 requirements.txt           # All Python dependencies
├── 📄 .env                      # Your API keys and model configuration (you must create this)
│
├── 🤖 enhanced_ecommerce_runner.py # Generates simulated application logs and incidents
├── 🐛 buggy_app.py                # The flawed source code that the AI agents analyze
│
├── 🧠 build_graph.py               # One-time script to parse buggy_app.py and create the knowledge graph
├── 🧠 code_intelligence_graph.graphml # The output of the build script; the "brain" for the RCA agent
│
├── 🔧 code_graph_tool.py          # The custom CrewAI tool that queries the knowledge graph
├── 🔧 llm_provider.py             # Handles the connection to your chosen LLM (e.g., OpenRouter)
│
├── 🌐 mcp_server.py               # The Flask backend that runs the CrewAI agents
└── 🎨 mcp_host_gradio.py          # The Gradio web interface you interact with

⚙️ Setup and Installation

Follow these steps to set up your environment and prepare the project for its first run.

1. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.
Bash

# Navigate to the project directory
cd ~/Documents/mcp_approach

# Create a virtual environment
python3 -m venv mcp_venv

# Activate the environment
source mcp_venv/bin/activate

2. Install Dependencies

Install all the required Python libraries from the requirements.txt file.
Bash

pip install --upgrade pip
pip install -r requirements.txt

3. Configure Your API Key

You need to provide your AI model's API key. This project is configured to work with OpenRouter, but can be adapted for any provider.

    Create a file named .env in the main project directory.

    Copy and paste the following content into it, adding your own API key and desired model.

    .env
    Code snippet

    # --- Set the provider to "openrouter" ---
    LLM_PROVIDER="openrouter"

    # --- Your OpenRouter Configuration ---
    # Get your key from https://openrouter.ai/keys
    OPENROUTER_API_KEY="sk-or-v1-..."

    # A reliable free model to start with
    OPENROUTER_MODEL_NAME="openrouter/mistralai/mistral-7b-instruct:free"

    # The OpenRouter API endpoint
    OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"

4. Build the Knowledge Graph

This is a crucial one-time step. Run the build_graph.py script to analyze the buggy_app.py source code and create the code_intelligence_graph.graphml file that the RCA agent needs.
Bash

python build_graph.py

🚀 How to Run the MCP

The workflow is divided into two main parts: generating an incident and then analyzing it.

Part A: The Error Generation Side (Simulating an Incident)

First, you need some log data to analyze. The enhanced_ecommerce_runner.py script creates this for you.

    Run the script:
    Bash

    python enhanced_ecommerce_runner.py

    Find the Input: The script will create a logs/ directory. Look inside for files like error_...log. Open one of these files and find an interesting error message. This is the "input" for the analysis phase.

        Example Input: INCIDENT_ID:c4a1-dbd3 - DATABASE DEADLOCK DETECTED

Part B: The MCP Agent Side (Analyzing the Incident)

Now you will start the server and the user interface to analyze the log you found. You will need two separate terminals for this.

    Start the Server (Terminal 1):
    Run the mcp_server.py script. It will start a web server and wait for requests from the UI.
    Bash

python mcp_server.py

You should see output indicating it's running on port 5001. Keep this terminal open.

Start the Host UI (Terminal 2):
Run the mcp_host_gradio.py script. This will launch the Gradio web interface.
Bash

    python mcp_host_gradio.py

    Your web browser should open automatically to the UI.

Using the Gradio Interface

You are now ready to analyze the incident.

    Provide Input:

        Option A: Copy the error line from your log file and paste it into the "Paste a Log Snippet" textbox.

        Option B: Click to upload the entire error_...log file using the "Upload a Raw Log File" component.

    Choose Analysis Depth:
    Select one of the three options from the radio buttons:

        RCA Only: The system will only run the Root Cause Analysis agent.

        RCA + Remediation: Runs the RCA agent, then the Remediation agent.

        Full Report: Runs all three agents in sequence to produce a complete postmortem.

    Analyze:
    Click the "🔍 Analyze Incident" button.

    View and Download:

        The analysis will appear in the "Live Analysis Output" box on the right, updating in real-time as each agent completes its task.

        If you chose "Full Report," a "Download Report" button will appear once the analysis is finished, allowing you to save the report as a markdown file.
