# Screenshot Caption Log

02-s3_carbon-range_2026-06-12: Drei horizontale Range-Balken (Verlust in ha, Carbon-Loss in Mio. t CO2e, Marktwert in Mio. USD) mit Low-/High-Markern – zeigt die Unsicherheits-Spanne des Sundarbans-Mangrovenverlusts (1996-2020) statt einer Punktschätzung.

Tabelle_wolkenarme_Tage: Top-10-Tabelle der STAC-Suchergebnisse (Sentinel-2-L2A, Sundarbans-Bbox, Q1 2020, Cloud Cover < 10%) sortiert nach Wolkenbedeckung – Basis für die Szenenauswahl.

03-s1_true-color_2026-06-13: True-Color-RGB (Percentile-Stretch) der Szene S2B_MSIL2A_20200201T043009_R133_T45QYE_20200930T090850 (2020-02-01, Cloud Cover 1.2%) über der Sundarbans-Bbox – Mangrovenwald sichtbar im rechten Bildbereich, helle Sandbänke/trübes Wasser im Mündungsbereich.

03-s1_ndvi_2026-06-13: NDVI-Karte derselben Szene (RdYlGn-Colormap, -1 bis +1), NDVI-Mean 0.252 – grüne Bereiche = Vegetation (Mangroven), rötlich/gelb = Wasser und Sandbänke; ca. 3% NaN-Pixel am Kachelrand (kein Sensor-Coverage).

03-s1_ndvi-gmw-overlay_2026-06-13: NDVI-Karte mit 2073 GMW-2020-Mangroven-Polygonen als blaue Outlines überlagert – die Polygon-Grenzen decken sich gut mit den hoch-NDVI (grünen) Bereichen, visueller Sanity-Check bestanden.

03-s2_label-mask_2026-07-12: Side-by-Side: True Color (20 m, links) und rasterisierte GMW-2020-Label-Maske (0/1, rechts, grün = Mangrove) – 38% Mangrove-Anteil im Tile T45QYE, höher als typisch weil Tile per GMW-Overlap-Ranking ausgewählt wurde.

03-s2_confusion-matrix_2026-07-12: Confusion Matrix (sklearn ConfusionMatrixDisplay) des Random Forest (balanced, 50 Bäume, max_depth=15) auf 20.000 Validierungspixeln – Non-Mangrove Precision 94%, Mangrove Recall 94%, gesamt 92% Accuracy.

03-s2_pred-map_2026-07-12: Vorhergesagte Klassifikationskarte über das gesamte Sentinel-2-Tile T45QYE (5490×5490 Pixel, 20 m) – Mangroven grün, Non-Mangrove weiß, NaN-Randpixel transparent; räumliche Struktur deckt sich gut mit GMW-Ground-Truth.

03-s2_gmw-vs-pred_2026-07-12: Side-by-Side GMW-2020-Label-Maske (links, Ground Truth) vs. RF-Vorhersage (rechts) – wichtigstes Portfolio-Bild der Session; Modell reproduziert die Mangroven-Ausdehnung gut, mit leichter Überklassifikation in Übergangszonen.
