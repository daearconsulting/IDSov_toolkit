from __future__ import annotations

"""
toolkit/sovereignty.py
Tribal Data Sovereignty Toolkit

Canonical, nation-agnostic sovereignty module.
All other repos in the Daear Consulting ecosystem import from here
rather than maintaining their own copies.

Usage
from toolkit.sovereignty import SovereigntyContext

ctx = SovereigntyContext.from_config("config/nation.yaml")
ctx.print_acknowledgment()
ctx.attach_provenance(my_geodataframe, source_key="usgs_nwis")

Adapting for a new Nation
Edit config/nation_template.yaml and save as config/nation.yaml
No code changes required.
"""

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Nation configuration

@dataclass
class NationConfig:
    """
    Holds all Nation-specific configuration loaded from nation.yaml.
    Fields map directly to config/nation_template.yaml.
    """
    # Identity
    name:           str
    collective:     str | None
    territory:      str
    census_name:    str
    language:       str | None
    demonym:        str | None

    # Provenance
    treaty_name:        str
    treaty_territory:   str
    treaty_status:      str
    legal_citations:    list[str]
    subsurface_note:    str | None

    # Stewardship
    department:    str
    contact_url:   str
    contact_note:  str

    # Frameworks
    frameworks_enabled: dict[str, bool]
    framework_refs:     dict[str, str]

    # Data classification
    classification_tiers: list[dict]

    # Attribution
    citation_format:  str
    acknowledgment:   str

    @classmethod
    def from_yaml(cls, path: str | Path) -> "NationConfig":
        """Load NationConfig from a YAML file."""
        try:
            import yaml
        except ImportError:
            raise ImportError("PyYAML is required: pip install pyyaml")

        with open(path) as f:
            cfg = yaml.safe_load(f)

        n  = cfg["nation"]
        p  = cfg["provenance"]
        s  = cfg["stewardship"]
        fw = cfg["frameworks"]
        at = cfg["attribution"]
        dc = cfg.get("data_classification", {})

        return cls(
            name           = n["name"],
            collective     = n.get("collective"),
            territory      = n["territory"],
            census_name    = n.get("census_name", n["name"]),
            language       = n.get("language"),
            demonym        = n.get("demonym"),
            treaty_name        = p["treaty_name"],
            treaty_territory   = p["treaty_territory"],
            treaty_status      = p["treaty_status"].strip(),
            legal_citations    = p.get("legal_citations", []),
            subsurface_note    = p.get("subsurface_note", "").strip() or None,
            department   = s["department"],
            contact_url  = s.get("contact_url", ""),
            contact_note = s.get("contact_note", "").strip(),
            frameworks_enabled = {k: fw[k]["enabled"] for k in fw},
            framework_refs     = {k: fw[k]["reference"] for k in fw},
            classification_tiers = dc.get("tiers", []),
            citation_format  = at.get("citation_format", "").strip(),
            acknowledgment   = at.get("acknowledgment", "").strip(),
        )

    @property
    def active_frameworks(self) -> list[str]:
        return [k for k, v in self.frameworks_enabled.items() if v]

    def validate(self) -> list[str]:
        """Return list of validation warnings (empty = valid)."""
        warnings = []
        if not self.name:
            warnings.append("nation.name is required")
        if not self.territory:
            warnings.append("nation.territory is required")
        if not self.treaty_name:
            warnings.append("provenance.treaty_name is required")
        if not self.treaty_status:
            warnings.append("provenance.treaty_status is required")
        if not self.department:
            warnings.append("stewardship.department is required")
        if not self.active_frameworks:
            warnings.append("At least one governance framework must be enabled")
        return warnings


# Sovereignty context

