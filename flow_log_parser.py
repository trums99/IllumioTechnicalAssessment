import csv
from collections import defaultdict

class FlowLogParser:
    def __init__(self, lookup_table_file_path, flow_logs_file_path, tag_counts_output_file_path, \
                    port_protocol_counts_output_file_path,protocol_numbers_file_path):
        self.lookup_table_file_path = lookup_table_file_path
        self.flow_logs_file_path = flow_logs_file_path
        self.tag_counts_output_file_path = tag_counts_output_file_path
        self.port_protocol_counts_output_file_path = port_protocol_counts_output_file_path
        self.protocol_numbers_file_path = protocol_numbers_file_path
        self.protocol_numbers_map = {}
        self.lookup_table = {}


    def parse_protocol_numbers(self): 
        """
        Parses the protocol numbers file and returns a dictionary where the key is the protocol number(Decimal)
        and the value is the protocol name(Keyword)
        """
        protocol_numbers_map = {}
        with open(self.protocol_numbers_file_path, mode = "r") as file:
            reader = csv.DictReader(file)

            for row in reader: 
                self.protocol_numbers_map[row["Decimal"]] = row["Keyword"].lower()


    def parse_lookup_table(self):
        """
        Parses the lookup table file and returns a dictionary where the key is a tuple (dstport, protocol)
        and the value is the tag
        """
        with open(self.lookup_table_file_path, mode ='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                dstport = row['dstport'].strip().lower()
                protocol = row['protocol'].strip().lower()
                tag = row['tag'].strip()
                self.lookup_table[(dstport, protocol)] = tag


    def parse_flow_logs(self):
        """
        Parses the flow log file, counts the occurrences of each tag and each port/protocol combination,
        and returns two dictionaries, tag_counts and port_protocol_counts
        """
        tag_counts = defaultdict(int)
        port_protocol_counts = defaultdict(int)

        for line in open(self.flow_logs_file_path, 'r'):
            line_parts = line.split()
            dstport = line_parts[6].strip().lower()
            protocol_number = line_parts[7].strip()

            protocol = self.protocol_numbers_map.get(protocol_number, 'unknown')
            port_protocol_counts[(dstport, protocol)] += 1

            tag = self.lookup_table.get((dstport, protocol), 'Untagged')
            tag_counts[tag] += 1
            
        return tag_counts, port_protocol_counts


    def write_tag_counts(self, tag_counts):
        """
        writes tag counts to file
        """
        with open(self.tag_counts_output_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Tag", "Count"])
            for tag, count in tag_counts.items():
                writer.writerow([tag, count])


    def write_port_protocol_counts(self, port_protocol_counts):
        """
        writes port protocol counts to file
        """
        with open(self.port_protocol_counts_output_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Port", "Protocol", "Count"])
            for (port, protocol), count in port_protocol_counts.items():
                writer.writerow([port, protocol, count])


    def run(self):
        self.parse_protocol_numbers()
        self.parse_lookup_table()
        tag_count, port_protocol_count = self.parse_flow_logs()
        self.write_tag_counts(tag_count)
        self.write_port_protocol_counts(port_protocol_count)

        
def main():
    lookup_table_file_path = 'lookup_table.csv'
    flow_logs_file_path = 'flow_logs.txt'
    tag_counts_output_file_path = 'tag_counts.csv'
    port_protocol_counts_output_file_path = 'port_protocols_counts.csv'
    protocol_numbers_file_path = 'protocol_numbers.csv'
    parser = FlowLogParser(lookup_table_file_path, flow_logs_file_path, tag_counts_output_file_path, \
                            port_protocol_counts_output_file_path, protocol_numbers_file_path)
    parser.run()



if __name__ == '__main__':
    main()