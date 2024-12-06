from setuptools import setup, find_packages

# Import version number
version = {}
with open("./ara_cli/version.py") as fp:
    exec(fp.read(), version)

setup(
    name="ara_cli",
    version=version['__version__'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ara = ara_cli.__main__:cli",
        ],
    },
    install_requires=[
        'langchain',
        'langchain-community',
        'langchain_openai',
        'llama-index',
        'llama-index-llms-openai',
        'llama-index-retrievers-bm25',
        'openai',
        'markdown-it-py',
        'json-repair',
        'tree_sitter',
        'tree_sitter_python',
        'tree_sitter_languages',
        'argparse',
        'argcomplete',
        'cmd2>=2.5',
    ],
)
