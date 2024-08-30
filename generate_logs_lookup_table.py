import random
import time
import string
from datetime import datetime
from flow_log_parser import FlowLogParser

def generate_flow_log_entry():
    #Function to generate a random log entry in version 2 format
    version = 2
    account_id = random.randint(100000000000, 999999999999)
    interface_id = 'eni-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    srcaddr = '.'.join(str(random.randint(0, 255)) for i in range(4))
    dstaddr = '.'.join(str(random.randint(0, 255)) for i in range(4))
    srcport = random.randint(1, 65535) #max port number
    dstport = random.randint(1, 65535)
    protocol = random.randint(0, 145) #146-255 are unassigned/reserved
    packets = random.randint(1, 10000)
    bytes_transferred = packets * random.randint(100, 1500) #estimate of avg bytes/packet
    start = int(time.time())
    end = start + random.randint(1, 60)
    action = random.choice(["ACCEPT", "REJECT"])
    log_status = "OK"

    flow_log_entry = (
        f"{version} {account_id} {interface_id} {srcaddr} {dstaddr} "
        f"{srcport} {dstport} {protocol} {packets} {bytes_transferred} "
        f"{start} {end} {action} {log_status}\n"
    )

    return flow_log_entry


def generate_flow_logs(log_file_path, num_entries):
    with open(log_file_path, 'w', newline='') as file:
        for i in range(num_entries):
            file.write(generate_flow_log_entry())
        return 


def generate_lookup_table(lookup_table_path, protocol_numbers_map, num_entries):
    with open(lookup_table_path, 'w', newline='') as file:
        file.write("dstport,protocol,tag\n")
        for i in range(0, num_entries):
            port = random.randint(1, 65535)
            protocol_number = random.randint(0, 145)
            file.write("{},{},{}\n".format(port, protocol_numbers_map.get(str(protocol_number), 'unknown'), \
                        random.choice(["sv_P1", "sv_P2", "sv_P3", "sv_P4", "sv_P5", "email"])))


if __name__ == "__main__":
    log_file_path = 'flow_logs_big.txt'
    generate_flow_logs(log_file_path, 100000)

    parser = FlowLogParser('','','','','protocol_numbers.csv')
    parser.parse_protocol_numbers()
    lookup_table_path = 'lookup_table_big.csv'
    generate_lookup_table(lookup_table_path, parser.protocol_numbers_map, 15000)
