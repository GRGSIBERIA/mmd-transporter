#-*- encoding: utf-8
import csv

class CSVImporter:
  def __init__(self):
    pass

  def toRowList(self, path):
    rows = []
    with open(path, "r") as f:
      reader = csv.reader(f)
      for row in reader:
        rows.append(row)
    return rows