from json import encoder
from packet import Packet
import json
from dataBase import DataBase

db = DataBase()


def deserialize(p: Packet):
    if p._pid == 9092:
        return deserialize_ChatServerMessage(p)
    elif p._pid == 3091:
        return deserialize_ExchangeStartedBidBuyerMessage(p)
    return False


def deserialize_ChatServerMessage(p: Packet):
    return {
        "pid": p._pid,
        "type": 'ChatServerMessage',
        "length": p._len,
        "channel": p.readByte(),
        "content": p.readUTF(),
        "timestamp": p.readUnsignedInt(),
        "fingerprint": p.readUTF(),
        "senderId": p.readDouble(),
        "senderName": p.readUTF(),
        "prefix": p.readUnsignedShort(),
        "senderAccountId": p.readUnsignedInt()
    }


def deserialize_ExchangeStartedBidBuyerMessage(p: Packet):
    quantitiesLen = p.readUnsignedShort()
    quantities = []
    for _ in range(quantitiesLen):
        quantities.append(p.readVarInt())

    typesLen = p.readUnsignedShort()
    types = []
    for _ in range(typesLen):
        type_id = p.readVarInt()
        types.append(db.getTypeName(type_id))

    return {
        "pid": p._pid,
        "type": 'ExchangeStartedBidBuyerMessage',
        "length": p._len,
        "quantities": quantities,
        "types": types,
        "taxPercentage": p.readFloat(),
        "taxModificationPercentage": p.readFloat(),
        "maxItemLevel": p.readUnsignedByte(),
        "maxItemPerAccount": p.readVarInt(),
        "ncpContextualId": p.readUnsignedInt(),
        "unsoldDelay": p.readVarShort(),
    }


# Teste :

if __name__ == "__main__":
    chat = Packet(
        "8e118906006372656372757465206b6f7272692073636f7265203330322063726120686162697475c3a92066756c6c206368616c6c206e6f206661696c20657420636f6d626174207261706969696964652c2036356b2f636d6274203220706c61637320646973706f6144f1e100086436646d707139724252364e403480000005536967656500000933b11d"
    )
    started_bid = Packet(
        "304d710003010a6400422e2f3035363738393a3b410f446768696a6b6d6e6f779901a401c301b2012223242627282932333c3f42464754575f60626c9801a701b301b601b701b901db01e401e501af019e019f01a001a101a201a301e701e801ee01f101400000003f8000003c04ffffffffa005304d710003010a6400422e2f3035363738393a3b410f446768696a6b6d6e6f779901a401c301b2012223242627282932333c3f42464754575f60626c9801a701b301b601b701b901db01e401e501af019e019f01a001a101a201a301e701e801ee01f101400000003f8000003c04ffffffffa0054128"
    )

    # print(json.dumps(deserialize_ChatServerMessage(chat), indent=2))
    print(
        json.dumps(deserialize_ExchangeStartedBidBuyerMessage(started_bid),
                   indent=2,
                   ensure_ascii=False))
