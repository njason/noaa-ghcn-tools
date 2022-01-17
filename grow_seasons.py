import argparse
import csv
import os
from datetime import datetime

parser = argparse.ArgumentParser('NOAA Grow Season Calculator')
parser.add_argument('-f', '--isftp', action='store_true')
parser.add_argument('input_file', type=str, help='Input CSV file from NOAA report, see README for details on obtaining report CSV file.')

args = parser.parse_args()

station = None
years = {}

def cToF(c):
    return (c * 9/5) + 32

def parseWebToolOutput():
    global station, years

    # parse input file
    with open(args.input_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not station:
                station = row['STATION']

            date = datetime.strptime(row['DATE'], '%Y-%m-%d')

            if row['TMIN'] == '':
                continue
            
            if date.year not in years:
                years[date.year] = []
            
            years[date.year].append(row['TMIN'])


def parseFtpOutput():
    global station, years

    input = []
    def sortFunc(r):
        return r['date']

    with open(args.input_file) as csvfile:
        reader = csv.DictReader(csvfile, ['station', 'date', 'type', 'value'])
        for row in reader:
            if not station:
                station = row['station']

            if row['type'] == 'TMIN':
                input.append(row)

        input.sort(key=sortFunc)

        for row in input:
            if row['value'] != '':
                date = datetime.strptime(row['date'], '%Y%m%d')
                
                if date.year not in years:
                    years[date.year] = []

                years[date.year].append(cToF(int(row['value']) / 10))
            
            

if args.isftp:
    parseFtpOutput()
else:
    parseWebToolOutput()

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
