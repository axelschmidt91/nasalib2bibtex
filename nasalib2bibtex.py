import requests
import json
import os


def get_results(query):

    url_search = r"https://ntrs.nasa.gov/api/citations/search"
    
    max_data_per_page = 100

    counter_for_recieved_results = 0

    results = []

    while True:

        data = {
            "page": {
            "size": max_data_per_page,
            "from": counter_for_recieved_results
            },
            "q": query,
        }
        r = requests.post(url_search, json=data)

        data = r.json()

        # print some stats
        log.debug(str(data.keys()))
        log.debug(data['stats'])

        # print the number of elements in data['results']
        log.debug("num of results in response: " + str(len(data['results'])))

        # add the number of elements in data['results'] to the counter
        counter_for_recieved_results += len(data['results'])

        # print the counter
        log.debug("counter: " + str(counter_for_recieved_results))

        # add the results to the results list
        results += data['results']

        # if the counter is equal to the total number of results, break the loop
        if counter_for_recieved_results == data['stats']['total']:
            break

    # save results to json file with tab indentation
    data_filename = "data.json"
    log.info("Saving API results to file: " + data_filename)
    with open(data_filename, 'w') as outfile:
        json.dump(results, outfile, indent=4)

    # print the number of results
    log.info("total number of results: " + str(len(results)))

    return results


def authors(result):
    authors_list = []
    for author in result['authorAffiliations']:
        author_str = author['meta']['author']['name']
        # if key organization exists and is not empty, add it to the author string
        if 'organization' in author['meta'] and author['meta']['organization'] != {}:
            author_str += " ("
            
            try:
                author_str += author['meta']['organization']['name'] 
            except:
                pass
            
            try:
                author_str += ", " + author['meta']['organization']['location']
            except:
                pass
            author_str += ")"

        authors_list.append(author_str)

    # convert list to string with comma as separator and return
    return '; '.join(authors_list)

def date_string(result):


    # get the first publication date if the key 'publications' and 'publicationDate' exists
    if 'publications' in result:
        if 'publicationDate' in result['publications'][0]:
            date = result['publications'][0]['publicationDate']
        # else get the "submittedDate"
        else:
            date = result['submittedDate']
    # else get the "submittedDate"
    else:
        date = result['submittedDate']
    
    return date

def year(result):
    date = date_string(result)
    
    year = date.split('-')[0]
    return year

def month(result):
    date = date_string(result)
    
    month = date.split('-')[1]
    if month == '01':
        return 'January'
    elif month == '02':
        return 'February'
    elif month == '03':
        return 'March'
    elif month == '04':
        return 'April'
    elif month == '05':
        return 'May'
    elif month == '06':
        return 'June'
    elif month == '07':
        return 'July'
    elif month == '08':
        return 'August'
    elif month == '09':
        return 'September'
    elif month == '10':
        return 'October'
    elif month == '11':
        return 'November'
    elif month == '12':
        return 'December'
    else:
        return ''


def categories(result):

    categories_list = result['subjectCategories']

    # convert list to string with comma as separator and return
    return '; '.join(categories_list)

def keywords(result):

    keywords_list = result['keywords']

    # convert list to string with comma as separator and return
    return '; '.join(keywords_list)
        

def abstract(result):
    abstract_str = result['abstract']

    # dict of unicode characters to replace and their replacement
    unicode_dict = {
        "\u02d9": "ff",
        "\u2212": "-",
        "\u0398": "Theta"
    }

    # replace unicode characters
    for unicode_char in unicode_dict:
        abstract_str = abstract_str.replace(unicode_char, unicode_dict[unicode_char])
    
    return abstract_str

def reportNumber(result):
    reportNumber_list = result['otherReportNumbers']

    # convert list to string with semicolon as separator and return
    return '; '.join(reportNumber_list)


