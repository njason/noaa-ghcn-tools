from datetime import datetime
import csv

def cToF(c):
    return round((c * 9/5) + 32, 2)

def parseWebToolOutput(args, dataType):
    station = None
    years = {}

    # parse input file
    with open(args.input_file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not station:
                station = row['STATION']

            date = datetime.strptime(row['DATE'], '%Y-%m-%d')

            if row[dataType] == '':
                continue
            
            if date.year not in years:
                years[date.year] = []
            
            years[date.year].append(row[dataType])

    return station, years


def parseFtpOutput(args, dataType):
    station = None
    years = {}
    input = []
    
    def sortFunc(r):
        return r['date']

    with open(args.input_file) as csvfile:
        reader = csv.DictReader(csvfile, ['station', 'date', 'type', 'value'])
        for row in reader:
            if not station:
                station = row['station']

            if row['type'] == dataType:
                input.append(row)

        input.sort(key=sortFunc)

        for row in input:
            if row['value'] != '':
                date = datetime.strptime(row['date'], '%Y%m%d')
                
                if date.year not in years:
                    years[date.year] = []

                years[date.year].append(cToF(int(row['value']) / 10))

    return station, years
