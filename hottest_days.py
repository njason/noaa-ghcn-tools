import argparse
import csv
import os
from datetime import datetime

from common import parseFtpOutput, parseWebToolOutput


parser = argparse.ArgumentParser('NOAA Grow Season Calculator')
parser.add_argument('-f', '--isftp', action='store_true')
parser.add_argument('input_file', type=str, help='Input CSV file from NOAA report, see README for details on obtaining report CSV file.')


args = parser.parse_args()

station, years =  parseFtpOutput(args, 'TMAX') if args.isftp else parseWebToolOutput(args, 'TMAX')

# output grow season length
with open('{0}-hottest-days.csv'.format(os.path.splitext(args.input_file)[0]), 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['STATION', 'YEAR', 'HOTTESTDAY', 'HOTTESTTEMP'], quoting=csv.QUOTE_ALL)
    writer.writeheader()

    for year, days in years.items():

        hottest_temp = None
        hottest_day = None

        for i, day_max_temp in enumerate(days):

            if hottest_day == None:
                hottest_temp = day_max_temp
                hottest_day = i
            elif hottest_temp < day_max_temp:
                hottest_temp = day_max_temp
                hottest_day = i

        writer.writerow({'STATION': station, 'YEAR': year, 'HOTTESTDAY': hottest_day, 'HOTTESTTEMP': hottest_temp})
