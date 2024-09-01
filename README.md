# Illumio Technical Assessment/Flow Log Parser
## Overview
`flow_log_parser.py` is a Python script designed to process Amazon VPC flow logs and generate reports based on the logs.

## Assumptions and Limitations
- **Log Format:** Only supports default log format (https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html)
- **Log Version:** Only Version 2 is supported
- **Lookup Table Format:** Only supports a csv file with three columns: `dstport`, `protocol` and `tag`. Values must be strings e.g. `tcp`,`udp`, `icmp`.
- **Log Size:** 10 MB or less is tested and supported
- **Lookup Table Size:** 10000 mappings or less is tested and supported
- **Case Insensitivity:** Parsing is case-insensitive, `TCP` is the same as `tcp`
- **Protocol Numbers:** The protocol numbers mapping based on (https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)

## Requirements
- Python 3.x 

## How to Run the Program
1. **Clone or Download the Repo**:

   - Ensure the following files are in the same directory: `flow_log_parser.py`, `lookup_table.csv`, `flow_logs.txt`, `protocol_numbers.csv`
   - Ensure that the `lookup_table.csv` file formatted correctly with the columns `dstport`, `protocol`, and `tag`.
   - Ensure that the `flow_logs.txt` file containing the flow log data is formatted according to (https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html)

3. **Run the Script**:
   - Open a terminal.
   - Navigate to the directory containing the script.
   - Run the script using Python:
     ```
     python3 flow_log_parser.py
     ```
   - The program will generate `tag_counts.csv` and `port_protocols_counts.csv` as output.

### Output
   - `tag_counts.csv`: A summary of how many times each tag appeared in the logs.
   - `port_protocols_counts.csv`: A breakdown of how many times each port/protocol combination appeared.

### Example Output
Tag,Count\
sv_P2,1\
sv_P1,2\
sv_P4,1\
email,3\
Untagged,9

Port,Protocol,Count\
22,tcp,1\
23,tcp,1\
25,tcp,1\
110,tcp,1\
143,tcp,1

## Testing
- Tested with `flow_logs.txt` with size of 10 MB and `lookup_table.csv` with 10000 mappings
- These can be randomly generated with `generate_logs_lookup_table.py`. Just run in the terminal using this command: `generate_logs_lookup_table.py`.

### Unit Tests
Tests covered:
- Parsing the `protocol_numbers.csv` correctly
- Parsing the `lookup_table.csv` correctly
- Parsing the `flow_logs.txt` correctly
- Writing the output correctly to `tag_counts.csv`
- Writing the output correctly to `port_protocols_counts.csv`

### How to Run the Unit Tests
1. Ensure the framework `unittest` is installed
2. Ensure `test_flow_log_parser.py` is in the same directory as all the previous other files
3. Run the tests:
   ```
   python3 test_flow_log_parser.py
   ```
