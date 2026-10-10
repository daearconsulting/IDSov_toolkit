from pathlib import Path

import pandas as pd
import pytest
import yaml

from toolkit.audit import SovereigntyAudit
from toolkit.drought import load_fixture, parse_noaa, prepare_annual
from toolkit.provenance import ProvenanceBuilder, ProvenanceRecord
from toolkit.teaching import load_context

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def context():
    return load_context(ROOT, "config/teaching_example.yaml")


def test_blank_template_requires_completion():
    with pytest.raises(ValueError, match="placeholder"):
        load_context(ROOT, "config/nation_template.yaml")


def test_explicit_config_and_framework_selection(context):
    other = load_context(ROOT, "config/teaching_second_nation.yaml")
    assert other.config.name != context.config.name
    assert other.config.analysis["divisions"] == [1, 2]
    audit = SovereigntyAudit("test", frameworks=other.config.active_frameworks)
    assert set(audit.frameworks) == {"CARE", "IEEE 2890-2025"}
    record = (
        ProvenanceBuilder("other")
        .for_nation(other)
        .for_dataset("test")
        .classify("PUBLIC")
        .build()
    )
    assert record.nation_name == other.config.name
    assert "FAIR" not in record.frameworks


def test_config_precedence_and_invalid_selection(tmp_path, monkeypatch):
    (tmp_path / "config").mkdir()
    teaching = (ROOT/"config/teaching_example.yaml").read_text(encoding="utf-8")
    (tmp_path/"config/teaching_example.yaml").write_text(teaching, encoding="utf-8")
    monkeypatch.delenv("IDSOV_CONFIG", raising=False)
    assert load_context(tmp_path).config.teaching
    other = (ROOT/"config/teaching_second_nation.yaml").read_text(encoding="utf-8")
    (tmp_path/"config/nation.yaml").write_text(other, encoding="utf-8")
    assert "Mountain" in load_context(tmp_path).config.name
    monkeypatch.setenv("IDSOV_CONFIG", "config/teaching_example.yaml")
    assert "River" in load_context(tmp_path).config.name
    assert "Mountain" in load_context(tmp_path, "config/nation.yaml").config.name
    monkeypatch.setenv("IDSOV_CONFIG", "missing.yaml")
    with pytest.raises(FileNotFoundError):
        load_context(tmp_path)


def test_one_yes_cannot_score_strong():
    audit = SovereigntyAudit("incomplete")
    audit.respond("OCAP-O1", "yes")
    assert audit.overall_score is None
    assert audit.completion == pytest.approx(1 / 27)
    assert "INCOMPLETE" in audit.report()
    assert "STRONG" not in audit.report()


def completed_audit():
    audit = SovereigntyAudit("complete", frameworks=["care"])
    for q in audit.questions:
        audit.respond(
            q.id,
            "yes",
            evidence="private:review/1",
            reviewer="Reviewer",
            reviewed_on="2026-10-09",
        )
    return audit


def test_approval_cannot_be_averaged_away():
    audit = completed_audit()
    assert audit.overall_score == 100
    assert "BLOCKED" in audit.readiness
    for gate in audit.approvals:
        audit.record_approval(
            gate,
            "approved",
            evidence="private:approval/1",
            reviewer="Authorized reviewer",
            reviewed_on="2026-10-09",
        )
    assert "DOCUMENTED FOR NATION REVIEW" in audit.readiness
    audit.record_approval("sharing_authorization", "revoked")
    assert "BLOCKED" in audit.readiness


def test_invalid_response_na_and_approval():
    audit = SovereigntyAudit("test")
    for value in ["YES", "maybe", ""]:
        with pytest.raises(ValueError):
            audit.respond("CARE-C1", value)
    with pytest.raises(ValueError, match="rationale"):
        audit.respond("CARE-C1", "na")
    with pytest.raises(ValueError, match="requires evidence"):
        audit.record_approval("research_authorization", "approved")
    with pytest.raises(ValueError):
        audit.respond("CARE-C1", "yes", reviewed_on="not-a-date")


def test_na_only_and_no_frameworks_never_ready():
    audit = SovereigntyAudit("na", frameworks=["fair"])
    for q in audit.questions:
        audit.respond(q.id, "na", notes="Documented scope exclusion")
    assert audit.overall_score is None
    assert "DOCUMENTED FOR NATION REVIEW" not in audit.readiness
    assert SovereigntyAudit("empty", frameworks=[]).overall_score is None


def test_missing_evidence_and_teaching_never_ready():
    audit = completed_audit()
    audit.teaching = True
    assert "TEACHING ONLY" in audit.readiness
    audit.respond("CARE-C1", "yes")
    assert audit.undocumented
    assert "Facilitated self-assessment" in audit.report()


