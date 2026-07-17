"""
toolkit/audit.py
Tribal Data Sovereignty Toolkit

Dataset sovereignty audit systematically evaluates a dataset or
analysis product against OCAP®, CARE, FAIR, and IEEE 2890-2025 criteria.

The audit produces a scored report that can be used to:
  - Identify governance gaps before publication
  - Guide data collection design
  - Demonstrate sovereignty compliance to funders and reviewers
  - Track improvement over time as governance matures

Audit structure
Each framework contributes a set of questions. Each question is answered
Yes / No / Partial / N/A. The audit produces:
  - A score per framework (0–100)
  - An overall sovereignty compliance score (0–100)
  - A prioritized list of gaps to address
  - A formatted report suitable for inclusion in a data package
 
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

ResponseType = Literal["yes", "no", "partial", "na"]
RESPONSE_SCORES = {"yes": 1.0, "no": 0.0, "partial": 0.5, "na": None}


@dataclass
class AuditQuestion:
    """A single audit question."""
    id:         str
    framework:  str
    principle:  str
    question:   str
    guidance:   str
    response:   ResponseType | None = None
    notes:      str = ""

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
    q(AuditQuestion(
        id="OCAP-O1", framework="OCAP®", principle="Ownership",
        question="Does the data collection agreement recognize the Tribal Nation's ownership of data about their lands and people?",
        guidance="Look for a data governance agreement, MOU, or data sharing agreement that explicitly names the Nation as data owner.",
    ))
    q(AuditQuestion(
        id="OCAP-O2", framework="OCAP®", principle="Ownership",
        question="Is there a clear statement that publication rights rest with the Tribal Nation, not the researcher?",
        guidance="The Nation should have the right to approve or decline publication of findings before they are shared externally.",
    ))
    q(AuditQuestion(
        id="OCAP-C1", framework="OCAP®", principle="Control",
        question="Did the Tribal Nation's governance structure approve this data collection or analysis?",
        guidance="Approval could come from Tribal Council, a Natural Resources Department, or a designated data governance body.",
    ))
    q(AuditQuestion(
        id="OCAP-C2", framework="OCAP®", principle="Control",
        question="Can the Tribal Nation stop, pause, or modify the research at any time?",
        guidance="Sovereignty requires that the Nation have the power to withdraw consent without penalty.",
    ))
    q(AuditQuestion(
        id="OCAP-A1", framework="OCAP®", principle="Access",
        question="Do Tribal members have meaningful access to the data and findings?",
        guidance="Data produced about a community should be returned to that community in a usable form, not only published in academic journals.",
    ))
    q(AuditQuestion(
        id="OCAP-A2", framework="OCAP®", principle="Access",
        question="Are findings communicated in formats accessible to non-researchers (plain language summaries, visualizations)?",
        guidance="Consider whether community members without technical backgrounds can understand and use the findings.",
    ))
    q(AuditQuestion(
        id="OCAP-P1", framework="OCAP®", principle="Possession",
        question="Does the Tribal Nation physically hold a copy of the data?",
        guidance="The Nation should not be dependent on the researcher or a federal agency to access data about their own territory.",
    ))
    q(AuditQuestion(
        id="OCAP-P2", framework="OCAP®", principle="Possession",
        question="Is Tribal-collected data stored on systems controlled by the Nation (not only on researcher's servers or cloud accounts)?",
        guidance="Physical possession means the data survives the end of a research relationship.",
    ))

    # CARE 
    q(AuditQuestion(
        id="CARE-C1", framework="CARE", principle="Collective Benefit",
        question="Is there a clear plan for how this data will benefit the Tribal community?",
        guidance="Articulate specific community benefits beyond the research value to the analyst or institution.",
    ))
    q(AuditQuestion(
        id="CARE-C2", framework="CARE", principle="Collective Benefit",
        question="Were community members involved in defining what counts as benefit?",
        guidance="Benefit as defined by the researcher may not match community priorities.",
    ))
    q(AuditQuestion(
        id="CARE-A1", framework="CARE", principle="Authority to Control",
        question="Does the Tribal Nation have authority to determine how this data is classified and shared?",
        guidance="The Nation should control which data is public, which is community-only, and which is restricted.",
    ))
    q(AuditQuestion(
        id="CARE-A2", framework="CARE", principle="Authority to Control",
        question="Are there mechanisms for the Nation to update or revoke data sharing permissions over time?",
        guidance="Governance is not one-time consent, it is an ongoing relationship.",
    ))
    q(AuditQuestion(
        id="CARE-R1", framework="CARE", principle="Responsibility",
        question="Is the analyst accountable to the Tribal Nation for how data is used?",
        guidance="Accountability means the Nation has recourse if the data is misused.",
    ))
    q(AuditQuestion(
        id="CARE-R2", framework="CARE", principle="Responsibility",
        question="Are data sharing agreements in place that specify permissible and impermissible uses?",
        guidance="Without explicit agreements, data can be reused in ways the Nation never intended.",
    ))
    q(AuditQuestion(
        id="CARE-E1", framework="CARE", principle="Ethics",
        question="Has the analysis considered potential harms to the community, to sacred places, to cultural knowledge?",
        guidance="Maps and data products can reveal sensitive information. Consider what should not be made public.",
    ))
    q(AuditQuestion(
        id="CARE-E2", framework="CARE", principle="Ethics",
        question="Are the ethical obligations of this research documented and will they be fulfilled after the project ends?",
        guidance="Ethics includes long-term relationship and responsibility.",
    ))

    # FAIR
    q(AuditQuestion(
        id="FAIR-F1", framework="FAIR", principle="Findable",
        question="Is the dataset assigned a persistent, unique identifier (DOI, accession number)?",
        guidance="A DOI from Zenodo or a data repository ensures the dataset can be cited and found.",
    ))
    q(AuditQuestion(
        id="FAIR-F2", framework="FAIR", principle="Findable",
        question="Is the dataset described with sufficient metadata for discovery?",
        guidance="Metadata should include: title, creator, date, coverage, keywords, and governance information.",
    ))
    q(AuditQuestion(
        id="FAIR-A1", framework="FAIR", principle="Accessible",
        question="Is the data accessible through a standardized protocol (HTTP, HTTPS, API)?",
        guidance="For data intended to be shared — not all data should be publicly accessible (see CARE).",
    ))
    q(AuditQuestion(
        id="FAIR-I1", framework="FAIR", principle="Interoperable",
        question="Does the data use standard formats and controlled vocabularies?",
        guidance="GeoJSON, netCDF, CSV with standard field names enable interoperability across tools.",
    ))
    q(AuditQuestion(
        id="FAIR-R1", framework="FAIR", principle="Reusable",
        question="Is the data released with a clear license that specifies permitted uses?",
        guidance="For Tribal data, the license should reflect OCAP® and CARE constraints, not just standard open licenses.",
    ))
    q(AuditQuestion(
        id="FAIR-R2", framework="FAIR", principle="Reusable",
        question="Is provenance documented sufficiently that the data could be reproduced or validated?",
        guidance="Provenance includes: who collected it, how, when, with what instruments or models.",
    ))

    # IEEE 2890-2025
    q(AuditQuestion(
        id="IEEE-1", framework="IEEE 2890-2025", principle="Provenance",
        question="Is the Tribal Nation's territorial and treaty provenance documented on every data product?",
        guidance="Every dataset, figure, and report should carry a statement identifying whose land it describes and under what treaty.",
    ))
    q(AuditQuestion(
        id="IEEE-2", framework="IEEE 2890-2025", principle="Provenance",
        question="Is the data steward (Tribal Nation department) identified in the provenance record?",
        guidance="The steward is the organization responsible for governing the data",
    ))
    q(AuditQuestion(
        id="IEEE-3", framework="IEEE 2890-2025", principle="Provenance",
        question="Are processing steps documented such that the data lineage is traceable?",
        guidance="From raw source to final product, every transformation should be documented.",
    ))
    q(AuditQuestion(
        id="IEEE-4", framework="IEEE 2890-2025", principle="Provenance",
        question="Are derived datasets linked back to their source provenance records?",
        guidance="If you create a new dataset by processing existing data, the new dataset inherits the governance obligations of the source.",
    ))
    q(AuditQuestion(
        id="IEEE-5", framework="IEEE 2890-2025", principle="Provenance",
        question="Is the data classification (public, community, restricted, gitignored) documented on every record?",
        guidance="Classification determines who may access and use the data.",
    ))

    return questions


# Audit

class SovereigntyAudit:
    """
    A sovereignty audit for a dataset or analysis product.

    Usage
    audit = SovereigntyAudit("Streamflow Analysis for Pine Ridge 2024")
    audit.respond("OCAP-O1", "yes")
    audit.respond("OCAP-O2", "partial", notes="MOU covers data sharing but not publication rights")
    audit.respond("CARE-C1", "no", notes="No formal benefit plan documented")
    # ... respond to all questions
    report = audit.report()
    audit.save("outputs/sovereignty_audit.txt")
    """

    def __init__(self, dataset_name: str):
        self.dataset_name = dataset_name
        self.questions    = _build_question_library()
        self._responses: dict[str, tuple[ResponseType, str]] = {}

    def respond(
        self,
        question_id: str,
        response: ResponseType,
        notes: str = "",
    ) -> None:
        """Record a response to a specific audit question."""
        q = next((q for q in self.questions if q.id == question_id), None)
        if q is None:
            raise ValueError(f"Unknown question ID: {question_id}. "
                             f"Valid IDs: {[q.id for q in self.questions]}")
        q.response = response
        q.notes    = notes

    def respond_all(self, responses: dict[str, tuple[ResponseType, str]]) -> None:
        """Respond to multiple questions at once."""
        for qid, (resp, notes) in responses.items():
            self.respond(qid, resp, notes)

    def interactive_audit(self, framework: str | None = None) -> None:
        """
        Walk through audit questions interactively, prompting for responses.
        Optionally filter to a specific framework.
        """
        questions = [q for q in self.questions
                     if framework is None or q.framework == framework]
        print(f"SOVEREIGNTY AUDIT {self.dataset_name}")
        if framework:
            print(f"Framework: {framework}")
        print(f"Questions: {len(questions)}")
        print("Responses: yes / no / partial / na")
        print()

        for q in questions:
            print(f"[{q.id}] {q.framework} {q.principle}")
            print(f"  {q.question}")
            print(f"  Guidance: {q.guidance[:80]}...")
            while True:
                resp = input("  Response [yes/no/partial/na]: ").strip().lower()
                if resp in ("yes", "no", "partial", "na"):
                    notes = input("  Notes (optional): ").strip()
                    self.respond(q.id, resp, notes)
                    break
                print("  Please enter: yes, no, partial, or na")
            print()

    # Scoring

    def _framework_score(self, framework: str) -> float | None:
        """Score for a specific framework (0–100). None if no responses."""
        qs = [q for q in self.questions
              if q.framework == framework and q.response is not None]
        applicable = [q for q in qs if q.response != "na"]
        if not applicable:
            return None
        return sum(q.score for q in applicable) / len(applicable) * 100

    @property
    def overall_score(self) -> float | None:
        """Overall compliance score (0–100)."""
        framework_scores = [
            self._framework_score(fw)
            for fw in self.frameworks
            if self._framework_score(fw) is not None
        ]
        if not framework_scores:
            return None
        return sum(framework_scores) / len(framework_scores)

    @property
    def frameworks(self) -> list[str]:
        return list(dict.fromkeys(q.framework for q in self.questions))

    @property
    def gaps(self) -> list[AuditQuestion]:
        """Questions answered 'no' or 'partial' have priority gaps to address."""
        return sorted(
            [q for q in self.questions
             if q.response in ("no", "partial")],
            key=lambda q: (q.response == "partial", q.framework)
        )

    @property
    def unanswered(self) -> list[AuditQuestion]:
        return [q for q in self.questions if q.response is None]

    # Reporting

    def report(self) -> str:
        """Generate a formatted audit report."""
        import datetime
        lines = [
            f"SOVEREIGNTY AUDIT REPORT",
            f"Dataset    : {self.dataset_name}",
            f"Date       : {datetime.date.today().isoformat()}",
            f"Questions  : {len(self.questions)}",
            f"Answered   : {len(self.questions) - len(self.unanswered)}",
            f"",
        ]

        # Score summary
        overall = self.overall_score
        if overall is not None:
            status = ("STRONG" if overall >= 80 else
                      "ADEQUATE" if overall >= 60 else
                      "NEEDS WORK" if overall >= 40 else "CRITICAL GAPS")
            lines += [
                f"OVERALL COMPLIANCE SCORE: {overall:.0f}/100  [{status}]",
                "",
                "BY FRAMEWORK",                
            ]
            for fw in self.frameworks:
                score = self._framework_score(fw)
                if score is not None:
                    bar = "█" * int(score/5) + "░" * (20 - int(score/5))
                    lines.append(f"  {fw:<20}: {score:>5.0f}/100  {bar}")
            lines.append("")
        else:
            lines += ["No responses recorded yet.", ""]

        # Gaps
        if self.gaps:
            lines += ["PRIORITY GAPS", ]
            for q in self.gaps:
                status = "NO" if q.response == "no" else "PARTIAL"
                lines.append(f"  [{status}] {q.id} {q.principle}")
                lines.append(f"         {q.question[:70]}...")
                if q.notes:
                    lines.append(f"         Note: {q.notes}")
            lines.append("")

        # Full detail
        lines += ["FULL AUDIT DETAIL", ]
        current_fw = None
        for q in self.questions:
            if q.framework != current_fw:
                current_fw = q.framework
                lines += [f"", f"  {q.framework}"]
            resp = q.response.upper() if q.response else "NOT ANSWERED"
            lines.append(f"  [{q.id}] {resp:<10} {q.question[:60]}...")
            if q.notes:
                lines.append(f"  {'':>8} Note: {q.notes}")

        lines += [
            "",
            "Generated by the Tribal Data Sovereignty Toolkit",
            "Standard: OCAP® | CARE | FAIR | IEEE 2890-2025",
        ]
        return "\n".join(lines)

    def save(self, path: str | Path) -> None:
        from pathlib import Path   # add this line
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.report(), encoding="utf-8")
        print(f"Audit report saved: {path}")

    def questions_list(self) -> str:
        """Return all question IDs and text for reference."""
        lines = ["AUDIT QUESTIONS Full List",]
        for fw in self.frameworks:
            lines.append(f"\n{fw}")
            for q in [q for q in self.questions if q.framework == fw]:
                lines.append(f"  [{q.id}] ({q.principle})")
                lines.append(f"    {q.question}")
        return "\n".join(lines)
