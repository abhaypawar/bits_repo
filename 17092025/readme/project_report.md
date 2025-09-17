LLM Powered Postmortem Automation for Site Reliability Engineering Teams

Course No: CC ZG628T

Dissertation (Mid-Term Report)

Student: Pawar Abhay Dnyandeo

BITS ID: 2022MT03552

Degree Program: Master of Technology in Cloud Computing

Dissertation / Project Work carried out at: Integra Micro Software Services (IMSS) Pvt Ltd, Bengaluru

Birla Institute of Technology & Science, Pilani – Rajasthan – 333031

First Semester 2025–2026 | September 15, 2025


Abstract

Modern systems are built as distributed microservices that amplify the cognitive load during incidents. Manually correlating logs, tracing code paths, diagnosing root causes, proposing remediations, and writing postmortems inflates Mean Time To Resolution (MTTR). This mid-term report presents a novel, operational prototype that reduces MTTR by combining a Graph-Powered Model Context Protocol (MCP) with a domain-specific multi-agent workflow. Instead of conventional vector-search-based RAG, the platform builds a Code Intelligence Graph from Abstract Syntax Trees (AST) and uses it to retrieve structurally causal context for Large Language Models (LLMs). A decoupled, local client–server architecture couples a Gradio host UI with a Flask backend that orchestrates three CrewAI agents: a Diagnostician (RCA), an SRE Engineer (Remediation), and a Technical Writer (Report). A realistic incident simulator generates high-fidelity logs, metrics, and business impact signals grounded in a deliberately buggy application. The prototype demonstrates accurate, explainable analysis for scenarios such as database deadlocks, slow queries, API incompatibilities, configuration lapses, and performance pathologies. The approach shows strong precision and auditability, while highlighting future needs for CI/CD graph refresh and telemetry enrichment.


Table of Contents

1.0 Introduction

1.1 The Real World Problem in Modern SRE: The Challenge of MTTR

1.2 The Inadequacy of Existing Paradigms for Code-Level Analysis

1.3 Thesis: A Novel Framework for Causal, Agentic Analysis

1.4 Core Contributions

2.0 System Architecture: A Decoupled, Multi-Component Design

2.1 Architectural Philosophy: The Decoupled Client–Server Model

2.2 The Multi-agent Collaborative Platform using Model Context Protocol

2.3 Component Deep Dive: The Role of Each File

3.0 The Simulation Environment: Generating High-Fidelity Incidents

3.1 Design Principles of the Incident Simulator

3.2 A Spectrum of Real-World Errors

3.3 The Ground Truth: buggy_app.py

4.0 The Core Innovation: The Graph-Powered Model Context Protocol

4.1 The Genesis of the Idea: From Semantic Failure to Structural Insight

4.2 The Code Intelligence Graph: A Deep Dive on the Schema

4.3 The Protocol in Action: An End-to-End Trace of a "Deadlock" Incident

5.0 Implementation and User Interaction

5.1 The Analysis Workflow: User-Controlled Depth

5.2 The Gradio Interface: An Interactive Gateway for SREs

5.3 Development Challenges and Resolutions

6.0 Evaluation and Results

6.1 Qualitative Assessment of Performance

6.2 Strengths and Limitations of the Framework

7.0 Conclusion and Future Work

Appendix A: Setup and Execution Guide

Appendix B: Sample Generated Postmortem Report


1.0 Introduction

1.1 The Real World Problem in Modern SRE: The Challenge of MTTR

As microservice ecosystems scale, incident responders confront fragmented telemetry, cross-service dependencies, and time pressure. Reconstructing causal chains from logs, metrics, and source code increases MTTR, affecting revenue and team morale. This work targets MTTR by automating the labor-intensive stages of diagnosis, remediation planning, and report writing while preserving transparency and control.

Beyond operational toil, prolonged MTTR compounds second-order effects: cascading retries expand blast radius, error budgets are rapidly consumed, and incident command overhead grows. Traditional postmortems often arrive too late to influence near-term engineering priorities. Our approach aims to compress this feedback loop by creating an AI-driven pipeline that moves from raw logs to audit-ready reports with explicit code citations—enabling earlier, more informed corrective actions.

1.2 The Inadequacy of Existing Paradigms for Code-Level Analysis

Standard RAG retrieves semantically similar text but lacks structural awareness. It cannot directly surface causally linked functions, resource lock ordering, or call graphs that explain failures such as deadlocks or API incompatibilities. The gap is not in language understanding but in context retrieval: semantic similarity ≠ causal relevance.

