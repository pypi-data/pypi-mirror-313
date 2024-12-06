# test_utils.py
from josephliu164_tools.tools.utils import list_tools
import os

def test_list_tools():
    print("Testing list_tools function...")
    tools = list_tools()
    print(f"\nFound {len(tools)} tools:")
    for name, tool in tools.items():
        print(f"\nTool: {name}")
        print(f"Details: {tool}")

if __name__ == "__main__":
    test_list_tools()

# test_yaml.py
import os
import pkg_resources

def test_yaml_files():
    print("Testing YAML files...")
    package_name = "josephliu164_tools"
    
    try:
        dist = pkg_resources.working_set.by_key[package_name]
        package_path = dist.location
        print(f"\nPackage installed at: {package_path}")
        
        yaml_dir = os.path.join(package_path, package_name, "yamls")
        print(f"\nLooking for YAML files in: {yaml_dir}")
        
        if os.path.exists(yaml_dir):
            yaml_files = [f for f in os.listdir(yaml_dir) if f.endswith('.yaml')]
            print(f"\nFound YAML files: {yaml_files}")
            
            for yaml_file in yaml_files:
                yaml_path = os.path.join(yaml_dir, yaml_file)
                with open(yaml_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"\nContent of {yaml_file}:")
                    print(content)
        else:
            print("\nYAML directory not found!")
    except KeyError:
        print(f"\nPackage {package_name} not found in working set!")

if __name__ == "__main__":
    test_yaml_files()