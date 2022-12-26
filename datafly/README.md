# Python Datafly

## Bugs Founded in prof. solutions:
- in line 248 pop inside a for
- occurences and list always inverted??

## Lessons Learned
- always use pandas
- debbuger with args:
insert "args" in .json of the debugger and then start debugging with F5
- using of sets to count unique values is super-efficient
- using a pop into a for can be very risky
- create a debug function, only working if _DEBUG = True

## Usage

Use the `--help` command to show the help message:

```
usage: python3 datafly.py [-h] --private_table PRIVATE_TABLE --quasi_identifier
                  QUASI_IDENTIFIER [QUASI_IDENTIFIER ...]
                  --domain_gen_hierarchies DOMAIN_GEN_HIERARCHIES
                  [DOMAIN_GEN_HIERARCHIES ...] -k K --output OUTPUT

Python implementation of the Datafly algorithm. Finds a k-anonymous
representation of a table.

optional arguments:
  -h, --help            show this help message and exit
  --private_table PRIVATE_TABLE, -pt PRIVATE_TABLE
                        Path to the CSV table to K-anonymize.
  --quasi_identifier QUASI_IDENTIFIER [QUASI_IDENTIFIER ...], -qi QUASI_IDENTIFIER [QUASI_IDENTIFIER ...]
                        Names of the attributes which are Quasi Identifiers.
  --domain_gen_hierarchies DOMAIN_GEN_HIERARCHIES [DOMAIN_GEN_HIERARCHIES ...], -dgh DOMAIN_GEN_HIERARCHIES [DOMAIN_GEN_HIERARCHIES ...]
                        Paths to the generalization files (must have same
                        order as the QI name list.
  -k K                  Value of K.
  --output OUTPUT, -o OUTPUT
                        Path to the output file.
```

#### Domain Generalization Hierarchy file format

For each Quasi Identifier attribute it must be specified a corresponding Domain Generalization Hierarchy, which is used to generalize the attribute values.

Each DGH is specified through a DGH file, which in each line specifies the hierarchy relationship of a value for that attribute. For example, for an attribute `age`, the file could be in this format:

```
...
42,30-45,30-60,1-60,1-120
43,30-45,30-60,1-60,1-120
44,30-45,30-60,1-60,1-120
45,30-45,30-60,1-60,1-120
46,45-60,30-60,1-60,1-120
...
```

As shown above each line specifies for a value not generalized (generalization level 0) its hierarchy relationship in the form `level 0,level 1,level 2,...,level n` (from not-generalized to most generic value).

#### Example of anonymization:

The `./example` folder contains four sample databases (`db_100.csv`,`db_10000.csv`,`db_50000.csv`,`db_100000.csv`), and some Domain Generalization Hierarchy (DGH) files (`age_generalization.csv`, `city_birth_generalization.csv`, `zip_code_generalization.csv`).

The following command will anonymize the table `db_100.csv` writing a new table `db_100_3_anon.csv` which is 3-anonymous (`k = 3`):

```
$ python datafly.py -pt "example/db_100.csv" -qi "age" "city_birth" "zip_code" -dgh "example/age_generalization.csv" "example/city_birth_generalization.csv" "example/zip_code_generalization.csv" -k 3 -o "example/db_100_3_anon.csv"
```

Note that the list of Quasi Identifier names and the corresponding DGH files paths must have the same order.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Credits 

[Alessio Vierti](https://github.com/alessiovierti)
