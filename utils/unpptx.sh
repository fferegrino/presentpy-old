#!/usr/bin/env bash

function unpptx {
    filename=$(basename -- $1)
    parentdir="$(dirname "$1")"
    extension=$2
    echo "Decompressing $filename into $parentdir"
    source=$1
    folder="$parentdir/${filename%.*}_${extension}"

    unzip -qq -o -d $folder $source

    find ./$folder -type f -name "*.xml" -exec  sh -c "cat {} | xmllint --format - | sponge {}" \;
    find ./$folder -type f -name "*.rels" -exec  sh -c "cat {} | xmllint --format - | sponge {}" \;
}

for i in `find . -name "*.pptx" -type f`; do
    unpptx "$i" "pptx"
done

for i in `find . -name "*.potx" -type f`; do
    unpptx "$i" "potx"
done