#!/usr/bin/env bash
# Descarga el PDF que genera Wikisource del capítulo II de El criterio (prueba realista de PDF).
destino="/mnt/d/Scriptorium/00_entrada/Balmes - El criterio - Capitulo II.pdf"
curl -sL -A "Scriptorium/0.1 (uso personal)" -o "$destino" "https://es.wikisource.org/api/rest_v1/page/pdf/El_criterio%2F02"
file "$destino"
ls -la "$destino"
pdfinfo "$destino" 2>/dev/null | grep -E "Pages|Title|Producer"
pdftotext -l 1 "$destino" - 2>/dev/null | head -n 25
