#!/bin/bash
cd "$(dirname "$0")/.."
echo "Open http://localhost:8080/dicom-viewer/ in your browser"
echo "Or embed in Gamma: http://localhost:8080/dicom-viewer/"
python3 -m http.server 8080
