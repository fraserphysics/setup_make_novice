include config.mk

TXT_FILES=$(wildcard books/*.txt) books/gray.txt
DAT_FILES=$(patsubst books/%.txt, %.dat, $(TXT_FILES))

# Generate summary table.
results.txt : $(ZIPF_SRC) $(DAT_FILES)
	$(ZIPF_EXE) $(DAT_FILES) > $@

# Count words.
.PHONY : dats
dats : $(DAT_FILES)

%.dat : books/%.txt $(COUNT_SRC)
	$(COUNT_EXE) $< $@

books/gray.txt:
	wget -O - https://www.gutenberg.org/ebooks/174.txt.utf-8 \
|tail +37|head -n -370 >$@

.PHONY : clean
clean :
	rm -f $(DAT_FILES)
	rm -f results.txt
	rm -f books/gray.txt

.PHONY : variables
variables:
	@echo TXT_FILES: $(TXT_FILES)
	@echo DAT_FILES: $(DAT_FILES)
