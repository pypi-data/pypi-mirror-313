from setuptools import setup, find_packages

setup(
    name="Patcher-Neo",  # Name of your package
    version="1.0.1",
    packages=find_packages(),  # Automatically finds all Python packages in the directory
    install_requires=[
        "typer==0.9.0",         # Required for Typer CLI
        "requests>=2.0.0",      # HTTP requests library
        "groq"
        # Add other external dependencies as needed
    ],
    entry_points={
        "console_scripts": [
            "patch=PatchTool.__init__:app",  # Replace `stack-cli` with your desired CLI command name
        ],
    },
    description="A tool for various automation and query tasks.",
    author="Aayushman Katariya",  # Replace with your name
    author_email="sukrinogreg@gmail.com",  # Replace with your email
    url="https://github.com/aayushmanrepo/patcher",  # Replace with your project repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",  # Specify the minimum Python version
)
