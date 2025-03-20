import pandas as pd
from matplotlib import pyplot as plt
import argparse

def create_parser():
    parser = argparse.ArgumentParser(description='Plot bridge codes statistics')
    parser.add_argument('statistics_file', type=str, help='Input statistics file name')
    parser.add_argument('mode', type=str, choices=['SE', 'PE'], help='Mode: SE or PE')
    parser.add_argument('input_path', type=str, help='Input path to statistics file')
    parser.add_argument('output_path', type=str, help='Output path for saving plots')
    parser.add_argument('u_parameter_arguments', type=str, help='U parameter arguments (comma-separated)')
    return parser

def plot_bridge_codes(args):
    u_parameter_arguments_list = [i.strip() for i in args.u_parameter_arguments.split(",")]
    color_dict = {}
    for i in u_parameter_arguments_list:
        if args.mode == "SE": 
            color_dict[i + "-DR"] = 'tab:green'
            color_dict[i + "-00"] = 'yellow'
            color_dict[i + "-0R"] = 'yellow'
            color_dict[i + "-D0"] = 'yellow'
        else:
            color_dict[i[0] + "-" + i[1] + "-DR"] = 'tab:green'
            color_dict[i[0] + "-" + i[1] + "-00"] = 'yellow'
            color_dict[i[0] + "-" + i[1] + "-0R"] = 'yellow'
            color_dict[i[0] + "-" + i[1] + "-D0"] = 'yellow'
            
        
    SE_code = {
        "Code": 
            ["0","F-00","F-0R","F-D0","F-DR","R-00","R-0R","R-D0","R-DR","FR"],
        "Description": 
            ["bridge not found",
            "F-bridge found, RNA and DNA parts did not pass the length filter",
            "F-bridge found, only the RNA part passed the length filter",
            "F-bridge found, only the DNA part passed the length filter",
            "F-bridge found, RNA and DNA parts were filtered for length",
            "R-bridge found, RNA and DNA parts did not pass the length filter",
            "R-bridge found, only the RNA part passed the length filter",
            "R-bridge found, only the DNA part passed the length filter",
            "R-bridge found, RNA and DNA parts were filtered for length",
            "both forward and reverse bridges found"]
    }

    PE_code = {
        "Code": ["R-0-DR","0-R-DR","F-0-DR","0-F-DR","R-0-0R","R-0-D0","R-0-00","0-R-0R","0-R-D0","0-R-00","F-0-0R","F-0-D0","F-0-00","0-F-0R","0-F-D0","0-F-00",
                 "0-0","0-FR","FR-0","R-R","F-F","R-F","F-R","R-FR","F-FR","FR-R","FR-F","FR-FR"],
        "Description": 
            ["reverse (R) bridge found in R1, RNA and DNA parts were filtered for length",
            "R-bridge found in R2, RNA and DNA parts were filtered for length",
            "forward (F) bridge found in R1, RNA and DNA parts were filtered for length",
            "F-bridge found in R2, RNA and DNA parts were filtered for length",
            "R-bridge found in R1, only the RNA part passed the length filter",
            "R-bridge found in R1, only the DNA part passed the length filter",
            "R-bridge found in R1, RNA and DNA parts did not pass the length filter",
            "R-bridge found in R2, only the RNA part passed the length filter",
            "R-bridge found in R2, only the RNA part passed the length filter",
            "R-bridge found in R2, RNA and DNA parts did not pass the length filter",
            "F-bridge found in R1, only the RNA part passed the length filter",
            "F-bridge found in R1, only the DNA part passed the length filter",
            "F-bridge found in R1, RNA and DNA parts did not pass the length filter",
            "F-bridge found in R2, only the RNA part passed the length filter",
            "F-bridge found in R2, only the DNA part passed the length filter",
            "F-bridge found in R2, RNA and DNA parts did not pass the length filter",
            "bridge not found",
            "two bridges forward and reverse found in R2",
            "two bridges forward and reverse found in R1",
            "found reverse bridge in R1 and in R2",
            "found forward bridge in R1 and in R2",
            "found reverse bridge in R1 and forward bridge in R2",
            "found forward bridge in R1 and reverse bridge in R2",
            "found reverse bridge in R1, and also forward and reverse bridge in R2",
            "found forward bridge in R1, and also forward and reverse bridge in R2",
            "forward and reverse bridge found in R1, and reverse bridge in R2",
            "forward and reverse bridge found in R1, and forward bridge in R2",
            "forward and reverse bridges are found in both R1 and R2"] 
        }

    statistics = pd.read_csv(args.input_path + args.statistics_file, header=None, sep='\t', dtype = 'str')
    statistics = statistics.rename({0: 'Code', 1: 'N-reads'}, axis='columns')
    statistics['N-reads'] = statistics['N-reads'].apply(lambda x: int(x))
    
    if args.mode == "SE":
        code_df = pd.DataFrame.from_dict(SE_code)
    else:
        code_df = pd.DataFrame.from_dict(PE_code)
    result = pd.merge(statistics, code_df, on="Code", how="left").sort_values(by="N-reads", ascending=False)
    
    color_list = []
    for i in result['Code'].values:
        if i in color_dict.keys():
            color_list.append(color_dict[i])
        else:
            color_list.append("tab:blue")

    fig, axs = plt.subplots(2,1)
    axs[0].axis('tight')
    axs[0].axis('off')
    the_table = axs[0].table(cellText=result.values, colLabels=['$\\bf{Code}$', '$\\bf{N-reads}$', '$\\bf{Description}$'], loc='center', cellLoc='left')
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(7)
    the_table.auto_set_column_width(col=list(range(len(result.columns)))) # Provide integer list of columns to adjust
    plt.tight_layout()

    
    axs[1].bar(result['Code'].values, result['N-reads'].values, label=result['Code'].values, color=color_list)
    axs[1].set_ylabel('N-reads')
    if args.mode == "PE":
        for tick in axs[1].get_xticklabels():
            tick.set_rotation(90)       
    colors = {'-u {}, RNA and DNA parts were filtered for length'.format(args.u_parameter_arguments): 'tab:green', 
          '-u {}, RNA and DNA parts did not pass the length filter'.format(args.u_parameter_arguments): 'yellow', 
          'all other cases': 'tab:blue'}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    plt.legend(handles, labels, prop={'size': 6})
    plt.yscale('log')
    #plt.show()

    plt.savefig('{output_path}{statistics_file}_{mode}.png'.format(
        output_path=args.output_path, 
        statistics_file=args.statistics_file, 
        mode=args.mode
    ), dpi=360, bbox_inches="tight")

def main():
    parser = create_parser()
    args = parser.parse_args()
    plot_bridge_codes(args)

if __name__ == '__main__':
    main()

#python plotBridgeCodes.py "SRR17331267_2.codes.tsv" "PE" "/home/snap/projects/nf-rnachrom-plots/BridgeCodes/data/" "/home/snap/projects/nf-rnachrom-plots/BridgeCodes/" "F0, R0"

#python plotBridgeCodes.py "SRR17331267.codes.tsv" "SE" "/home/snap/projects/nf-rnachrom-plots/BridgeCodes/data/" "/home/snap/projects/nf-rnachrom-plots/BridgeCodes/" "F"