import pyshark
import socket
import sys
import json
from dataBase import DataBase
from packet import Packet
from deserializer import deserialize

# CONFIG

WHITELIST = [
    'ExchangeTypesItemsExchangerDescriptionForUserMessage',
    'ExchangeTypesExchangerDescriptionForUserMessage',
    'ExchangeStartedBidBuyerMessage', 'ObjectAveragePricesMessage'
]
# WHITELIST = ['ChatServerMessage']
BLACKLIST = [
    'GameMapMovementMessage',
    'GameMapChangeOrientationMessage',
    'GameRolePlayShowActorMessage',
    'GameMapMovementRequestMessage',
    'UpdateMapPlayersAgressableStatusMessage',
]

USE_WHITELIST = '-wl' in sys.argv
USE_BLACKLIST = '-bl' in sys.argv

# END CONFIG

db = DataBase()
print('ids loaded')
capture = pyshark.LiveCapture(interface='Ethernet',
                              bpf_filter='tcp port 5555 and len > 66')
print('pyshark connected')

for packet in capture.sniff_continuously():
    if not hasattr(packet, 'data') or not hasattr(packet.data, 'data'):
        continue
    p = Packet(packet.data.data)
    receiving: bool = packet.ip.src == socket.gethostbyname(
        socket.gethostname())
    prefix = "<- " if receiving else "-> "

    if p._pid in db._protocolId:
        pid_type = db._protocolId[p._pid]
        if USE_BLACKLIST and pid_type in BLACKLIST: continue
        if USE_WHITELIST and pid_type not in WHITELIST: continue

        obj = deserialize(p)
        if obj is not False:
            print("%s %s\n%s" %
                  (prefix, p._init_data, json.dumps(obj, indent=2)))
        else:
            print("%s [id:%s] [type:%s] %s" %
                  (prefix, p._pid, pid_type, p._init_data))
    else:
        print("ERR: NOT FOUND PID : %s" % (p._pid))