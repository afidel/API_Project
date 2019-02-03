# API_Project
This project gets article data from The Guardian and New York Times APIs and puts that data into a csv table.
The program will search for an exact match of a phrase in the two APIs and return articles that include that phrase.
Data from those articles will populate a CSV.

ACCOMPANYING FILES

SI506F18_final_project.py
cache_file_name.json
SAMPLEarticle_data.csv

HOW TO RUN IT

Run the file as is to return a search about the topic of digital advertising fraud.
If you would like to search the APIs for some other phrase, assign a new value to the variable SEARCH_TERM on line 6.
This will run an exact phrase match search for your newly updated variable.
No other stpes are needed. Your CSV will output after running.

WHAT SHOULD OUTPUT

A CSV should output with the column headers, ARTICLE_TITLE,	AUTHOR,	SECTION,	NUMBER_OF_WORDS_IN_TITLE,	PUBLICATION,	URL,	and KEYWORDS.
The rows below should be filled with data from New York Times and The Guardian articles.

INTERACTIVITY

The program does not default to interactivity. If you wish to change the value of SEARCH_TERM to something new, that will be the limit of interactivity.

DESCRIPTION

Cache all data
  45-50
  69-73
Retrieve data from 2 different API endpoints
  33-45
  55-68
Include 2+ function definitions
  31
  53
  145
Include 2+ class definitions
  77
  102
Create 1 instance of each class
  130
  138
Invoke methods from each class
  152 (created a function that uses the same method defined in both classes)
  157,158 (invoke that function)
Accumulate data
  130
  138
Write data to file
  145 (create function that writes data)
  157,158 (invoke that function)
