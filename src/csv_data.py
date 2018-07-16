import csv
import subprocess


class CSVData:

    def __init__(self, table):
        self.table = table

    def read(self):
        subprocess.call('touch %s.csv' % self.table, shell=True)
        with open('%s.csv' % self.table, 'rb') as csv_file:
            reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
            ids = []
            for row in reader:
                ids.append(int(row[0]))
        return ids

    def write(self, rows):
        with open('%s.csv' % self.table, 'wb') as csv_file:
            writer = csv.writer(csv_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in rows:
                if type(row) is not list:
                    writer.writerow([row])
                elif type(row) is list:
                    writer.writerow(map(str, row))
