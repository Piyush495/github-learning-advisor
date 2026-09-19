from fastapi import APIRouter
router=APIRouter()

@router.get("/health")
def health():
    return{"Status:OK"}

@router.post("/analyze")
def analyze():
    return{"Analyzing github repo"}