import base64
import re
import httpx
from fastapi import HTTPException

def parse_github_url(url: str) -> tuple[str, str]:
    """Extract (owner, repo) from various GitHub URL formats."""
    clean_url = url.strip().rstrip("/")
    if clean_url.endswith(".git"):
        clean_url = clean_url[:-4]
    
    pattern = r"(?:https?://github\.com/)?([^/]+)/([^/]+)"
    match = re.search(pattern, clean_url)
    if not match:
        raise HTTPException(status_code=400, detail="Invalid GitHub repository URL format.")
    
    return match.group(1), match.group(2)

async def fetch_repo_context(owner: str, repo: str) -> dict:
    """Fetch repo metadata, README, and top-level directory structure using GitHub REST API."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    async with httpx.AsyncClient(headers=headers, timeout=10.0) as client:
        # Fetch Repository Metadata
        meta_res = await client.get(f"https://api.github.com/repos/{owner}/{repo}")
        if meta_res.status_code == 404:
            raise HTTPException(status_code=404, detail="Repository not found on GitHub.")
        elif meta_res.status_code != 200:
            raise HTTPException(status_code=meta_res.status_code, detail="Failed to fetch repository info from GitHub.")
        
        meta_data = meta_res.json()
        
        # Fetch README content
        readme_content = "No README found."
        readme_res = await client.get(f"https://api.github.com/repos/{owner}/{repo}/readme")
        if readme_res.status_code == 200:
            readme_json = readme_res.json()
            try:
                readme_content = base64.b64decode(readme_json["content"]).decode("utf-8", errors="ignore")
                readme_content = readme_content[:4000]
            except Exception:
                readme_content = "Failed to decode README content."

        # Fetch top-level contents / structure
        files_list = []
        contents_res = await client.get(f"https://api.github.com/repos/{owner}/{repo}/contents")
        if contents_res.status_code == 200:
            contents_json = contents_res.json()
            files_list = [item["name"] for item in contents_json if isinstance(item, dict) and "name" in item]

        return {
            "name": meta_data.get("name", repo),
            "owner": owner,
            "description": meta_data.get("description", "No description provided."),
            "primary_language": meta_data.get("language", "Not specified"),
            "stars": meta_data.get("stargazers_count", 0),
            "files": files_list[:30],
            "readme": readme_content
        }