This limitation manifests in practice: given a "deadlock" keyword, a vector index may return commentary or unrelated helper functions that happen to mention locks. It will rarely reconstruct the lock acquisition order across functions, nor will it isolate the exact code paths that can cause circular waits. Likewise, configuration incidents (e.g., missing `SMTP_HOST`) are often best explained by the absence of required environment checks at specific code points—again, a structural question rather than a semantic one.

1.3 Thesis: A Novel Framework for Causal, Agentic Analysis

We hypothesize that a Code Intelligence Graph, assembled from AST-based static analysis and curated domain mappings, provides superior context for RCA than vector indices. Coupled with a multi-agent workflow operating over a Model Context Protocol, this enables precise, explainable diagnoses, targeted remediation, and high-quality postmortems.

Novelty arises from treating context as a first-class, typed graph that encodes causality, not a bag of tokens. By elevating retrieval to structured traversal, we ensure that LLM reasoning starts with the right evidence—the precise functions, their relationships, and the resources they contend for—thereby improving both accuracy and explainability.

1.4 Core Contributions

- A Graph-Powered Model Context Protocol that replaces vector search with a queryable, causally structured knowledge graph.
- A domain-specific CrewAI multi-agent pipeline (Diagnostician → Engineer → Writer) aligned to SRE workflows.
- An end-to-end prototype: incident generation → graph ingestion → agentic analysis → downloadable postmortem.

Additional novelties delivered in the prototype include a streaming, stage-gated workflow (RCA → Remediation → Report) that mirrors real incident handling, surgical prompt assembly with minimal noise and maximal code signal, and an auditable trail that ties every conclusion back to concrete code excerpts.


2.0 System Architecture: A Decoupled, Multi-Component Design

2.1 Architectural Philosophy: The Decoupled Client–Server Model

The system separates interaction from computation. The Gradio client (`mcp_host_gradio.py`) focuses on ingestion, controls (analysis depth, file vs text), streaming display, and artifact download. The Flask server (`mcp_server.py`) orchestrates agents and tools, streams intermediate outputs, and assembles the final report. This design supports independent evolution of UI, tools, and LLM providers.

Decoupling also improves resource isolation (UI remains responsive while long-running analysis executes on the server), enables horizontal scaling of backend workers, and permits per-stage checkpointing. The server emits a deterministic end-of-stream token for artifact generation, ensuring reproducibility and easy integration with external systems.

2.2 The Multi-agent Collaborative Platform using Model Context Protocol

MCP stages: (1) Acquisition of raw signal (log snippet/file), (2) Transformation & Enrichment via graph queries (structural context, not semantic matches), and (3) Assembly of a surgical prompt for the LLM. Three specialized agents execute sequentially using CrewAI: an RCA agent with the Code Graph Tool, a remediation agent, and a report writer. The backend streams results stepwise to the UI.

Unlike generic agents, our MCP-aware pipeline explicitly routes tool calls: only the diagnostician wields the Code Graph Tool, while subsequent agents consume structured outputs rather than re-querying raw logs. This separation limits prompt drift, reduces hallucination risk, and keeps each stage accountable to its defined inputs and outputs.

2.3 Component Deep Dive: The Role of Each File

- `enhanced_ecommerce_runner.py`: Generates realistic incidents, categorized logs, access logs, metrics, and business impact; persists `incident_data/*.json` and structured logs.
- `buggy_app.py`: Ground-truth buggy Flask app embodying deliberate failure modes: lock-order deadlock (`create_order`, `process_inventory_update`), slow query, env-misconfig, version mismatch, and long-running work.
- `build_graph.py`: Parses `buggy_app.py` with AST to construct a `networkx` directed graph; adds nodes for functions, services, database tables, and error types; writes `code_intelligence_graph.graphml`.
- `code_intelligence_graph.graphml`: Serialized knowledge graph with function source code stored as attributes and typed edges (`CONTAINS`, `CALLS`, `MODIFIES`, `CAN_CAUSE`, `IMPLEMENTS`).
- `code_graph_tool.py`: Agent tool to query the graph by `ErrorType` and retrieve causally linked functions with code.
- `mcp_server.py`: Flask API `/analyze` that builds stage-specific crews, injects context between stages, and streams outputs with an end-of-stream token.
- `mcp_host_gradio.py`: UI for text/file input, analysis depth selection (RCA Only, RCA + Remediation, Full Report), live streaming, and report download.
- `llm_provider.py`: Provider-agnostic LLM factory; current configuration supports OpenRouter and can be extended.

Collectively, these components provide end-to-end traceability: from an incident ID through simulator artifacts, to graph traversals, to the final markdown report with verbatim code citations.


3.0 The Simulation Environment: Generating High-Fidelity Incidents

3.1 Design Principles of the Incident Simulator

