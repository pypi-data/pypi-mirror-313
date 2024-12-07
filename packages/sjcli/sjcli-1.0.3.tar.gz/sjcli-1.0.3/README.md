## Running Test
python -m unittest discover -s tests -p '*_test.py' -v
python -m unittest tests/utils_helpers_test.py -v

poetry shell
poetry install
pip install --editable .

mkdir package
cd package
poetry init
poetry add click
poetry add tabulate
poetry add duckdb

poetry version 1.0.0