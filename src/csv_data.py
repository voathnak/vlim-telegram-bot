import csv
import subprocess


class CSVData:

    def __init__(self, table):
        self.table = table
        self.path = 'vlim-telegram-bot-csv-data'
        subprocess.call("mkdir -p %s" % self.path, shell=True)

    def read_ids(self):
        subprocess.call('touch %s/%s.csv' % (self.path, self.table), shell=True)
        with open('%s/%s.csv' % (self.path, self.table), 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
            ids = []
            for row in reader:
                ids.append(int(row[0]))
        return ids

    def read(self):
        subprocess.call('touch %s/%s.csv' % (self.path, self.table), shell=True)
        with open('%s/%s.csv' % (self.path, self.table), 'rt') as csv_file:
            reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
            data = []
            for row in reader:
                if not len(row):
                    data.append([])
                elif len(row) == 1:
                    data.append([int(row[0])])
                else:
                    data.append([int(row[0])] + row[1:])
        return data

    def write(self, rows):
        with open('%s/%s.csv' % (self.path, self.table), 'wt') as csv_file:
            writer = csv.writer(csv_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in rows:
                if type(row) is not list:
                    writer.writerow([row])
                elif type(row) is list:
                    writer.writerow(map(str, row))
