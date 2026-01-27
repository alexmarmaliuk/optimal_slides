#!/usr/bin/env bash
set -euo pipefail

# Clean LaTeX build artifacts recursively
find . -type f \( \
    -name "*.aux"   \
    -o -name "*.bbl"   \
    -o -name "*.bcf"   \
    -o -name "*.blg"   \
    -o -name "*.fdb_latexmk" \
    -o -name "*.fls"   \
    -o -name "*.log"   \
    -o -name "*.nav"   \
    -o -name "*.out"   \
    -o -name "*.pdfpc" \
    -o -name "*.run.xml" \
    -o -name "*.snm"   \
    -o -name "*.toc"   \
    -o -name "*.gz" \
\) -delete

echo "LaTeX junk cleaned."