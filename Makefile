all: proposal.pdf
	echo "done"

proposal.pdf: proposal.tex
	xelatex proposal.tex
	bibtex proposal
	xelatex proposal.tex && open proposal.pdf

.PHONY: clean
clean:
	rm *.aux *.log *.pdf
