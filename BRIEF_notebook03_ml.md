# Brief für Claude Code — Notebook 03: Multispektral + STAC + ML

## Kontext (Repo-Stand)
Dies ist das bestehende Repo `mangroven-tracker`. Vorhanden:
- `notebooks/02_sundarbans_loss.ipynb` — analysiert Mangroven-Verlust 1996→2020 über **Vektor-Polygone** (Global Mangrove Watch v3, Shapefiles in `data/raw/gmw_v3_1996/` und `gmw_v3_2020/`), berechnet Fläche (EPSG:6933), CO₂-Schätzung, Karte via leafmap.
- `app.py` — Streamlit-App mit hardcodeten Kennzahlen + vorberechneter leafmap-HTML.
- `requirements.txt` — enthält bereits `geopandas, rioxarray, xarray, pystac-client, planetary-computer, leafmap, plotly, numpy, pandas`.
- `src/` — leere Modul-Stubs (`data_loader.py`, `analysis.py`, `carbon_calc.py`, `visualizations.py`).
- `.venv` ist vorhanden.

**Lücke, die dieses Side-Project schließt:** Bisher nur fertige Vektor-Produkte. Es fehlt echte Arbeit mit **rohen Multispektralbändern**, **STAC** und **Machine Learning**. Genau das soll Notebook 03 abdecken — damit „STAC, rioxarray, multispectral, NDVI, ML" wahrheitsgemäß im Lebenslauf stehen darf.

## Ziel
Ein neues, lauffähiges `notebooks/03_sentinel_ml.ipynb`, das:
1. eine Sentinel-2-Szene der Sundarbans **per STAC** über Microsoft Planetary Computer lädt,
2. mit **rioxarray/xarray** auf die Bounding Box clippt und **NDVI** berechnet,
3. die **GMW-Polygone zu einer Pixel-Maske rasterisiert** (Trainingslabels: Mangrove = 1, sonst = 0),
4. einen **scikit-learn RandomForest** auf dem Band-Stack trainiert (Mangrove vs. Nicht-Mangrove pro Pixel),
5. **Accuracy + Confusion-Matrix auf einem Held-out-Split** ausgibt und die Klassifikationskarte plottet.

## Tech-Stack / zusätzliche Dependencies
Bereits vorhanden nutzen. Neu zu `requirements.txt` hinzufügen und installieren:
- `scikit-learn`
- `rasterio` (für `rasterio.features.rasterize`)
- `matplotlib`
- optional `stackstac` (bequemes STAC→xarray-Stacking) — falls genutzt, dokumentieren.

## Schritt-für-Schritt-Plan (Time-Box ~2h)
1. **Setup & STAC-Query (30 min)**
   - `pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")`, `planetary_computer.sign_inplace`.
   - Collection `sentinel-2-l2a`, BBOX = `(88.0, 21.3, 90.7, 23.0)` (gleiche wie Notebook 02), `datetime` ~ Trockenzeit z. B. `"2020-01-01/2020-03-31"`, `query={"eo:cloud_cover": {"lt": 10}}`.
   - Wolkenärmste Szene auswählen.
2. **Laden & NDVI (20 min)**
   - Bänder B04 (Red), B08 (NIR), optional B03/B02/B11/B12 via rioxarray laden, auf BBOX clippen.
   - NDVI = (NIR − Red) / (NIR + Red), als Layer plotten.
3. **Labels rasterisieren (30 min)**
   - GMW-2020-Polygone (clippen wie in Notebook 02) zur gleichen Auflösung/Transform wie das Sentinel-Raster rasterisieren → Maske (1/0).
   - **CRS und Transform MÜSSEN exakt mit dem Sentinel-Raster übereinstimmen** (gleiches CRS reprojizieren, `out_shape`/`transform` aus dem rioxarray-Objekt).
4. **ML (40 min)**
   - Feature-Matrix X = gestapelte Bänder + NDVI (Pixel als Zeilen), y = Maske.
   - NaN/no-data-Pixel rausfiltern.
   - `train_test_split` (z. B. 70/30, stratify=y), `RandomForestClassifier(n_estimators=100, n_jobs=-1)`.
   - `accuracy_score` + `confusion_matrix` + `classification_report` ausgeben.
   - Vorhersage über das ganze Raster → Klassifikationskarte plotten, neben GMW-Maske zum Vergleich.

## Deliverables / Acceptance Criteria
- `notebooks/03_sentinel_ml.ipynb` läuft **von oben bis unten ohne Fehler** durch (`Restart & Run All`).
- Gibt am Ende aus: Held-out Accuracy (Zahl), Confusion-Matrix, eine Klassifikationskarten-Abbildung.
- Wiederverwendbare Funktionen in `src/data_loader.py` (STAC-Laden) und `src/analysis.py` (NDVI, rasterize, train) statt alles im Notebook — Notebook ruft die Funktionen auf.
- `requirements.txt` aktualisiert.
- Kurzer Abschnitt in `README.md` ergänzt: was Notebook 03 macht + erreichte Accuracy.

## Constraints / Hinweise
- **Bestehende Dateien nicht kaputt machen:** Notebook 02 und `app.py` unverändert lassen.
- Kommentare auf **Deutsch**, knapp, erklären *warum* (nicht nur *was*) — Stil wie in Notebook 02.
- **Speicher:** ggf. Auflösung reduzieren / nur BBOX-Window laden, nicht die ganze Szene in den RAM. Bei Bedarf auf 20 m oder gröber resamplen.
- **Reproduzierbarkeit:** `random_state=42` setzen.
- **Ehrlichkeit:** keine geschönten Metriken; wenn Accuracy mittelmäßig ist, so dokumentieren (Labels stammen aus 2020-GMW, Bildjahr ggf. abweichend — als Limitation nennen).
- Wenn der Planetary-Computer-Zugriff scheitert, prüfen ob `planetary_computer.sign_inplace` korrekt angewendet wird; kein alternatives Scraping, sondern Fehler melden.

## Erstes Kommando an Claude Code (Vorschlag)
> „Lies BRIEF_notebook03_ml.md und Notebook 02. Erstelle dann notebook03 + die src-Funktionen genau nach Brief. Installiere neue Dependencies ins vorhandene .venv. Führe das Notebook am Ende einmal komplett aus und zeig mir Accuracy + Confusion-Matrix."
