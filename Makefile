fignames=mean_v_var curve_family
figformat=png
figures=figures $(patsubst %, figures/%.$(figformat), $(fignames))


.PHONY: all clean show

all: $(figures)

clean: 
	rm -f data/*.pkl figures/*.svg

show: all
	eog figures/mean_v_var.svg

data/bbs.csv: scripts/mk_csv.py data/bbs.sqlite data/bbs_query.sql
	python $< > $@

figures:
	mkdir figures


data/richness_correlates.pkl: scripts/richness_correlates.py data/bbs.csv data/bbs.new data/env_data.csv
	python $<

figures/mean_v_var.%: scripts/plot_mean_var.py data/richness_correlates.pkl
	python $< $@


data/group_richness.pkl: scripts/group_richness.py data/bbs.csv data/bbs.new
	python $<

figures/curve_family.%: scripts/plot_curve_family.py data/group_richness.pkl
	python $< $@