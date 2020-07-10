# covid-webscraping

## Project Title
This repository is to store webscrappers that scrap covid-19 related policy for 6 states. We plan on using the scrapped information to analyze whether county-level policies would influence people's attitudes towards covid-19.

### File structure 
- state
  - data
    - date 
      - <county>.txt
      - <county>-PDF folder 
  - scripts 

### How to use 
If you want to run scrapping for North Carolina, go to the run_all.py script under North Carolina/scripts in terminal. Then, type in "python3 run_all.py".
The run_all.py script under scripts would automatically run all the scripts under scripts folder and put all the scrapped data inside a  newly created directory with date as its name. 

If you want to scrap a single county such as Durham under North Carolina, go to the durham.py scripty under North Carolina/scripts in terminal. Then, type in "python3 durham.py". The data will be available under data with names "durham.txt" and "durham-PDF" if durham county website has PDFs.


## Built With
Selenium Webdriver 
Beautiful Soup 

## Authors
Anni Chen, Dylan Zumar, Rami Sbahi, Raghav Rasal, Qi Xuan Khoo

## Acknowledgments
This project is led by Elizabeth Albright, Ph.D. <elizabeth.albright@duke.edu>.
