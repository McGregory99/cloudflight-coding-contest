#!/bin/zsh
# Usage: _collect.sh <challenge-folder-name>
# Moves level-*.zip from ~/Downloads into training/<name>/ and extracts each one.
set -e
name="$1"
dest="/Users/gcancio/DEVELOPMENT/CCC/training/$name"
mkdir -p "$dest"
mv ~/Downloads/level-*.zip "$dest/"
cd "$dest"
for z in level-*.zip; do
  d="${z%.zip}"
  mkdir -p "$d"
  unzip -oq "$z" -d "$d"
  rm "$z"
done
ls
