"""
toolkit/audit.py
Tribal Data Sovereignty Toolkit

Dataset sovereignty audit systematically evaluates a dataset or
analysis product against OCAP®, CARE, FAIR, and IEEE 2890-2025 criteria.

The audit produces a scored report that can be used to:
  - Identify governance gaps before publication
  - Guide data collection design
  - Document evidence and unresolved decisions for reviewers
  - Track improvement over time as governance matures

Audit structure
Each framework contributes a set of questions. Each question is answered
Yes / No / Partial / N/A. The audit produces:
  - A score per framework (0–100)
  - An indicative self-assessment score (0–100)
  - A prioritized list of gaps to address
  - A formatted report suitable for inclusion in a data package

"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Literal

ResponseType = Literal["yes", "no", "partial", "na"]
RESPONSE_SCORES = {"yes": 1.0, "no": 0.0, "partial": 0.5, "na": None}


@dataclass
class AuditQuestion:
    """A single audit question."""

    id: str
    framework: str
    principle: str
    question: str
    guidance: str
    response: ResponseType | None = None
    notes: str = ""
    evidence: str = ""
    reviewer: str = ""
    reviewed_on: str = ""

    @property
    def score(self) -> float | None:
        """Numeric score for this question. None = not applicable."""
        if self.response is None:
            return None
        return RESPONSE_SCORES.get(self.response)


# Question library


def _build_question_library() -> list[AuditQuestion]:
    """Return the full set of audit questions."""
    questions = []
    q = questions.append

    # OCAP®
    q(
        AuditQuestion(
            id="OCAP-O1",
            framework="OCAP®",
            principle="Ownership",
            question=(
                "Does the data collection agreement recognize the Tribal "
                "Nation's ownership of data about their lands and people?"
            ),
            guidance=(
                "Look for a data governance agreement, MOU, or data sharing "
                "agreement that explicitly names the Nation as data owner."
            ),
        )
    )
    q(
        AuditQuestion(
            id="OCAP-O2",
            framework="OCAP®",
            principle="Ownership",
            question=(
                "Is there a clear statement that publication rights rest "
                "with the Tribal Nation, not the researcher?"
            ),
            guidance=(
                "The Nation should have the right to approve or decline "
                "publication of findings before they are shared externally."
            ),
        )
    )
    q(
        AuditQuestion(
            id="OCAP-C1",
            framework="OCAP®",
            principle="Control",
            question=(
                "Did the Tribal Nation's governance structure approve this "
                "data collection or analysis?"
            ),
            guidance=(
                "Approval could come from Tribal Council, a Natural "
                "Resources Department, or a designated data governance "
                "body."
            ),
        )
    )
    q(
        AuditQuestion(
            id="OCAP-C2",
            framework="OCAP®",
            principle="Control",
            question=(
                "Can the Tribal Nation stop, pause, or modify the research at any time?"
            ),
            guidance=(
                "Sovereignty requires that the Nation have the power to "
                "withdraw consent without penalty."
            ),
        )
    )
    q(
        AuditQuestion(
            id="OCAP-A1",
            framework="OCAP®",
            principle="Access",
            question=(
                "Do Tribal members have meaningful access to the data and findings?"
            ),
            guidance=(
                "Data produced about a community should be returned to that "
                "community in a usable form, not only published in academic "
                "journals."
            ),
        )
    )
    q(
        AuditQuestion(
            id="OCAP-A2",
            framework="OCAP®",
            principle="Access",
            question=(
                "Are findings communicated in formats accessible to "
                "non-researchers (plain language summaries, "
                "visualizations)?"
            ),
            guidance=(
                "Consider whether community members without technical "
                "backgrounds can understand and use the findings."
            ),
        )
    )
    q(
        AuditQuestion(
            id="OCAP-P1",
            framework="OCAP®",
            principle="Possession",
            question="Does the Tribal Nation physically hold a copy of the data?",
            guidance=(
                "The Nation should not be dependent on the researcher or a "
                "federal agency to access data about their own territory."
            ),
        )
    )
    q(
        AuditQuestion(
            id="OCAP-P2",
            framework="OCAP®",
            principle="Possession",
            question=(
                "Is Tribal-collected data stored on systems controlled by "
                "the Nation (not only on researcher's servers or cloud "
                "accounts)?"
            ),
            guidance=(
                "Physical possession means the data survives the end of a "
                "research relationship."
            ),
        )
    )

    # CARE
    q(
        AuditQuestion(
            id="CARE-C1",
            framework="CARE",
            principle="Collective Benefit",
            question=(
                "Is there a clear plan for how this data will benefit the "
                "Tribal community?"
            ),
            guidance=(
                "Articulate specific community benefits beyond the research "
                "value to the analyst or institution."
            ),
        )
    )
    q(
        AuditQuestion(
            id="CARE-C2",
            framework="CARE",
            principle="Collective Benefit",
            question=(
                "Were community members involved in defining what counts as benefit?"
            ),
            guidance=(
                "Benefit as defined by the researcher may not match "
                "community priorities."
            ),
        )
    )
    q(
        AuditQuestion(
            id="CARE-A1",
            framework="CARE",
            principle="Authority to Control",
            question=(
                "Does the Tribal Nation have authority to determine how "
                "this data is classified and shared?"
            ),
            guidance=(
                "The Nation should control which data is public, which is "
                "community-only, and which is restricted."
            ),
        )
    )
    q(
        AuditQuestion(
            id="CARE-A2",
            framework="CARE",
            principle="Authority to Control",
            question=(
                "Are there mechanisms for the Nation to update or revoke "
                "data sharing permissions over time?"
            ),
            guidance=(
                "Governance is not one-time consent, it is an ongoing relationship."
            ),
        )
    )
    q(
        AuditQuestion(
            id="CARE-R1",
            framework="CARE",
            principle="Responsibility",
            question=(
                "Is the analyst accountable to the Tribal Nation for how data is used?"
            ),
            guidance=(
                "Accountability means the Nation has recourse if the data is misused."
            ),
        )
    )
    q(
        AuditQuestion(
            id="CARE-R2",
            framework="CARE",
            principle="Responsibility",
            question=(
                "Are data sharing agreements in place that specify "
                "permissible and impermissible uses?"
            ),
            guidance=(
                "Without explicit agreements, data can be reused in ways "
                "the Nation never intended."
            ),
        )
    )
    q(
        AuditQuestion(
            id="CARE-E1",
            framework="CARE",
            principle="Ethics",
            question=(
                "Has the analysis considered potential harms to the "
                "community, to sacred places, to cultural knowledge?"
            ),
            guidance=(
                "Maps and data products can reveal sensitive information. "
                "Consider what should not be made public."
            ),
        )
    )
    q(
        AuditQuestion(
            id="CARE-E2",
            framework="CARE",
            principle="Ethics",
            question=(
                "Are the ethical obligations of this research documented "
                "and will they be fulfilled after the project ends?"
            ),
            guidance="Ethics includes long-term relationship and responsibility.",
        )
    )

    # FAIR
    q(
        AuditQuestion(
            id="FAIR-F1",
            framework="FAIR",
            principle="Findable",
            question=(
                "Is the dataset assigned a persistent, unique identifier "
                "(DOI, accession number)?"
            ),
            guidance=(
                "A DOI from Zenodo or a data repository ensures the dataset "
                "can be cited and found."
            ),
        )
    )
    q(
        AuditQuestion(
            id="FAIR-F2",
            framework="FAIR",
            principle="Findable",
            question="Is the dataset described with sufficient metadata for discovery?",
            guidance=(
                "Metadata should include: title, creator, date, coverage, "
                "keywords, and governance information."
            ),
        )
    )
    q(
        AuditQuestion(
            id="FAIR-A1",
            framework="FAIR",
            principle="Accessible",
            question=(
                "Is the data accessible through a standardized protocol "
                "(HTTP, HTTPS, API)?"
            ),
            guidance=(
                "Restricted data can be FAIR: use authentication and "
                "authorization where needed."
            ),
        )
    )
    q(
        AuditQuestion(
            id="FAIR-I1",
            framework="FAIR",
            principle="Interoperable",
            question="Does the data use standard formats and controlled vocabularies?",
            guidance=(
                "GeoJSON, netCDF, CSV with standard field names enable "
                "interoperability across tools."
            ),
        )
    )
    q(
        AuditQuestion(
            id="FAIR-R1",
            framework="FAIR",
            principle="Reusable",
            question=(
                "Is the data released with a clear license that specifies "
                "permitted uses?"
            ),
            guidance=(
                "For Tribal data, use terms should reflect Nation-selected "
                "constraints, not just standard open licenses."
            ),
        )
    )
    q(
        AuditQuestion(
            id="FAIR-R2",
            framework="FAIR",
            principle="Reusable",
            question=(
                "Is provenance documented sufficiently that the data could "
                "be reproduced or validated?"
            ),
            guidance=(
                "Provenance includes: who collected it, how, when, with "
                "what instruments or models."
            ),
        )
    )

    # IEEE 2890-2025
    q(
        AuditQuestion(
            id="IEEE-1",
            framework="IEEE 2890-2025",
            principle="Provenance",
            question=(
                "Is the Tribal Nation's territorial and applicable "
                "governance authority provenance documented on every data "
                "product?"
            ),
            guidance=(
                "Every dataset, figure, and report should carry a statement "
                "identifying whose land it describes and the applicable "
                "authority, including a treaty where relevant."
            ),
        )
    )
    q(
        AuditQuestion(
            id="IEEE-2",
            framework="IEEE 2890-2025",
            principle="Provenance",
            question=(
                "Is the data steward (Tribal Nation department) identified "
                "in the provenance record?"
            ),
            guidance=(
                "The steward is the organization responsible for governing the data"
            ),
        )
    )
    q(
        AuditQuestion(
            id="IEEE-3",
            framework="IEEE 2890-2025",
            principle="Provenance",
            question=(
                "Are processing steps documented such that the data lineage "
                "is traceable?"
            ),
            guidance=(
                "From raw source to final product, every transformation "
                "should be documented."
            ),
        )
    )
    q(
        AuditQuestion(
            id="IEEE-4",
            framework="IEEE 2890-2025",
            principle="Provenance",
            question=(
                "Are derived datasets linked back to their source provenance records?"
            ),
            guidance=(
                "If you create a new dataset by processing existing data, "
                "the new dataset inherits the governance obligations of the "
                "source."
            ),
        )
    )
    q(
        AuditQuestion(
            id="IEEE-5",
            framework="IEEE 2890-2025",
            principle="Provenance",
            question=(
                "Is the data classification (using the Nation-selected "
                "access tiers) documented on every record?"
            ),
            guidance="Classification determines who may access and use the data.",
        )
    )

    return questions


FRAMEWORK_LABELS = {
    "ocap": "OCAP®",
    "care": "CARE",
    "fair": "FAIR",
    "ieee_2890": "IEEE 2890-2025",
}
REQUIRED_GATES = ("research_authorization", "sharing_authorization")


@dataclass
class Approval:
    status: str = "pending"
    evidence: str = ""
    reviewer: str = ""
    reviewed_on: str = ""

    @property
    def documented(self):
        return self.status == "approved" and all(
            (self.evidence, self.reviewer, self.reviewed_on)
        )


class SovereigntyAudit:
    """Evidence-backed self-assessment. Scores never authorize release.

    Pass frameworks=ctx.config.active_frameworks for Nation-selected questions.
    Required research and sharing approvals remain separate from framework scores.
    """

    def __init__(
        self,
        dataset_name,
        reviewer="",
        evidence_location="",
        frameworks=None,
        teaching=False,
    ):
        self.dataset_name = dataset_name
        self.reviewer = reviewer
        self.evidence_location = evidence_location
        self.teaching = teaching
        selected = list(FRAMEWORK_LABELS) if frameworks is None else list(frameworks)
        allowed = (
            set(FRAMEWORK_LABELS) | set(FRAMEWORK_LABELS.values()) | {"local_contexts"}
        )
        if set(selected) - allowed:
            raise ValueError(f"Unsupported frameworks: {set(selected) - allowed}")
        labels = {FRAMEWORK_LABELS.get(f, f) for f in selected}
        self.manual_frameworks = [f for f in selected if f == "local_contexts"]
        self.questions = [q for q in _build_question_library() if q.framework in labels]
        self.approvals = {name: Approval() for name in REQUIRED_GATES}

    def respond(
        self,
        question_id,
        response,
        notes="",
        *,
        evidence="",
        reviewer="",
        reviewed_on="",
    ):
        if response not in RESPONSE_SCORES:
            raise ValueError("Response must be yes, no, partial, or na")
        if response == "na" and not notes.strip():
            raise ValueError("An na response requires a rationale in notes")
        if reviewed_on:
            date.fromisoformat(reviewed_on)
        question = next((q for q in self.questions if q.id == question_id), None)
        if question is None:
            raise ValueError(f"Unknown or inactive question ID: {question_id}")
        question.response, question.notes = response, notes
        question.evidence = evidence.strip()
        question.reviewer = reviewer.strip() or self.reviewer
        question.reviewed_on = reviewed_on

    def respond_all(self, responses):
        for qid, (response, notes) in responses.items():
            self.respond(qid, response, notes)

    def record_approval(
        self, gate, status, *, evidence="", reviewer="", reviewed_on=""
    ):
        if gate not in self.approvals:
            raise ValueError(f"Unknown approval gate: {gate}")
        if status not in {"pending", "approved", "denied", "revoked"}:
            raise ValueError("Invalid approval status")
        if status == "approved" and not all(
            x.strip() for x in (evidence, reviewer, reviewed_on)
        ):
            raise ValueError("Approval requires evidence, reviewer, and date")
        if reviewed_on:
            date.fromisoformat(reviewed_on)
        self.approvals[gate] = Approval(status, evidence, reviewer, reviewed_on)

    @property
    def unanswered(self):
        return [q for q in self.questions if q.response is None]

    @property
    def completion(self):
        return (
            (len(self.questions) - len(self.unanswered)) / len(self.questions)
            if self.questions
            else 0.0
        )

    @property
    def undocumented(self):
        return [
            q
            for q in self.questions
            if q.response is not None
            and not all((q.evidence, q.reviewer, q.reviewed_on))
        ]

    @property
    def frameworks(self):
        return list(dict.fromkeys(q.framework for q in self.questions))

    def _framework_score(self, framework):
        questions = [q for q in self.questions if q.framework == framework]
        if not questions or any(q.response is None for q in questions):
            return None
        applicable = [q for q in questions if q.response != "na"]
        return (
            sum(q.score for q in applicable) / len(applicable) * 100
            if applicable
            else None
        )

    @property
    def overall_score(self):
        if self.unanswered or not self.questions:
            return None
        scores = [self._framework_score(f) for f in self.frameworks]
        scores = [score for score in scores if score is not None]
        return sum(scores) / len(scores) if scores else None

    @property
    def gaps(self):
        return sorted(
            [q for q in self.questions if q.response in ("no", "partial")],
            key=lambda q: (q.response == "partial", q.framework),
        )

    @property
    def readiness(self):
        if self.teaching:
            return "TEACHING ONLY: no actual authorization established"
        if self.unanswered or not self.questions:
            return "INCOMPLETE: readiness withheld"
        if any(not approval.documented for approval in self.approvals.values()):
            return "BLOCKED: required authorization missing, denied, or revoked"
        if self.overall_score is None:
            return "REVIEW REQUIRED: no applicable questions assessed"
        if self.undocumented or self.gaps or self.manual_frameworks:
            return (
                "REVIEW REQUIRED: evidence, gaps, or manual framework "
                "review outstanding"
            )
        return "DOCUMENTED FOR NATION REVIEW: this tool does not authorize release"

    def report(self):
        answered = len(self.questions) - len(self.unanswered)
        lines = [
            "SOVEREIGNTY SELF-ASSESSMENT",
            f"Dataset: {self.dataset_name}",
            f"Reviewer: {self.reviewer or 'Not recorded'}",
            f"Evidence index: {self.evidence_location or 'Not recorded'}",
            "Facilitated self-assessment; not legal, ethical, or "
            "governance certification.",
            f"Completion: {answered}/{len(self.questions)} ({self.completion:.0%})",
            f"Status: {self.readiness}",
        ]
        score = self.overall_score
        lines.append(
            "Indicative score: withheld (incomplete or no applicable responses)"
            if score is None
            else f"Indicative score: {score:.1f}/100; not release permission"
        )
        for framework in self.frameworks:
            value = self._framework_score(framework)
            lines.append(f"{framework}: {value if value is not None else 'withheld'}")
        lines.append("REQUIRED AUTHORIZATIONS")
        for name, approval in self.approvals.items():
            lines.extend(
                [
                    f"{name}: {approval.status}",
                    f"Evidence: {approval.evidence or 'missing'}",
                    f"Reviewer: {approval.reviewer or 'missing'}",
                    f"Date: {approval.reviewed_on or 'missing'}",
                ]
            )
        if self.manual_frameworks:
            lines.append("Manual review required: " + ", ".join(self.manual_frameworks))
        lines.append("FULL QUESTION AND EVIDENCE DETAIL")
        for q in self.questions:
            lines.extend(
                [
                    f"{q.id} [{q.response or 'unanswered'}] {q.question}",
                    f"Notes: {q.notes}",
                    f"Evidence: {q.evidence or 'missing'}",
                    f"Reviewer: {q.reviewer or 'missing'}",
                    f"Date: {q.reviewed_on or 'missing'}",
                ]
            )
        return "\n".join(lines)

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.report(), encoding="utf-8")

    def questions_list(self):
        return "\n".join(f"{q.id} [{q.framework}] {q.question}" for q in self.questions)

    def interactive_audit(self, framework=None):
        for q in self.questions:
            if framework is not None and q.framework != framework:
                continue
            print(q.id, q.question, q.guidance, sep="\n")
            while True:
                try:
                    self.respond(
                        q.id,
                        input("yes/no/partial/na: ").strip().lower(),
                        notes=input("Notes / na rationale: "),
                        evidence=input("Evidence reference: "),
                        reviewer=input("Reviewer: "),
                        reviewed_on=input("Review date YYYY-MM-DD (or blank): "),
                    )
                    break
                except ValueError as error:
                    print(error)
