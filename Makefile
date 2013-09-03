fignames=mean_v_var.svg
figures=$(patsubst %, figures/%, $(fignames))


.PHONY: all clean show

all: $(figures)

clean: 
	rm -f data/*.pkl figures/*.svg

show: all
	eog figures/mean_v_var.svg

data/bbs.csv: scripts/mk_csv.py data/bbs.sqlite data/bbs_query.sql
	python $< > $@

data/richness_correlates.pkl: scripts/richness_correlates.py data/bbs.csv data/bbs.new data/env_data.csv
	python $<

figures:
	mkdir figures

figures/mean_v_var.svg: scripts/plot.py data/richness_correlates.pkl
	python $< $@