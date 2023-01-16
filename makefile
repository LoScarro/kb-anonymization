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
#graphics:
#	$(EX) $(GRA)
#
#storage:
#	$(EX) $(STO) configurations/client_server.cfg #--verbose
#
clean:
	@$(foreach datasets,$(DATASETS), \
		rm results/modules_$(datasets).png ; \
	)

	@$(foreach bpl,$(BPL), \
		rm results/$(bpl)_time.png ; \
	)

	rm results/modules.png results/results.txt results/total_time.png results/output_rows.png
#usage: 
# for executing and generating graphics: make main dataset='value' bpl='value'
# for generating only graphics: make graphics
# for executing storage: make storage
# for deleting output files: make clean