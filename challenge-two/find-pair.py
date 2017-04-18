import sys
import os.path

def run():
  if len(sys.argv) < 2:
    print('No data file specified')
    return
  if len(sys.argv) < 3:
    print('No total price specified')
    return
  file_path = sys.argv[1]
  total_price = int(sys.argv[2])
  if not os.path.isfile(file_path):
    print('No file found at ' + file_path)
    return
  prices_file = open(file_path, 'r')
  best_item_collection = get_best_item_colletion(prices_file, total_price)
  if best_item_collection == None:
    print('Not possible\n')
  else:
    print_item_collection(best_item_collection)

def print_item_collection(item_collection):
  output = ''
  for item in item_collection.get_items():
    if len(output) > 0:
      output += ', '
    output += item.name + ' ' + str(item.price)
  print(output)

def get_best_item_colletion(prices_file, total_price):
  item_collections = []
  best_item_collection = None
  for line in prices_file:
    separator = ', '
    if separator not in line:
      continue
    line_values = line.split(separator)
    if len(line_values) < 2:
      continue
    item_name = line_values[0]
    item_price = int(line_values[1].rstrip('\n'))
    item = Item(item_name, item_price)
    response = process_item(item, item_collections, best_item_collection, total_price)
    best_item_collection = response[0]
    item_collections = response[1]
  return best_item_collection

def process_item(item, item_collections, best_item_collection, total_price):
  new_item_collections = []
  if item.price <= total_price:
    item_collection = ItemCollection()
    item_collection.add_item(item)
    new_item_collections.append(item_collection)
  for item_collection in item_collections:
    if len(item_collection.get_items()) == 2:
      continue
    if item_collection.get_total_price() + item.price <= total_price:
      new_item_collection = item_collection.copy()
      new_item_collection.add_item(item)
      new_item_collections.append(new_item_collection)
      if best_item_collection == None or new_item_collection.get_total_price() > best_item_collection.get_total_price():
        best_item_collection = new_item_collection
  item_collections = item_collections + new_item_collections
  return (best_item_collection, item_collections)

class Item:
  def __init__(self, name, price):
    self.name = name
    self.price = price

class ItemCollection:
  def __init__(self):
    self.__items = []
    self.__total_price = 0
  def add_item(self, item):
    self.__items.append(item)
    self.__total_price += item.price
  def get_items(self):
    return self.__items
  def get_total_price(self):
    return self.__total_price
  def copy(self):
    new_item_collection = ItemCollection()
    new_item_collection.__items = list(self.__items)
    new_item_collection.__total_price = self.__total_price
    return new_item_collection

run()
