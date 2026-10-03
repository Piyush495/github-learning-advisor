from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyzeRequest, RepoSummary
from app.services.github_service import parse_github_url, fetch_repo_context
from app.services.llm_service import generate_repo_summary

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "OK"}

@router.post("/analyze", response_model=RepoSummary)
async def analyze(payload: AnalyzeRequest):
    try:
        owner, repo = parse_github_url(payload.repo_url)
        context = await fetch_repo_context(owner, repo)
        summary = generate_repo_summary(context)
        return summary
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
