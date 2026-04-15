import re
import dateparser
from dateutil import parser 
from datetime import datetime
from dataclasses import dataclass
from bs4 import BeautifulSoup

@dataclass
class GrantInfo: 
    title: str | None = None
    amount: str | None = None
    open_date: str | None = None
    close_date: str | None = None
    Requirements: str | None = None
    Requirements_length: int | None = None
    Description: str | None = None
    Description_length: int | None = None
    link: str | None = None
    score: int | None = None

money_range_regex = r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s*(?:to|-)\s*\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?"
money_value_regex = r"\$\d+(?:,\d{3})*(?:\.\d{2})?(?:\s?(?:hundred|thousand|million|k))?"
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
    r"eligibility|"
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
useful_url_regex = re.compile(r"\b(?:learn more|more info(?:rmation)?|details|view details|full details|eligibility|program info|grant info|application form|download application|request for proposals|rfp|nofo|read more|view more|see more)\b")

def check_page_validatiy(site):
    if not site:
        return False
    else:
        return True

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
            # ##print"Seasons are listed here: " + season_match)
            if season_match:
                # the_date = time_marker + " " + season_match.group()
                parsed_dates.append((season_match.group().title(), label))
                # ##print"___________________"+ x)

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

        current_deadline = print_deadline(dt)

        if label == "Deadline":
            if entry.close_date:
                entry.close_date = entry.close_date + " to " + current_deadline
                # multiple_closings = True
            else:
                entry.close_date = current_deadline
        elif label == "Opens":
            if entry.open_date and entry.open_date != current_deadline:
                entry.open_date = entry.open_date +" to "+ current_deadline
                # multiple_openings = True
            else:
                entry.open_date = current_deadline
        
        deadline = current_deadline
        ##printlabel, ":", deadline)
        
        x += 1


def parse_money(text, entry):
   ##print"checking " + text)
   range_values = re.findall(money_range_regex, text)
   
   if range_values:
       money = range_values
   else:
       money =  re.findall(money_value_regex, text)

   
   ##print"Amount", money)
   if money and not entry.amount:
       entry.amount = money

def parse_description(text, entry):
    benefits = ""
    requirements = ""
    benefitsL = []
    requirementsL = []
    sentences = re.split(r'(?<!\b[A-Z])(\. )(?=[A-Z])', text)


    for sentence in sentences: #text.split(". "):
        if grant_benefits_regex.search(sentence):
        #    ##print"offered", sentence.strip(),"\n")
           benefitsL.append((sentence.strip() + "\n"))

        if grant_requirements_regex.search(sentence):
            # ##print"Eligibility:", sentence.strip()+ "\n")
            requirementsL.append((sentence.strip()+ "\n"))
    

    if benefitsL:
        benefits =  "\n".join(benefitsL)
    if requirementsL:
        requirements =  "\n".join(requirementsL)
    
    if benefits:
        if not entry.Description:
            entry.Description = benefits
        elif entry.Description_length <= 5:
            entry.Description = entry.Description + benefits
        entry.Description_length += 1
    
    if requirements:
        if not entry.Requirements:
            entry.Requirements = requirements
        elif entry.Requirements_length <= 5:
            entry.Requirements = entry.Requirements + requirements
        entry.Requirements_length +=1

        

def parse(site, source_url):
   grant_list = []
   titles = ["h1", "h2", "h3"]
       
   for header in site.find_all(titles):
        title = header.text.strip()
        ##printtitle)
        if not re.search(grant_title_regex, title) or ("?" in title):
            continue

        entry = GrantInfo(title=title, Description_length=0, Requirements_length=0, link=source_url, score=0)        

        current = header.find_next_sibling()
        

        while current:
            if current.name in titles:
                break
            if current.name == "p":
                
                if current:
                    # ##print next_p.get_text(strip=True))
                    info = current.get_text()
                    
                    parse_money(info, entry)
                    parse_deadline(info, entry)
                    parse_description(info, entry)

                    if entry.title:
                        grant_list.append(entry)
                
                next_a = header.find_next("a")
                if next_a: 
                    link = next_a.get("href")
                    link_text = next_a.get_text(strip=True)
                    link_text = re.search(useful_url_regex, link_text)
                    if link and link_text:
                        print("link: " + link)
                        # print("link text: " + link_text)
                        entry.link = link
                    
            current = current.find_next_sibling()
            
   return grant_list

def extract_urls(site):
    extracted_urls = []
    links = site.find_all("a")
    # ##print"========================found Links=========================")
    for link in links:
        # ##printlink)
        extracted_urls.append(link.get("href"))
    # ##print"=================================================")
    return extracted_urls

