from __future__ import annotations

"""
toolkit/provenance.py
Tribal Data Sovereignty Toolkit

IEEE 2890-2025 provenance record generation.
Implements the Recommended Practice for Provenance of Indigenous Peoples' Data.

IEEE 2890-2025 establishes that provenance records for Indigenous data must
document not only technical lineage (who created the data, how, when) but
also governance lineage (whose land it describes, under what authority it was
collected, and what obligations attach to its use).

This module operationalizes that standard into Python-native data structures
that can be attached to any dataset, exported as JSON or CSV, and included
in data packages and publications.
"""

import json
import datetime
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


# Provenance record

@dataclass
class ProvenanceRecord:
    """
    A single IEEE 2890-2025 compliant provenance record.

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
    record_id:          str
    dataset_name:       str
    created_date:       str = field(
        default_factory=lambda: datetime.date.today().isoformat()
    )

    # Indigenous data governance provenance (IEEE 2890-2025 core)
    nation_name:        str = ""
    territory_name:     str = ""
    treaty_reference:   str = ""
    treaty_status:      str = ""
    legal_citation:     str = ""

    # Technical provenance (W3C PROV-compatible)
    data_source_name:   str = ""
    data_source_url:    str = ""
    data_steward:       str = ""
    license:            str = ""
    collection_method:  str = ""
    collection_date:    str = ""

    # Governancea 
    classification:     str = "PUBLIC"
    frameworks:         str = ""
    stewardship_dept:   str = ""

    # Analyst
    analyst_name:       str = ""
    analyst_org:        str = ""
    analysis_purpose:   str = ""

    # Lineage
    processing_steps:   list[str] = field(default_factory=list)
    derived_from:       list[str] = field(default_factory=list)
    notes:              str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def to_markdown(self) -> str:
        """Return a formatted markdown provenance statement."""
        lines = [
            f"## Data Provenance {self.dataset_name}",
            f"",
            f"**Record ID:** `{self.record_id}`  ",
            f"**Created:** {self.created_date}  ",
            f"",
            f"### Territorial Provenance",
            f"",
            f"| Field | Value |",
            f"|---|---|",
            f"| Nation | {self.nation_name} |",
            f"| Territory | {self.territory_name} |",
            f"| Treaty | {self.treaty_reference} |",
        ]
        if self.treaty_status:
            lines += [f"", f"**Status:** {self.treaty_status}", f""]
        if self.legal_citation:
            lines += [f"**Legal citation:** {self.legal_citation}", f""]

        lines += [
            f"### Data Source",
            f"",
            f"| Field | Value |",
            f"|---|---|",
            f"| Source | {self.data_source_name} |",
            f"| URL | {self.data_source_url} |",
            f"| Steward | {self.data_steward} |",
            f"| License | {self.license} |",
            f"| Classification | {self.classification} |",
            f"| Frameworks | {self.frameworks} |",
            f"",
        ]

        if self.processing_steps:
            lines += ["### Processing Steps", ""]
            for i, step in enumerate(self.processing_steps, 1):
                lines.append(f"{i}. {step}")
            lines.append("")

        if self.notes:
            lines += [f"### Notes", f"", f"{self.notes}", f""]

        lines += [
            f"---",
            f"*Generated by the Tribal Data Sovereignty Toolkit "
            f"IEEE 2890-2025 compliant*",
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
        self._data.update({
            "nation_name":      cfg.name,
            "territory_name":   cfg.territory,
            "treaty_reference": cfg.treaty_name,
            "treaty_status":    cfg.treaty_status,
            "legal_citation":   (cfg.legal_citations[0]
                                  if cfg.legal_citations else ""),
            "stewardship_dept": cfg.department,
            "frameworks":       " | ".join(
                k.upper() for k, v in cfg.frameworks_enabled.items() if v
            ),
        })
        self._ctx = ctx
        return self

    def for_dataset(self, name: str) -> "ProvenanceBuilder":
        self._data["dataset_name"] = name
        return self

    def from_source(self, source_key: str) -> "ProvenanceBuilder":
        """Auto-populate source fields from the SovereigntyContext registry."""
        if hasattr(self, "_ctx"):
            src = self._ctx._sources.get(source_key, {})
            self._data.update({
                "data_source_name": src.get("name", source_key),
                "data_source_url":  src.get("url", ""),
                "data_steward":     src.get("steward", ""),
                "license":          src.get("license", ""),
            })
        return self

    def collected_by(
        self, org: str, method: str = "", date: str = ""
    ) -> "ProvenanceBuilder":
        self._data.update({
            "data_steward":     org,
            "collection_method":method,
            "collection_date":  date,
        })
        return self

    def processed_by(
        self, analyst: str, org: str = "", purpose: str = ""
    ) -> "ProvenanceBuilder":
        self._data.update({
            "analyst_name":    analyst,
            "analyst_org":     org,
            "analysis_purpose":purpose,
        })
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
        return next((r for r in self._records
                     if r.record_id == record_id), None)

    def filter_by_nation(self, nation_name: str) -> list[ProvenanceRecord]:
        return [r for r in self._records if r.nation_name == nation_name]

    def filter_by_classification(
        self, classification: str
    ) -> list[ProvenanceRecord]:
        return [r for r in self._records
                if r.classification == classification]

    def to_dict(self) -> dict:
        return {
            "project":  self.project_name,
            "created":  datetime.date.today().isoformat(),
            "standard": "IEEE 2890-2025",
            "records":  [r.to_dict() for r in self._records],
        }

    def save(self, path: str | Path) -> None:
        from pathlib import Path
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False),
            encoding="utf-8"
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
