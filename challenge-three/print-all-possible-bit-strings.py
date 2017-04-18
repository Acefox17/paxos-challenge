import sys

def run():
  if len(sys.argv) < 2:
    print('No input string specified')
    return
  bit_string = sys.argv[1]
  index = 0
  print_bit_string(bit_string, index)

def print_bit_string(bit_string, index):
  if len(bit_string) <= index:
    print(bit_string)
    return
  new_index = index + 1
  character = bit_string[index:new_index]
  if character == 'X':
    print_bit_string(bit_string[:index] + '0' + bit_string[new_index:], new_index)
    print_bit_string(bit_string[:index] + '1' + bit_string[new_index:], new_index)
  else:
    print_bit_string(bit_string, new_index)

run()
