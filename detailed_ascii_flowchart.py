def print_detailed_basketball_flowchart():
    flowchart = """
    +--------------------------------+
    |        basketball_info.csv     |
    | (Players, Rules, Equipment)    |
    +--------------------------------+
                   ↓
    +--------------------------------+
    |       Data Loading (Pandas)    |
    |     Chunk Processing: 1000     |
    +--------------------------------+
                   ↓
    +--------------------------------+
    |      Multi-Agent Analysis      |
    +--------------------------------+
            ↙        ↓         ↘
    +-----------+ +----------+ +------------------+
    | Data Agent | |   Web    | |    Assistant    |
    |  Analysis  | | Surfer   | |     Agent       |
    +-----------+ +----------+ +------------------+
         ↓            ↓              ↓
    +-----------+ +----------+ +------------------+
    | Sport Data | |  Latest  | | Recommendations |
    | Processing | |   News   | |  & Guidelines   |
    +-----------+ +----------+ +------------------+
            ↘         ↓         ↙
    +--------------------------------+
    |    Comprehensive Analysis      |
    |   & Final Recommendations     |
    +--------------------------------+
                   ↓
    +--------------------------------+
    |    Output: CSV Log File        |
    | (all_conversation_log.csv)     |
    +--------------------------------+
    """
    print(flowchart)

if __name__ == '__main__':
    print_detailed_basketball_flowchart()
