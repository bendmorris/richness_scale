fignames=mean_v_var curve_family
figformat=png
dataset=bbs
figures=figures $(patsubst figures/%.$(figformat), \
          figures/$(dataset)_%.$(figformat), \
          $(patsubst %, figures/%.$(figformat), $(fignames)))


.PHONY: all clean show
.PRECIOUS: data/%_env_data.pkl data/%_richness_correlates.pkl

all: $(figures)

clean: 
	rm -rf data/*.pkl figures

data/%.csv: scripts/mk_csv.py data/%.sqlite data/%_query.sql
	python $< $* > $@

figures:
	mkdir figures


data/%_env_data.pkl: scripts/get_env_data.py data/%.csv
	python $< $*
data/%_richness_correlates.pkl: scripts/richness_correlates.py data/%.csv data/%.new data/%_env_data.pkl
	python $< $*

figures/%_mean_v_var.$(figformat): scripts/plot_mean_var.py data/%_richness_correlates.pkl
	python $< $* $@

data/%_group_richness.pkl: scripts/group_richness.py data/bbs.csv data/bbs.new
	python $< $*

figures/%_curve_family.$(figformat): scripts/plot_curve_family.py data/group_richness.pkl
	python $< $* $@