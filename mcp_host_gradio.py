# # import gradio as gr
# # import requests
# # import json

# # # The server URL remains the same, regardless of the model being used.
# # MCP_SERVER_URL = "http://127.0.0.1:5001/analyze"

# # def analyze_incident(incident_log: str):
# #     """
# #     Sends the incident log to the MCP server and returns the final report.
# #     This function doesn't need to know which model the server is using.
# #     """
# #     if not incident_log.strip():
# #         return "Please enter an incident log snippet."
    
# #     # The payload is simple: just the text from the user.
# #     payload = {"incident_description": incident_log}
    
# #     try:
# #         # It sends the request to the server and waits for the final result.
# #         response = requests.post(MCP_SERVER_URL, json=payload, timeout=300) # 5 min timeout
# #         response.raise_for_status() # Raise an exception for bad status codes
        
# #         data = response.json()
# #         if "result" in data:
# #             return data["result"]
# #         elif "error" in data:
# #             return f"Error from server: {data['error']}"
# #         else:
# #             return "Received an unexpected response from the server."
            
# #     except requests.exceptions.RequestException as e:
# #         return f"Failed to connect to the MCP server at {MCP_SERVER_URL}. Is it running? \n\nError: {e}"
# #     except json.JSONDecodeError:
# #         return "Failed to decode the server's response. The server might have returned invalid JSON."

# # # Example logs remain useful for testing any model
# # example_logs = [
# #     "INCIDENT_ID:c4a1-dbd3 - DATABASE DEADLOCK DETECTED\nDeadlock detected between transactions tx_001 and tx_002",
# #     "INCIDENT_ID:b2f2-a1b9 - SQL INJECTION ATTEMPT DETECTED\nSuspicious query pattern detected: ' OR '1'='1 --",
# #     "INCIDENT_ID:a1c3-e4d5 - ENVIRONMENT VARIABLE MISSING\nRequired environment variable SMTP_HOST not set"
# # ]

# # with gr.Blocks(theme=gr.themes.Soft()) as demo:
# #     gr.Markdown("# 🤖 MCP: Multi-agent Collaborative Platform for SRE")
# #     gr.Markdown(
# #         "Enter a log snippet from an incident below. The MCP agents will perform a root cause analysis "
# #         "using the Code Intelligence Graph, propose a remediation plan, and write a full postmortem report."
# #     )
    
# #     with gr.Row():
# #         incident_input = gr.Textbox(
# #             label="Incident Log Snippet", 
# #             placeholder="Paste a log line here, e.g., 'DATABASE DEADLOCK DETECTED...'",
# #             lines=5
# #         )
    
# #     analyze_button = gr.Button("🔍 Analyze Incident", variant="primary")
    
# #     gr.Examples(
# #         examples=example_logs,
# #         inputs=incident_input,
# #         label="Example Incidents"
# #     )
    
# #     with gr.Accordion("Show Postmortem Report", open=True):
# #         output_report = gr.Markdown(label="Generated Report")
        
# #     analyze_button.click(
# #         fn=analyze_incident,
# #         inputs=incident_input,
# #         outputs=output_report
# #     )

# # if __name__ == "__main__":
# #     demo.launch()
# import gradio as gr
# import requests
# import json
# import time
# import os

# MCP_SERVER_URL = "http://127.0.0.1:5001/analyze"

# # Ensure a directory for reports exists
# os.makedirs("reports", exist_ok=True)

# def analyze_incident(incident_log: str, analysis_level: str):
#     """
#     Sends the incident log and analysis level to the server, then streams the response.
#     """
#     # Start with empty/hidden components
#     yield {
#         output_report: "",
#         download_button: gr.File(visible=False)
#     }

#     if not incident_log.strip():
#         yield {output_report: "Please enter an incident log snippet."}
#         return

#     payload = {
#         "incident_description": incident_log,
#         "analysis_level": analysis_level
#     }
    
#     full_response_text = ""
#     try:
#         response = requests.post(MCP_SERVER_URL, json=payload, stream=True, timeout=300)
#         response.raise_for_status()
        
#         for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
#             if "__END_OF_STREAM__" in chunk:
#                 # Handle the end of the stream and get the final report for download
#                 parts = chunk.split("__END_OF_STREAM__\n")
#                 if len(parts) > 1:
#                     final_report_content = parts[1]
#                 else: # if the token is the very last thing
#                     final_report_content = full_response_text.replace("### 🕵️‍♂️ Starting Root Cause Analysis...\n\n", "").replace("### 🛠️ Generating Remediation Plan...\n\n", "").replace("### 📝 Compiling Full Postmortem Report...\n\n", "")

#                 if analysis_level == 'Full Report':
#                     # Save the final report to a file
#                     timestamp = time.strftime("%Y%m%d-%H%M%S")
#                     report_filename = f"reports/mcp_report_{timestamp}.md"
#                     with open(report_filename, "w") as f:
#                         f.write(final_report_content)
                    
#                     # Make the download button visible
#                     yield {
#                         output_report: full_response_text, 
#                         download_button: gr.File(value=report_filename, visible=True, label="Download Report")
#                     }
#                 break # Exit the loop
            
#             full_response_text += chunk
#             yield {output_report: full_response_text}

