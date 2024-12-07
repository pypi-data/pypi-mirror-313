# LangAgent/setup.py

# * LIBRARIES

from setuptools import setup, find_packages

# Load the README file as the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="LangAgent",  # The name of your package
    version="2.1.1",  # Initial version
    author='Kwadwo Daddy Nyame Owusu - Boakye',  # Author's name
    author_email='kwadwo.owusuboakye@outlook.com',  # Author's contact email
    description=(
        "LangAgent is a versatile multi-agent system designed to streamline complex tasks such as research, "
        "automated code generation, logical reasoning, data analysis, and dynamic reporting. Powered by advanced "
        "language models, it integrates seamlessly with external APIs, databases, and a variety of data formats, "
        "enabling developers and professionals to automate workflows, extract insights, and generate professional-grade "
        "reports effortlessly."
    ),  # Detailed short description
    long_description=long_description,  # Long description from README.md
    long_description_content_type="text/markdown",  # Content type of README
    url='https://github.com/knowusuboaky/LangAgent',  # GitHub repository URL
    packages=find_packages(include=["langagent", "langagent.*"]),  # Automatically find and include all packages in LangAgent
    install_requires=[  # List of dependencies required to run the package
        "langchain==0.1.16",
        "langchain-community==0.0.33",
        "langchain-core==0.1.52",
        "langchain-experimental==0.0.57",
        "langchain-groq==0.1.3",
        "langchain-openai==0.0.8",
        "langchain-text-splitters==0.0.1",
        "langgraph==0.0.48",
        "langsmith==0.1.27",
        "tavily-python",
        "ipython==8.18.0",
        "ipywidgets==8.1.2",
        "plotly>=5.0.0",
        "kubernetes==29.0.0",
        "yfinance>=0.1.0",
        "PyYAML>=6.0",
        "sqlalchemy>=2.0.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.2",
        "tqdm>=4.0.0",
        "pandas>=1.1.0",
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3",
        "numpy>=1.21.0",
        "scikit-learn>=0.24.0",
        "sentence-transformers>=2.2.2",
        "pypdf2>=3.0.0",
        "python-pptx>=0.6.21",
        "python-docx>=0.8.11",
        "nbformat>=4.2.0",
        "numexpr>=2.8.4",
        "pyowm>=3.3.0",
    ],
    classifiers=[  # Optional classifiers for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',  # Minimum Python version requirement
    keywords=[
        'AI', 'machine learning', 'language models', 'multi-agent systems', 'research automation', 
        'code generation', 'data analysis', 'reasoning', 'reporting', 'LangChain', 'Python', 
        'SQL', 'data visualization', 'automation', 'OpenAI', 'data science', 'natural language processing', 
        'deep learning', 'document summarization', 'web scraping', 'APIs', 'business intelligence', 'LangChain', 'LangSmith'
    ],  # Keywords for discoverability
)
