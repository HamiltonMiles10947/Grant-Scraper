import json
import requests
import re
import dateparser
from dateutil import parser 
from datetime import datetime
from dataclasses import dataclass
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# from openai import OpenAI
# client = OpenAI()

url = "https://innovateschoolfood.org/other-grant-opportunities/"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    }
response = requests.get(url , headers=headers, timeout=20)


soup = BeautifulSoup(response.text, "html.parser")

money_range_regex = r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*(?:to|-)\s*\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?"
date_info_regex = r"\b(?:open|opens|deadline|closes)\b"

grant_benefits_regex  = re.compile(
    r"\b("
    r"provide(?:s)?|"
    r"grant includes?|"
    r"acquiring|"
    r"assist organizations?|"
    r"offers?|"
    r"aimed at|"
    r"apprenticeship|"
    r"funding can assist|"
    r"support(?:s|ed|ing)?|"
    r"will support|"
    r"available for|"
    r"funding may be used|"
    r"covers? expenses?|"
    r"funding covers?|"
    r"resources?\s+.*include"
    r")\b",
    re.IGNORECASE
)
grant_requirements_regex = re.compile(
    r"\b("
    r"eligible applicants? include|"
    r"applicants? must|"
    r"requirements? include|"
    r"must be|"
    r"restricted to|"
    r"limited to|"
    r"applicants?|"
    r"intended for|"
    r"organizations? must|"
    r"designed for|"
    r"available to|"
    r"open to|"
    r"pre[-\s]?requisite"
    r")\b",
    re.IGNORECASE
)
grant_title_regex = re.compile(r"\b(?:grant|program|challenge|fellowship|partnership|prize|award|fund|initiative|competition|accelerator|scholarship|residency|incubator|project)s?\b", re.IGNORECASE)

grant_list = []


@dataclass
class GrantInfo: 
    title: str | None = None
    amount: str | None = None
    open_date: str | None = None
    close_date: str | None = None
    Requirements: str | None = None
    Description: str | None = None
    link: str | None = None

def parse_link(links):
    for link_title, link in links:
        if link_title:
            break
        # if link_title is something like learn more or sound like a grant
        #     then we good
        # if not then it still might be fine
        # if link leads to something grant related we also good

def check_info_validatiy():
    x = 0
    # make sure that the links title and text all seem to be related somehow
    # maybe give points for shared words and hope it gets a high enough score to signifiy similarity

def create_new_grant_entry(title, info, links):
    parse_link(links)
    check_info_validaty()
    entry = GrantInfo(title = title)
    
    parse_money(info, entry )
    parse_deadline(info, entry)
    parse_description(info, entry)

    grant_list.append(entry)

# not currently used? why?
def get_text_from_page():
    titles = ["h1", "h2", "h3", "h4", "h5", "h6"]
    for header in soup.findAll(titles):
        header_type = header.name
        bibliography = []
        text_entry = []
        if grant_title_regex.search(header):
            # add the header to the list or just do the work
            title = header.text.strip()
            
            # find next paragraph or list. whicever comes first
            distance_from_title = 0
            for next_tag in header.find_next(["p", "ul", "a"]+ titles):
                if distance_from_title >= 4 or next_tag.name in titles:
                    break
                elif(next_tag.name == "p"):
                    text_entry.append(next_tag.get_text())
                elif(next_tag.name == "ul"):
                    for bullet in next_tag.find_all("li"):
                        text_entry.append(bullet.get_text())

                elif(next_tag.name == "a"):
                    link = next_tag.get("href")
                    link_text = next_tag.get_text(strip=True)
                    bibliography.append((link_text, link))
                    # parsed_links = parse_link(link_text, link)
                distance_from_title += 1
            
            final_text = "\n".join(text_entry)
            
            create_new_grant_entry(title, final_text, bibliography) 




            


def print_deadline( date):
    dline = "?"
    
    try: 
        dline = (date.strftime("%B"))
    except:
        dline = (date)
    
    return dline

