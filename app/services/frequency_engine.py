from dataclasses import dataclass, field
from typing import Any
from app.db.database import get_connection


@dataclass
class FrequencyDecision:
    matched: bool
    frequency: str | None = None
    action: str | None = None
    citation: str | None = None
    regulation: str | None = None
    section: str | None = None
    confidence: str = "Low"
    missing_information: list[str] = field(default_factory=list)
    reason: str | None = None


def _matches(value: Any, rule_value: Any) -> bool:
    if rule_value in (None, "", "ANY"):
        return True
    if value in (None, ""):
        return False
    return str(value).lower() == str(rule_value).lower()


def _provided_filter(value: Any) -> str | None:
    if value in (None, ""):
        return None
    value = str(value).strip()
    if not value or value.lower() == "all":
        return None
    return value.lower()


def determine_frequency(case: dict) -> FrequencyDecision:
    parameter = (case.get("parameter") or case.get("topic") or "").strip().lower()
    if not parameter:
        return FrequencyDecision(matched=False, missing_information=["parameter"], reason="Parameter is required.")

    jurisdiction = _provided_filter(case.get("jurisdiction"))
    regulation = _provided_filter(case.get("regulation"))

    query = """
        SELECT fr.*, r.regulation, r.section
        FROM frequency_rules fr
        JOIN regulations r ON r.id = fr.regulation_id
        WHERE LOWER(fr.parameter) LIKE ?
    """
    params: list[Any] = [f"%{parameter}%"]

    if jurisdiction:
        query += " AND LOWER(r.jurisdiction) = ?"
        params.append(jurisdiction)

    if regulation:
        query += " AND LOWER(r.regulation) = ?"
        params.append(regulation)

    query += " ORDER BY fr.specificity DESC, fr.id ASC"

    with get_connection() as conn:
        rules = conn.execute(query, params).fetchall()

    if not rules:
        return FrequencyDecision(matched=False, reason="No frequency rule found for this parameter.")

    for rule in rules:
        required = [x.strip() for x in (rule["missing_required_fields"] or "").split(",") if x.strip()]
        missing = [field for field in required if case.get(field) in (None, "")]
        if missing:
            return FrequencyDecision(
                matched=False,
                missing_information=missing,
                citation=rule["citation"],
                regulation=rule["regulation"],
                section=rule["section"],
                confidence="Low",
                reason="Missing required case information.",
            )

        pop = case.get("population_served")
        if pop not in (None, ""):
            pop = int(pop)
            if rule["population_min"] is not None and pop < rule["population_min"]:
                continue
            if rule["population_max"] is not None and pop > rule["population_max"]:
                continue

        if not _matches(case.get("system_type"), rule["system_type"]):
            continue
        if not _matches(case.get("source_type"), rule["source_type"]):
            continue
        if not _matches(case.get("result"), rule["result_condition"]):
            continue
        if not _matches(case.get("waiver_status"), rule["waiver_status"]):
            continue

        return FrequencyDecision(
            matched=True,
            frequency=rule["frequency"],
            action=rule["action"],
            citation=rule["citation"],
            regulation=rule["regulation"],
            section=rule["section"],
            confidence="High",
        )

    return FrequencyDecision(matched=False, reason="No matching rule for the case facts provided.")
