#!/usr/bin/env bash

function unpptx {
    parent_dir="$(dirname "$1")"
    filename=$(basename -- "$1")
    extension=$2
    echo "Decompressing $filename into $parent_dir"
    source=$1
    folder="$parent_dir/${filename%.*}_${extension}"

    unzip -qq -o -d "$folder" "$source"

    find "$folder" -type f -name "*.xml" -exec sh -c "cat {} | xmllint --format - | sponge {}" \;
    find "$folder" -type f -name "*.rels" -exec sh -c "cat {} | xmllint --format - | sponge {}" \;
}

search_path="${1:-$PWD}"

for i in $(find $search_path -name "*.pptx" -type f); do
    unpptx "$i" "pptx"
done

for i in $(find $search_path -name "*.potx" -type f); do
    unpptx "$i" "potx"
done
