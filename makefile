# install requirements
# run main datasets, pt it pf
# stats partial
# stats full


EX = python3
MAIN = main.py
STAT = statistics.py
BPL = cg ka pe
DATASETS = 100 500 1000 2000 5000 10000

install:
	pip install -r requirements.txt

main:
	$(EX) $(MAIN) --input_file data/db_$(dataset).csv --bpl $(bpl)

partial:
	$(EX) $(STAT) --n_used "100, 500, 1000"

full:
	$(EX) $(STAT) --n_used "100, 500, 1000, 2000, 5000, 10000"

clean:
	@$(foreach datasets,$(DATASETS), \
		rm results/modules_$(datasets).png ; \
	)

	@$(foreach bpl,$(BPL), \
		rm results/$(bpl)_time.png ; \
	)

	rm results/modules.png results/results.txt results/total_time.png results/output_rows.png
# usage: 
# for install dependecies: make install
# for executing main: make main dataset='value' bpl='value'
# for executing statistics on few datasets: make partial
# for executing statistics on all datasets: make full
# for deleting output files: make clean