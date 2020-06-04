# pip install datetime beautifulsoup4 requests -t ./ --upgrade

from covid19scraper import scrapeGlobalCase
testResults = scrapeGlobalCase()
print(testResults)
