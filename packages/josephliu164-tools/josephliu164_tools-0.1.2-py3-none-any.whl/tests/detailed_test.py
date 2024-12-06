import sys
import os
from importlib.metadata import entry_points, distribution

def run_tests():
    print("=== Environment Information ===")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    print("\n=== Package Check ===")
    try:
        import my_tools
        print(f"my_tools package found at: {my_tools.__file__}")
    except ImportError as e:
        print(f"Failed to import my_tools: {e}")
    
    print("\n=== Entry Points Check ===")
    eps = entry_points()
    print("Available entry point groups:")
    for group in eps.groups:
        print(f"- {group}")
    
    print("\nLooking for package_tools entry points:")
    if hasattr(eps, "select"):
        tools = eps.select(group="package_tools")
    else:
        tools = eps.get("package_tools", [])
    
    for tool in tools:
        print(f"Found tool: {tool.name} = {tool.value}")
    
    print("\n=== Tools List Check ===")
    try:
        from my_tools.tools.utils import list_tools
        tools = list_tools()
        print(f"Available tools: {list(tools.keys())}")
    except Exception as e:
        print(f"Failed to list tools: {e}")

if __name__ == "__main__":
    run_tests()