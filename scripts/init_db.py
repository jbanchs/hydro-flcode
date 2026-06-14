import os
import sqlite3
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from app.services.auth_service import hash_password

DB = Path(os.getenv("HYDRO_DATABASE_PATH", BASE_DIR / "hydro.db"))

schema = """
DROP TABLE IF EXISTS frequency_rules;
DROP TABLE IF EXISTS regulations;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE regulations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    topic TEXT NOT NULL,
    regulation TEXT NOT NULL,
    section TEXT NOT NULL,
    description TEXT NOT NULL,
    frequency_summary TEXT NOT NULL,
    frequency_type TEXT NOT NULL,
    jurisdiction TEXT NOT NULL,
    citation TEXT NOT NULL,
    keywords TEXT NOT NULL
);

CREATE TABLE frequency_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    regulation_id INTEGER NOT NULL,
    parameter TEXT NOT NULL,
    system_type TEXT DEFAULT 'ANY',
    source_type TEXT DEFAULT 'ANY',
    population_min INTEGER,
    population_max INTEGER,
    result_condition TEXT DEFAULT 'ANY',
    waiver_status TEXT DEFAULT 'ANY',
    frequency TEXT NOT NULL,
    action TEXT NOT NULL,
    missing_required_fields TEXT DEFAULT '',
    citation TEXT NOT NULL,
    specificity INTEGER DEFAULT 0,
    FOREIGN KEY(regulation_id) REFERENCES regulations(id)
);
"""

regulations = [
    ("Maximum Contaminant Level", "Nitrate as N", "40 CFR Part 141", "141.62(b)", "Maximum contaminant level for nitrate as nitrogen.", "Monitor according to inorganic chemical monitoring schedule.", "conditional", "Federal", "40 CFR 141.62(b)", "nitrate nitrogen mcl inorganic"),
    ("Maximum Contaminant Level", "Nitrate as N", "FAC 62-550", "62-550.310 / 62-550.320", "Florida drinking water standards for maximum contaminant levels.", "Monitor according to FAC 62-550 monitoring schedule.", "conditional", "Florida", "FAC 62-550.310; FAC 62-550.320", "nitrate nitrogen mcl florida"),
    ("Microbiological Monitoring", "Total Coliform", "40 CFR Part 141", "Subpart Y", "Revised Total Coliform Rule requirements for routine/repeat monitoring and assessments.", "Routine frequency plus triggered repeat/assessment actions.", "triggered", "Federal", "40 CFR Part 141 Subpart Y", "total coliform rtcr repeat assessment"),
    ("Microbiological Monitoring", "Total Coliform", "FAC 62-550", "62-550.518 / 62-550.830", "Florida microbiological monitoring and RTCR implementation requirements.", "Routine monitoring; triggered actions after positive results.", "triggered", "Florida", "FAC 62-550.518; FAC 62-550.830", "total coliform rtcr florida microbiological"),
    ("Reporting", "Consumer Confidence Report", "40 CFR Part 141", "Subpart O", "Minimum federal requirements for Consumer Confidence Reports.", "Annual.", "annual", "Federal", "40 CFR Part 141 Subpart O", "consumer confidence report ccr annual"),
    ("Reporting", "Consumer Confidence Report", "FAC 62-550", "62-550.824", "Florida Consumer Confidence Report requirements for community water systems.", "Annual.", "annual", "Florida", "FAC 62-550.824", "consumer confidence report ccr florida annual"),
    ("Reporting", "Public Notification", "40 CFR Part 141", "Subpart Q", "Public notification requirements for violations and situations requiring notice.", "Triggered by violation; Tier 1, 2, or 3 timing.", "triggered", "Federal", "40 CFR Part 141 Subpart Q", "public notification violation tier"),
    ("Reporting", "General Reporting", "FAC 62-550", "62-550.730", "Florida public water system reporting requirements.", "As required by result, event, or reporting schedule.", "conditional", "Florida", "FAC 62-550.730", "reporting florida dep forms"),
]

frequency_rules = [
    # regulation index, parameter, system_type, source_type, pop_min, pop_max, result, waiver, frequency, action, required, citation, specificity
    (1, "nitrate", "ANY", "ANY", None, None, "ANY", "ANY", "conditional", "Use inorganic chemical monitoring schedule; frequency depends on system/source and compliance history.", "system_type,source_type", "40 CFR 141.62(b)", 10),
    (2, "nitrate", "ANY", "ANY", None, None, "ANY", "ANY", "conditional", "Use Florida monitoring schedule for nitrate/inorganic chemicals.", "system_type,source_type", "FAC 62-550.310; FAC 62-550.320", 10),
    (3, "total coliform", "ANY", "ANY", None, None, "positive", "ANY", "triggered", "Positive routine total coliform result triggers repeat monitoring and may trigger assessment based on follow-up results/history.", "result", "40 CFR Part 141 Subpart Y", 50),
    (4, "total coliform", "ANY", "ANY", None, None, "positive", "ANY", "triggered", "Florida RTCR implementation applies; repeat/assessment action required based on result pattern.", "result", "FAC 62-550.518; FAC 62-550.830", 50),
    (3, "total coliform", "ANY", "ANY", None, None, "routine", "ANY", "monthly / population-based", "Routine total coliform monitoring frequency depends on system type and population served.", "system_type,population_served", "40 CFR Part 141 Subpart Y", 20),
    (5, "consumer confidence report", "CWS", "ANY", None, None, "ANY", "ANY", "annual", "Community water systems must prepare and deliver a Consumer Confidence Report annually.", "system_type", "40 CFR Part 141 Subpart O", 40),
    (6, "consumer confidence report", "CWS", "ANY", None, None, "ANY", "ANY", "annual", "Florida community water systems must comply with CCR requirements annually.", "system_type", "FAC 62-550.824", 40),
    (7, "public notification", "ANY", "ANY", None, None, "violation", "ANY", "triggered", "Public notification timing depends on Tier 1, Tier 2, or Tier 3 classification.", "result", "40 CFR Part 141 Subpart Q", 40),
]

with sqlite3.connect(DB) as conn:
    conn.executescript(schema)
    admin_password = os.getenv("HYDRO_BOOTSTRAP_ADMIN_PASSWORD")
    if admin_password:
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (os.getenv("HYDRO_BOOTSTRAP_ADMIN_USERNAME", "admin"), hash_password(admin_password)),
        )
    conn.executemany(
        """
        INSERT INTO regulations (category, topic, regulation, section, description, frequency_summary, frequency_type, jurisdiction, citation, keywords)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        regulations,
    )
    conn.executemany(
        """
        INSERT INTO frequency_rules (regulation_id, parameter, system_type, source_type, population_min, population_max, result_condition, waiver_status, frequency, action, missing_required_fields, citation, specificity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        frequency_rules,
    )
print(f"Initialized database at {DB}")
