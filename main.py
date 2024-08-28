import csv
from collections import defaultdict


def parse_protocol_numbers(file_path): 
    """
    Parses the protocol numbers file and returns a dictionary where the key is the protocol number(Decimal)
    and the value is the protocol name(Keyword)
    """
    protocol_numbers_map = {}
    with open(file_path, mode = "r") as file:
        reader = csv.DictReader(file)

        for row in reader: 
            protocol_numbers_map[row["Decimal"]] = row["Keyword"].lower()
    
    return protocol_numbers_map


def parse_lookup_table(file_path):
    """
    Parses the lookup table file and returns a dictionary where the key is a tuple (dstport, protocol)
    and the value is the tag
    """
    lookup_table = {}
    with open(file_path, mode ='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            dstport = row['dstport'].strip().lower()
            protocol = row['protocol'].strip().lower()
            tag = row['tag'].strip()
            lookup_table[(dstport, protocol)] = tag

    return lookup_table


def parse_flow_logs(flow_logs_file_path, lookup_table, protocol_numbers_map):
    """
    Parses the flow log file, counts the occurrences of each tag and each port/protocol combination,
    and returns two dictionaries, tag_counts and port_protocol_counts
    """
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)

    for line in open(flow_logs_file_path, 'r'):
        line_parts = line.split()
        dstport = line_parts[6].strip().lower()
        protocol_number = line_parts[7].strip()

        protocol = protocol_numbers_map.get(protocol_number, 'unknown')
        port_protocol_counts[(dstport, protocol)] += 1

        tag = lookup_table.get((dstport, protocol), 'Untagged')
        tag_counts[tag] += 1
        
    return tag_counts, port_protocol_counts


def generate_output(output_file_path, tag_counts, port_protocol_counts):
    """
    Writes the summary report to an output file.
    """
    with open(output_file_path, mode='w') as file:
        file.write("Tag,Count\n")
        for tag, count in tag_counts.items():
            file.write(f"{tag},{count}\n")

        file.write("Port,Protocol,Count\n")
        for (dstport, protocol), count in port_protocol_counts.items():
            file.write(f"{dstport},{protocol},{count}\n")


def main():
    lookup_table_file_path = 'lookup_table.csv'
    flow_logs_file_path = 'flow_logs.txt'
    output_file_path = 'output.txt'
    protocol_numbers_file_path = 'protocol_numbers.csv'

    protocol_numbers_map = parse_protocol_numbers(protocol_numbers_file_path)
    lookup_table = parse_lookup_table(lookup_table_file_path)
    tag_counts, port_protocol_counts = parse_flow_logs(flow_logs_file_path, lookup_table, protocol_numbers_map)

    generate_output(output_file_path, tag_counts, port_protocol_counts)
    

if __name__ == '__main__':
    main()