import pytest

from toolkit.audit import SovereigntyAudit
from toolkit.provenance import ProvenanceBuilder
from toolkit.sovereignty import SovereigntyContext


@pytest.fixture
def context():
    return SovereigntyContext.from_config("config/nation_template.yaml")


def test_template_configuration_is_valid(context):
    assert context.config.validate() == []


def test_provenance_requires_explicit_classification():
    builder = ProvenanceBuilder("example").for_dataset("Example dataset")
    with pytest.raises(ValueError, match="explicit classification"):
        builder.build()


def test_context_requires_explicit_classification(context):
    with pytest.raises(ValueError, match="explicit classification"):
        context.governance_report("Example dataset")


def test_audit_report_is_not_a_certification():
    audit = SovereigntyAudit("Example dataset", reviewer="Data steward")
    audit.respond("OCAP-O1", "yes", notes="Agreement reviewed")
    report = audit.report()
    assert "Facilitated self-assessment" in report
    assert "Data steward" in report
