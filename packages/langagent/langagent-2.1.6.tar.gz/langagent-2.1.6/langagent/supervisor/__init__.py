# LangAgent/supervisor/__init__.py

from .supervisor_chain import create_supervisor_chain as supervisor_chain

# Define what will be accessible when doing `from LangAgent.supervisor import *`
__all__ = ['supervisor_chain']
