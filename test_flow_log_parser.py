import unittest
from unittest.mock import mock_open, patch
from io import StringIO
from flow_log_parser import FlowLogParser

class TestFlowLogParser(unittest.TestCase):
    def setUp(self):
        self.lookup_table_file_path = 'lookup_table.csv'
        self.flow_logs_file_path = 'flow_logs.txt'
        self.tag_counts_output_file_path = 'tag_counts.csv'
        self.port_protocol_counts_output_file_path = 'port_protocols_counts.csv'
        self.protocol_numbers_file_path = 'protocol_numbers.csv'
        self.parser = FlowLogParser(
            self.lookup_table_file_path,
            self.flow_logs_file_path,
            self.tag_counts_output_file_path,
            self.port_protocol_counts_output_file_path,
            self.protocol_numbers_file_path
        )


    @patch('builtins.open', new_callable=mock_open)
    def test_parse_protocol_numbers(self, mock_file):
        protocol_content = """Decimal,Keyword
                                6,tcp
                                17,udp
                                1,icmp
                                """
        mock_file.return_value = StringIO(protocol_content)
        self.parser.parse_protocol_numbers()

        expected_protocol_map = {
            '6': 'tcp',
            '17': 'udp',
            '1': 'icmp'
        }

        self.assertEqual(self.parser.protocol_numbers_map, expected_protocol_map)


    @patch('builtins.open', new_callable=mock_open)
    def test_parse_lookup_table(self, mock_file):
        lookup_content = """dstport,protocol,tag
                            25,tcp,sv_P1 
                            68,udp,sv_P2 
                            23,tcp,sv_P1 
                            31,udp,SV_P3 
                            443,tcp,sv_P2 
                            22,tcp,sv_P4 
                            3389,tcp,sv_P5 
                            0,icmp,sv_P5 
                            110,tcp,email 
                            993,tcp,email 
                            143,tcp,email 
                            """
        mock_file.return_value = StringIO(lookup_content)
        self.parser.parse_lookup_table()

        expected_lookup_table = {
            ('25', 'tcp'): 'sv_P1', ('68', 'udp'): 'sv_P2', ('23', 'tcp'): 'sv_P1', 
            ('31', 'udp'): 'SV_P3', ('443', 'tcp'): 'sv_P2', ('22', 'tcp'): 'sv_P4', 
            ('3389', 'tcp'): 'sv_P5', ('0', 'icmp'): 'sv_P5', ('110', 'tcp'): 'email',
            ('993', 'tcp'): 'email', ('143', 'tcp'): 'email'
        }
        self.assertEqual(self.parser.lookup_table, expected_lookup_table)


    @patch('builtins.open', new_callable=mock_open)
    def test_parse_flow_logs(self, mock_file):
        flow_logs_content = """2 123456789012 eni-1a2b3c4d 10.0.1.102 172.217.7.228 1030 443 6 8 4000 1620140661 1620140721 ACCEPT OK 
                                2 123456789012 eni-5f6g7h8i 10.0.2.103 52.26.198.183 56000 23 6 15 7500 1620140661 1620140721 REJECT OK 
                                2 123456789012 eni-9k10l11m 192.168.1.5 51.15.99.115 49321 25 6 20 10000 1620140661 1620140721 ACCEPT OK 
                                """
        mock_file.return_value = StringIO(flow_logs_content)

        self.parser.protocol_numbers_map = {
            '6': 'tcp',
            '17': 'udp',
            '1': 'icmp'
        }
        self.parser.lookup_table = {
            ('25', 'tcp'): 'sv_P1', ('68', 'udp'): 'sv_P2', ('23', 'tcp'): 'sv_P1', 
            ('31', 'udp'): 'SV_P3', ('443', 'tcp'): 'sv_P2', ('22', 'tcp'): 'sv_P4', 
            ('3389', 'tcp'): 'sv_P5', ('0', 'icmp'): 'sv_P5', ('110', 'tcp'): 'email',
            ('993', 'tcp'): 'email', ('143', 'tcp'): 'email'
        }
        tag_counts, port_protocol_counts = self.parser.parse_flow_logs()
        
        expected_tag_counts = {
            'sv_P2': 1,
            'sv_P1': 2
        }
        expected_port_protocol_counts = {
            ('443', 'tcp'): 1,
            ('23', 'tcp'): 1, 
            ('25', 'tcp'): 1
        }

        self.assertEqual(tag_counts, expected_tag_counts)
        self.assertEqual(port_protocol_counts, expected_port_protocol_counts)


    @patch('builtins.open', new_callable=mock_open)
    def test_write_tag_counts(self, mock_file):
        tag_counts = {
            'sv_P2': 1,
            'sv_P1': 2
        }

        self.parser.write_tag_counts(tag_counts)
        mock_file.assert_called_once_with(self.tag_counts_output_file_path, 'w', newline='')
        mock_file().write.assert_has_calls([
        unittest.mock.call('Tag,Count\r\n'),
        unittest.mock.call('sv_P2,1\r\n'),
        unittest.mock.call('sv_P1,2\r\n')
        ])


    @patch('builtins.open', new_callable=mock_open)
    def test_write_port_protocol_counts(self, mock_file):
        port_protocol_counts = {
            ('80', 'tcp'): 10,
            ('443', 'tcp'): 20,
            ('53', 'udp'): 5
        }

        self.parser.write_port_protocol_counts(port_protocol_counts)
        mock_file.assert_called_once_with(self.port_protocol_counts_output_file_path, 'w', newline='')
        mock_file().write.assert_has_calls([
            unittest.mock.call('Port,Protocol,Count\r\n'),
            unittest.mock.call('80,tcp,10\r\n'),
            unittest.mock.call('443,tcp,20\r\n'),
            unittest.mock.call('53,udp,5\r\n')
        ])


if __name__ == '__main__':
    unittest.main()
