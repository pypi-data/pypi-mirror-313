from setuptools import find_packages, setup

setup(
    name="josephliu164_tools",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "redis",
        "supabase",
        "promptflow",
        "asyncio"
    ],
    entry_points={
        "package_tools": [
            "josephliu164_tools_tools = my_tools.tools.utils:list_tools"
        ],
    },
    include_package_data=True,
    package_data={
        'josephliu164_tools': ['yamls/*.yaml']
    }
)