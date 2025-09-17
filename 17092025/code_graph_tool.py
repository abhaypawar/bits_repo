import networkx as nx
import os
from crewai.tools import tool # <-- FINAL FIX: The correct path is 'crewai.tools'

# The logic engine remains the same, no changes needed here.
class GraphQueryEngine:
    """A query engine for the Code Intelligence Graph."""
    def __init__(self, graph_path="code_intelligence_graph.graphml"):
        if not os.path.exists(graph_path):
            raise FileNotFoundError(f"Graph file not found: {graph_path}.")
        self.graph = nx.read_graphml(graph_path)

    def find_functions_causing_error(self, error_type: str) -> list[str]:
        culprits = []
        if not self.graph.has_node(error_type): return []
        for predecessor in self.graph.predecessors(error_type):
            if (self.graph.nodes[predecessor].get('type') == 'Function' and
                self.graph[predecessor][error_type].get('type') == 'CAN_CAUSE'):
                culprits.append(predecessor)
        return culprits

    def find_modified_tables(self, function_names: list[str]) -> dict:
        modification_map = {}
        for func_name in function_names:
            modified_tables = []
            if not self.graph.has_node(func_name): continue
            for successor in self.graph.successors(func_name):
                if (self.graph.nodes[successor].get('type') == 'DatabaseTable' and
                    self.graph[func_name][successor].get('type') == 'MODIFIES'):
                    modified_tables.append(successor)
            modification_map[func_name] = modified_tables
        return modification_map

    def get_function_source_code(self, function_name: str) -> str:
        if self.graph.has_node(function_name):
            return self.graph.nodes[function_name].get('source_code', '# Source code not found.')
        return f"# Function '{function_name}' not found in graph."


@tool("Code Intelligence Graph Tool")
def code_graph_tool(error_type: str) -> str:
    """
    Analyzes the application's source code for root causes of an error.
    The input must be a single string representing the `ErrorType` from a log,
    such as 'database_deadlock' or 'sql_injection_attempt'.
    """
    try:
        engine = GraphQueryEngine()
        
        culprit_functions = engine.find_functions_causing_error(error_type)
        if not culprit_functions:
            return f"No functions found in the knowledge graph that are known to cause '{error_type}'."
        
        table_modifications = engine.find_modified_tables(culprit_functions)
        
        result = f"Analysis for ErrorType '{error_type}':\n"
        result += f"Found {len(culprit_functions)} potential culprit function(s): {', '.join(culprit_functions)}\n\n"
        
        for func in culprit_functions:
            source_code = engine.get_function_source_code(func)
            modified = table_modifications.get(func, [])
            result += f"--- Details for function: {func} ---\n"
            if modified:
                result += f"Modifies Resources: {', '.join(modified)}\n"
            result += "Source Code:\n```python\n"
            result += source_code + "\n```\n\n"
            
        return result
    except FileNotFoundError as e:
        return f"Error: The code intelligence graph file has not been generated yet. Please run build_graph.py. Details: {e}"
    except Exception as e:
        return f"An unexpected error occurred while querying the code graph: {e}"