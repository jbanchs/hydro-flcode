from app.db.database import get_connection


def list_regulations(search: str | None = None, jurisdiction: str | None = None, regulation: str | None = None):
    query = "SELECT * FROM regulations WHERE 1=1"
    params: list[str] = []

    if search:
        query += " AND (LOWER(topic) LIKE ? OR LOWER(description) LIKE ? OR LOWER(keywords) LIKE ? OR LOWER(section) LIKE ?)"
        term = f"%{search.lower()}%"
        params.extend([term, term, term, term])

    if jurisdiction and jurisdiction != "All":
        query += " AND jurisdiction = ?"
        params.append(jurisdiction)

    if regulation and regulation != "All":
        query += " AND regulation = ?"
        params.append(regulation)

    query += " ORDER BY category, topic, regulation"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def find_regulatory_records(parameter: str, jurisdiction: str | None = None):
    return list_regulations(search=parameter, jurisdiction=jurisdiction)
