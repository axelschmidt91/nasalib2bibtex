# nasalib2bibtex

This command line tool performs an API request on the given query at the NASA NTRS website https://ntrs.nasa.gov/search and saves the results as a bibtex file.

## Usage

The converter help can be viewed by typing the following:
```
python nasalib2bibtex.py -h
```

The required arguments is the query to be searched for. If there are any spaces in the query the string needs to be set between abostrophes  `'`. For example: `'NACA foil'` 

## Sources

NASA NTRS Search
https://ntrs.nasa.gov/search

NASA NTRS API Swagger
https://ntrs.nasa.gov/api/openapi/#/

bibtex Entry Types:
https://www.bibtex.com/e/entry-types/

bibtex Fields:
https://www.openoffice.org/bibliographic/bibtex-defs.html
