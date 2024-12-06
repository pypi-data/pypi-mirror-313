# test_yaml.py
import os
import pkg_resources

def test_yaml_files():
    print("Testing YAML files...")
    package_name = "josephliu164_tools"
    
    # 获取包的安装位置
    dist = pkg_resources.working_set.by_key[package_name]
    package_path = dist.location
    print(f"\nPackage installed at: {package_path}")
    
    # 检查 yamls 目录
    yaml_dir = os.path.join(package_path, package_name, "yamls")
    print(f"\nLooking for YAML files in: {yaml_dir}")
    
    if os.path.exists(yaml_dir):
        yaml_files = [f for f in os.listdir(yaml_dir) if f.endswith('.yaml')]
        print(f"\nFound YAML files: {yaml_files}")
        
        # 读取每个 YAML 文件的内容
        for yaml_file in yaml_files:
            yaml_path = os.path.join(yaml_dir, yaml_file)
            with open(yaml_path, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"\nContent of {yaml_file}:")
                print(content)
    else:
        print("\nYAML directory not found!")