#     except requests.exceptions.RequestException as e:
#         yield {output_report: f"Failed to connect to MCP server: {e}"}

# # --- Gradio UI Definition ---
# example_logs = [
#     "INCIDENT_ID:c4a1-dbd3 - DATABASE DEADLOCK DETECTED...",
#     "INCIDENT_ID:b2f2-a1b9 - SQL INJECTION ATTEMPT DETECTED...",
#     "INCIDENT_ID:a1c3-e4d5 - ENVIRONMENT VARIABLE MISSING..."
# ]
# analysis_options = ["RCA Only", "RCA + Remediation", "Full Report"]

# with gr.Blocks(theme=gr.themes.Soft()) as demo:
#     gr.Markdown("# 🤖 MCP: Multi-agent Collaborative Platform for SRE")
#     gr.Markdown("Enter a log snippet, choose the analysis depth, and the MCP agents will get to work.")
    
#     with gr.Row():
#         with gr.Column(scale=2):
#             incident_input = gr.Textbox(
#                 label="Incident Log Snippet",
#                 placeholder="Paste a log line here...",
#                 lines=5
#             )
#             level_input = gr.Radio(
#                 choices=analysis_options,
#                 label="Analysis Level",
#                 value="Full Report"
#             )
#             gr.Examples(examples=example_logs, inputs=incident_input)
        
#         with gr.Column(scale=3):
#             output_report = gr.Markdown(label="Analysis Output")
#             download_button = gr.File(label="Download Report", visible=False)

#     analyze_button = gr.Button("🔍 Analyze Incident", variant="primary")

#     analyze_button.click(
#         fn=analyze_incident,
#         inputs=[incident_input, level_input],
#         outputs=[output_report, download_button]
#     )

# if __name__ == "__main__":
#     demo.launch()
import gradio as gr
import requests
import json
import time
import os

MCP_SERVER_URL = "http://127.0.0.1:5001/analyze"

# Ensure a directory for reports exists
os.makedirs("reports", exist_ok=True)

def analyze_incident(incident_text: str, incident_file, analysis_level: str):
    """
    Handles both text and file input, sends it to the server, and streams the response.
    """
    # Start with empty/hidden components
    yield {
        output_report: "",
        download_button: gr.File(visible=False)
    }

    incident_log = ""
    # Prioritize file input if it exists
    if incident_file is not None:
        incident_log = incident_file.decode('utf-8')
    elif incident_text.strip():
        incident_log = incident_text
    else:
        yield {output_report: "Please enter an incident log snippet or upload a log file."}
        return
    
    payload = {
        "incident_description": incident_log,
        "analysis_level": analysis_level
    }
    
    full_response_text = ""
    try:
        # The rest of the streaming logic is the same
        response = requests.post(MCP_SERVER_URL, json=payload, stream=True, timeout=600) # Increased timeout for larger logs
        response.raise_for_status()
        
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if "__END_OF_STREAM__" in chunk:
                parts = chunk.split("__END_OF_STREAM__\n")
                final_report_content = parts[1] if len(parts) > 1 else full_response_text
                
                if analysis_level == 'Full Report':
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    report_filename = f"reports/mcp_report_{timestamp}.md"
                    with open(report_filename, "w", encoding='utf-8') as f:
                        f.write(final_report_content)
                    
                    yield {
                        output_report: full_response_text, 
                        download_button: gr.File(value=report_filename, visible=True, label="Download Report")
                    }
                break
            
            full_response_text += chunk
            yield {output_report: full_response_text}

    except requests.exceptions.RequestException as e:
        yield {output_report: f"Failed to connect to MCP server: {e}"}

# --- Gradio UI Definition ---
example_logs = [
    "INCIDENT_ID:c4a1-dbd3 - DATABASE DEADLOCK DETECTED...",
    "INCIDENT_ID:b2f2-a1b9 - SQL INJECTION ATTEMPT DETECTED...",
    "INCIDENT_ID:a1c3-e4d5 - ENVIRONMENT VARIABLE MISSING..."
]
analysis_options = ["RCA Only", "RCA + Remediation", "Full Report"]

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 MCP: Multi-agent Collaborative Platform for SRE")
    
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### 1. Provide Incident Data")
            incident_input_text = gr.Textbox(
                label="Option A: Paste a Log Snippet",
                placeholder="Paste a key log line here...",
                lines=5
            )
            incident_input_file = gr.File(
                label="Option B: Upload a Raw Log File (.log, .txt)",
                file_types=['.log', '.txt']
            )
            
            gr.Markdown("### 2. Choose Analysis Depth")
            level_input = gr.Radio(
                choices=analysis_options,
                label="Analysis Level",
                value="Full Report"
            )
            
            analyze_button = gr.Button("🔍 Analyze Incident", variant="primary")
            gr.Examples(examples=example_logs, inputs=incident_input_text, label="Example Snippets")

        with gr.Column(scale=3):
            gr.Markdown("### 3. Review Analysis")
            output_report = gr.Markdown(label="Live Analysis Output")
            download_button = gr.File(label="Download Full Report", visible=False)

    analyze_button.click(
        fn=analyze_incident,
        inputs=[incident_input_text, incident_input_file, level_input],
        outputs=[output_report, download_button]
    )

if __name__ == "__main__":
    demo.launch()