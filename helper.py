def getProtocolIds(filename):
    protocol_ids_file = open(filename, 'r')
    protocol_ids = dict()
    for line in protocol_ids_file.readlines():
        line = line.split(':')
        protocol_ids[int(line[0])] = line[1][:-1]
    return protocol_ids