The simulator produces rich, correlated telemetry: application, error, and access logs; per-service metrics; incident metadata; and business impact summaries. It models realistic load patterns, recovery transitions, and category-specific signatures to validate graph-guided RCA.

Each simulated run emits:
- Timestamped application and error logs with SRE-friendly phrasing and stack patterns.
- Access logs with realistic endpoints, HTTP verbs, status codes, and response times.
- Structured incident JSON rows recording severity, fingerprint, affected services, and metrics snapshot.
- Periodic metrics frames linking service health, error rates, and throughput to ongoing incidents.
- Optional recovery events that transition services through down → critical → degraded → running, enabling lifecycle analysis.

3.2 A Spectrum of Real-World Errors

Categories and examples synthesized by `enhanced_ecommerce_runner.py`:

- Database Issues: connection leaks, deadlocks, slow queries, replication lag, connection timeouts.
- API Failures: third-party failure, rate limiting, service mesh failure, circuit breaker open, load balancer failure.
- Performance Bottlenecks: memory leak, high CPU, cache thrashing, thread pool exhaustion, GC pressure.
- Infrastructure Issues: disk space issues, network timeouts, DNS failures, Kubernetes pod evictions, autoscaling failures.
- Security Incidents: authentication failures, SQL injection attempts, DDoS, certificate expiration, unauthorized access attempts.
- Deployment Issues: configuration errors, rollback failures, health check failures, version incompatibilities, missing environment variables.

3.3 The Ground Truth: buggy_app.py

Each simulated incident maps to explicit defects in `buggy_app.py`, enabling objective validation of RCA correctness. Notably, the deadlock arises from inconsistent lock ordering between `create_order` (ORDERS→INVENTORY) and `process_inventory_update` (INVENTORY→ORDERS).

Additional ground-truth mappings include: environment misconfiguration in `send_notification` (missing `SMTP_HOST`), version incompatibility in `call_payment_service_from_order_service` (v2 vs v3 API), intentional slow path in `product_search`, and thread pool pressure via `run_heavy_computation`.


4.0 The Core Innovation: The Graph-Powered Model Context Protocol

4.1 The Genesis of the Idea: From Semantic Failure to Structural Insight

Early vector-based retrieval surfaced thematically similar content but missed causal code paths. Debugging depends on structure: call relationships, resource mutations, and error affinities. Representing code as a typed, directed graph enables targeted traversal for causality, not mere topical overlap.

Our approach prioritizes determinism and auditability: traversals replay exactly, edges encode intent (e.g., `CAN_CAUSE` expresses failure affinity), and function nodes carry full `source_code` for faithful citation. This re-centers the LLM on verifiable evidence.

4.2 The Code Intelligence Graph: A Deep Dive on the Schema

Node types: `Service`, `File`, `Function` (with `source_code`), `DatabaseTable`, and `ErrorType`.

Edge types: `IMPLEMENTS` (Service→Function), `CONTAINS` (File→Function), `CALLS` (Function→Function), `MODIFIES` (Function→Resource), `CAN_CAUSE` (Function→ErrorType).

This schema enables precise queries, e.g., from an `ErrorType` to the set of candidate `Function` nodes, and then extraction of exact source text used for a surgical prompt.

The builder stores complete function bodies, preserves file containment via `CONTAINS`, and enriches the graph with service-function `IMPLEMENTS` links defined by domain mapping. Together, these enable queries that bridge operational symptoms (error type) to implementation reality (functions and resources touched).

4.3 The Protocol in Action: An End-to-End Trace of a "Deadlock" Incident

Input: A log snippet featuring "DATABASE DEADLOCK DETECTED".

Transformation: The RCA agent identifies `database_deadlock` and invokes the Code Graph Tool. The tool traverses incoming `CAN_CAUSE` to `create_order` and `process_inventory_update`, retrieving their full source code attributes.

Assembly: The backend composes an RCA prompt enriched with the two functions and their lock usage. Subsequent agents generate a remediation plan (standardize lock order) and finalize a cohesive report.

Surgical prompt assembly purposely removes non-causal noise and includes just-enough context: function sources, relevant edges, and minimal instructions. This improves model focus, reduces token waste, and increases repeatability across runs.


5.0 Implementation and User Interaction

5.1 The Analysis Workflow: User-Controlled Depth

The UI exposes three analysis modes: (1) RCA Only (fast diagnosis), (2) RCA + Remediation (adds stepwise plan), and (3) Full Report (compiles a publishable postmortem). The server executes stage-specific crews in sequence and streams partial results.

Streaming includes human-friendly stage banners and a terminal token (`__END_OF_STREAM__`) to drive artifact persistence. File uploads are decoded and prioritized over text when present, ensuring fidelity for large incidents.

