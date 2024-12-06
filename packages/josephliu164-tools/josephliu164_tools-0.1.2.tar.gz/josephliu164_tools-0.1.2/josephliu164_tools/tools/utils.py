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


def list_tools():
    """List all available tools in the package."""
    tools = {}
    # 使用 Path 来处理路径
    current_dir = Path(__file__).parent.parent
    yaml_dir = current_dir / "yamls"
    
    print(f"Looking for YAMLs in: {yaml_dir}")  # 调试信息
    
    if not yaml_dir.exists():
        print(f"Warning: YAML directory not found at {yaml_dir}")
        return tools
        
    for yaml_file in yaml_dir.glob("*.yaml"):
        try:
            with yaml_file.open('r', encoding='utf-8') as f:
                tool_dict = yaml.safe_load(f)
                name = tool_dict.get('name', '').lower().replace(' ', '_')
                if name:
                    # 设置正确的模块路径
                    base_module = 'josephliu164_tools.tools'
                    tool_file = yaml_file.stem
                    tool_dict['module'] = f'{base_module}.{tool_file}'
                    print(f"Loaded tool: {name} from {yaml_file}")  # 调试信息
                    tools[name] = tool_dict
        except Exception as e:
            print(f"Error loading {yaml_file}: {str(e)}")
                
    return tools