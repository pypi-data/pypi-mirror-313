# LangAgent/logic_team/agents/__init__.py

from .calculator import create_calculator as calculator
from .reasoner import create_reasoner as reasoner

# Define what will be accessible when doing `from LangAgent.logic_team.agents import *`
__all__ = ['calculator', 'reasoner']
