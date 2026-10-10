# Synthetic drought fixture

`synthetic_pdsi.csv` is generated classroom data, not NOAA observations.
Division IDs 7 and 8 are demonstration keys and do not establish a study area.
Values use `3.8*sin((year-1980)*0.63 + month/12) + 0.6*cos(month) + 0.2*(division-7)`.
The fixture covers 1980–2024. April 1992 lacks division 8 and 2024 has only
January–June. These deliberate gaps teach coverage checks. Annual analysis
must exclude both years, leaving 43 complete years. Do not interpret its
trend as a finding about any real Nation or territory.
