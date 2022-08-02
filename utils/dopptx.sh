#!/usr/bin/env bash

function dopptx {
    parent_dir="$(dirname "$1")"
    source_folder="$PWD/$parent_dir/$(basename -- "$1")"
    tmp_folder="${source_folder}_tmp"
    extension=${source_folder#*_}
    slides_name="${source_folder%%_*}.${extension}"
    mkdir "$tmp_folder"
    cp -r "$source_folder"/* "$tmp_folder"

    find "$tmp_folder" -type f -name "*.xml" -exec sh -c "cat {} | xmllint --noblanks - | sponge {}" \;
    find "$tmp_folder" -type f -name "*.rels" -exec sh -c "cat {} | xmllint --noblanks - | sponge {}" \;

    (cd "$tmp_folder"; zip -qq -r -X "$slides_name" *)

    rm -rf "$tmp_folder"
}

search_path="${1:-$PWD}"

for i in $(find $search_path -name "*_pptx" -type d); do
    dopptx "$i"
done

for i in $(find $search_path -name "*_potx" -type d); do
    dopptx "$i"
done
