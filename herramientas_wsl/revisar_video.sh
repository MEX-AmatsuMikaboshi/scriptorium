#!/usr/bin/env bash
d=/mnt/d/Scriptorium/02_derivados/jaime-balmes-el-criterio
ls -la "$d/video"
for f in "$d"/video/*.mp4 "$d"/audio/audiolibro.m4b "$d"/audio/podcast.mp3 "$d"/audio/audioguia.mp3; do
  [ -f "$f" ] && printf '%-60s %s\n' "$(basename "$f")" "$(ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact=p=0:nk=1 "$f" | tr '\n' ' ')"
done
ffprobe -v error -show_chapters -of compact=p=0 "$d/audio/audiolibro.m4b" | head -n 8
ls -la /mnt/d/Scriptorium/03_biblioteca/
