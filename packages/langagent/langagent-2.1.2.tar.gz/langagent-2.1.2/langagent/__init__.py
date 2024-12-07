# LangAgent/__init__.py

# Import agents from the research team
from .research_team.agents.researcher import create_researcher as researcher
from .research_team.agents.coder import create_coder as coder
from .research_team.agents.weather import create_weather as weather

# Import agents from the logic team
from .logic_team.agents.calculator import create_calculator as calculator
from .logic_team.agents.reasoner import create_reasoner as reasoner

# Import agents from the analysis team
from .analysis_team.agents.sql_databaser import create_sql_databaser as sql_databaser
from .analysis_team.agents.topic_generator import create_topic_generator as topic_generator

# Import agents from the reporting team
from .reporting_team.agents.interpreter import create_interpreter as interpreter
from .reporting_team.agents.summarizer import create_summarizer as summarizer

# Import supervisor chain
from .supervisor.supervisor_chain import create_supervisor_chain as supervisor_chain

# Define what will be accessible when doing `from LangAgent import *`
__all__ = [
    'researcher', 'coder', 'weather',       # Research team agents
    'calculator', 'reasoner',               # Logic team agents
    'sql_databaser', 'topic_generator',     # Analysis team agents
    'interpreter', 'summarizer',            # Reporting team agents
    'supervisor_chain'                      # Supervisor agent
]
