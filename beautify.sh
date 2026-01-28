find . -type f -name "*.tex" -print0 \
  | xargs -0 latexindent -w

echo "LaTeX formatting done."