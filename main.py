import pyshark
import socket
import sys
from helper import getHeader, getProtocolIds

# CONFIG #

WHITELIST = [
    'ExchangeTypesItemsExchangerDescriptionForUserMessage',
    'ExchangeTypesExchangerDescriptionForUserMessage',
    'ExchangeStartedBidBuyerMessage', 'ObjectAveragePricesMessage'
]
BLACKLIST = [
    'GameMapMovementMessage',
    'GameMapChangeOrientationMessage',
    'GameRolePlayShowActorMessage',
    'GameMapMovementRequestMessage',
    'UpdateMapPlayersAgressableStatusMessage',
]

USE_WHITELIST = '-wl' in sys.argv
USE_BLACKLIST = '-bl' in sys.argv

# END CONFIG #

protocol_ids = getProtocolIds("protocolIds.txt")
print('ids loaded')
capture = pyshark.LiveCapture(interface='Ethernet',
                              bpf_filter='tcp port 5555 and len > 66')
print('pyshark connected')

for packet in capture.sniff_continuously():
    if not hasattr(packet, 'data') or not hasattr(packet.data, 'data'):
        continue
    data = packet.data.data
    receiving: bool = packet.ip.src == socket.gethostbyname(
        socket.gethostname())
    prefix = "<- " if receiving else "-> "

    pid = getHeader(data)[0]
    if pid in protocol_ids:
        pid_type = protocol_ids[pid]
        if USE_BLACKLIST and pid_type in BLACKLIST: continue
        if USE_WHITELIST and pid_type not in WHITELIST: continue

        # SCAN HERE

        print("%s [id:%s] [type:%s] %s" % (prefix, pid, pid_type, data))
    else:
        print("err NOT FOUND PID : %s" % (pid))