# LangAgent/research_team/agents/__init__.py

from .researcher import create_researcher as researcher
from .coder import create_coder as coder
from .weather import create_weather as weather

# Define what will be accessible when doing `from LangAgent.research_team.agents import *`
__all__ = ['researcher', 'coder', 'weather']
