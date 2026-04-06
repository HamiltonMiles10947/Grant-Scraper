##################################################
# CONFIGURATION / CONSTANTS
##################################################

# Define seed URLs (trusted starting points)
# Example: government, education, nonprofit sites
SEED_URLS = [
    # "https://example.gov/grants",
]

# Maximum number of pages to crawl
MAX_PAGES = 100

# Optional: maximum crawl depth
MAX_DEPTH = 2

# Delay between requests (seconds) to avoid being blocked
REQUEST_DELAY = 1

# Keywords for quick relevance filtering
RELEVANT_KEYWORDS = [
    # "grant", "funding", "application", etc.
]


##################################################
# MAIN ENTRY POINT
##################################################

def main():
    """
    Entry point of the program.

    Responsibilities:
    - Initialize crawler state (frontier, seen sets, etc.)
    - Start crawl loop
    - Optionally handle final reporting / cleanup
    """
    pass


##################################################
# CRAWLER CORE LOGIC
##################################################

def crawl(seed_urls):
    """
    Core crawl loop.

    Responsibilities:
    - Maintain URL frontier (queue)
    - Track seen URLs to avoid duplicates
    - Enforce limits (MAX_PAGES, MAX_DEPTH)
    - Coordinate fetching, parsing, and link extraction

    Flow:
    1. Initialize frontier with seed URLs
    2. While frontier not empty and under MAX_PAGES:
        a. Get next URL
        b. Check if already seen
        c. Fetch HTML
        d. Run relevance check
        e. If relevant → run full parser + store result
        f. Extract links
        g. Filter links
        h. Add new links to frontier
    """
    pass


##################################################
# FETCHING / DOWNLOADING
##################################################

def fetch_page(url):
    """
    Download HTML content for a given URL.

    Responsibilities:
    - Make HTTP request (requests.get)
    - Handle timeouts and errors
    - Return raw HTML text (or None if failed)

    Future improvements:
    - Retry logic
    - User-agent headers
    - Playwright fallback for dynamic pages
    """
    pass


##################################################
# RELEVANCE FILTER (LIGHTWEIGHT)
##################################################

def is_relevant(html):
    """
    Quick check to determine if a page is worth parsing.

    Responsibilities:
    - Look for presence of key terms (RELEVANT_KEYWORDS)
    - Be fast and simple (avoid heavy parsing)

    Purpose:
    - Prevent wasting time on irrelevant pages
    """
    pass


##################################################
# FULL CONTENT PARSER (YOUR MAIN LOGIC)
##################################################

def parse_grant_page(html, url):
    """
    Extract structured grant information from a page.

    Responsibilities:
    - Extract fields like:
        - title
        - description
        - eligibility
        - deadline
        - funding amount
    - Return structured data (dict or object)

    Notes:
    - This is your "heavy" parser
    - Only called if page passes relevance check
    """
    pass


##################################################
# DATA STORAGE
##################################################

def store_result(data):
    """
    Store parsed grant data.

    Responsibilities:
    - Save to CSV, JSON, or database
    - Handle missing/partial data gracefully

    Important:
    - Should write incrementally (not all at end)
    """
    pass


##################################################
# LINK EXTRACTION
##################################################

def extract_links(html, base_url):
    """
    Extract all links from a page.

    Responsibilities:
    - Parse <a> tags
    - Convert relative URLs → absolute URLs
    - Return list of URLs

    Notes:
    - Does NOT filter links (that happens later)
    """
    pass


##################################################
# URL FILTERING
##################################################

def is_valid_url(url):
    """
    Determine whether a URL should be crawled.

    Responsibilities:
    - Filter out:
        - Non-HTML resources (pdf, images, zip, etc.)
        - Social media / irrelevant domains
    - Optionally enforce domain restrictions
    - Optionally check for relevant keywords in URL

    Purpose:
    - Keep crawler focused and efficient
    """
    pass


##################################################
# URL NORMALIZATION
##################################################

def normalize_url(url):
    """
    Normalize URLs to avoid duplicates.

    Responsibilities:
    - Remove fragments (#section)
    - Standardize trailing slashes
    - Optionally remove query parameters

    Purpose:
    - Prevent duplicate crawling of same page
    """
    pass


##################################################
# OPTIONAL: CONTENT DEDUPLICATION
##################################################

def is_duplicate_content(html):
    """
    Detect duplicate page content.

    Responsibi
