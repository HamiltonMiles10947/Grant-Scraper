import re

good_site_keyword_regex = re.compile(r"\b(?:grant|program|school|food|\.gov|student|award|\.edu|equipment|education|nutrition|meal|opportunity|rfp|lunch)s?\b", re.IGNORECASE)
bad_site_keyword_regex = re.compile(r"\.(?:pdf|jpg|jpeg|png|gif|zip|docx?|xlsx?|pptx?)$|login|signin|signup|blog|blogs|privacy|terms|youtube|twitter|instagram|facebook|linkedin", re.IGNORECASE)
money_regex = re.compile(r"\$\d+(?:,\d{3})*(?:\.\d{2})?(?:\s?(?:hundred|thousand|million|k))?")


def filter_urls(url):
    if url and re.search(bad_site_keyword_regex, url):
        return False
    elif url and re.search(good_site_keyword_regex, url):
        return True
    
def filter_grants_list(grant_list):
    for grant in grant_list:
        #check title for not being dumb 
        money_in_title = re.findall(money_regex, grant.title)
        if money_in_title:
            grant.title = re.sub(money_regex, "", grant.title)
            if not grant.amount:
                grant.amount = money_in_title


        if grant.title: grant.score += 3
        if grant.amount: grant.score += 3
        if grant.link: grant.score += 2
        if grant.Requirements: grant.score += 2
        if grant.Description: grant.score += 2
        if grant.open_date: grant.score += 1
        if grant.close_date: grant.score += 1
    
    grant_list.sort(key=lambda g: g.score, reverse=True)
    return grant_list

