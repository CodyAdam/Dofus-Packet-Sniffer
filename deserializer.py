from json import encoder
from packet import Packet
import json
from dataBase import DataBase

db = DataBase()


def deserialize(p: Packet):
    if p._pid == "9092":
        return deserialize_ChatServerMessage(p)
    elif p._pid == "3091":
        return deserialize_ExchangeStartedBidBuyerMessage(p)
    elif p._pid == "234":
        return deserialize_ExchangeTypesExchangerDescriptionForUserMessage(p)
    elif p._pid == "6162":
        return deserialize_ExchangeTypesItemsExchangerDescriptionForUserMessage(
            p)
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


def deserialize_ExchangeTypesExchangerDescriptionForUserMessage(p: Packet):
    objectType = p.readInt()

    typeDescriptionLen = p.readUnsignedShort()
    typeDescription = []
    for i in range(typeDescriptionLen):
        typeDescription.append(db.getItemName(p.readVarInt()))

    return {
        "pid": p._pid,
        "type": 'ExchangeTypesExchangerDescriptionForUserMessage',
        "length": p._len,
        "objectType": objectType,
        "typeDescriptionLen": typeDescriptionLen,
        "typeDescription": typeDescription,
    }


def deserialize_ExchangeTypesItemsExchangerDescriptionForUserMessage(
        p: Packet):
    objectType = p.readInt()

    itemTypeDescriptionsLen = p.readUnsignedShort()
    itemTypeDescriptions = []
    for i in range(itemTypeDescriptionsLen):
        objectUID = p.readVarInt()
        objectGID = p.readVarShort()
        objectType2 = p.readInt()
        effectsLen = p.readUnsignedShort()
        effects = []
        for j in range(effectsLen):
            id = p.readUnsignedShort()
            actionId = p.readVarShort()
            ## TODO ProtocolTypeManager.getInstance(ObjectEffect,_id4)
            objectEffect = {
                "id": id,
                "actionId": actionId,
            }
            effects.append(objectEffect)
        pricesLen = p.readUnsignedShort()
        prices = []
        for j in range(pricesLen):
            prices.append(p.readVarLong())

        bidExchangerObjectInfo = {
            "objectUID": objectUID,
            "objectGID": objectGID,
            "objectType": objectType2,
            "effectsLen": effectsLen,
            "effects": effects,
            "pricesLen": pricesLen,
            "prices": prices,
        }
        itemTypeDescriptions.append(bidExchangerObjectInfo)

    return {
        "pid": p._pid,
        "type": 'ExchangeTypesExchangerDescriptionForUserMessage',
        "length": p._len,
        "objectType": objectType,
        "itemTypeDescriptionsLen": itemTypeDescriptionsLen,
        "itemTypeDescriptions": itemTypeDescriptions,
    }


# Teste :

if __name__ == "__main__":
    chat = Packet(
        "8e118906006372656372757465206b6f7272692073636f7265203330322063726120686162697475c3a92066756c6c206368616c6c206e6f206661696c20657420636f6d626174207261706969696964652c2036356b2f636d6274203220706c61637320646973706f6144f1e100086436646d707139724252364e403480000005536967656500000933b11d"
    )
    started_bid = Packet(
        "304d710003010a6400422e2f3035363738393a3b410f446768696a6b6d6e6f779901a401c301b2012223242627282932333c3f42464754575f60626c9801a701b301b601b701b901db01e401e501af019e019f01a001a101a201a301e701e801ee01f101400000003f8000003c04ffffffffa005304d710003010a6400422e2f3035363738393a3b410f446768696a6b6d6e6f779901a401c301b2012223242627282932333c3f42464754575f60626c9801a701b301b601b701b901db01e401e501af019e019f01a001a101a201a301e701e801ee01f101400000003f8000003c04ffffffffa0054128"
    )

    item = Packet(
        "60491b000000280001e2e609ec050000002800000003ef0d9a9c0195dd084128")

    # print(json.dumps(deserialize_ChatServerMessage(chat), indent=2))
    print(
        json.dumps(
            deserialize_ExchangeTypesItemsExchangerDescriptionForUserMessage(
                started_bid),
            indent=2,
            ensure_ascii=False))