5.2 The Gradio Interface: An Interactive Gateway for SREs

`mcp_host_gradio.py` accepts pasted text or uploaded files, displays streaming progress for each stage, and enables Markdown report download for Full Report runs. Examples are provided to accelerate testing.

UX choices intentionally mirror incident management mental models: left-pane inputs (signal and scope), right-pane live narrative (analysis as it happens), and a single-click export into ticketing or docs. The interface stays stable while backends evolve, honoring the decoupled architecture.

5.3 Development Challenges and Resolutions

- Python environment inconsistencies (_ctypes and dependency resolution) were stabilized using a dedicated virtual environment.
- CrewAI API changes for tools and execution were adapted by passing the `code_graph_tool` function directly and by restructuring stage-wise crews.
- OpenRouter connectivity required specific header configuration and exact model naming; a provider-agnostic `get_llm()` factory encapsulates this.

Key lesson: tool scoping and stage isolation reduce brittleness. By constraining which agent invokes which tool, we achieved more stable outputs and fewer regressions when upgrading dependencies.


6.0 Evaluation and Results

6.1 Qualitative Assessment of Performance

Across simulated incidents, the graph-first context consistently surfaced causally relevant functions and code, enabling high-fidelity RCA. In the deadlock case, the system reliably cited both conflicting functions and their lock order, yielding a remediation with immediate effect on recurrence risk.

Qualitative observations across other scenarios:
- Environment variable missing: quickly pinpointed `send_notification` guard path and proposed configuration plus runtime safeguards.
- Version mismatch: identified `call_payment_service_from_order_service` and the deprecated path, suggesting contract alignment and feature-flagged interoperability.
- Slow queries: highlighted the synthetic latency in `product_search` and recommended indexing/caching strategies.

6.2 Strengths and Limitations of the Framework

- Strengths: Causal precision; explainability via explicit function/code citation; modular, decoupled design; user-controlled analysis depth; realistic, correlated simulation data.
- Limitations: Static graph requires regeneration to track code evolution; current graph focuses on a single service codebase; broader multi-repo, polyglot support and continuous ingestion are planned.

Practical mitigations include wiring graph regeneration into CI, adding incremental builders for changed files, and introducing runtime traces as edge priors to fuse static and dynamic views.


7.0 Conclusion and Future Work

This mid-term prototype operationalizes a Graph-Powered MCP for SRE tasks, replacing semantic retrieval with structural reasoning. The approach demonstrably improves diagnostic focus and report quality while preserving a clear audit trail from logs to code. Next steps include:

- CI/CD Integration: Automated graph build on every commit and versioned snapshots.
- Graph Enrichment: Incorporate Git history, authorship, change frequency, APM metrics (latency/error rates), and runtime traces as node/edge attributes.
- Agent Memory: Persist incident learnings to inform future RCA and remediation recommendations.
- Multi-repo and Polyglot Support: Extend parsers and schema to heterogeneous tech stacks.

The academic significance lies in demonstrating that structural retrieval materially improves LLM effectiveness for software diagnostics. By grounding generation in typed graphs and enforceable workflows, we move from "best-guess narratives" to traceable, systems-grade analysis suitable for production SRE.


Appendix A: Setup and Execution Guide

1. Create and activate a Python virtual environment.
2. Run `pip install -r requirements.txt`.
3. Create a `.env` with LLM provider details (e.g., OpenRouter API key, base URL, model).
4. Build the knowledge graph: `python build_graph.py`.
5. Generate incident logs and artifacts: `python enhanced_ecommerce_runner.py`.
6. Start the MCP backend server: `python mcp_server.py`.
7. Launch the Gradio host UI: `python mcp_host_gradio.py`.
8. Use the web UI to paste or upload logs, select analysis depth, and download the final report.


Appendix B: Sample Generated Postmortem Report (Excerpt)

## Postmortem Report

### 1. Summary
An incident occurred involving a database deadlock that impacted the `order-service` and `inventory-service`. The issue prevented the successful creation of new orders. The root cause was an inconsistent lock acquisition order between two competing transactions. A remediation plan standardizes lock order across functions.

### 2. Root Cause Analysis
The deadlock was caused by a race between `create_order` (locks `ORDERS` then `INVENTORY`) and `process_inventory_update` (locks `INVENTORY` then `ORDERS`). Under concurrency, each waits on the other, producing a deadlock detectable in logs and metrics.

### 3. Remediation Plan
1. Refactor `process_inventory_update` to acquire locks in the same order as `create_order` (ORDERS → INVENTORY).
2. Add code review guidelines and static checks for consistent multi-resource lock ordering.
3. Instrument deadlock counters and alerts; fail fast with retries to reduce user-facing impact.


