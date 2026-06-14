from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.auth import require_user
from app.services.regulation_service import list_regulations
from app.services.hydro_agent import answer_case

router = APIRouter(prefix="/api", tags=["api"], dependencies=[Depends(require_user)])


class HydroCase(BaseModel):
    jurisdiction: str | None = None
    regulation: str | None = None
    system_type: str | None = None
    source_type: str | None = None
    population_served: int | None = None
    parameter: str
    sample_type: str | None = None
    result: str | None = None
    previous_results: str | None = None
    waiver_status: str | None = None
    compliance_history: str | None = None


@router.get("/regulations")
def regulations(search: str | None = None, jurisdiction: str | None = None, regulation: str | None = None):
    return {"items": list_regulations(search=search, jurisdiction=jurisdiction, regulation=regulation)}


@router.post("/ask")
def ask_hydro(case: HydroCase):
    return answer_case(case.model_dump())
