def print_basketball_analysis_flowchart():
    flowchart = """
    +------------------------+
    |    basketball_info.csv |
    |     (Input Data)      |
    +------------------------+
              ↓
    +------------------------+
    |    Data Processing    |
    | (Chunks of 1000 rows) |
    +------------------------+
              ↓
    +------------------------+
    |   Analysis Process    |
    +------------------------+
         ↙     ↓      ↘
    +-------+ +-------+ +-----------------+
    |Sport  | |Latest | |Recommendations |
    |Benefits| |Info   | |& Guidelines    |
    +-------+ +-------+ +-----------------+
    """
    print(flowchart)

if __name__ == '__main__':
    print_basketball_analysis_flowchart()
