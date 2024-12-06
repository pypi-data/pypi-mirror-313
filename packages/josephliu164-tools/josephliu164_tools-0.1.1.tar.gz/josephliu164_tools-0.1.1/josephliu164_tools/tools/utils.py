from ruamel.yaml import YAML
from pathlib import Path
from typing import Dict, Any  # 确保导入 Dict
import os


def collect_tools_from_directory(base_dir) -> dict:
    tools = {}
    yaml = YAML()
    for f in Path(base_dir).glob("**/*.yaml"):
        with open(f, "r") as f:
            tools_in_file = yaml.load(f)
            for identifier, tool in tools_in_file.items():
                tools[identifier] = tool
    return tools


def list_package_tools():
    """List package tools"""
    yaml_dir = Path(__file__).parents[1] / "yamls"
    return collect_tools_from_directory(yaml_dir)



def list_tools() -> Dict[str, Any]:
    """List all tools in the package"""
    tools = {}
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.dirname(__file__))
    yaml_dir = os.path.join(current_dir, "yamls")
    
    # 确保yamls目录存在
    if not os.path.exists(yaml_dir):
        print(f"YAML directory not found: {yaml_dir}")
        return tools
    
    # 读取所有YAML文件
    for yaml_file in os.listdir(yaml_dir):
        if yaml_file.endswith('.yaml'):
            try:
                yaml_path = os.path.join(yaml_dir, yaml_file)
                with open(yaml_path, 'r', encoding='utf-8') as f:
                    tool_name = yaml_file[:-5]  # 移除 .yaml 扩展名
                    tools[tool_name] = f.read()
                    print(f"Loaded tool: {tool_name} from {yaml_file}")
            except Exception as e:
                print(f"Error loading {yaml_file}: {str(e)}")
    
    return tools