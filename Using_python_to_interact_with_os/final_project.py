#!/usr/bin/env python3

import csv
import re
import sys


errors_dictionary = {}
users_dictionary = {}

with open("syslog.log") as log:
  for record in log:
    username = re.search(r"\((.*)\)",record).group(1)
    count = {'INFO': 0, 'ERROR': 0}

    if username not in users_dictionary:
      users_dictionary[username] = count

    if "INFO" in record:
      users_dictionary[username]['INFO'] += 1

    elif "ERROR" in record:
      err_msg = re.search(r"ERROR (.*) ",record).group(1)
      if err_msg not in errors_dictionary:
        errors_dictionary[err_msg] = 0
      errors_dictionary[err_msg] += 1
      users_dictionary[username]['ERROR'] += 1


sorting_errors = []
sorting_users = []

for error, count in sorted(errors_dictionary.items(), key=lambda item: item[1],reverse=True):
  sorting_errors.append([error, count])

for username in sorted(users_dictionary.keys()):
  sorting_users.append([username, users_dictionary[username]["INFO"], users_dictionary[username]["ERROR"]])

sorting_errors.insert(0,["Error","Count"])

sorting_users.insert(0,["Username","INFO","ERROR"])

with open("error_message.csv","w") as error_msg_file:
  csv_writer = csv.writer(error_msg_file)
  csv_writer.writerows(sorting_users)
  error_msg_file.close()

with open("user_statistics.csv", "w") as usrstats:
  csv_writer = csv.writer(usrstats)
  csv_writer.writerows(sorting_users)
  usrstats.close()


