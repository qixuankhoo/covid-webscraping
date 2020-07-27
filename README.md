# covid-webscraping

## Project Title
This repository is to store web scrapers that scrape covid-19 related policies for 6 states. We plan on using the scraped information to analyze how county-level policies influence people's attitudes towards covid-19, along with the number of cases.

### File structure 
- state
  - data
    - date 
      - <county>.txt
      - <county>-PDF folder 
  - scripts 

### How to use 
If you want to scrape for North Carolina, go to the run_all.py script under North Carolina/scripts in terminal. Then, type in "python3 run_all.py".
The run_all.py script under scripts will automatically run all the scripts under scripts folder and put all the scraped data inside a newly created directory with the current date as its name. 

If you want to scrape a single county such as Durham under North Carolina, go to the durham.py script under North Carolina/scripts in terminal. Then, type in "python3 durham.py". The data will be available under data with the names "durham.txt" and "durham-PDF" (if the Durham county website has PDFs).


### Built With
Selenium Webdriver 
Beautiful Soup 

### Authors
Anni Chen, Dylan Zumar, Rami Sbahi, Raghav Rasal, Qi Xuan Khoo

### Acknowledgments
This project is led by Elizabeth Albright, Ph.D. <elizabeth.albright@duke.edu>.
