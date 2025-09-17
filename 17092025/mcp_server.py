# # # import os
# # # from flask import Flask, request, jsonify
# # # from dotenv import load_dotenv
# # # from crewai import Agent, Task, Crew, Process

# # # # Load environment variables from .env file
# # # load_dotenv()

# # # # Import our custom tool
# # # # from code_graph_tool import CodeGraphTool
# # # from code_graph_tool import code_graph_tool
# # # # --- NEW: Model-Agnostic LLM Factory ---
# # # def get_llm():
# # #     """
# # #     Reads the .env file and dynamically initializes the correct LLM
# # #     based on the specified provider.
# # #     """
# # #     provider = os.getenv("LLM_PROVIDER", "openai").lower()
# # #     print(f"🤖 Initializing LLM for provider: {provider}")

# # #     # --- OpenRouter Provider (Simplified and Corrected) ---
# # #     if provider == "openrouter":
# # #         from langchain_openai import ChatOpenAI
# # #         api_key = os.getenv("OPENROUTER_API_KEY")
# # #         model_name = os.getenv("OPENROUTER_MODEL_NAME")
# # #         base_url = os.getenv("OPENROUTER_BASE_URL")

# # #         if not all([api_key, model_name, base_url]):
# # #             raise ValueError("OPENROUTER_API_KEY, OPENROUTER_MODEL_NAME, and OPENROUTER_BASE_URL must be set in .env")

# # #         # This is the cleanest, most direct way to do this.
# # #         # We let ChatOpenAI handle the connection and just inject the
# # #         # extra headers that OpenRouter requires.
# # #         return ChatOpenAI(
# # #             model=model_name,
# # #             api_key=api_key,
# # #             base_url=base_url,
# # #             default_headers={
# # #                 "HTTP-Referer": "http://localhost:5001",
# # #                 "X-Title": "MCP SRE Assistant"
# # #             }
# # #         )

# # #     # --- Other provider logic remains below ---
# # #     elif provider == "openai":
# # #         from langchain_openai import ChatOpenAI
# # #         # ... (code for OpenAI remains the same)

# # #     elif provider == "mistral":
# # #         from langchain_mistralai.chat_models import ChatMistralAI
# # #         # ... (code for Mistral remains the same)

# # #     else:
# # #         raise ValueError(f"Unsupported LLM_PROVIDER: '{provider}'. Check your .env file.")

# # # # --- Flask App and CrewAI setup (mostly unchanged) ---
# # # app = Flask(__name__)

# # # @app.route('/analyze', methods=['POST'])
# # # def analyze_incident():
# # #     data = request.get_json()
# # #     if not data or 'incident_description' not in data:
# # #         return jsonify({"error": "Missing 'incident_description' in request"}), 400

# # #     incident_description = data['incident_description']
    
# # #     try:
# # #         # The only change is this single line!
# # #         llm = get_llm()
        
# # #         code_graph_tool = CodeGraphTool()

# # #         # Agent definitions remain the same
# # #         rca_agent = Agent(
# # #             role='Expert System Diagnostician',
# # #             goal="Analyze incident logs and use the Code Intelligence Graph to pinpoint the exact root cause in the source code.",
# # #             backstory="You are a specialized AI agent designed for root cause analysis. You excel at interpreting logs to extract key error types and then using a knowledge graph of the codebase to find the exact functions responsible for the failure.",
# # #             tools=[code_graph_tool], llm=llm, verbose=True
# # #         )
# # #         remediation_agent = Agent(
# # #             role='Senior Site Reliability Engineer (SRE)',
# # #             goal="Create a clear, actionable, step-by-step remediation plan based on the identified root cause from the diagnostician.",
# # #             backstory="You are a seasoned SRE with decades of experience in fixing critical production issues. Your plans are practical, safe, and easy for developers to follow. You prioritize system stability and preventing future recurrences.",
# # #             llm=llm, verbose=True
# # #         )
# # #         report_writer_agent = Agent(
# # #             role='Technical Postmortem Writer',
# # #             goal="Generate a comprehensive, blame-free postmortem report detailing the incident, its root cause, and the proposed remediation plan.",
# # #             backstory="You are an expert technical writer known for creating clear, concise, and professional postmortem documents. Your reports help teams learn from incidents and improve system resilience without assigning blame.",
# # #             llm=llm, verbose=True
# # #         )

