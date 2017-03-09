import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


# Reads in txt file, returns two floats for active and passive ratio
def read_txt(txt_file):
    active_cut = 25
    passive_cut = 26
    # Open .txt file
    with open(txt_file) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    active_string = content[0][active_cut:len(content[0])]
    passive_string = content[1][passive_cut:len(content[1])]
    return float(active_string), float(passive_string)


# Filters out list with keyword
def filter_list(input_list, keyword):
    output_list = []
    for item in input_list:
        if keyword in item:
            output_list.append(item)
    return output_list


# Main method
def main():
    txt_files = sys.argv[1:len(sys.argv)]
    txt_files.sort()

    # Get rat numbers
    active_rat = ""
    passive_rat = ""
    if 'dom' in txt_files[0]:
        active_rat = txt_files[0][14:16]  # Accounts for assets/Stage*/
        passive_rat = txt_files[0][16:18]
    else:
        active_rat = txt_files[0][16:18]
        passive_rat = txt_files[0][14:16]

    # Get stage number
    stage_num = 'Control'
    if "Stage1" in txt_files[0]:
        stage_num = '1'
    elif "Stage2" in txt_files[0]:
        stage_num = '2'
    elif "Stage3" in txt_files[0]:
        stage_num = '3'

    # Get ratio data
    active_ratios = []
    passive_ratios = []
    for i in range(len(txt_files)):
        active_ratio, passive_ratio = read_txt(txt_files[i])
        active_ratios.append(active_ratio)
        passive_ratios.append(passive_ratio)

    # Plot data
    days = range(1, len(txt_files) + 1)
    plt.plot(days, active_ratios, color='b', label='Active Rat')
    plt.plot(days, passive_ratios, color='r', label='Passive Rat')
    plt.title('SD' + active_rat + '\nStage ' + stage_num)
    plt.xticks(range(1, len(txt_files), 1))
    plt.yticks(np.arange(0.0, 1.2, 0.2))
    plt.xlabel('Day')
    plt.ylabel('Grooming Ratio')
    blue_patch = mpatches.Patch(color='blue', label='SD' + active_rat + ' (Active)')
    red_patch = mpatches.Patch(color='red', label='SD' + passive_rat + ' (Passive)')
    plt.legend(handles=[blue_patch, red_patch])
    plt.savefig('SD' + active_rat + '-Stage' + stage_num)
    plt.show()
    return

# Run main method
if __name__ == "__main__":
    main()