class SovereigntyContext:
    """
    Main interface for the sovereignty toolkit.
    Wraps a NationConfig and provides methods for acknowledgment,
    provenance attachment, citation generation, and governance auditing.

    Examples
    ctx = SovereigntyContext.from_config("config/nation.yaml")
    ctx.print_acknowledgment()
    ctx.print_data_sources(["usgs_nwis", "usda_ssurgo"])
    gdf = ctx.attach_provenance(gdf, source_key="usgs_nwis")
    report = ctx.governance_report(dataset_name="streamflow_2024")
    """

    # Built-in source registry: extend with register_source()
    _BUILTIN_SOURCES: dict[str, dict] = {
        "usgs_nwis_streamflow": {
            "name":     "USGS National Water Information System Streamflow",
            "steward":  "US Geological Survey",
            "license":  "Public domain",
            "url":      "https://waterdata.usgs.gov/nwis/",
            "note":     (
                "USGS streamflow monitoring coverage on Tribal lands is "
                "systematically sparse. Monitoring gaps are a federal "
                "infrastructure equity finding, not a data error."
            ),
        },
        "usgs_nwis_groundwater": {
            "name":     "USGS National Water Information System Groundwater",
            "steward":  "US Geological Survey",
            "license":  "Public domain",
            "url":      "https://waterdata.usgs.gov/nwis/",
            "note":     (
                "USGS groundwater monitoring well density on Tribal lands "
                "is a fraction of that in adjacent agricultural counties. "
                "This is a federal investment equity gap."
            ),
        },
        "usgs_3d_model": {
            "name":     "USGS 3D Geological Model of Western South Dakota",
            "steward":  "US Geological Survey, Rocky Mountain Region",
            "license":  "CC0 1.0 Universal (Public Domain)",
            "url":      "https://doi.org/10.5066/P9LK4QHJ",
            "citation": (
                "Spangler, L.R., 2024, Digital data for a 3D Geological "
                "Model of western South Dakota, USA: U.S. Geological Survey "
                "data release, https://doi.org/10.5066/P9LK4QHJ."
            ),
            "note": None,
        },
        "usda_ssurgo": {
            "name":     "USDA NRCS SSURGO Soil Survey Geographic Database",
            "steward":  "USDA Natural Resources Conservation Service",
            "license":  "Public domain",
            "url":      "https://websoilsurvey.nrcs.usda.gov/",
            "note":     (
                "SSURGO sampling density on Tribal lands is frequently lower "
                "than adjacent non-Tribal agricultural lands. This is a "
                "federal investment gap, not evidence of uniform soil conditions."
            ),
        },
        "census_aiannh": {
            "name":     "US Census Bureau TIGER/Line AIANNH Boundaries",
            "steward":  "US Census Bureau",
            "license":  "Public domain",
            "url":      "https://www.census.gov/geographies/mapping-files/",
            "note":     (
                "Census boundaries are for statistical purposes only. "
                "They do not represent legal jurisdiction or Tribal "
                "self-definition."
            ),
        },
        "noaa_pdsi": {
            "name":     "NOAA Climate Division PDSI",
            "steward":  "National Oceanic and Atmospheric Administration",
            "license":  "Public domain",
            "url":      "https://www.ncei.noaa.gov/pub/data/cirs/climdiv/",
            "note":     (
                "NOAA PDSI is computed from weather station observations. "
                "Station density on Tribal lands is lower than surrounding "
                "areas, affecting index accuracy for specific communities."
            ),
        },
        "daymet": {
            "name":     "Daymet Daily Surface Weather Data",
            "steward":  "NASA/Oak Ridge National Laboratory",
            "license":  "Public domain",
            "url":      "https://daymet.ornl.gov/",
            "note":     (
                "Daymet is a modeled dataset interpolated from ground "
                "station observations. Accuracy is limited in areas with "
                "sparse ground station coverage, including many Tribal lands."
            ),
        },
        "usgs_mrds": {
            "name":     "USGS Mineral Resources Data System (MRDS)",
            "steward":  "US Geological Survey",
            "license":  "Public domain",
            "url":      "https://mrdata.usgs.gov/mrds/",
            "note":     None,
        },
        "tribal_field_data": {
            "name":     "Tribal-Collected Field Data",
            "steward":  "Tribal Nation: governed by OCAP®",
            "license":  "Tribal: not for public release without authorization",
            "url":      "data/raw/ (local only: gitignored)",
            "note":     (
                "This data is collected by or in partnership with Tribal "
                "natural resource staff. Under OCAP® principles, the "
                "collecting Nation retains Ownership, Control, Access, and "
                "Possession. Never commit to version control or share without "
                "explicit Tribal authorization."
            ),
        },
    }

    def __init__(self, config: NationConfig):
        self.config   = config
        self._sources = dict(self._BUILTIN_SOURCES)

    @classmethod
    def from_config(cls, path: str | Path) -> "SovereigntyContext":
        """Load from a YAML config file."""
        config = NationConfig.from_yaml(path)
        errors = config.validate()
        if errors:
            print("Configuration warnings:")
            for e in errors:
                print(f"  ! {e}")
        return cls(config)

    @classmethod
    def from_dict(cls, cfg: dict) -> "SovereigntyContext":
        """
        Create a minimal SovereigntyContext from a dictionary.
        Useful for quick setup in notebooks without a YAML file.

        Example
        ctx = SovereigntyContext.from_dict({
            "name": "Navajo Nation",
            "territory": "Navajo Nation Reservation",
            "treaty_name": "1868 Treaty of Bosque Redondo",
        })
        """
        config = NationConfig(
            name            = cfg.get("name", "Tribal Nation"),
            collective      = cfg.get("collective"),
            territory       = cfg.get("territory", "Tribal Territory"),
            census_name     = cfg.get("census_name", cfg.get("name", "")),
            language        = cfg.get("language"),
            demonym         = cfg.get("demonym"),
            treaty_name     = cfg.get("treaty_name", ""),
            treaty_territory= cfg.get("treaty_territory", ""),
            treaty_status   = cfg.get("treaty_status",
                "This data describes the sovereign territory and resources "
                "of an Indigenous Nation. All use is subject to OCAP® principles."),
            legal_citations    = cfg.get("legal_citations", []),
            subsurface_note    = cfg.get("subsurface_note"),
            department   = cfg.get("department", "Natural Resources Department"),
            contact_url  = cfg.get("contact_url", ""),
            contact_note = cfg.get("contact_note", ""),
            frameworks_enabled = cfg.get("frameworks_enabled", {
                "ocap": True, "care": True, "fair": True, "ieee_2890": True,
                "local_contexts": False,
            }),
            framework_refs = {
                "ocap":           "https://fnigc.ca/ocap-training/",
                "care":           "https://www.gida-global.org/care",
                "fair":           "https://www.go-fair.org/fair-principles/",
                "ieee_2890":      "https://standards.ieee.org/ieee/2890/10318/",
                "local_contexts": "https://localcontexts.org/",
            },
            classification_tiers = cfg.get("classification_tiers", []),
            citation_format  = cfg.get("citation_format", ""),
            acknowledgment   = cfg.get("acknowledgment", ""),
        )
        return cls(config)

    def register_source(self, key: str, source: dict) -> None:
        """
        Register a new data source for use with attach_provenance()
        and generate_citations().

        Parameters
        key    : Unique identifier string (e.g. "my_custom_dataset")
        source : Dict with keys: name, steward, license, url, note (optional),
                 citation (optional)
        """
        required = ["name", "steward", "license", "url"]
        for r in required:
            if r not in source:
                raise ValueError(f"Source must include '{r}'")
        self._sources[key] = source

    # Acknowledgment methods

    def print_acknowledgment(
        self,
        source_keys: list[str] | None = None,
        include_data_sources: bool = True,
    ) -> None:
        """
        Print the full data governance acknowledgment.
        Call at the top of every notebook.
        """
        cfg = self.config
        print("TRIBAL DATA SOVEREIGNTY ACKNOWLEDGMENT")
        print()
        print(f"  Nation    : {cfg.name}")
        if cfg.collective:
            print(f"  Collective: {cfg.collective}")
        print(f"  Territory : {cfg.territory}")
        print()
        print("  This analysis describes the lands, waters, and communities")
        print(f"  of the {cfg.name} people.")
        print()
        print(f"  Treaty: {cfg.treaty_name}")
        print(f"  {cfg.treaty_status}")
        if cfg.legal_citations:
            for cite in cfg.legal_citations:
                print(f"  Citation: {cite}")
        print()

        # Governance frameworks
        print("  GOVERNANCE FRAMEWORKS")
        fw_labels = {
            "ocap":           ("OCAP®",        "Ownership, Control, Access, Possession"),
            "care":           ("CARE",          "Collective Benefit, Authority, Responsibility, Ethics"),
            "fair":           ("FAIR",          "Findable, Accessible, Interoperable, Reusable"),
            "ieee_2890":      ("IEEE 2890-2025","Recommended Practice for Provenance of Indigenous Data"),
            "local_contexts": ("Local Contexts","Traditional Knowledge Labels and Notices"),
        }
        for fw_key, enabled in cfg.frameworks_enabled.items():
            if enabled:
                label, desc = fw_labels.get(fw_key, (fw_key.upper(), ""))
                ref         = cfg.framework_refs.get(fw_key, "")
                print(f"  {label:<18}: {desc}")
                print(f"  {'':<18}  {ref}")
                print()

        if include_data_sources and source_keys:
            print("  DATA SOURCES")
            print(" + ")
            for key in source_keys:
                src = self._sources.get(key)
                if not src:
                    print(f"  [Unknown source: {key}]")
                    continue
                print(f"  {src['name']}")
                print(f"    Steward : {src['steward']}")
                print(f"    License : {src['license']}")
                if src.get("note"):
                    print(f"    Note    : {src['note'][:80]}...")
                print()

    def generate_citations(self, source_keys: list[str]) -> str:
        """Return a plain-text citation block."""
        cfg   = self.config
        lines = ["DATA CITATIONS", ]

        for key in source_keys:
            src = self._sources.get(key)
            if not src:
                continue
            lines.append(f"\n{src['name']}")
            if src.get("citation"):
                lines.append(f"  {src['citation']}")
            lines.append(f"  {src['url']}")
            lines.append(f"  Steward: {src['steward']} | License: {src['license']}")

        lines += [
            "\nTERRITORIAL PROVENANCE",
            f"  Treaty: {cfg.treaty_name} — {cfg.treaty_territory}",
            f"  {cfg.treaty_status}",
        ]
        if cfg.legal_citations:
            for cite in cfg.legal_citations:
                lines.append(f"  {cite}")

        fw_str = " | ".join(
            k.upper().replace("_", " ")
            for k, v in cfg.frameworks_enabled.items() if v
        )
        lines.append(f"\nGOVERNANCE: {fw_str}")
        return "\n".join(lines)

    # Provenance attachment

    def attach_provenance(
        self,
        gdf,
        source_key: str,
        classification: str = "PUBLIC",
        additional: dict | None = None,
    ):
        """
        Attach IEEE 2890-2025 provenance attributes to a GeoDataFrame.

        Parameters
        gdf            : GeoDataFrame to annotate
        source_key     : Key in the source registry
        classification : Data classification tier ID (from nation.yaml)
        additional     : Any additional provenance fields to attach

        Returns
        Annotated GeoDataFrame (copy)
        """
        cfg = self.config
        src = self._sources.get(source_key, {})
        out = gdf.copy()

        # IEEE 2890-2025 required provenance fields
        out["prov_nation"]          = cfg.name
        out["prov_territory"]       = cfg.territory
        out["prov_treaty"]          = cfg.treaty_name
        out["prov_data_source"]     = src.get("name", source_key)
        out["prov_steward"]         = src.get("steward", "")
        out["prov_license"]         = src.get("license", "")
        out["prov_url"]             = src.get("url", "")
        out["prov_classification"]  = classification
        out["prov_frameworks"]      = " | ".join(
            k.upper() for k, v in cfg.frameworks_enabled.items() if v
        )
        out["prov_dept"]            = cfg.department

        if additional:
            for k, v in additional.items():
                out[f"prov_{k}"] = v

        return out

    # Governance report

    def governance_report(
        self,
        dataset_name: str,
        source_keys: list[str] | None = None,
        classification: str = "PUBLIC",
        analyst_name: str = "",
        notes: str = "",
    ) -> str:
        """
        Generate a governance report for a dataset or analysis product.
        Returns a formatted string suitable for inclusion in a README
        or data package.
        """
        import datetime
        cfg  = self.config
        date = datetime.date.today().isoformat()

        lines = [
            f"DATA GOVERNANCE REPORT",
            f"Dataset       : {dataset_name}",
            f"Nation        : {cfg.name}",
            f"Territory     : {cfg.territory}",
            f"Classification: {classification}",
            f"Report date   : {date}",
        ]
        if analyst_name:
            lines.append(f"Analyst       : {analyst_name}")
        lines += [
            "",
            "TERRITORIAL PROVENANCE",
            f"  Treaty    : {cfg.treaty_name}",
            f"  Territory : {cfg.treaty_territory}",
            f"  Status    : {cfg.treaty_status}",
        ]
        if cfg.legal_citations:
            for cite in cfg.legal_citations:
                lines.append(f"  Citation  : {cite}")

        lines += ["", "GOVERNANCE FRAMEWORKS"]
        for fw, enabled in cfg.frameworks_enabled.items():
            if enabled:
                ref = cfg.framework_refs.get(fw, "")
                lines.append(f"  {fw.upper():<18}: {ref}")

        if source_keys:
            lines += ["", "DATA SOURCES"]
            for key in source_keys:
                src = self._sources.get(key)
                if src:
                    lines.append(f"  {src['name']}")
                    lines.append(f"    Steward : {src['steward']}")
                    lines.append(f"    License : {src['license']}")

        lines += [
            "",
            "STEWARDSHIP",
            f"  Department : {cfg.department}",
            f"  Contact    : {cfg.contact_url or 'See Tribal administration'}",
            f"  Note       : {cfg.contact_note}",
        ]

        if notes:
            lines += ["", "ANALYST NOTES", f"  {notes}"]

        lines += [
            "",
            "This report was generated by the Tribal Data Sovereignty Toolkit.",
            "Daear Consulting, LLC daear-consulting.com",
        ]

        return "\n".join(lines)

    # Data classification

    def classify(self, dataset_description: str) -> str:
        """
        Interactive classification helper prints classification tiers
        and prompts analyst to select appropriate tier for a dataset.
        Returns the selected tier ID.
        """
        cfg   = self.config
        tiers = cfg.classification_tiers

        if not tiers:
            print("No classification tiers defined in config. Using PUBLIC.")
            return "PUBLIC"

        print(f"DATA CLASSIFICATION — {cfg.name}")
        print(f"Dataset: {dataset_description}")
        print()
        for i, tier in enumerate(tiers, 1):
            print(f"  [{i}] {tier['label']}")
            print(f"      {tier['description'].strip()[:100]}")
            if tier.get("examples"):
                print(f"      Examples: {', '.join(tier['examples'][:2])}")
            print()

        while True:
            try:
                choice = int(input("Select classification [number]: "))
                if 1 <= choice <= len(tiers):
                    selected = tiers[choice - 1]
                    print(f"\nClassified as: {selected['label']}")
                    return selected["id"]
            except (ValueError, KeyboardInterrupt):
                pass
            print("Please enter a number from the list.")


# Module CLI

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Tribal Data Sovereignty Toolkit sovereignty.py"
    )
    parser.add_argument("--config", default="config/nation.yaml",
                        help="Path to nation YAML config file")
    parser.add_argument("--validate", action="store_true",
                        help="Validate config and print acknowledgment")
    parser.add_argument("--report", metavar="DATASET",
                        help="Generate a governance report for a dataset")
    args = parser.parse_args()

    ctx = SovereigntyContext.from_config(args.config)

    if args.validate:
        print("Config loaded successfully.\n")
        ctx.print_acknowledgment()

    if args.report:
        print(ctx.governance_report(dataset_name=args.report))