# # #         # Task definitions remain the same
# # #         rca_task = Task(
# # #             description=f"Analyze the following incident log to identify the primary error type. Then, use the Code Intelligence Graph Tool with the identified error type to find the root cause in the source code. Your final answer must be a detailed explanation of the root cause, citing the specific functions and code snippets involved.\n\nIncident Log:\n---\n{incident_description}\n---",
# # #             expected_output="A detailed root cause analysis report, including the names of the faulty functions and the relevant code excerpts that explain the failure.",
# # #             agent=rca_agent
# # #         )
# # #         remediation_task = Task(
# # #             description="Based on the root cause analysis provided, create a step-by-step remediation plan. The plan should be clear, concise, and actionable for a development team. Include code suggestions for the fix if applicable.",
# # #             expected_output="A numbered list of steps to resolve the issue and prevent it from happening again.",
# # #             agent=remediation_agent, context=[rca_task]
# # #         )
# # #         report_task = Task(
# # #             description="Combine the root cause analysis and the remediation plan into a single, professional postmortem report. The report should have clear sections: 1. Summary, 2. Timeline, 3. Root Cause Analysis, 4. Remediation Plan, 5. Lessons Learned. The timeline can be a placeholder.",
# # #             expected_output="A complete, well-formatted markdown postmortem document.",
# # #             agent=report_writer_agent, context=[rca_task, remediation_task]
# # #         )

# # #         # Crew execution remains the same
# # #         incident_crew = Crew(
# # #             agents=[rca_agent, remediation_agent, report_writer_agent],
# # #             tasks=[rca_task, remediation_task, report_task],
# # #             process=Process.sequential, verbose=2
# # #         )
# # #         result = incident_crew.kickoff()
# # #         return jsonify({"result": result})

# # #     except Exception as e:
# # #         # Provide a more informative error message
# # #         return jsonify({"error": f"An error occurred in the backend: {str(e)}"}), 500

# # # if __name__ == '__main__':
# # #     app.run(host='0.0.0.0', port=5001, debug=True)
# # import os
# # from flask import Flask, request, jsonify
# # from dotenv import load_dotenv
# # from crewai import Agent, Task, Crew, Process
# # import traceback

# # # Load environment variables from .env file
# # load_dotenv()

# # # Import our custom tool function
# # from code_graph_tool import code_graph_tool

# # def get_llm():
# #     """
# #     Reads the .env file and dynamically initializes the correct LLM
# #     based on the specified provider.
# #     """
# #     provider = os.getenv("LLM_PROVIDER", "openai").lower()
# #     print(f"🤖 Initializing LLM for provider: {provider}")

# #     if provider == "openrouter":
# #         from langchain_openai import ChatOpenAI
# #         api_key = os.getenv("OPENROUTER_API_KEY")
# #         model_name = os.getenv("OPENROUTER_MODEL_NAME")
# #         base_url = os.getenv("OPENROUTER_BASE_URL")

# #         if not all([api_key, model_name, base_url]):
# #             raise ValueError("OPENROUTER_API_KEY, OPENROUTER_MODEL_NAME, and OPENROUTER_BASE_URL must be set in .env")

# #         return ChatOpenAI(
# #             model=model_name,
# #             api_key=api_key,
# #             base_url=base_url,
# #             default_headers={
# #                 "HTTP-Referer": "http://localhost:5001",
# #                 "X-Title": "MCP SRE Assistant"
# #             }
# #         )
# #     # Add other providers like openai, mistral here if needed
# #     else:
# #         raise ValueError(f"Unsupported LLM_PROVIDER: '{provider}'. Please check your .env file.")

# # app = Flask(__name__)

# # @app.route('/analyze', methods=['POST'])
# # def analyze_incident():
# #     data = request.get_json()
# #     if not data or 'incident_description' not in data:
# #         return jsonify({"error": "Missing 'incident_description' in request"}), 400

# #     incident_description = data['incident_description']
    
# #     try:
# #         llm = get_llm()
        
# #         # NOTE: The incorrect line 'code_graph_tool = CodeGraphTool()' has been removed.
        
