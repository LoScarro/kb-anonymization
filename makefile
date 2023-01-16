# install requirements
# run main datasets, pt it pf
# stats partial
# stats full


EX = python3
MAIN = main.py
STAT = statistics.py

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
#clean:
#	for number in 0.5 0.9 0.95 0.99 ; do \
#		rm out.txt_$$number ; \
#	done

#usage: 
# for executing and generating graphics: make main dataset='value' bpl='value'
# for generating only graphics: make graphics
# for executing storage: make storage
# for deleting output files: make clean