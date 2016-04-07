all: egpaper_final.pdf
	echo "done"

egpaper_final.pdf: egpaper_final.tex
	xelatex egpaper_final.tex
	open egpaper_final.pdf

.PHONY: clean
clean:
	rm *.aux *.log *.pdf