# #         rca_agent = Agent(
# #             role='Expert System Diagnostician',
# #             goal="Analyze incident logs and use the Code Intelligence Graph to pinpoint the exact root cause in the source code.",
# #             backstory="You are a specialized AI agent designed for root cause analysis...",
# #             tools=[code_graph_tool], # Pass the imported function directly
# #             llm=llm, 
# #             verbose=True
# #         )
# #         remediation_agent = Agent(
# #             role='Senior Site Reliability Engineer (SRE)',
# #             goal="Create a clear, actionable, step-by-step remediation plan...",
# #             backstory="You are a seasoned SRE with decades of experience...",
# #             llm=llm, 
# #             verbose=True
# #         )
# #         report_writer_agent = Agent(
# #             role='Technical Postmortem Writer',
# #             goal="Generate a comprehensive, blame-free postmortem report...",
# #             backstory="You are an expert technical writer...",
# #             llm=llm, 
# #             verbose=True
# #         )

# #         rca_task = Task(
# #             description=f"Analyze the incident log to find the error type. Use the tool with the error type to get source code and find the root cause.\n\nLog:\n---\n{incident_description}\n---",
# #             expected_output="A detailed root cause analysis, citing the faulty functions and code.",
# #             agent=rca_agent
# #         )
# #         remediation_task = Task(
# #             description="Based on the root cause analysis, create a step-by-step remediation plan.",
# #             expected_output="A numbered list of steps to resolve the issue.",
# #             agent=remediation_agent, 
# #             context=[rca_task]
# #         )
# #         report_task = Task(
# #             description="Combine the root cause and remediation plan into a professional postmortem report.",
# #             expected_output="A complete, well-formatted markdown postmortem document.",
# #             agent=report_writer_agent, 
# #             context=[rca_task, remediation_task]
# #         )

# #         incident_crew = Crew(
# #             agents=[rca_agent, remediation_agent, report_writer_agent],
# #             tasks=[rca_task, remediation_task, report_task],
# #             process=Process.sequential, 
# #             verbose=True
# #         )
# #         result = incident_crew.kickoff()
# #         return jsonify({"result": result.raw})

# #     except Exception as e:
# #         print(f"!!! AN ERROR OCCURRED: {e}") 
# #         traceback.print_exc()
# #         return jsonify({"error": f"An error occurred in the backend: {str(e)}"}), 500

# # if __name__ == '__main__':
# #     app.run(host='0.0.0.0', port=5001, debug=True)

# import os
# import traceback
# from flask import Flask, request, Response, stream_with_context
# from dotenv import load_dotenv
# from crewai import Agent, Task, Crew, Process

# # Load environment variables and import tool/LLM factory
# load_dotenv()
# from code_graph_tool import code_graph_tool
# from llm_provider import get_llm

# app = Flask(__name__)

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     data = request.get_json()
#     incident_description = data.get('incident_description')
#     analysis_level = data.get('analysis_level', 'Full Report')

#     if not incident_description:
#         return Response("Error: Missing 'incident_description' in request", status=400)

#     def stream_analysis():
#         """
#         A generator function that builds a crew based on the analysis level
#         and then streams the step-by-step results.
#         """
#         try:
#             llm = get_llm()

#             # --- 1. Define all possible agents and tasks ---
#             rca_agent = Agent(
#                 role='Expert System Diagnostician',
#                 goal="Analyze logs and use the Code Intelligence Graph to find the root cause.",
#                 backstory="You are a specialized AI agent for root cause analysis...",
#                 tools=[code_graph_tool], llm=llm, verbose=False
#             )
#             remediation_agent = Agent(
#                 role='Senior Site Reliability Engineer (SRE)',
#                 goal="Create a clear, actionable remediation plan based on a root cause analysis.",
#                 backstory="You are a seasoned SRE with decades of experience...",
#                 llm=llm, verbose=False
#             )
#             report_writer_agent = Agent(
#                 role='Technical Postmortem Writer',
#                 goal="Generate a comprehensive, blame-free postmortem report.",
#                 backstory="You are an expert technical writer...",
#                 llm=llm, verbose=False
#             )

