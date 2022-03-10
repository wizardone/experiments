# VERSION 3.0
filename = "./stimlist.csv"
max_run_seconds = 2
import csv
import random
import time

def create_randomized_files():
    with open(filename, newline='') as csvfile:
        start = time.time()
        randomized = True
        num_iterations = 0
        lines = []
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            lines.append(row)
        header = lines.pop(0)
        random.shuffle(lines)  # Randomising all trials
        print("Total number of lines:")
        print(len(lines))
        f = 1 # Generating each new file
        while f <= 5:
            i = 0
            new_trial = [] # Generating a new trial
            print("Number of lines left:")
            print(len(lines))
            while i <= 27:
                if time.time() - start > max_run_seconds:
                    print("PLEASE RERUN TRIAL")
                    randomized = False
                    break
                current_row = lines[0] # Current row for the very first trial of the experiment
                #print(current_row)
                current_seq = current_row[6] # Column 6 contains Pair # info
                if len(new_trial) == 0:
                    print("Appending first item")
                    new_trial.append(current_row)
                    lines.pop(0)
                    i += 1
                elif len(new_trial) == 1: # Checking trial #2
                    previous_trial = new_trial[0]
                    previous_trial_current_seq = previous_trial[6]
                    if current_seq == previous_trial_current_seq:
                        num_iterations +=1
                        print("Skipping this iteration and reshuffling:")
                        random.shuffle(lines)  # Randomising the remaininig trials
                    else:
                        print("Current pair is not equal to previous")
                        new_trial.append(current_row)
                        lines.pop(0)
                        i += 1 # Until the condition is satisfied shuffling continues
                else:   # Checking all remaining trials
                    previous_2trials = new_trial[i-2] # Current line minus 2
                    previous_trial = new_trial[i-1] # Current line minus 1
                    previous_trial_current_seq = previous_trial[6]
                    previous_trial_current_seq2 = previous_2trials[6]
                    if current_seq == previous_trial_current_seq or current_seq == previous_trial_current_seq2:
                        num_iterations +=1
                        print("Skipping this iteration and reshuffling:")
                        random.shuffle(lines)
                    else:
                        print("Current pair is not equal to previous 2")
                        new_trial.append(current_row)
                        lines.pop(0)
                        i += 1

            print("Generated 1 file:")
            #print(new_trial)

            with open('BlockX{}.csv'.format(f), 'w', newline='') as myfile:
                wr = csv.writer(myfile)
                wr.writerow(header)
                wr.writerows(new_trial)
            f += 1
        print("Code iterations:", num_iterations) 
        return randomized

success = False
while success == False:
    success = create_randomized_files()
