#Gets list of all stocks in the S&P500

#!/usr/bin/python
# -*- coding: utf-8 -*-

import lxml.html

def obtain_parse_wiki_snp500():

# Use libxml to download the list of S&P500Â£ companies and obtain the symbol table
	page = lxml.html.parse("http://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
	symbolslist = page.xpath("//table[1]/tr")[1:502]
# Obtain the symbol information for each
# row in the S&P500 constituent table
	symbols = []
	for i, symbol in enumerate(symbolslist):
		tds = symbol.getchildren()
		sd = {"ticker": tds[0].getchildren()[0].text,"name": tds[2].getchildren()[0].text,"sector": tds[3].text}
# Create a tuple (for the DB format) and append to the grand list
		symbols.append((sd["ticker"],sd["sector"]) )
	return symbols

if __name__ == "__main__":
    symbols = obtain_parse_wiki_snp500()
    print symbols
    print len(symbols)