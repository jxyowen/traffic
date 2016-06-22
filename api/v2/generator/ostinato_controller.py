__author__ = 'jxy'

from ostinato_light.drone import Drone
from ostinato_light.port_list import PortList
from ostinato_light.stream_list import StreamList
from ostinato_light.protocols import *
import time

tx_port_number = 0
tx_port_list = PortList()
tx_port_list.add_port(port_number=tx_port_number)

host_name = '10.10.20.38'
traffic_server = '172.19.50.125'
local_host = '127.0.0.1'
drone = Drone(host_name=local_host, tx_port_list=tx_port_list)

is_drone_started_up = False
while not is_drone_started_up:
    try:
        drone.connect()
        is_drone_started_up = True
    except:
        print('Drone has not been started up, wait for 10 seconds ...')
        time.sleep(10)

port_config_list = drone.get_port_config_list().port
print(port_config_list)
drone.disconnect()

while True:
    try:
        for port in port_config_list:
            print('%d.%s (%s)' % (port.port_id.id, port.name, port.description))

            tx_port_number = port.port_id.id
            tx_port_list = PortList()
            tx_port_list.add_port(port_number=tx_port_number)
            tx_port = tx_port_list.current_port

            print('port_number=' + str(tx_port_number))


            stream_list = StreamList(tx_port=tx_port, is_loop_mode=True)


            # stream_list.add_stream(is_stream_packet_size_random_mode=True,
            #                          stream_packet_size_random_min_bytes=800,
            #                          stream_packet_size_random_max_bytes=1200,
            #                          stream_packet_num=1000,
            #                          stream_packets_per_second=100)
            stream_list.current_stream.configure_protocols(MAC(src_mac='ab:cd:ef:11:00:22',
                                                                dst_mac='00:11:22:33:44:55',
                                                                src_mac_mode=Enum.MAC_ADDRESS_MODE_FIEXD),
                                                            Ethernet(),
                                                            IP4(src_ip='10.10.20.38',
                                                                dst_ip='10.10.20.39'),
                                                            IGMP(type=0xfe11,
                                                                 group_address=IGMPIPAddress(v4='222.168.10.22'),
                                                                 sources=[IGMPIPAddress(v4='111.168.10.22'), IGMPIPAddress(v4='29.168.10.22')]),
                                                            )
            #
            # stream_list.add_stream(is_stream_packet_size_random_mode=True,
            #                          stream_packet_size_random_min_bytes=800,
            #                          stream_packet_size_random_max_bytes=1200,
            #                          stream_packet_num=100,
            #                          stream_packets_per_second=100)
            # stream_list.current_stream.configure_protocols(MAC(src_mac='ab:cd:ef:11:00:22',
            #                                                     dst_mac='00:11:22:33:44:55',
            #                                                     src_mac_mode=Enum.MAC_ADDRESS_MODE_FIEXD),
            #                                                 Ethernet(),
            #                                                 IP4(src_ip='10.10.20.38',
            #                                                     dst_ip='10.10.20.39'),
            #                                                 TCP(src_port=77,
            #                                                     dst_port=90),
            #                                                 )
            #
            # stream_list.add_stream(stream_average_bps=1000*20)
            # stream_list.current_stream.configure_protocols(MAC(src_mac='FE:DC:BA:99:88:77',
            #                                                     dst_mac='55:Ab:2E:ff:dd:ee',
            #                                                     src_mac_mode=Enum.MAC_ADDRESS_MODE_FIEXD),
            #                                                 Ethernet(),
            #                                                 IP4(src_ip='10.10.20.38',
            #                                                     dst_ip='10.10.20.39'),
            #                                                 TCP(src_port=7337,
            #                                                     dst_port=3903),
            #                                                 )
            #
            # stream_list.add_stream(stream_average_bps=1000*60)
            # stream_list.current_stream.configure_protocols(MAC(src_mac='FE:DC:BA:99:88:77',
            #                                                     dst_mac='55:Ab:2E:ff:dd:ee',
            #                                                     src_mac_mode=Enum.MAC_ADDRESS_MODE_FIEXD),
            #                                                 Ethernet(),
            #                                                 IP4(src_ip='10.10.20.38',
            #                                                     dst_ip='10.10.20.39'),
            #                                                 UDP(src_port=1233,
            #                                                     dst_port=3221),
            #                                                 )
            #
            # stream_list.add_stream(stream_average_bps=1000*30)
            # stream_list.current_stream.configure_protocols(MAC(src_mac='FE:DC:BA:99:88:77',
            #                                                     dst_mac='55:Ab:2E:ff:dd:ee',
            #                                                     src_mac_mode=Enum.MAC_ADDRESS_MODE_FIEXD),
            #                                                 Ethernet(),
            #                                                 ARP(sender_hw_addr='ab:cd:ef:11:00:22', sender_proto_addr='122.168.10.22',
            #                                                 target_hw_addr='00:11:22:33:44:55', target_proto_addr='177.168.10.32',
            #                                                 op_code=0),
            #                                                 )
            #
            # stream_list.add_stream(stream_average_bps=1000*30)
            # stream_list.current_stream.configure_protocols(MAC(src_mac='FE:DC:BA:99:88:77',
            #                                                     dst_mac='55:Ab:2E:ff:dd:ee',
            #                                                     src_mac_mode=Enum.MAC_ADDRESS_MODE_FIEXD),
            #                                                 Ethernet(),
            #                                                 IP4(src_ip='10.10.20.38',
            #                                                     src_ip_mask='255.255.255.0',
            #                                                     src_ip_mode=Enum.IP4_ADDRESS_MODE_RANDOM,
            #                                                     dst_ip='10.10.20.39'),
            #                                                 ICMP()
            #                                                 )

            stream_list.add_stream(stream_average_bps=1024*1024*1000,
                                    stream_packet_size_bytes=150,
                                    stream_duration_second=5)
            stream_list.current_stream.configure_protocols(MAC(src_mac='FE:DC:BA:99:88:77',
                                                                dst_mac='55:Ab:2E:ff:dd:ee',
                                                                src_mac_mode=Enum.MAC_ADDRESS_MODE_FIEXD),
                                                            Ethernet(),
                                                            IP4(src_ip='10.10.20.38',
                                                                src_ip_mask='255.255.255.0',
                                                                src_ip_mode=Enum.IP4_ADDRESS_MODE_RANDOM,
                                                                dst_ip='10.10.20.39'),
                                                            TCP(),
                                                            TextProtocol(text='GET /index.html HTTP/1.1\x0aconnection: close\x0aHost: www.google.cn\x0a\x0a',
                                                                         eol=Enum.TEXT_PROTOCOL_END_OF_LINE_CRLF),
                                                            HexDump(content='\x124Vx\xad\xef\xdf"E4\xed\xdf\xad#B?\xdf\xdf#'),
                                                            )

            is_drone_started_up = False
            while not is_drone_started_up:
                try:
                    drone.connect()
                    is_drone_started_up = True
                except:
                    print('Drone has not been started up, wait for 10 seconds ...')
                    time.sleep(10)

            # for port in drone.get_port_config_list().port:
            #     print('%d.%s (%s)' % (port.port_id.id, port.name, port.description))
                # if port.name == target_port_name:




            drone.stop_transmit()
            drone.add_stream_list(stream_list)
            # drone.tx_port_start_capture()

            drone.start_transmit()
            drone.wait_for_transmission_complete(time_out=10)
            drone.stop_transmit()
            drone.remove_current_stream_list()
            # drone.tx_port_stop_capture()
            # drone.fetch_capture_buffer_tx_port()
            drone.disconnect()
    except:
        pass