def parse_deadline(text, entry, ref=None):
    date_patterns = {
        "numeric": re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"),
        "ordinal": re.compile(r"\b\d{1,2}(st|nd|rd|th)\b"), 
        "months": re.compile(r"\b(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|"
        r"jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b", re.IGNORECASE),
        "seasons": re.compile(r"\b(?:early|late)?\s*(winter|spring|summer|fall|autumn)\b", re.IGNORECASE),
    }
    seasons_regex = re.compile(r"\b(?:early|late)?\s*(winter|spring|summer|fall|autumn)\b", re.IGNORECASE)
   
   
    potential_dates = []
    dt = dateparser.parse(text, settings={"PREFER_DATES_FROM": "future"})
    year = datetime.now().year
    
    
    for name, pattern in date_patterns.items():
        for match in pattern.finditer(text):
            potential_dates.append((match.group(), match.start(), match.end()))

    parsed_dates = [] 
    for date, start, end in potential_dates:
        snippet = text[max(0, start-40):min(len(text),end+1)]
        label = " "

        info_match = re.search(date_info_regex, snippet)
        if info_match:
            word = info_match.group().lower()
            if word in ("open", "opens"):
                label = "Opens"
            elif word in ("deadline", "closes"):
                label = "Deadline"
            # elif word in ("from"):
            #     # there is the open and deadline>
            #     continue

        try:
            # time_marker = date.split()[0]
            season_match = re.search(seasons_regex, date)
            # print("Seasons are listed here: " + season_match)
            if season_match:
                # the_date = time_marker + " " + season_match.group()
                parsed_dates.append((season_match.group().title(), label))
                # print("___________________"+ x)

            else:
                # the_date = time_marker + " " + parser.parse(date, fuzzy=True)
                parsed_dates.append((parser.parse(date, fuzzy=True), label))
        except:
            pass
    
    x = 1  
    
    for dt, label in parsed_dates:
        if label == " " and x == 1:
            label = "Opens"  
        elif label == " " and x == 2:
            label = "Deadline"            

        if label == "Deadline":
            if entry.close_date:
                entry.close_date = entry.close_date + " to " + print_deadline(dt)
                # multiple_closings = True
            else:
                entry.close_date = print_deadline(dt)
        elif label == "Opens":
            if entry.open_date:
                entry.open_date = entry.open_date +" to "+ print_deadline(dt)
                # multiple_openings = True
            else:
                entry.open_date = print_deadline(dt)
        
        deadline = print_deadline( dt)
        print(label, ":", deadline)
        
        x += 1


def parse_money(text, entry):
   range_values = re.findall(money_range_regex, text)
   
   if range_values:
       money = range_values
   else:
       money =  re.findall(r"\$\d+(?:,\d{3})*(?:\.\d{2})?", text)
   
   print("Amount", money)
   entry.amount = money

def parse_description(text, entry):
    benefits = ""
    requirements = ""
    benefitsL = []
    requirementsL = []
    sentences = re.split(r'(?<!\b[A-Z])(\. )(?=[A-Z])', text)
    for sentence in sentences: #text.split(". "):
        if grant_benefits_regex.search(sentence):
        #    print("offered", sentence.strip(),"\n")
           benefitsL.append((sentence.strip() + "\n"))

        if grant_requirements_regex.search(sentence):
            # print("Eligibility:", sentence.strip()+ "\n")
            requirementsL.append((sentence.strip()+ "\n"))
    
    if benefitsL:
        benefits =  "\n".join(benefitsL)
    if requirementsL:
        requirements =  "\n".join(requirementsL)

    entry.Description = benefits
    entry.Requirements = requirements

@app.route("/")
def index():
    return render_template("home.html")


@app.route("/api/data")
def get_data():
    print("Headers _-----------------------------")
    grant_list = []

    # get_text_from_page()

    for header in soup.find_all("h2"):
        title = header.text.strip()
        print(title)
        
        entry = GrantInfo(title=title)        

        next_p = header.find_next_sibling("p")
        if next_p:
            # print( next_p.get_text(strip=True))
            info = next_p.get_text()
            
            parse_money(info, entry )
            parse_deadline(info, entry)
            parse_description(info, entry)

            grant_list.append(entry)
        else:
            print("no P")
        
        next_a = header.find_next("a")
        if next_a: 
            link = next_a.get("href")
            link_text = next_a.get_text(strip=True)
            entry.link = link
            print(link_text + " " + link)
        else: 
            print("no a")
        

    return jsonify(grant_list)

if __name__ == "__main__":
    app.run(debug=True)

# @app.route("/extract", methods=["POST"])
# def extract():
#     text = request.json.get("text", "")
#     results = []

# get_data()
# it
# cybersecurity 
# software engineering 
# hardware engineer 
# UI/UX 
# Web design 
# Data analysis 
# create AI 
# signals company in utah working on ai with the uninitiatied