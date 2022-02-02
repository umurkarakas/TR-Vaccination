Data recording stopped on August 17, as the Health Ministry of Turkey stopped sharing daily vaccination numbers for each city.

-------------------------------------------------------------------------------------------------------------------------------

A Python Script for Extracting Turkey Vaccination Numbers


This Python script extracts the latest vaccination numbers from the Health Ministry of Turkey's
corresponding website (covid19asi.saglik.gov.tr) and appends the data to the previously created
csv file. 


In this script, I used requests and BeautifulSoup libraries to extract the data from the website.
I create a separate DataFrame for each run and then I append it to the previously created data.


I personally created a task scheduler for each day at 00:00:01 in order to check the daily numbers. 
Anyone can set up a task scheduler for different periods at different times for their goal and 
research.

For the calculation of vaccination rate over 18, I used the TUIK (Turkish Statistical Institute)
data for the population over 18. 
