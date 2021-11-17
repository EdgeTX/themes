#!/usr/bin/env bash
SCRIPT_DIR="$(realpath $(dirname "$BASH_SOURCE"))"
THEMES_DIR="$(realpath "${SCRIPT_DIR}"/../THEMES)"

echo "Themes dir: '${THEMES_DIR}' ..."
cd "${THEMES_DIR}" || exit

# For each individual theme
for i in *.yml; do
    [ -f "$i" ] || break
    themename=${i##*/}
    themename=${themename%.yml}
    echo "Converting '$themename' to v2.6 format..."

    if [ ! -d "${THEMES_DIR}/$themename" ]; then
        mkdir -p "${THEMES_DIR}/$themename"
    fi

    if [ -f "${themename}.yml" ]; then
        mv "${THEMES_DIR}/${themename}.yml" "${THEMES_DIR}/${themename}/theme.yml"
    else
        "[ERROR] ${themename} is missing '${themename}.yml' file!"
    fi

    if [ -f "${themename}.png" ]; then
        mv "${THEMES_DIR}/${themename}.png" "${THEMES_DIR}/${themename}/logo.png"
    else
        "[ERROR] ${themename} is missing '${themename}.png' file!"
    fi

    if [ -f "${themename}1.png" ]; then
        mv "${THEMES_DIR}/${themename}1.png" "${THEMES_DIR}/${themename}/screenshot1.png"
    else
        "[ERROR] ${themename} is missing '${themename}1.png' file!"
    fi

    if [ -f "${themename}2.png" ]; then
        mv "${THEMES_DIR}/${themename}2.png" "${THEMES_DIR}/${themename}/screenshot2.png"
    else
        "[ERROR] ${themename} is missing '${themename}1.png' file!"
    fi

    if [ -f "${themename}3.png" ]; then
        mv "${THEMES_DIR}/${themename}3.png" "${THEMES_DIR}/${themename}/screenshot3.png"
    else
        "[ERROR] ${themename} is missing '${themename}3.png' file!"
    fi

    if [ -f "${themename}_bg_480x272.png" ]; then
        mv "${THEMES_DIR}/${themename}_bg_480x272.png" "${THEMES_DIR}/${themename}/background_480x272.png"
    fi

    if [ -f "${themename}_bg_320x480.png" ]; then
        mv "${THEMES_DIR}/${themename}_bg_320x480.png" "${THEMES_DIR}/${themename}/background_320x480.png"
    fi

    if [ -f "${themename}_readme.txt" ]; then
        mv "${THEMES_DIR}/${themename}_readme.txt" "${THEMES_DIR}/${themename}/readme.txt"
    fi
done