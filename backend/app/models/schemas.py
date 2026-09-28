from pydantic import Field
from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    repo_url:str=Field(...,description="Full GitHub repository URL or owner/repo string")


class RepoSummary(BaseModel):
    project_summary: str = Field(..., description="A concise 2-3 sentence overview of what the repository does and its main purpose.")
    tech_stack: list[str] = Field(..., description="List of core programming languages, frameworks, databases, and key libraries used.")
    main_features: list[str] = Field(..., description="List of top key features or capabilities provided by the repository.")
    how_to_run: list[str] = Field(...,description="Step-by-step instructions (commands) to clone, install, and run the repository.")
    difficulty: str = Field(...,description="Estimated difficulty level to understand and work with this project: 'Beginner', 'Intermediate', or 'Advanced'.")
