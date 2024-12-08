import re
import uuid
from typing import List, Union
from dataclasses import dataclass
from .analysis import parse_analysis_options, AnalysisOption

# Core system prompt focused on role and purpose
SYSTEM_PROMPT = """I am Janito, your friendly software development buddy. I help you with coding tasks while being clear and concise in my responses."""


SELECTED_OPTION_PROMPT = """
Original request: {request}

Please provide detailed implementation using the following guide:
{option_text}

Current files:
<files>
{files_content}
</files>

RULES:
- When revmoing constants, ensure they are not used elsewhere
- When adding new features to python files, add the necessary imports
- Python imports should be inserted at the top of the file

Please provide the changes in this format:

## {uuid} file <filepath> modify "short file change description" ##
## {uuid} search/replace "short change description" ##
<search_content>
## {uuid} replace with ##
<replace_content>
## {uuid} file end ##

Or to delete content:
## {uuid} file <filepath> modify ##
## {uuid} search/delete "short change description" ##
<content_to_delete>
## {uuid} file end ##

For new files:
## {uuid} file <filepath> create "short description" ##
<full_file_content>
## {uuid} file end ##

RULES:
1. search_content MUST preserve the original identation/whitespace 
"""

def build_selected_option_prompt(option_text: str, request: str, files_content: str = "") -> str:
    """Build prompt for selected option details
    
    Args:
        option_text: Formatted text describing the selected option
        request: The original user request
        files_content: Content of relevant files
    """
    short_uuid = str(uuid.uuid4())[:8]
    
    return SELECTED_OPTION_PROMPT.format(
        option_text=option_text,
        request=request,
        files_content=files_content,
        uuid=short_uuid
    )
