from setuptools import find_packages, setup

setup(
    name="josephliu164_tools",
    version="0.1.2",
    packages=find_packages(),  # 改用 find_packages()
    install_requires=[
        'redis',
        'supabase',
        'promptflow',
        'asyncio',
        'pyyaml'
    ],
    entry_points={
        "package_tools": [
            "josephliu164_tools = josephliu164_tools.tools.utils:list_tools"
        ],
    },
    include_package_data=True,
    package_data={
        'josephliu164_tools': ['yamls/*.yaml'],  # 确保包含 YAML 文件
    }
)