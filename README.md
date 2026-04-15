# Grant Scraper & Parser

## Overview
This project is a web-based tool that discovers, extracts, and displays grant information from multiple online sources. It focuses on school food service grants and aims to turn unstructured web content into structured, usable data.

## What It Does
Crawls web pages starting from a set of seed URLs
Extracts relevant grant information (e.g., title, amount, eligibility, deadlines)
Ranks results based on completeness and usefulness
Displays the data in a structured table for easy browsing

## How It Works
### 1. Crawler
Starts from predefined seed URLs
Traverses links to discover additional relevant pages
Filters and tracks visited URLs to avoid duplication
### 2. Parser
Fetches and parses HTML content using structured rules and regex
Extracts key fields such as:
Grant title
Funding amount
Eligibility
Timeline
Handles inconsistent page structures and missing data
Assigns a quality score based on available information
### 3. UI
Displays results in a table format
Sorts entries by completeness/usefulness
Includes links to original sources for further details

## Challenges
Inconsistent HTML structures across different websites
Unstructured text parsing, especially for monetary values and deadlines
Identifying relevant links (e.g., “Apply” vs unrelated navigation links)
Balancing data completeness vs coverage when scraping imperfect sources
Performance limitations when crawling multiple sites sequentially
Future Improvements
Improve parsing accuracy for edge cases and unusual formatting (possibly utilizing AI/ML tools)
Optimize crawling speed (e.g., async requests, caching)
Store scraped results in a database for persistence
Add filtering/search functionality in the UI
Track application status or user interactions with grants
Enhance error handling and logging

## Notes
Run this project by running main.py and going to "http://127.0.0.1:5000" to see the resulting table.
