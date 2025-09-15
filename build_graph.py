#!/usr/bin/env python3
"""
Code Intelligence Graph Builder

This script parses a Python source file (buggy_app.py) using the `ast` module
to build a knowledge graph of its components and relationships using `networkx`.

The graph includes:
- Nodes for files, services, functions, database tables (locks), and error types.
- Edges for relationships like `CALLS`, `MODIFIES`, `CAN_CAUSE`, etc.

The resulting graph is saved as 'code_intelligence_graph.graphml' and a visualization
is displayed.
"""
import ast
import networkx as nx
import matplotlib.pyplot as plt
import os

# Helper to get the full source code of a function/class from the AST tree
from astunparse import unparse

class CodeVisitor(ast.NodeVisitor):
    """
    Traverses the Abstract Syntax Tree to find nodes and relationships.
    """
    def __init__(self, graph, filepath):
        self.graph = graph
        self.filepath = filepath
        self.current_function = None

    def visit_FunctionDef(self, node):
        """Called for each function definition."""
        self.current_function = node.name
        # Add the function node with its source code
        self.graph.add_node(
            node.name, 
            type='Function', 
            file=self.filepath,
            source_code=unparse(node).strip()
        )
        self.graph.add_edge(self.filepath, node.name, type='CONTAINS')
        
        # Let the visitor visit the children of this node
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        """Called for each function call."""
        if self.current_function and isinstance(node.func, ast.Name):
            callee_name = node.func.id
            # We only add call edges for functions defined in our app
            if callee_name in self.graph:
                self.graph.add_edge(self.current_function, callee_name, type='CALLS')
        self.generic_visit(node)
        
    def visit_With(self, node):
        """Called for 'with' statements, used here to detect lock usage."""
        if not self.current_function:
            self.generic_visit(node)
            return
            
        for item in node.items:
            if isinstance(item.context_expr, ast.Name):
                lock_name = item.context_expr.id
                if lock_name in ['DB_LOCK_INVENTORY', 'DB_LOCK_ORDERS']:
                    # Map lock variable to a conceptual database table
                    table_name = lock_name.replace('DB_LOCK_', '')
                    if not self.graph.has_node(table_name):
                        self.graph.add_node(table_name, type='DatabaseTable')
                    
                    self.graph.add_edge(self.current_function, table_name, type='MODIFIES')
        self.generic_visit(node)

class CodeGraphBuilder:
    """
    Builds and manages the Code Intelligence Graph.
    """
    def __init__(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Source file not found: {filepath}")
        self.filepath = filepath
        self.graph = nx.DiGraph()
        self.source_code = ""

    def build(self):
        """
        Main method to build the graph.
        1. Parses code with AST.
        2. Adds manual, high-level mappings.
        """
        print(f"1. Parsing source file: {self.filepath}...")
        with open(self.filepath, 'r') as f:
            self.source_code = f.read()
        
        # Add the file itself as the root node
        self.graph.add_node(self.filepath, type='File')
        
        tree = ast.parse(self.source_code)
        visitor = CodeVisitor(self.graph, self.filepath)
        visitor.visit(tree)
        print("   - AST parsing complete. Found functions and relationships.")
        
        print("2. Adding manual intelligence layer (Services, Errors)...")
        self._add_manual_mappings()
        print("   - Manual mappings applied.")

    def _add_manual_mappings(self):
        """
        This is a crucial step where we add domain knowledge that can't be
        inferred from the AST alone. We map functions to services and potential errors.
        """
        # --- Map Functions to Services ---
        service_mapping = {
            'user-service': ['user_login'],
            'product-service': ['product_search'],
            'order-service': ['create_order', 'call_payment_service_from_order_service'],
            'inventory-service': ['process_inventory_update'],
            'payment-service': ['process_payment'],
            'notification-service': ['send_notification'],
            'worker-service': ['run_heavy_computation']
        }
        for service, funcs in service_mapping.items():
            self.graph.add_node(service, type='Service')
            for func in funcs:
                if self.graph.has_node(func):
                    self.graph.add_edge(service, func, type='IMPLEMENTS')

        # --- Map Functions to Potential Errors (The "Intelligence") ---
        error_mapping = {
            'sql_injection_attempt': ['user_login'],
            'database_slow_queries': ['product_search'],
            'database_deadlock': ['create_order', 'process_inventory_update'],
            'version_compatibility_issue': ['call_payment_service_from_order_service'],
            'environment_variable_missing': ['send_notification'],
            'thread_pool_exhaustion': ['run_heavy_computation']
        }
        for error, funcs in error_mapping.items():
            self.graph.add_node(error, type='ErrorType')
            for func in funcs:
                if self.graph.has_node(func):
                    self.graph.add_edge(func, error, type='CAN_CAUSE')
                    
    def save_graph(self, output_path="code_intelligence_graph.graphml"):
        """Saves the graph to a file."""
        print(f"3. Saving graph to {output_path}...")
        # Add source code as a graph attribute
        self.graph.graph['source_code'] = self.source_code
        nx.write_graphml(self.graph, output_path)
        print("   - Graph saved successfully.")

    def visualize_graph(self):
        """Creates and displays a visualization of the graph."""
        print("4. Generating graph visualization...")
        plt.figure(figsize=(20, 20))
        
        pos = nx.spring_layout(self.graph, k=0.9, iterations=50)

        # Define colors for each node type
        color_map = {
            'File': 'gold', 'Service': 'skyblue', 'Function': 'lightgreen',
            'DatabaseTable': 'salmon', 'ErrorType': 'tomato'
        }
        node_colors = [color_map.get(self.graph.nodes[n].get('type', 'default'), 'grey') for n in self.graph.nodes]
        
        nx.draw_networkx_nodes(self.graph, pos, node_size=3000, node_color=node_colors)
        nx.draw_networkx_labels(self.graph, pos, font_size=10, font_weight='bold')
        
        edge_labels = nx.get_edge_attributes(self.graph, 'type')
        nx.draw_networkx_edges(self.graph, pos, arrowstyle='->', arrowsize=20, connectionstyle='arc3,rad=0.1')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, font_color='red')

        plt.title("Code Intelligence Graph", size=20)
        plt.show()
        print("   - Visualization complete.")

def main():
    """Main execution function."""
    source_file = "buggy_app.py"
    if not os.path.exists(source_file):
        print(f"ERROR: The source file '{source_file}' was not found.")
        print("Please ensure you have saved the buggy Flask application code in the same directory.")
        return

    try:
        # Step 1: Install astunparse if not present
        import astunparse
    except ImportError:
        print("Required library 'astunparse' not found. Installing...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "astunparse"])
        print("'astunparse' installed successfully.")

    builder = CodeGraphBuilder(source_file)
    builder.build()
    builder.save_graph()
    builder.visualize_graph()
    
    print("\n✅ Ingestion process complete!")
    print("Your Code Intelligence Graph is ready and saved as 'code_intelligence_graph.graphml'.")


if __name__ == "__main__":
    main()
