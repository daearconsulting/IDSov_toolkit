"""Reproducible monthly drought preparation for the SEEDS lesson."""

import hashlib
import re
from pathlib import Path

import numpy as np
import pandas as pd
import requests


def load_noaa(state_code, divisions, start_year=1980):
    """Download and parse NOAA's latest explicitly dated PDSI file.

    Network failures raise. No fallback to synthetic observations occurs.
    Returns division-month records and source metadata including payload hash.
    """
    if state_code is None or not divisions:
        raise ValueError("Configure state_code and divisions before live retrieval")
    base = "https://www.ncei.noaa.gov/pub/data/cirs/climdiv/"
    listing = requests.get(base, timeout=30)
    listing.raise_for_status()
    names = re.findall(r"climdiv-pdsidv-v1\.0\.0-\d{8}", listing.text)
    if not names:
        raise ValueError("No dated NOAA PDSI file found in the directory listing")
    url = base + max(names)
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    frame = parse_noaa(response.text, state_code, divisions, start_year)
    return frame, {
        "url": url,
        "sha256": hashlib.sha256(response.content).hexdigest(),
        "retrieved_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "synthetic": False,
    }


def parse_noaa(text, state_code, divisions, start_year=1980):
    records = []
    state = str(state_code).zfill(2)
    for line in text.splitlines():
        parts = line.split()
        if not parts:
            continue
        code = parts[0]
        if len(code) != 10 or not code.isdigit():
            continue
        if code[:2] != state or code[4:6] != "05":
            continue
        division, year = int(code[2:4]), int(code[6:])
        if division not in divisions or year < start_year:
            continue
        if len(parts) != 13:
            raise ValueError(f"Malformed NOAA row: {code}")
        for month, raw in enumerate(parts[1:], 1):
            value = float(raw)
            records.append(
                {
                    "date": pd.Timestamp(year, month, 1),
                    "division": division,
                    "pdsi": np.nan if value <= -99 else value,
                }
            )
    if not records:
        raise ValueError("No matching observations; verify retrieval and geography")
    return pd.DataFrame(records)


def load_fixture(path):
    path = Path(path)
    frame = pd.read_csv(path, parse_dates=["date"])
    return frame, {
        "source": path.name,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "synthetic": True,
        "method": "Deterministic sinusoidal classroom fixture",
    }


def prepare_annual(frame, divisions):
    """Equal-weight mean only when every selected division is present.

    Reject duplicate month/division observations. Keep missing months in coverage,
    and exclude every incomplete calendar year from annual count comparisons.
    Returns monthly data, complete annual data, and annual coverage diagnostics.
    """
    if not divisions or len(set(divisions)) != len(divisions):
        raise ValueError("Select distinct division identifiers")
    data = frame.loc[frame["division"].isin(divisions)].copy()
    if data.empty:
        raise ValueError("No selected division observations")
    data["date"] = pd.to_datetime(data["date"])
    data["date"] = data["date"].dt.to_period("M").dt.to_timestamp()
    data["pdsi"] = pd.to_numeric(data["pdsi"], errors="raise")
    data.loc[(data["pdsi"] <= -99) | ~np.isfinite(data["pdsi"]), "pdsi"] = np.nan
    if data.duplicated(["date", "division"]).any():
        raise ValueError("Duplicate month/division observations")
    wide = data.pivot(index="date", columns="division", values="pdsi")
    dates = pd.date_range(
        f"{data.date.min().year}-01-01", f"{data.date.max().year}-12-01", freq="MS"
    )
    wide = wide.reindex(index=dates, columns=divisions)
    monthly = pd.DataFrame({"date": dates})
    monthly["division_count"] = wide.notna().sum(axis=1).to_numpy()
    monthly["pdsi_avg"] = wide.mean(axis=1).where(wide.notna().all(axis=1)).to_numpy()
    monthly["year"] = monthly.date.dt.year
    for division in divisions:
        monthly[f"division_{division}_pdsi"] = wide[division].to_numpy()
    coverage = monthly.groupby("year").agg(valid_months=("pdsi_avg", "count"))
    coverage["included"] = coverage.valid_months.eq(12)
    coverage["excluded_months"] = 12 - coverage.valid_months
    complete = monthly[monthly.year.isin(coverage.index[coverage.included])]
    annual = (
        complete.groupby("year")
        .agg(
            mean_pdsi=("pdsi_avg", "mean"),
            drought_months=("pdsi_avg", lambda x: int((x <= -2).sum())),
            extreme_months=("pdsi_avg", lambda x: int((x <= -4).sum())),
        )
        .reset_index()
    )
    if annual.empty:
        raise ValueError("No complete years with all selected divisions")
    return monthly, annual, coverage.reset_index()
