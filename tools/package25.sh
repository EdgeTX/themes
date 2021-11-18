#!/usr/bin/env bash
SCRIPT_DIR="$(realpath "$(dirname "${BASH_SOURCE[0]:-$0}")")"
THEMES_DIR="$(realpath "${SCRIPT_DIR}"/../THEMES)"
BUILD_DIR="$(realpath "${SCRIPT_DIR}"/../build)"

if [ ! -d "${BUILD_DIR}" ]; then
    mkdir -p "${BUILD_DIR}"
fi

cd "${BUILD_DIR}" || exit
echo "Work dir: '${BUILD_DIR}' ..."
rm ./*.zip 2> /dev/null

# Individual themes
cd "${THEMES_DIR}" || exit 1
for i in *.yml; do
    [ -f "$i" ] || break
   themename=${i##*/}
   themename=${themename%.yml}
   echo "Packaging $themename ..."
   zip -r -q "${BUILD_DIR}/$themename.zip" . -i "$themename"*
done

# All themes
echo "Packaging all themes ..."
zip -r -q "${BUILD_DIR}/_all-themes.zip" . -i ./*
