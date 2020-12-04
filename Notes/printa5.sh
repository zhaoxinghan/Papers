file_input=$1

pandoc --pdf-engine=xelatex --template=/Users/zhaoxinghan/GitHub/LaTeX-Workshop/template.latex $file_input -o forprint.pdf