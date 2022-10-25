import argparse
import csv
import os

from common import parseFtpOutput, parseWebToolOutput


parser = argparse.ArgumentParser('NOAA Grow Season Calculator')
parser.add_argument('-f', '--isftp', action='store_true')
parser.add_argument('input_file', type=str, help='Input CSV file from NOAA report, see README for details on obtaining report CSV file.')

args = parser.parse_args()

station = None
years = {}

station, years =  parseFtpOutput(args, 'TMIN') if args.isftp else parseWebToolOutput(args, 'TMIN')
    
# output grow season length
with open('{0}-grow-seasons.csv'.format(os.path.splitext(args.input_file)[0]), 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['STATION', 'YEAR', 'SEASONDAYS'], quoting=csv.QUOTE_ALL)
    writer.writeheader()

    for year, days in years.items():

        if len(days) < 365:
            continue

        last_spring_frost = None
        first_fall_frost = None

        for i, day_min_temp in enumerate(days):
            # the 200th day of the year is in the middle of July, hottest time of the year anywhere is the continental USA
            if i < 200 and int(day_min_temp) < 33:
                last_spring_frost = i
            elif i >= 200 and int(day_min_temp) < 33:
                first_fall_frost = i
                break

        if not last_spring_frost or not first_fall_frost:
            continue

        writer.writerow({'STATION': station, 'YEAR': year, 'SEASONDAYS': first_fall_frost - last_spring_frost})
