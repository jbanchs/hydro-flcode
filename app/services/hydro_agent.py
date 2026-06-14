from app.services.frequency_engine import determine_frequency
from app.services.regulation_service import find_regulatory_records


def answer_case(case: dict) -> dict:
    decision = determine_frequency(case)
    records = find_regulatory_records(case.get("parameter", ""), case.get("jurisdiction"))

    if not decision.matched:
        return {
            "answer": "I cannot confirm the required frequency from the available regulatory records.",
            "required_frequency": None,
            "action": None,
            "citation": decision.citation,
            "missing_information": decision.missing_information,
            "confidence": decision.confidence,
            "interpretation": decision.reason or "No cited rule matched this case.",
            "records": records,
        }

    return {
        "answer": "Based on the case provided, HYDRO found a cited regulatory frequency/action.",
        "required_frequency": decision.frequency,
        "action": decision.action,
        "citation": decision.citation,
        "regulation": decision.regulation,
        "section": decision.section,
        "missing_information": [],
        "confidence": decision.confidence,
        "interpretation": "Apply this frequency/action only to the case factors provided. If population, source type, waiver, or compliance status changes, the result may change.",
        "records": records,
    }
