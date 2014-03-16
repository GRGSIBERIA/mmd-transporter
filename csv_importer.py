#-*- encoding: utf-8
import csv

class CSVSplitter:
  def __init__(self):
    pass

  def toLineList(self, path):
    lines = []
    with open(path, "r") as f:
      for line in f:
        lines.append(line)
    return lines