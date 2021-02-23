# NOAA Grow Season Calculator

This script takes a CSV report from NOAA and exports a CSV containing the grow seasons for each year. Specifically, the amount of days between the last Spring and first Fall frosts.

## Generate a report

Use the [NOAA Climate Data Online Search](https://www.ncdc.noaa.gov/cdo-web/search) utility. Dataset to `Daily Summaries`, select desired date range and location. Next click the `SEARCH` button. Select the desired location details on the left in the next screen and add to cart. Next checkout but clicking on the cart in the top right corner and clicking `VIEW ALL ITEMS (1)`. In this screen, set the Output Format to `Custom GHCN-Daily CSV`, then click `CONTINUE`. On the next screen enter your email address and click `SUBMIT ORDER`. Then you will have to wait for the system to email you the CSV report. The time you have to wait depends on the size of the report. Small reports take minutes, big reports can take hours.

*NOTE* the input report csv file must be ascending order by date, but this is how it is given from the NOAA online search. Remove any incomplete years from the report file.

## Run

```
$ python noaa_grow_seasons.py <path to CSV report file>
```
