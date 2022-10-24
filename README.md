# nasalib2bibtex

This command line tool performs an API request on the given query at the NASA NTRS website https://ntrs.nasa.gov/search and saves the results as a bibtex file.

## Installation for Python

_python_ is used for this tool.

To install the relevant packages run:
```sh
pip install -r requirement.txt
``` 

## Usage

The converter help can be viewed by typing the following:
```sh
python nasalib2bibtex.py -h
```

The required arguments is the query to be searched for. If there are any spaces in the query the string needs to be set between abostrophes  `'`. For example: `'NACA foil'` 

The bibtex entries will be written to `data.bib`.

## Logging
The logfile `console.log` will be written.

## Standalone Usage

For Windows download the corresponding release files and open a terminal/cml in the located folder and run:
```sh
nasalib2bibtex -h
```
For Linux download the corresponding release files and open a terminal in the located folder and run:
```sh
./nasalib2bibtex -h
```


## Sources

NASA NTRS Search
https://ntrs.nasa.gov/search

NASA NTRS API Swagger
https://ntrs.nasa.gov/api/openapi/#/

bibtex Entry Types:
https://www.bibtex.com/e/entry-types/

bibtex Fields:
https://www.openoffice.org/bibliographic/bibtex-defs.html
