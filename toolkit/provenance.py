"""Toolkit-defined provenance records.

These fields support documenting governance and technical lineage. They are
not a certified IEEE or W3C serialization. See docs/frameworks_reference.md.
"""

from __future__ import annotations

import datetime
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

# Provenance record


@dataclass
class ProvenanceRecord:
    """
    A single toolkit-defined provenance record.

    This record captures both technical provenance (the standard W3C PROV
    elements: entity, agent, activity) and Indigenous data governance
    provenance (territorial, treaty, stewardship).

    Fields
    record_id        : Unique identifier for this provenance record
    dataset_name     : Human-readable name of the dataset
    created_date     : ISO 8601 date the record was created
    nation_name      : Indigenous Nation whose territory/people the data describes
    territory_name   : Territory name
    treaty_reference : Governing treaty
    data_source_name : Name of the organization or system that produced the data
    data_source_url  : URL to the data source
    data_steward     : Organization responsible for governing the data
    license          : Data license
    classification   : Data classification tier
    frameworks       : Governance frameworks applied
    collection_method: How the datwas collected (survey, remote sensing, etc.)
    collection_date  : When the data was collected (approximate)
    analyst_name     : Name of the person creating this provenance record
    analyst_org      : Organization of the analyst
    processing_steps : List of processing steps applied to the data
    notes            : Any additional governance or provenance notes
    """

    record_id: str
    dataset_name: str
    created_date: str = field(default_factory=lambda: datetime.date.today().isoformat())

    # Indigenous data governance provenance (IEEE 2890-2025 core)
    nation_name: str = ""
    territory_name: str = ""
    treaty_reference: str = ""
    treaty_status: str = ""
    legal_citation: str = ""

    # Technical lineage (toolkit fields, not a W3C serialization)
    data_source_name: str = ""
    data_source_url: str = ""
    data_steward: str = ""
    license: str = ""
    collection_method: str = ""
    collection_date: str = ""

    # Governance
    classification: str = "UNCLASSIFIED"
    approved_storage: str = "UNSPECIFIED"
    version_control: str = "prohibited unless explicitly authorized"
    publication_status: str = "pending"
    approval_evidence: str = ""
    approval_reviewer: str = ""
    approval_date: str = ""
    teaching: bool = False
    frameworks: str = ""
    stewardship_dept: str = ""

    # Analyst
    analyst_name: str = ""
    analyst_org: str = ""
    analysis_purpose: str = ""

    # Lineage
    processing_steps: list[str] = field(default_factory=list)
    derived_from: list[str] = field(default_factory=list)
    notes: str = ""

    def __post_init__(self):
        if not self.classification or self.classification in {
            "UNCLASSIFIED",
            "GITIGNORED",
        }:
            raise ValueError("An explicit classification access tier is required")
        if self.publication_status not in {"pending", "approved", "denied", "revoked"}:
            raise ValueError("Invalid publication status")
        if self.teaching and self.publication_status == "approved":
            raise ValueError("Teaching records cannot assert real publication approval")
        if self.publication_status == "approved":
            if not all(
                (self.approval_evidence, self.approval_reviewer, self.approval_date)
            ):
                raise ValueError(
                    "Publication approval requires evidence, reviewer, and date"
                )
            datetime.date.fromisoformat(self.approval_date)

    def to_dict(self) -> dict:
        self.__post_init__()
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def to_markdown(self) -> str:
        """Return a formatted markdown provenance statement."""
        self.__post_init__()
        lines = [
            f"## Data Provenance {self.dataset_name}",
            "",
            f"**Record ID:** `{self.record_id}`  ",
            f"**Created:** {self.created_date}  ",
            "",
            "### Territorial Provenance",
            "",
            "| Field | Value |",
            "|---|---|",
            f"| Nation | {self.nation_name} |",
            f"| Territory | {self.territory_name} |",
            f"| Treaty | {self.treaty_reference} |",
        ]
        if self.treaty_status:
            lines += ["", f"**Status:** {self.treaty_status}", ""]
        if self.legal_citation:
            lines += [f"**Legal citation:** {self.legal_citation}", ""]

        lines += [
            "### Data Source",
            "",
            "| Field | Value |",
            "|---|---|",
            f"| Source | {self.data_source_name} |",
            f"| URL | {self.data_source_url} |",
            f"| Steward | {self.data_steward} |",
            f"| License | {self.license} |",
            f"| Classification | {self.classification} |",
            f"| Approved storage | {self.approved_storage} |",
            f"| Version control | {self.version_control} |",
            f"| Publication status | {self.publication_status} |",
            f"| Approval evidence | {self.approval_evidence or 'Not recorded'} |",
            f"| Approval reviewer | {self.approval_reviewer or 'Not recorded'} |",
            f"| Approval date | {self.approval_date or 'Not recorded'} |",
            f"| Teaching scenario | {self.teaching} |",
            f"| Frameworks | {self.frameworks} |",
            "",
        ]

        if self.processing_steps:
            lines += ["### Processing Steps", ""]
            for i, step in enumerate(self.processing_steps, 1):
                lines.append(f"{i}. {step}")
            lines.append("")

        if self.notes:
            lines += ["### Notes", "", f"{self.notes}", ""]

        lines += [
            "---",
            "*Generated by the Tribal Data Sovereignty Toolkit "
            "Toolkit schema; IEEE conformance not established*",
        ]
        return "\n".join(lines)

    def save(self, path: str | Path, format: str = "json") -> None:
        """Save the provenance record to a file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if format == "json":
            path.write_text(self.to_json(), encoding="utf-8")
        elif format == "markdown":
            path.write_text(self.to_markdown(), encoding="utf-8")
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'json' or 'markdown'.")


# Provenance builder


class ProvenanceBuilder:
    """
    Fluent builder for ProvenanceRecord objects.
    Integrates with SovereigntyContext to auto-populate Nation fields.

    Example
    record = (
        ProvenanceBuilder("streamflow-pine-ridge-2024")
        .for_nation(ctx)
        .from_source("usgs_nwis_streamflow")
        .collected_by("USGS", method="continuous gauging")
        .processed_by("Daear Consulting", purpose="drought analysis")
        .step("Loaded from USGS NWIS RDB format")
        .step("Computed 7-day minimum flow per year")
        .classify("PUBLIC")
        .build()
    )
    """

    def __init__(self, record_id: str):
        self._data: dict[str, Any] = {"record_id": record_id}

    def for_nation(self, ctx) -> "ProvenanceBuilder":
        """Populate Nation fields from a SovereigntyContext."""
        cfg = ctx.config
        self._data.update(
            {
                "teaching": cfg.teaching,
                "approved_storage": cfg.handling.get("approved_storage", "UNSPECIFIED"),
                "version_control": cfg.handling.get(
                    "version_control", "prohibited unless explicitly authorized"
                ),
                "nation_name": cfg.name,
                "territory_name": cfg.territory,
                "treaty_reference": cfg.treaty_name,
                "treaty_status": cfg.treaty_status,
                "legal_citation": (
                    cfg.legal_citations[0] if cfg.legal_citations else ""
                ),
                "stewardship_dept": cfg.department,
                "frameworks": " | ".join(
                    k.upper() for k, v in cfg.frameworks_enabled.items() if v
                ),
            }
        )
        self._ctx = ctx
        return self

    def for_dataset(self, name: str) -> "ProvenanceBuilder":
        self._data["dataset_name"] = name
        return self

    def from_source(self, source_key: str) -> "ProvenanceBuilder":
        """Auto-populate source fields from the SovereigntyContext registry."""
        if hasattr(self, "_ctx"):
            src = self._ctx._sources.get(source_key, {})
            self._data.update(
                {
                    "data_source_name": src.get("name", source_key),
                    "data_source_url": src.get("url", ""),
                    "data_steward": src.get("steward", ""),
                    "license": src.get("license", ""),
                }
            )
        return self

    def collected_by(
        self, org: str, method: str = "", date: str = ""
    ) -> "ProvenanceBuilder":
        self._data.update(
            {
                "data_steward": org,
                "collection_method": method,
                "collection_date": date,
            }
        )
        return self

    def processed_by(
        self, analyst: str, org: str = "", purpose: str = ""
    ) -> "ProvenanceBuilder":
        self._data.update(
            {
                "analyst_name": analyst,
                "analyst_org": org,
                "analysis_purpose": purpose,
            }
        )
        return self

    def step(self, description: str) -> "ProvenanceBuilder":
        self._data.setdefault("processing_steps", []).append(description)
        return self

    def derived_from(self, *record_ids: str) -> "ProvenanceBuilder":
        self._data.setdefault("derived_from", []).extend(record_ids)
        return self

    def classify(self, tier_id: str) -> "ProvenanceBuilder":
        self._data["classification"] = tier_id
        return self

    def note(self, text: str) -> "ProvenanceBuilder":
        self._data["notes"] = text
        return self

    def build(self) -> ProvenanceRecord:
        if "dataset_name" not in self._data:
            self._data["dataset_name"] = self._data["record_id"]
        if "classification" not in self._data:
            raise ValueError(
                (
                    "An explicit classification is required before building a "
                    "provenance record."
                )
            )
        if hasattr(self, "_ctx"):
            tiers = {tier["id"] for tier in self._ctx.config.classification_tiers}
            if self._data["classification"] not in tiers:
                raise ValueError("Classification is not in the Nation configuration")
        return ProvenanceRecord(**self._data)


# Provenance catalog


class ProvenanceCatalog:
    """
    A collection of ProvenanceRecord objects for a project or organization.
    Supports JSON export for inclusion in data packages.

    Example
    catalog = ProvenanceCatalog("Tribal Water Monitoring — 2024")
    catalog.add(record1)
    catalog.add(record2)
    catalog.save("outputs/provenance_catalog.json")
    catalog.print_summary()
    """

    def __init__(self, project_name: str):
        self.project_name = project_name
        self._records: list[ProvenanceRecord] = []

    def add(self, record: ProvenanceRecord) -> None:
        self._records.append(record)

    def get(self, record_id: str) -> ProvenanceRecord | None:
        return next((r for r in self._records if r.record_id == record_id), None)

    def filter_by_nation(self, nation_name: str) -> list[ProvenanceRecord]:
        return [r for r in self._records if r.nation_name == nation_name]

    def filter_by_classification(self, classification: str) -> list[ProvenanceRecord]:
        return [r for r in self._records if r.classification == classification]

    def to_dict(self) -> dict:
        return {
            "project": self.project_name,
            "created": datetime.date.today().isoformat(),
            "schema": "idsov-toolkit-provenance-v2",
            "conformance": "IEEE conformance not established",
            "records": [r.to_dict() for r in self._records],
        }

    def save(self, path: str | Path) -> None:
        from pathlib import Path

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"Provenance catalog saved: {path}")

    def print_summary(self) -> None:
        print(f"PROVENANCE CATALOG — {self.project_name}")
        print(f"Records: {len(self._records)}")
        print()
        for r in self._records:
            print(f"  {r.record_id}")
            print(f"    Dataset      : {r.dataset_name}")
            print(f"    Nation       : {r.nation_name}")
            print(f"    Classification: {r.classification}")
            print(f"    Source       : {r.data_source_name}")
            print()
