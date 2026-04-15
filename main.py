import re
from flask import Flask, request, jsonify, render_template
from collections import deque
import filters, fetcher, parser

app = Flask(__name__)
MAX_COUNTER = 10

@app.route("/")
def index():
    return render_template("home.html")

Urls = []

@app.route("/api/data")
def main():
    print("Headers _-----------------------------")
    grant_list = []
    
    # get Url
    seeds = [
            "https://schoolnutrition.org/snf/equipment-grants/",
            "https://innovateschoolfood.org/other-grant-opportunities/",
            "https://www.fns.usda.gov/cn/support-schools",
            "https://education.vermont.gov/student-support/nutrition/school-meals/Grant-Opportunities",
            ]
    Urls = deque(seeds)
    
    # make sure its relevant 
        # look for keywords in the url
        # look for trusted site .edu/.gov
        # look to see if its a pdf or jpg because those are different
    max_site_counter = 0
    # for url in Urls[:]: #make a copy so you don't skip any elements in list
    seen = set()
    grants_seen = set()
    while Urls: 
        print(max_site_counter)
        url = Urls.popleft()   

        if url in seen:
            continue
        seen.add(url)

        if max_site_counter >= MAX_COUNTER:
            break
        max_site_counter +=1

        if filters.filter_urls(url):
            # download and get info
                # fetcher
            site = fetcher.fetch_site(url)
            # Make sure page is on topic
            if not parser.check_page_validatiy(site):
                continue
            #parse
                # run it through requester.py to get information for table
            parsed_site_info = parser.parse(site, url)
            if parsed_site_info:
                for grant in parsed_site_info:
                    if grant.title not in grants_seen:
                        grant_list.append(grant)
                        grants_seen.add(grant.title)
            #get other URLs from page
                # extract other Urls from page and add them to site
            
            new_urls = parser.extract_urls(site)
            if new_urls:
                for new_url in new_urls:
                    if new_url not in seen:
                        Urls.append(new_url)


            #loop again 
        # else:
        #     Urls.remove(url)

    # print(max_site_counter)
    grant_list = filters.filter_grants_list(grant_list)
    return jsonify(grant_list)

if __name__ == "__main__":
    app.run(debug=True)
