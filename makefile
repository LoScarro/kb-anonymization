# install requirements
# run main datasets, pt it pf
# stats partial
# stats full


EX = python3
MAIN = main.py
STAT = statistics.py
MODULE = cg ka pe
DATASETS = 100 500 1000 2000 5000 10000

install:
	pip install -r requirements.txt

main:
	$(EX) $(MAIN) --input_file data/db_$(dataset).csv --bpl $(bpl)

test-partial:
	$(EX) $(STAT) --n_used "100, 500, 1000"

test-full:
	$(EX) $(STAT) --n_used "100, 500, 1000, 2000, 5000, 10000"

clean:
	@$(foreach datasets,$(DATASETS), \
		rm results/modules_$(datasets).png ; \
	)

	@$(foreach module,$(MODULE), \
		rm results/$(module)_time.png ; \
	)

	rm results/modules.png results/results.txt results/total_time.png results/output_rows.png
