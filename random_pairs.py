filename = "./stimlist.csv"

import csv
import random

with open(filename, newline='') as csvfile:
    lines = []
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        lines.append(row)
    #lines = [line for line in csvfile]
    #print(lines)
    header = lines.pop(0)
    print(header)
    random.shuffle(lines)
    f = 0
    while f < 4:
        i = 0
        new_csv_lines = []
        while i <= 30:
            chosen_row = lines[i]
            print(chosen_row)
            unique_seq = chosen_row[6]
            if len(new_csv_lines) == 0:
                print("Appending first item")
                new_csv_lines.append(chosen_row)
                i += 1
            elif len(new_csv_lines) == 1:
                new_csv_current_item = new_csv_lines[0]
                new_csv_current_item_unique_seq = new_csv_current_item[6]
                if unique_seq == new_csv_current_item_unique_seq:
                    print("Skipping this iteration and reshuffling:")
                    random.shuffle(lines)
                else:
                    print("Current pair is not equal to previous")
                    new_csv_lines.append(chosen_row)
                    i += 1
            else:
                new_csv_current_item_2 = new_csv_lines[i-2]
                new_csv_current_item = new_csv_lines[i-1]
                new_csv_current_item_unique_seq = new_csv_current_item[6]
                new_csv_current_item_unique_seq_2 = new_csv_current_item[6]
                if unique_seq == new_csv_current_item_unique_seq or unique_seq == new_csv_current_item_unique_seq_2:
                    print("Skipping this iteration and reshuffling:")
                    random.shuffle(lines)
                else:
                    print("Current pair is not equal to previous 2")
                    new_csv_lines.append(chosen_row)
                    i += 1

        print("Generated 1 file:")
        print(new_csv_lines)

        with open('stimuli_{}.csv'.format(f), 'w', newline='') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(header)
            wr.writerows(new_csv_lines)
        f += 1
