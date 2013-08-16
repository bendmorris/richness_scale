all: mean_v_var.png

show: all
	eog mean_v_var.png

bbs.csv: bbs.sqlite bbs_query.sql
	python mk_csv.py > bbs.csv

richness_correlates.pkl: richness_correlates.py bbs.csv bbs.new env_data.csv
	python $<

mean_v_var.png: plot.py richness_correlates.pkl
	python $< $@