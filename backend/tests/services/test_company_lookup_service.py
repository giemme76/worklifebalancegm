from app.services.company_lookup_service import lookup_company


def test_lookup_company_proposes_a_plausible_domain():
    result = lookup_company("Acme S.r.l.")
    assert result.website == "https://www.acme.com"


def test_lookup_company_strips_non_alphanumeric_and_legal_suffixes():
    result = lookup_company("Beta & Co. SpA")
    assert result.website == "https://www.betaco.com"


def test_lookup_company_headquarters_not_yet_determined():
    result = lookup_company("Acme")
    assert result.suggested_headquarters is None
