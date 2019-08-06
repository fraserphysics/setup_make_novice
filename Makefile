SHELL=/bin/bash

TXT_FILES=$(addprefix books/, abyss.txt isles.txt last.txt sierra.txt)
DAT_FILES=$(patsubst books/%.txt, %.dat, $(TXT_FILES))
PLOT_FILES=$(patsubst books/%.txt, %.pdf, $(TXT_FILES))
RESULTS=$(PLOT_FILES) results.tex file_list.tex abyss.head

## all           : The default target is report.pdf
.PHONY : all
all : report.pdf

## results.tex   : Make a Zipf summary table in LaTeX format.
results.tex : $(DAT_FILES) testzipf.py
	python testzipf.py --latex $(DAT_FILES) > $@

# EG makes abyss.dat from books/abyss.txt
%.dat : books/%.txt countwords.py
	python countwords.py $< $*.dat

# EG makes abyss.pdf from abyss.dat
%.pdf : %.dat plotcounts.py
	python plotcounts.py $*.dat $*.pdf

## file_list.tex : Make a list of files under version control, ie, source files
file_list.tex:
	echo -e "\\\begin{verbatim}\n$$ git ls-files" > $@
	git ls-files >> $@
	echo "\end{verbatim}" >> $@

# Print the first two fields of the first ten lines of %dat
%.head : %.dat
	head $< |awk '{print $$1, $$2}' > $@

## report.pdf    : Build the pdf document
report.pdf: local.bib report.tex $(RESULTS)
	pdflatex report
	bibtex report
	pdflatex report
	pdflatex report
report.aux: report.tex $(RESULTS)
	pdflatex report

## report.bbl    : Build the bibliography for the report
report.bbl: local.bib report.aux
	bibtex report

## clean         : Remove the auto-generated files.
.PHONY : clean
clean :
	rm -f *.head *.pdf *.dat results.txt
	rm -rf __pycache__
	rm -f report.aux report.blg report.bbl report.log file_list.tex results.tex

## variables     : Print selected variables.
.PHONY : variables
variables:
	@echo TXT_FILES: $(TXT_FILES)
	@echo DAT_FILES: $(DAT_FILES)
	@echo PLOT_FILES: $(PLOT_FILES)

.PHONY : help
help : Makefile
	@sed -n 's/^##//p' $<