#             rca_task = Task(
#                 description=f"Analyze the incident log to find the error type. Use the tool with that error type to find the root cause in the source code.\n\nLog:\n---\n{incident_description}\n---",
#                 expected_output="A detailed root cause analysis, citing the faulty functions and code.",
#                 agent=rca_agent
#             )
#             remediation_task = Task(
#                 description="Based on the root cause analysis from the previous step, create a step-by-step remediation plan.",
#                 expected_output="A numbered list of steps to resolve the issue.",
#                 agent=remediation_agent,
#                 context=[rca_task] # This links the tasks together
#             )
#             report_task = Task(
#                 description="Combine the root cause analysis and remediation plan into a single, professional postmortem report with sections for Summary, Root Cause, and Remediation.",
#                 expected_output="A complete, well-formatted markdown postmortem document.",
#                 agent=report_writer_agent,
#                 context=[remediation_task] # This task uses the output of the remediation task
#             )

#             # --- 2. Dynamically build the list of tasks based on user's choice ---
#             yield "### ⚙️ Configuring analysis level...\n\n"
            
#             tasks_to_run = []
#             if analysis_level == "RCA Only":
#                 tasks_to_run = [rca_task]
#                 yield "Selected analysis: Root Cause Analysis Only.\n\n"
#             elif analysis_level == "RCA + Remediation":
#                 tasks_to_run = [rca_task, remediation_task]
#                 yield "Selected analysis: RCA + Remediation Plan.\n\n"
#             elif analysis_level == "Full Report":
#                 tasks_to_run = [rca_task, remediation_task, report_task]
#                 yield "Selected analysis: Full Postmortem Report.\n\n"

#             # --- 3. Execute the crew and stream output ---
#             # NOTE: Because we are streaming, we run tasks one-by-one to send results as they complete.
            
#             final_report_content = ""
            
#             # Execute RCA Task
#             yield "### 🕵️‍♂️ Starting Root Cause Analysis...\n\n"
#             rca_output = rca_task.execute()
#             final_report_content += f"## Root Cause Analysis\n\n{rca_output}\n\n---\n"
#             yield final_report_content

#             # Execute Remediation Task if needed
#             if analysis_level in ["RCA + Remediation", "Full Report"]:
#                 yield "### 🛠️ Generating Remediation Plan...\n\n"
#                 remediation_output = remediation_task.execute(context=rca_output)
#                 remediation_text = f"## Remediation Plan\n\n{remediation_output}\n\n---\n"
#                 final_report_content += remediation_text
#                 yield final_report_content

#             # Execute Report Task if needed
#             if analysis_level == "Full Report":
#                  yield "### 📝 Compiling Full Postmortem Report...\n\n"
#                  report_output = report_task.execute(context=remediation_output)
#                  # For the final step, we replace the whole text with the properly formatted report
#                  final_report_content = f"## Postmortem Report\n\n{report_output}"
#                  yield final_report_content

#             # Signal the end of the stream for the download button
#             yield f"__END_OF_STREAM__\n{final_report_content}"

#         except Exception as e:
#             tb = traceback.format_exc()
#             print(f"!!! AN ERROR OCCURRED: {e}\n{tb}")
#             yield f"### ❌ An error occurred during analysis:\n\n```\n{e}\n```"

#     return Response(stream_with_context(stream_analysis()), mimetype='text/event-stream')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5001, debug=True)

import os
import traceback
from flask import Flask, request, Response, stream_with_context
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process

