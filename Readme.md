Setup
1.Start virtual environment on command prompt, '.venv/bin/activate'
2.Install prequisite packages, 'pip install -r requirements.txt'
3.Specify start and end index when script runs (i.e index.py, index2.py files)
*The start index and end index locates the positions of backer's list to crawl for data

#File/Folder Brief Description
index.py - Scrapes for backer's bio and their invested projects (e.g. bio, websites, project title, project description, creator name, pledge amt)
index2.py -Scrape detail information of backer's invested projects (e.g. Campaign's Story & Risk, Pledge info, Updates, no. of comments, comments content)
backer_list.pickle - contains backer's url links which are used as input data for index.py file
profile feature introduction.docx - A small documentation of our dicussion to crawl for backer's info, implemented on index.py file
data - A folder that stores output data after execution of index.py file
new_data - A folder that stores output data after execution of index2.py file
screenshot.png - An illustration of Kickstarter's anti-bot verification
ProjectProgress - Manual log to keep track of the progress of crawled backer's projects of backer's list for index2.py script
requirements.txt - List of package names and versions that are used for web scraping scripts 
