from setuptools import setup, find_packages

setup(
    name="ASTAligner",                     
    version="0.9.0",                       
    author="Semeru Lab",
    author_email="svelascodimate@wm.edu",
    description="ASTAligner is designed to align tokens from source code snippets to Abstract Syntax Tree (AST) nodes using Tree-sitter for AST generation and various HuggingFace tokenizers for language tokenization. The library supports a wide range of programming languages and Fast tokenizers, enabling precise mapping between source code elements and their AST representations.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/csci-435-fall-2024/csci-435-24_p4_ast",  
    packages=find_packages(),              
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',               
    install_requires=[
        "Flask==3.0.3",
        "Flask-Cors==5.0.0",
        "protobuf",
        "sentencepiece==0.2.0",
        "tokenizers==0.19.1",
        "transformers==4.44.2",
        "tree-sitter==0.23.0",
        "tree-sitter-cpp==0.23.1",
        "tree-sitter-java==0.23.2",
        "tree-sitter-python==0.23.2",
        "tree_sitter_c_sharp==0.23.1",
        "tree_sitter_go==0.23.3",
        "tree_sitter_haskell==0.23.1",
        "tree_sitter_javascript==0.23.1",
        "tree_sitter_kotlin==1.0.1",
        "tree_sitter_rust==0.23.1",
        "tree_sitter_html==0.23.2",
        "tree_sitter_c==0.23.2",
        "tree-sitter-ruby==0.23.1",
        "concurrently"
    ]
)
