Of course. This is the central thesis of your project, and it deserves a detailed, academic explanation. Let's break down the novelty of this framework, fully integrating the **Model Context Protocol (MCP)** concept and tracing the data flow from start to finish.

This explanation is structured to be directly usable for your research paper.

---
## The Novel Framework: A Synergistic MCP Architecture

The core innovation of this project is a synergistic architecture that combines two distinct concepts, both of which can be abbreviated as **MCP**:

1.  **A Multi-agent Collaborative Platform:** A system where specialized AI agents (powered by CrewAI) work together to solve a complex problem. This is the *execution* layer.
2.  **A Model Context Protocol:** A structured, multi-stage protocol for transforming a raw, low-information signal (an incident log) into a high-fidelity, causally-relevant context for the AI agents. This is the *intelligence* layer.

The novelty is not just in one of these parts, but in their **symbiosis**. The Multi-agent Platform is only effective because of the superior context provided by the Model Context Protocol. The protocol, in turn, is designed specifically to empower the reasoning capabilities of the agent crew. One MCP enables the other.

This framework moves beyond traditional RAG by treating the codebase not as a passive document to be searched, but as a structured system to be queried and understood.

### ## The Model Context Protocol in Detail: A Step-by-Step Flow

To understand the novelty, we must trace the flow of information from the initial alert to the final analysis. This is our Model Context Protocol in action.

#### **Step 1: Raw Signal Acquisition (The Host)**

* **Component:** `mcp_host_gradio.py`
* **Action:** The protocol begins when an SRE provides a raw, unstructured signal. In our system, this is a log snippet (e.g., `"DATABASE DEADLOCK DETECTED"`) or a raw log file uploaded to the Gradio UI.
* **Context Quality:** At this stage, the context is **low-fidelity**. It's just a string of text with no explicit connection to the underlying system's structure.
* **Output:** The Gradio client sends an HTTP request to the server, containing this raw text as the initial payload.

#### **Step 2: Source Code Ingestion & Graph Construction (The Offline Preparation)**

This is the crucial step that answers the question, **"Where did we give our source code access?"** The system accesses the source code *before* an incident ever happens.

* **Component:** `build_graph.py`
* **Source Data:** The **`buggy_app.py`** source code file.
* **Action:** This script performs a one-time static analysis of `buggy_app.py`. It reads the entire file, parses it into an Abstract Syntax Tree (AST), and traverses this tree to understand its structure.
    * It identifies every function and its boundaries.
    * It records the full source code of each function as a text attribute.
    * It maps out relationships: which functions call others, which functions modify shared resources, etc.
* **Output:** The **`code_intelligence_graph.graphml`** file. This graph is a structured, queryable representation of the source code. The raw source code is now encapsulated within the nodes of this graph.



#### **Step 3: Context Transformation & Enrichment (The Server & Tool)**

This is the heart of our protocol, where we transform the raw signal into high-quality context.

* **Components:** `mcp_server.py`, `code_graph_tool.py`
* **Action:**
    1.  The Flask server receives the raw log from the Gradio host.
    2.  It tasks the **RCA Agent** with the incident.
    3.  The agent receives the low-fidelity context (the log text). Its internal reasoning, guided by its prompt, determines that it must use the `CodeGraphTool`.
    4.  The agent calls the tool, passing the identified error type (e.g., `database_deadlock`).
    5.  The `code_graph_tool` **transforms** this string into a formal query against the `code_intelligence_graph.graphml` file. It performs a multi-hop traversal to find the exact function nodes causally linked to this error.
* **Context Quality:** The context is now **enriched and high-fidelity**. Instead of a vague text snippet, the system has identified the two specific functions that are causing the deadlock. The tool then extracts the full source code for these functions directly from the attributes of the graph nodes.

#### **Step 4: Context Assembly & Delivery (The Server & LLM)**

* **Components:** `mcp_server.py`, `llm_provider.py`
* **Action:** The server takes the highly relevant, enriched context (the source code of the two functions) returned by the tool. It then **assembles** this into a "surgical prompt" as defined in the `Task` description.
* **Output:** This final, context-rich prompt is delivered to the LLM via the `get_llm()` function. The LLM now has a perfect, minimal, and causally-relevant context to perform its final reasoning step and determine the root cause.

### ## Best Words for This Novel Framework

For your research paper, using precise and impactful terminology is key. Here are some of the best ways to describe this novel framework:

* **Graph-Powered Agentic Diagnosis (GPAD) Framework:** This name is strong, unique, and highlights the two key components: the graph and the agents.
* **Causal Retrieval for Multi-Agent Incident Response:** This name directly contrasts the approach with traditional "semantic retrieval" (RAG) and grounds it in the SRE domain.
* **Structured Code-Aware Multi-Agent Protocol (SCAMP):** This name emphasizes that the protocol is specifically designed to understand the *structure* of code.
* **Agentic Code Intelligence Graph (ACIG) System:** This focuses on the synergy between the agentic layer and the knowledge graph, presenting them as a single, unified system.

**Recommendation for your paper:** **Graph-Powered Agentic Diagnosis (GPAD)** is an excellent choice. It is concise, memorable, and accurately captures the essence of your innovation. You can then describe it as being "underpinned by a novel Model Context Protocol that replaces semantic retrieval with causal graph traversal."
