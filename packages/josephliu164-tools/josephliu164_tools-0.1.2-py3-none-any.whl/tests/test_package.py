# test_package.py
import importlib
import importlib.metadata

PACKAGE_TOOLS_ENTRY = "package_tools"

def test():
    """Test if package tools are correctly configured and accessible"""
    print("Starting package tools test...")
    
    # 1. Check if package is installed
    try:
        import josephliu164_tools
        print("\n✓ Package 'josephliu164_tools' is installed")
        print(f"Version: {josephliu164_tools.__version__ if hasattr(josephliu164_tools, '__version__') else 'unknown'}")
        print(f"Location: {josephliu164_tools.__file__}")
    except ImportError as e:
        print("\n✗ Failed to import package 'josephliu164_tools'")
        print(f"Error: {str(e)}")
        return

    # 2. Check entry points
    print("\nChecking package tools entry points...")
    entry_points = importlib.metadata.entry_points()
    if hasattr(entry_points, "select"):
        entry_points = entry_points.select(group=PACKAGE_TOOLS_ENTRY)
    else:
        entry_points = entry_points.get(PACKAGE_TOOLS_ENTRY, [])
    
    entry_points = list(entry_points)
    if not entry_points:
        print("✗ No package tools entry points found")
        return
        
    print(f"Found {len(entry_points)} entry points:")
    for ep in entry_points:
        print(f"\nEntry point: {ep}")
        try:
            list_tool_func = ep.load()
            print("✓ Successfully loaded entry point function")
            
            # 3. Check tools list
            print("\nAttempting to list tools...")
            tools = list_tool_func()
            if not tools:
                print("✗ No tools returned by list function")
            else:
                print(f"✓ Found {len(tools)} tools:")
                for identifier, tool in tools.items():
                    print(f"\n  Tool: {identifier}")
                    print(f"  Details: {tool}")
                    
                    # 4. Try importing the tool module
                    try:
                        if "module" in tool:
                            importlib.import_module(tool["module"])
                            print(f"  ✓ Successfully imported module {tool['module']}")
                    except Exception as e:
                        print(f"  ✗ Failed to import module: {str(e)}")
                        
        except Exception as e:
            print(f"✗ Error loading entry point: {str(e)}")

if __name__ == "__main__":
    test()