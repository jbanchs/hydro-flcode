from app.services.frequency_engine import determine_frequency


def test_ccr_is_annual_for_cws():
    decision = determine_frequency({"parameter": "consumer confidence report", "system_type": "CWS"})
    assert decision.matched is True
    assert decision.frequency == "annual"
    assert "141" in decision.citation or "62-550" in decision.citation


def test_jurisdiction_filter_selects_florida_rule():
    decision = determine_frequency(
        {"parameter": "consumer confidence report", "system_type": "CWS", "jurisdiction": "Florida"}
    )
    assert decision.matched is True
    assert decision.frequency == "annual"
    assert decision.regulation == "FAC 62-550"
    assert "62-550" in decision.citation


def test_jurisdiction_filter_selects_federal_rule():
    decision = determine_frequency(
        {"parameter": "consumer confidence report", "system_type": "CWS", "jurisdiction": "Federal"}
    )
    assert decision.matched is True
    assert decision.frequency == "annual"
    assert decision.regulation == "40 CFR Part 141"
    assert "40 CFR" in decision.citation


def test_regulation_filter_selects_requested_regulation():
    decision = determine_frequency(
        {"parameter": "total coliform", "result": "positive", "regulation": "FAC 62-550"}
    )
    assert decision.matched is True
    assert decision.frequency == "triggered"
    assert decision.regulation == "FAC 62-550"
    assert "62-550" in decision.citation


def test_conflicting_jurisdiction_and_regulation_do_not_cross_match():
    decision = determine_frequency(
        {
            "parameter": "consumer confidence report",
            "system_type": "CWS",
            "jurisdiction": "Florida",
            "regulation": "40 CFR Part 141",
        }
    )
    assert decision.matched is False
    assert decision.reason == "No frequency rule found for this parameter."


def test_unknown_jurisdiction_does_not_fallback_to_other_jurisdiction():
    decision = determine_frequency(
        {"parameter": "consumer confidence report", "system_type": "CWS", "jurisdiction": "Palm Beach County"}
    )
    assert decision.matched is False
    assert decision.reason == "No frequency rule found for this parameter."


def test_positive_total_coliform_is_triggered():
    decision = determine_frequency({"parameter": "total coliform", "result": "positive"})
    assert decision.matched is True
    assert decision.frequency == "triggered"
    assert decision.citation


def test_missing_parameter_returns_missing_information():
    decision = determine_frequency({})
    assert decision.matched is False
    assert "parameter" in decision.missing_information


def test_routine_total_coliform_requires_population_and_system_type():
    decision = determine_frequency({"parameter": "total coliform", "result": "routine"})
    assert decision.matched is False
    assert "system_type" in decision.missing_information
    assert "population_served" in decision.missing_information
