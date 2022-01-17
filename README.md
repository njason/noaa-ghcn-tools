# NOAA Grow Season Calculator

This script takes a CSV report from NOAA and exports a CSV containing the grow seasons for each year. Specifically, the amount of days between the last Spring and first Fall frosts.

## Get Data files

### Web Tool

For small amounts of data, use the [NOAA Climate Data Online Search](https://www.ncdc.noaa.gov/cdo-web/search) utility. It has a limit of 10,000 station days per order.

Dataset to `Daily Summaries`, select desired date range and location. Next click the `SEARCH` button. Select the desired location details on the left in the next screen and add to cart. Next checkout but clicking on the cart in the top right corner and clicking `VIEW ALL ITEMS (1)`. In this screen, set the Output Format to `Custom GHCN-Daily CSV`, then click `CONTINUE`. On the next screen enter your email address and click `SUBMIT ORDER`. Then you will have to wait for the system to email you the CSV report. The time you have to wait depends on the size of the report. Small reports take minutes, big reports can take hours.

*NOTE* the input report csv file must be ascending order by date, but this is how it is given from the NOAA online search. Remove any incomplete years from the report file.

```
$ python <python script> <path to CSV report file>
```
A new CSV file will be created in the same location as the input file with `grow-seasons` at the end of the file name.

### FTP

For bigger datasets, use the FTP server. With an FTP client, open `ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/`. Find the station's ID with the web tool, then download the file with the station ID name in the `by_station` directory on the FTP server.

The FTP data file is in a different format than the web tool, use the `-f` flag to indicate the FTP format.

```
$ python -f <python script> <path to CSV report file>
```
