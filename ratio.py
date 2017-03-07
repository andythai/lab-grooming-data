import sys
import csv

# Constants
START_TIME = 0
END_TIME = 1
LABEL = 4


# Convert csv to list []
def load_csv(csv_filename):
    # Open CSV file
    f = open(csv_filename)
    reader = csv.reader(f)
    # Append contents to list variable
    list = []
    for row in reader:
        list.append(row)
    f.close()
    return list


# Convert time string to seconds
def convert_time(time_string):
    ftr = [60, 1]
    return sum([a * b for a, b in zip(ftr, map(float, time_string.split(':')))])


# Returns start and end times of duration for entire video
def get_video_duration(csv_list):
    # Find starting time for air
    air_intervals = []
    for row in csv_list:
        if row[LABEL] == 'Air Active' or row[LABEL] == 'Air Passive':
            air_intervals.append(row)
    air_intervals.sort()
    start = air_intervals[0][START_TIME]
    # Find ending time for duration
    end = air_intervals[len(air_intervals) - 1][END_TIME]
    return start, end


# Return list with valid grooming durations for active rat
def get_grooming_active(csv_list, duration_start, duration_end, start_string, end_string):
    active_grooming = []
    for row in csv_list:
        if row[LABEL] == 'Grooming Active':
            groom_start_string = row[START_TIME]
            groom_start = convert_time(groom_start_string)
            groom_end_string = row[END_TIME]
            groom_end = convert_time(groom_end_string)

            # Cut down on intervals that overlap; if grooming before start, but goes past start
            if groom_start < duration_start and groom_end > duration_start:
                row[START_TIME] = start_string
                groom_start = convert_time(start_string)

            # If grooming before end, but goes past end
            if groom_start < duration_end and groom_end > duration_end:
                row[END_TIME] = end_string
                groom_end = convert_time(end_string)
            if groom_start >= duration_start and groom_end <= duration_end:
                active_grooming.append(row)
    return active_grooming


# Return list with valid grooming durations for passive rat
def get_grooming_passive(csv_list, duration_start, duration_end, start_string, end_string):
    passive_grooming = []
    for row in csv_list:
        if row[LABEL] == 'Grooming Passive':
            groom_start_string = row[START_TIME]
            groom_start = convert_time(groom_start_string)
            groom_end_string = row[END_TIME]
            groom_end = convert_time(groom_end_string)

            # Cut down on intervals that overlap; if grooming before start, but goes past start
            if groom_start < duration_start and groom_end > duration_start:
                row[START_TIME] = start_string
                groom_start = convert_time(start_string)

            # If grooming before end, but goes past end
            if groom_start < duration_end and groom_end > duration_end:
                row[END_TIME] = end_string
                groom_end = convert_time(end_string)

            if groom_start >= duration_start and groom_end <= duration_end:
                passive_grooming.append(row)
    return passive_grooming


# Given a csv-like list, calculate the total duration of all entries; right now used for counting grooming
def calculate_total_duration(list):
    total_duration = 0
    for row in list:
        start = convert_time(row[START_TIME])
        end = convert_time(row[END_TIME])
        total_duration = total_duration + (end - start)
    return total_duration


# Main method
def main():
    # Load CSV
    csv_list = load_csv(sys.argv[1])

    # Get duration
    start_string, end_string = get_video_duration(csv_list)

    # Convert times
    duration_start = convert_time(start_string)
    duration_end = convert_time(end_string)

    # Duration length
    duration = duration_end - duration_start

    # Get grooming lists
    active_grooming_list = get_grooming_active(csv_list, duration_start, duration_end, start_string, end_string)
    passive_grooming_list = get_grooming_passive(csv_list, duration_start, duration_end, start_string, end_string)

    # Calculate total grooming durations
    total_grooming_duration_active = calculate_total_duration(active_grooming_list)
    total_grooming_duration_passive = calculate_total_duration(passive_grooming_list)

    # Calculate ratio
    ratio_active = total_grooming_duration_active / duration
    ratio_passive = total_grooming_duration_passive / duration
    print("\nGrooming (Active) ratio: \t" + str(ratio_active))
    print("Grooming (Passive) ratio: \t" + str(ratio_passive))

    # Write to log file
    index = sys.argv[1].find(".csv")
    saved_filename = sys.argv[1][0:index]
    saved_file = open(saved_filename + ".txt", "w")
    saved_file.write("Grooming (Active) ratio: " + str(ratio_active))
    saved_file.write("\nGrooming (Passive) ratio: " + str(ratio_passive))
    saved_file.close()

# Run main method
if __name__ == "__main__":
    main()