# test_tools.py
import importlib.metadata

def test_package_tools():
    print("Starting test...")
    
    entry_points = importlib.metadata.entry_points()
    print(f"Found entry_points: {entry_points}")
    
    if hasattr(entry_points, "select"):
        print("Using select method")
        package_tools = entry_points.select(group="package_tools")
    else:
        print("Using get method")
        package_tools = entry_points.get("package_tools", [])
    
    print(f"Package tools: {package_tools}")
    
    print("\nAll available entry points groups:")
    for group in entry_points.groups:
        print(f"- {group}")

if __name__ == "__main__":
    test_package_tools()