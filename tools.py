import os
from crewai_tools import SerperDevTool  # type: ignore

os.environ["SERPER_API_KEY"] = "e83255269f1119f5f8e5a51eb2535f2f7c4690b2"
google_search_tool = SerperDevTool()
