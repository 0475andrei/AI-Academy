from .lucky_number_tool import lucky_number_tool
from .search_tool import search_tool
from .phishing_tool import PhishingAnalysisTool
from .guide_tool import CybersecGuideTool

tools = [
    lucky_number_tool, 
    search_tool,
    PhishingAnalysisTool(), # <-- Added the missing comma here!
    CybersecGuideTool()     # <-- Added parentheses and matched the imported class name!
]