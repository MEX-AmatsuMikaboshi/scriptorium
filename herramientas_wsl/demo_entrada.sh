#!/usr/bin/env bash
# Crea la carpeta de datos en D: y deja el texto de la demo en 00_entrada.
D=/mnt/d/Scriptorium
mkdir -p "$D/00_entrada" "$D/01_canonico" "$D/02_derivados" "$D/03_biblioteca"
salida="$D/00_entrada/Balmes - El criterio - Capitulo I.md"
{
  printf -- '---\ntitulo: El criterio\nautor: Jaime Balmes\nfecha: 1845\nfuente: Wikisource (dominio público)\n---\n\n'
  printf '# Capítulo I. Consideraciones preliminares\n\n'
  sed -E 's/^== (.*) ==$/## \1/' /tmp/demo/balmes01.txt
} > "$salida"
ls -la "$D/00_entrada"
head -n 12 "$salida"