# Load environment variables and import tool/LLM factory
load_dotenv()
from code_graph_tool import code_graph_tool
from llm_provider import get_llm

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    incident_description = data.get('incident_description')
    analysis_level = data.get('analysis_level', 'Full Report')

    if not incident_description:
        return Response("Error: Missing 'incident_description' in request", status=400)

    def stream_analysis():
        """
        A generator function that runs tasks in stages using dedicated crews
        and yields the output of each stage.
        """
        final_report_content = ""
        try:
            llm = get_llm()

            # --- 1. Define all agents ---
            rca_agent = Agent(
                role='Expert System Diagnostician',
                goal="Analyze logs and use the Code Intelligence Graph to find the root cause.",
                backstory="You are a specialized AI agent for root cause analysis...",
                tools=[code_graph_tool], llm=llm, verbose=False
            )
            remediation_agent = Agent(
                role='Senior Site Reliability Engineer (SRE)',
                goal="Create a clear, actionable remediation plan based on a root cause analysis.",
                backstory="You are a seasoned SRE with decades of experience...",
                llm=llm, verbose=False
            )
            report_writer_agent = Agent(
                role='Technical Postmortem Writer',
                goal="Generate a comprehensive, blame-free postmortem report.",
                backstory="You are an expert technical writer...",
                llm=llm, verbose=False
            )

            # --- 2. Define tasks (descriptions will be updated with context later) ---
            # rca_task = Task(
            #     description=f"Analyze the incident log to find the error type. Use the tool with that error type to find the root cause in the source code.\n\nLog:\n---\n{incident_description}\n---",
            #     expected_output="A detailed root cause analysis, citing the faulty functions and code.",
            #     agent=rca_agent
            # )
            rca_task = Task(
                description=(
                    "Analyze the following incident log data to identify the primary error type. "
                    "The log may contain multiple entries; find the most critical pattern "
                    "(e.g., 'deadlock', 'exception', 'timeout', 'injection attempt'). "
                    "Once you identify the core ErrorType, use the Code Intelligence Graph Tool with that "
                    "ErrorType to find the root cause in the source code.\n\n"
                    f"Log Data:\n---\n{incident_description}\n---"
                ),
                expected_output="A detailed root cause analysis, citing the faulty functions and code.",
                agent=rca_agent
            )
            remediation_task = Task(
                description="Create a step-by-step remediation plan based on the provided root cause analysis.",
                expected_output="A numbered list of steps to resolve the issue.",
                agent=remediation_agent
            )
            report_task = Task(
                description="Combine the provided root cause analysis and remediation plan into a single, professional postmortem report.",
                expected_output="A complete, well-formatted markdown postmortem document.",
                agent=report_writer_agent
            )

            # --- 3. Execute each stage with its own crew and stream results ---
            
            # STAGE 1: Root Cause Analysis
            yield "### 🕵️‍♂️ Starting Root Cause Analysis...\n\n"
            rca_crew = Crew(agents=[rca_agent], tasks=[rca_task], process=Process.sequential)
            rca_output = rca_crew.kickoff()
            result_so_far = f"## Root Cause Analysis\n\n{rca_output}\n\n---\n"
            yield result_so_far

            # STAGE 2: Remediation Plan (if requested)
            if analysis_level in ["RCA + Remediation", "Full Report"]:
                yield "\n### 🛠️ Generating Remediation Plan...\n\n"
                # Inject the output of the first task into the description of the second
                remediation_task.description = f"Based on the following root cause analysis, create a step-by-step remediation plan.\n\n--- ANALYSIS ---\n{rca_output}\n---"
                remediation_crew = Crew(agents=[remediation_agent], tasks=[remediation_task], process=Process.sequential)
                remediation_output = remediation_crew.kickoff()
                result_so_far += f"## Remediation Plan\n\n{remediation_output}\n\n---\n"
                yield result_so_far

            # STAGE 3: Full Report (if requested)
            if analysis_level == "Full Report":
                yield "\n### 📝 Compiling Full Postmortem Report...\n\n"
                # Inject the output of both previous tasks into the report task description
                report_task.description = f"Combine the following root cause analysis and remediation plan into a single, professional postmortem report with sections for Summary, Root Cause, and Remediation.\n\n--- ROOT CAUSE ---\n{rca_output}\n\n--- REMEDIATION PLAN ---\n{remediation_output}\n---"
                report_crew = Crew(agents=[report_writer_agent], tasks=[report_task], process=Process.sequential)
                report_output = report_crew.kickoff()
                # For the final report, we replace all previous text with the final formatted output
                result_so_far = f"## Postmortem Report\n\n{report_output}"
                yield result_so_far
            
            final_report_content = result_so_far # Store the final complete text for download
            yield f"__END_OF_STREAM__\n{final_report_content}"

        except Exception as e:
            tb = traceback.format_exc()
            print(f"!!! AN ERROR OCCURRED: {e}\n{tb}")
            yield f"### ❌ An error occurred during analysis:\n\n```\n{e}\n```"

    return Response(stream_with_context(stream_analysis()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)