from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from app.models.schemas import RepoSummary

def generate_repo_summary(repo_context: dict) -> RepoSummary:
    """Generate structured summary using LangChain's modern init_chat_model factory."""
    
    llm = init_chat_model("gpt-4o-mini", model_provider="openai", temperature=0)
    
    # Bind Pydantic structured output
    structured_llm = llm.with_structured_output(RepoSummary)
    
    system_prompt = (
        "You are an expert software engineer and technical educator. "
        "Analyze the provided GitHub repository context and generate a structured summary.\n\n"
        "Repository Details:\n"
        "- Name: {name}\n"
        "- Owner: {owner}\n"
        "- Description: {description}\n"
        "- Primary Language: {primary_language}\n"
        "- Stars: {stars}\n"
        "- Directory Structure / Files: {files}\n\n"
        "README Snippet:\n{readme}\n"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "Summarize this repository.")
    ])

    chain = prompt | structured_llm
    
    summary: RepoSummary = chain.invoke({
        "name": repo_context["name"],
        "owner": repo_context["owner"],
        "description": repo_context["description"],
        "primary_language": repo_context["primary_language"],
        "stars": repo_context["stars"],
        "files": ", ".join(repo_context["files"]),
        "readme": repo_context["readme"]
    })

    return summary