def write_results(results):

    url = r"https://ntrs.nasa.gov"

    # load stiTypes assigned to bibtex types from stiTypes_assigned.json
    with open('stiTypes_assigned.json') as json_file:
        stiTypes_assigned = json.load(json_file)

    # write the results to a bibtec file
    output_filename = 'data.bib'
    log.info("Writing results to file: " + output_filename)
    with open(output_filename, 'w') as outfile:
        for result in results:
            # print ID and title of the result
            log.debug("ID: " + str(result['id']) + " - Title: " + result['title'])

            # the bibtex type is the stiType of the result if it is in stiTypes_assigned
            if result['stiType'] in stiTypes_assigned:
                bibtex_type = stiTypes_assigned[result['stiType']]
            # otherwise the bibtex type is 'misc'
            else:
                bibtex_type = 'misc'

            # write the bibtex type and the id of the result to the file
            outfile.write('@' + bibtex_type + '{' + str(result['id']) + ',\n')

            # write the title of the result to the file
            outfile.write('\ttitle = "' + result['title'] + '",\n')

            # write the authors of the result to the file if the key 'authorAffiliations' exists
            if 'authorAffiliations' in result:
                outfile.write('\tauthor = "' + authors(result) + '",\n')

            # write the year of the result to the file
            outfile.write('\tyear = "' + str(year(result)) + '",\n')

            # write the month of the result to the file
            outfile.write('\tmonth = "' + str(month(result)) + '",\n')

            # write the url of the result to the file if key downloads exists and is not empty list
            if 'downloads' in result and result['downloads']:
                outfile.write('\turl = "' + url + result['downloads'][0]['links']['original'] + '",\n')

            # write the abstract of the result to the file if key abstract exists
            if 'abstract' in result:
                outfile.write('\tabstract = "' + abstract(result) + '",\n')

            # write the keywords of the result to the file if the key exists
            if 'keywords' in result:
                outfile.write('\tkeywords = "' + keywords(result) + '",\n')

            # write the categories of the result to the file if the key exists
            if 'subjectCategories' in result:
                outfile.write('\tcategories = "' + categories(result) + '",\n')

            # write the DocumentType of the result to the file if the key exists
            if 'stiTypeDetails' in result:
                outfile.write('\tdocumentType = "' + result['stiTypeDetails'] + '",\n')

            # write the DOI of the result to the file if the key exists and is not empty
            if 'sourceIdentifiers' in result and result['sourceIdentifiers']:
                if 'doi' in result['sourceIdentifiers'][0]['number'] or 'DOI' in result['sourceIdentifiers'][0]['type']:
                    outfile.write('\tdoi = "' + result['sourceIdentifiers'][0]['number'] + '",\n')

            # write booktitle of the result to the file if the bibtex type is 'inbook'
            if bibtex_type == 'inbook':
                outfile.write('\tbooktitle = "' + result['publications'][0]['publicationName'] + '",\n')
            elif bibtex_type == 'inproceedings' or bibtex_type == 'conference':
                if 'meetings' in result:
                    outfile.write('\tbooktitle = "' + result['meetings'][0]['name'] + '",\n')
                elif 'publications' in result:
                    if 'publicationName' in result['publications'][0]:
                        outfile.write('\tbooktitle = "' + result['publications'][0]['publicationName'] + '",\n')
            
            # write the publisher of the result to the file if the key exists
            if 'publications' in result:
                if 'publisher' in result['publications'][0]:
                    outfile.write('\tpublisher = "' + result['publications'][0]['publisher'] + '",\n')
                elif 'meetings' in result:
                    if 'sponsor' in result['meetings'][0]:
                        outfile.write('\tpublisher = "' + result['meetings'][0]['sponsors'][0]['meta']['organization']['name'] + '",\n')
            elif 'meetings' in result:
                if 'sponsor' in result['meetings'][0]:
                    outfile.write('\tpublisher = "' + result['meetings'][0]['sponsors'][0]['meta']['organization']['name'] + '",\n')
                
            # write the address of the result to the file if the key exists
            if 'meetings' in result:
                if 'location' in result['meetings'][0]:
                    outfile.write('\taddress = "' + result['meetings'][0]['location'] + '",\n')

            # write the report number if bibtype is 'techreport'
            if bibtex_type == 'techreport':
                outfile.write('\tnumber = "' + reportNumber(result) + '",\n')

            
            # strip the last comma and newline from the file
            outfile.seek(outfile.tell() - 2, os.SEEK_SET)
            outfile.truncate()

            # write closing bracket to the file
            outfile.write('\n}\n\n')


def main(query):
    # get the results from the API
    log.info("Getting results from API")
    results = get_results(query)

    # write the results to a bibtec file
    write_results(results)

if __name__ == "__main__":

    import logging

    # dir(logging)

    # Create and configure logger
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename = "console.log",
                        level = logging.INFO,
                        format = LOG_FORMAT,
                        # filemode = 'w',       # 'w' Override logfile every time, 'a' append the messages
                        filemode = 'a')         
    log = logging.getLogger()

    search_query = '(3d|"3 d"|"3-d"|three*dimension|3*dimension)+("woven"|weav*)+(“textile”|fib*|”composite”|”component|”plastic”)+(torsi*|bend*|mechanic*|compres*|tensi*|flex*|impact)+( stress|load*|force*|strain|propert*|failure|fatique|damage)+(“z-“|orthogonal|angle|interlock)-(nonwoven|print*|*bio*|therm*|concrete)'

    import argparse
    # cml tool nasalib2bib
    parser = argparse.ArgumentParser(description='Requests literature from a query send to NASAs NTRS database and exports the results to a bibtex file.')
    parser.add_argument('query', help='The query to be used.')
    
    # add logging level
    parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')

    args = parser.parse_args()

    if args.verbose:
        log.info("Verbose mode on")
        log.setLevel(logging.DEBUG)

    log.info("Starting nasalib2bib")
    log.info("Query: " + args.query)

    main(args.query)

    log.info("Finished nasalib2bib")