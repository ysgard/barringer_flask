#!/usr/bin/env python3

# barringer.py
#
# A script to produce a randome hireling for Dungeon World, based on
# following a series of selections from random tables.

import random
import sys

HIRELING_TABLE = "hireling.tbl"
DEBUG = False


class Row:
    def __init__(self):
        self.weight = 0
        self.val = ""


class Table:
    def __init__(self):
        self.rows = []


class Tables:
    def __init__(self):
        self.tabledict = {}


# Load the hireling table into memory
def read_table(table=HIRELING_TABLE):
    with open(table, 'r') as f:
        lead = f.readline().rstrip()
        tables = Tables()
        for line in f:
            if DEBUG:
                print("Parsing: {}".format(line))
            clean_line = line.rstrip()
            if clean_line == "":
                cur_table = ""
            elif cur_table == "":
                cur_table = clean_line
                tables.tabledict[cur_table] = Table()
            else:
                row = Row()
                if clean_line.find(' ')  > -1:
                    digit_end = clean_line.find(' ')
                    row.val = clean_line[digit_end + 1:len(clean_line)]
                    row.weight = int(clean_line[0:digit_end])
                else:
                    digit_end = clean_line.find('\n')
                    row.val = ""
                    row.weight = int(clean_line)
                tables.tabledict[cur_table].rows.append(row)
    return (lead, tables)

# Read a raw file of values - this is treated as a table whose name matches
# the filename and whose values all have the same weight.
# If the table already exists we don't do anything, just return
def read_raw_table(tables, file_name):
    if file_name in tables.tabledict:
        return
    tables.tabledict[file_name] = Table()
    with open(file_name, 'r') as f:
        for line in f:
            cleaned = line.rstrip()
            if cleaned != "":
                row = Row()
                row.weight = 1
                row.val = cleaned
                tables.tabledict[file_name].rows.append(row)

# Get a weighted random row from a given table
def get_row(tables, table_name):
    t = tables.tabledict[table_name]
    total_weight = 0
    for i in t.rows:
        total_weight += i.weight
    random_num = random.SystemRandom().randint(1, total_weight)
    current_weight = 0
    for i in t.rows:
        current_weight += i.weight
        if random_num <= current_weight:
            return i.val

def gen_hirelings(table_file, count):
    results = ""
    for i in range(0, count):
        results += gen_hireling(table_file) + "\n\n"
    return results

def roll_dice(dice_string):
    d_loc = dice_string.find('d')
    roll_number = 1
    dice_mod = 0
    if d_loc > 0:
        roll_number = int(dice_string[0:d_loc])
    dmod_plus = dice_string.find('+')
    dmod_minus = dice_string.find('-')
    if dmod_plus > -1:
        dice_mod = int(dice_string[dmod_plus + 1:len(dice_string)])
        die = int(dice_string[d_loc + 1:dmod_plus])
    elif dmod_minus > -1:
        dice_mod = -1 * int(dice_string[dmod_minus + 1:len(dice_string)])
        die = int(dice_string[d_loc + 1:dmod_minus])
    else:
        die = int(dice_string[d_loc + 1:len(dice_string)])
    total = 0
    for dice in range(0, roll_number):
        roll = random.SystemRandom().randint(1, die)
        total += roll
    total += dice_mod
    return total
        

def gen_hireling(table_file):
    # Initialize RNG
    random.seed(random.SystemRandom().randint(1, 65000))
    (lead, tables) = read_table(table_file)
    vars = {}
    # Parse the lead, looking up the values in the tables
    while lead.find('{') > -1:
        begin_bracket = lead.find('{')
        end_bracket = lead.find('}')
        command = lead[begin_bracket + 1:end_bracket]
        # handle variables
        if command[0:1] == '%':
            # Define a variable
            if command.find('=') > -1:
                varname = command[1:command.find('=')]
                vars[varname] = int(command[command.find('=')+1:len(command)])
                lead = lead[0:begin_bracket] + lead[end_bracket + 1:len(lead)]
            # Handle adding or subtracting to a variable
            elif command.find('+') > -1:
                varname = lead[1:lead.find('+')]
                vars[varname] += int(command[command.find('+') + 1:len(command)])
                lead = lead[0:begin_bracket] + lead[end_bracket + 1:len(lead)]
            # Insert the value of the variable
            else:
                lead = lead[0:begin_bracket] + \
                    str(vars[command[1:len(command)]]) + \
                    lead[end_bracket + 1:len(lead)]
        # Handle newlines
        elif command[0:2] == '\\n':
            lead = lead[0:begin_bracket] + '\n' + \
                lead[end_bracket + 1:len(lead)]
        # Insert call to raw table
        elif command.find('^') > -1:
            # Throw away for now
            read_raw_table(tables, command[1:len(command)])
            lead = lead[0:begin_bracket] + \
                get_row(tables, command[1:len(command)]) + \
                lead[end_bracket + 1:len(lead)]
        # Generate a random number using ndx syntax
        elif command.find('#') > -1:
            num = roll_dice(command[1:len(command)])
            lead = lead[0:begin_bracket] + \
                "{}".format(roll_dice(command[1:])) + \
                lead[end_bracket + 1:len(lead)]
        # Otherwise just insert the result of rolling on the given table
        else:
            lead = lead[0:begin_bracket] + \
                get_row(tables, command) + \
                lead[end_bracket + 1:len(lead)]
    return lead

if __name__ == "__main__":
    if len(sys.argv) < 1 or len(sys.argv) > 3:
        print("Usage: python {} [count] [table_file]".format(sys.argv[0]))
    count = 1
    table_file = HIRELING_TABLE
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
    if len(sys.argv) > 2:
        table_file = sys.argv[2]
    result = gen_hirelings(table_file, count)
    print(result)
