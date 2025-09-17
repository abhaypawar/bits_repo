#!/usr/bin/env python3
"""
Code Intelligence Graph - Online Retrieval Tool

This script loads the pre-built code graph and provides functions to perform
multi-hop traversal queries to diagnose incidents. It simulates the process
an AI agent would use to find the root cause of an issue.

Scenario Simulated:
- Incident: A 'database_deadlock' is reported.
- Goal: Find the culpable functions, their source code, and construct a
  precise prompt for an LLM to perform the final analysis.
"""
import networkx as nx
import os

class GraphQueryEngine:
    """
    A tool for performing intelligent queries on the Code Intelligence Graph.
    This would be provided to a CrewAI agent.
    """
    def __init__(self, graph_path="code_intelligence_graph.graphml"):
        if not os.path.exists(graph_path):
            raise FileNotFoundError(f"Graph file not found: {graph_path}. Please run build_graph.py first.")
        
        print(f"🧠 Loading Code Intelligence Graph from '{graph_path}'...")
        self.graph = nx.read_graphml(graph_path)
        print("   - Graph loaded successfully.")

    def find_functions_causing_error(self, error_type: str) -> list[str]:
        """
        Performs the initial query to find functions linked to a specific error type.
        
        Query: "Find all Function nodes that have a 'CAN_CAUSE' relationship
                with the given ErrorType node."
        """
        culprits = []
        # The graph is directional. Edges go from Function -> ErrorType.
        # So we need to find the predecessors of the error_type node.
        if not self.graph.has_node(error_type):
            return []
            
        for predecessor in self.graph.predecessors(error_type):
            # Ensure the predecessor is a function and the edge type is correct.
            if (self.graph.nodes[predecessor].get('type') == 'Function' and
                self.graph[predecessor][error_type].get('type') == 'CAN_CAUSE'):
                culprits.append(predecessor)
        return culprits

    def find_modified_tables(self, function_names: list[str]) -> dict:
        """
        Performs a multi-hop query to find what database tables a list of
        functions interact with.
        
        Query: "For the given functions, find all DatabaseTable nodes they have
                a 'MODIFIES' relationship with."
        """
        modification_map = {}
        for func_name in function_names:
            modified_tables = []
            if not self.graph.has_node(func_name):
                continue

            for successor in self.graph.successors(func_name):
                if (self.graph.nodes[successor].get('type') == 'DatabaseTable' and
                    self.graph[func_name][successor].get('type') == 'MODIFIES'):
                    modified_tables.append(successor)
            modification_map[func_name] = modified_tables
        return modification_map

    def get_function_source_code(self, function_name: str) -> str:
        """
        Performs targeted retrieval of a function's source code from its node attribute.
        """
        if self.graph.has_node(function_name):
            return self.graph.nodes[function_name].get('source_code', '# Source code not found.')
        return f"# Function '{function_name}' not found in graph."

def run_deadlock_scenario(engine: GraphQueryEngine):
    """
    Simulates the end-to-end retrieval process for a database deadlock incident.
    """
    print("\n" + "="*70)
    print("🚨 SIMULATING INCIDENT: 'database_deadlock' detected!")
    print("="*70)

    incident_error_type = 'database_deadlock'

    # --- Step A: Initial Query ---
    print("\n[STEP 1/4] 🎯 Initial Query: Finding potential culprits...")
    print(f"   - Querying graph: Which functions CAN_CAUSE '{incident_error_type}'?")
    culprit_functions = engine.find_functions_causing_error(incident_error_type)
    
    if not culprit_functions:
        print("   - No functions found associated with this error. Exiting.")
        return

    print(f"   - ✅ Found {len(culprit_functions)} potential culprits: {', '.join(culprit_functions)}")

    # --- Step B: Multi-Hop Query ---
    print("\n[STEP 2/4] 🔗 Multi-Hop Query: Understanding resource contention...")
    print("   - Querying graph: Which DatabaseTables do these functions MODIFY?")
    table_modifications = engine.find_modified_tables(culprit_functions)
    
    print("   - ✅ Resource interactions found:")
    for func, tables in table_modifications.items():
        print(f"     - Function '{func}' modifies: {', '.join(tables)}")
        
    # --- Step C: Targeted Retrieval ---
    print("\n[STEP 3/4] 🔍 Targeted Retrieval: Fetching precise source code...")
    retrieved_code = {}
    for func_name in culprit_functions:
        print(f"   - Retrieving source for '{func_name}'...")
        retrieved_code[func_name] = engine.get_function_source_code(func_name)

    print("   - ✅ Source code retrieved for all culprits.")

    # --- Step D: Construct Augmented Prompt ---
    print("\n[STEP 4/4] 📝 Augmented Prompt Construction...")
    
    prompt_context = "A 'database_deadlock' incident occurred. A Code Intelligence Graph analysis has identified the following functions as the most likely root cause due to their interaction with shared database resources. The relevant source code is provided below."
    
    final_prompt = f"{prompt_context}\n\n"
    final_prompt += "#" * 50 + "\n"
    final_prompt += "# CULPRIT ANALYSIS\n"
    final_prompt += "#" * 50 + "\n\n"

    for func_name, source_code in retrieved_code.items():
        final_prompt += f"--- Function: {func_name} ---\n"
        final_prompt += f"--- Modifies Tables: {', '.join(table_modifications.get(func_name, []))} ---\n"
        final_prompt += "```python\n"
        final_prompt += source_code + "\n"
        final_prompt += "```\n\n"

    final_prompt += "--- TASK ---\n"
    final_prompt += "Analyze the provided source code for these functions. Specifically, examine the order in which they acquire database locks (e.g., `DB_LOCK_ORDERS`, `DB_LOCK_INVENTORY`). Identify the inconsistent lock ordering that is causing the deadlock and describe the exact remediation required to fix it."

    print("   - ✅ Final, surgical prompt for the LLM has been constructed:")
    print("\n" + "-"*70)
    print(final_prompt)
    print("-"*70)

def main():
    """Main execution function."""
    try:
        query_engine = GraphQueryEngine()
        run_deadlock_scenario(query_engine)
    except FileNotFoundError as e:
        print(f"\nERROR: {e}")
        print("Please ensure you have run 'build_graph.py' to generate the graph file first.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
