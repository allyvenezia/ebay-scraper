# Ebay Scraper

Ebay-dl.py is a python program that scrapes the first 10 pages of a Ebay 
given a specific search term and extracts specific details using Beautiful Soup. 

The project used practice pages, not real Ebay data (since Ebay blocks live requests). 
The exact commands that I ran are:
python ebay-dl.py --search "garden tools" --pages-dir practice-pages
python ebay-dl.py --search "drill press" --pages-dir practice-pages
python ebay-dl.py --search "stuffed animal" --pages-dir practice-pages


For each listing, the code records name price (as an integer), the item's condition, a Boolean value 
of if the item has free returns or not, and how many of the items have been sold. 

# Project 

This project was created for CSCI40 at Claremont McKenna College, 
https://csci40.rtealwitter.com/projects/02_webscraping/project.html 