def test_provenance_requires_classification_and_approval_evidence(context):
    with pytest.raises(ValueError, match="explicit classification"):
        ProvenanceBuilder("example").build()
    with pytest.raises(ValueError, match="explicit classification"):
        ProvenanceRecord("example", "dataset")
    for tier in ["GITIGNORED", "TYPO"]:
        with pytest.raises(ValueError):
            ProvenanceBuilder("example").for_nation(context).classify(tier).build()
    with pytest.raises(ValueError, match="evidence"):
        ProvenanceRecord(
            "example", "dataset", classification="PUBLIC", publication_status="approved"
        )
    with pytest.raises(ValueError, match="Unknown classification"):
        context.governance_report("Example", classification="TYPO")


def test_no_treaty_needed_for_valid_config(tmp_path):
    data = yaml.safe_load(
        (ROOT/"config/teaching_example.yaml").read_text(encoding="utf-8")
    )
    data["provenance"]["treaty_name"] = ""
    path = tmp_path/"nation.yaml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    assert load_context(ROOT, path).config.validate() == []


def test_fixture_excludes_partial_years_and_retains_divisions():
    frame, source = load_fixture(ROOT/"examples/data/synthetic_pdsi.csv")
    monthly, annual, coverage = prepare_annual(frame, [7, 8])
    assert source["synthetic"]
    assert len(annual) == 43
    assert set(coverage.loc[~coverage.included, "year"]) == {1992, 2024}
    assert {"division_7_pdsi", "division_8_pdsi"}.issubset(monthly.columns)
    missing = monthly.loc[monthly.date.eq("1992-04-01")].iloc[0]
    assert missing.division_count == 1
    assert pd.isna(missing.pdsi_avg)


def test_duplicate_and_missing_divisions_rejected():
    frame, _ = load_fixture(ROOT/"examples/data/synthetic_pdsi.csv")
    with pytest.raises(ValueError, match="Duplicate"):
        prepare_annual(pd.concat([frame, frame.iloc[:1]]), [7, 8])
    with pytest.raises(ValueError, match="No complete years"):
        prepare_annual(frame, [7, 99])


def test_noaa_parser_retains_missing_values_and_rejects_empty():
    text = "3907052000 " + " ".join(["-1"] * 11 + ["-99.99"])
    frame = parse_noaa(text, "39", [7])
    assert len(frame) == 12
    assert frame.pdsi.isna().sum() == 1
    with pytest.raises(ValueError, match="No matching"):
        parse_noaa(text, "39", [8])
    with pytest.raises(ValueError, match="Malformed"):
        parse_noaa("3907052000 -1", "39", [7])


def test_from_dict_preserves_configuration_fields():
    from toolkit.sovereignty import SovereigntyContext

    ctx = SovereigntyContext.from_dict(
        {
            "name": "Fictional",
            "teaching": True,
            "handling": {"approved_storage": "Synthetic classroom directory"},
            "analysis": {"divisions": [1, 2]},
        }
    )
    assert ctx.config.teaching
    assert ctx.config.analysis["divisions"] == [1, 2]
    assert not ctx.config.frameworks_enabled["ocap"]


def test_missing_evidence_blocks_documented_status():
    audit = completed_audit()
    for gate in audit.approvals:
        audit.record_approval(
            gate,
            "approved",
            evidence="private:1",
            reviewer="Reviewer",
            reviewed_on="2026-10-09",
        )
    audit.respond("CARE-C1", "yes")
    assert "REVIEW REQUIRED" in audit.readiness


def test_custom_tier_and_handling_propagate(context):
    context.config.classification_tiers = [{"id": "INTERNAL"}]
    record = (
        ProvenanceBuilder("custom").for_nation(context).classify("INTERNAL").build()
    )
    assert record.classification == "INTERNAL"
    assert record.approved_storage == context.config.handling["approved_storage"]
    assert record.publication_status == "pending"
    assert record.teaching


def test_noaa_latest_file_and_failed_fetch(monkeypatch):
    import requests

    from toolkit.drought import load_noaa

    urls = []

    class Response:
        def __init__(self, text):
            self.text = text
            self.content = text.encode()

        def raise_for_status(self):
            pass

    def get(url, timeout):
        urls.append(url)
        if url.endswith("/"):
            return Response(
                "climdiv-pdsidv-v1.0.0-20260101 climdiv-pdsidv-v1.0.0-20250101"
            )
        return Response("3907052000 " + " ".join(["-2"] * 12))

    monkeypatch.setattr(requests, "get", get)
    frame, source = load_noaa("39", [7])
    assert urls[-1].endswith("20260101")
    assert not source["synthetic"]
    assert len(source["sha256"]) == 64
    _, annual, _ = prepare_annual(frame, [7])
    assert annual.drought_months.iloc[0] == 12

    def fail(url, timeout):
        raise requests.ConnectionError("offline")

    monkeypatch.setattr(requests, "get", fail)
    with pytest.raises(requests.ConnectionError):
        load_noaa("39", [7])
