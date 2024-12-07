import json
import requests
from .defichainUtils import utils,customTxDecode

class Node:
    def __init__(self,nodeURL, nodeUser=None, nodePassword=None) -> None:
        self.nodeURL = nodeURL
        self.nodeUser = nodeUser
        self.nodePassword = nodePassword

    def rpc(self, method, params=None, silentErrors=False):
        if params is None:
            params = []
        data = json.dumps({
            "jsonrpc": "2.0",
            "id": "meBe",
            "method": method,
            "params": params
        })
        if self.nodeUser is None:
            result = requests.post(self.nodeURL, auth=(self.nodeUser, self.nodePassword), data=data)
        else:
            result = requests.post(self.nodeURL, data=data)

        return result.json()['result']


def decodeCustomTx(hex:str):
    expectedOPReturn = hex[:2]
    
    hexLength=hex[2:4]
    if hexLength == '4c':
        hexLength = hexLength=hex[4:6]
        DfTxStart = 6
    elif hexLength == '4d':
        hexLength = utils.convert_hex(hex[4:8],'little','big')
        DfTxStart = 8
    else:
        DfTxStart = 4
    expectedDfMarker = hex[DfTxStart:DfTxStart + 8]

    #hexLengthV2=hex[4:6]
    #expectedDfTxMarkerV2 = hex[6:14]
    if expectedOPReturn != '6a':
        # TODO: Raise Error
        return {
            'error': 1,
            'msg': 'Missing key word for OP_RETURN'
        }
    if expectedDfMarker == utils.stringToHex('DfTx'):
        hex = hex[DfTxStart + 8:] 
    elif expectedDfMarker == utils.stringToHex('DfAf'):
        hex = hex[DfTxStart + 8:] 
    elif expectedDfMarker == utils.stringToHex('DfAP'):
        hex = hex[DfTxStart + 8:] 
    elif expectedDfMarker == utils.stringToHex('DfTS'):
        hex = hex[DfTxStart + 8:] 
    else:
        # TODO: Raise Error
        return {
            'error': 1,
            'msg': 'Missing key word for Marker'
        }

    if int(hexLength,16) != int(len(hex)/2) + len('DfTx'):
        # TODO: Raise Error
        return {
            'error': 1,
            'msg': 'Indicated length in hex string does fit string length'
        }
    return customTxDecode.decodeCustomTx(hex,expectedDfMarker)

if __name__ == '__main__':
    res = decodeCustomTx("6a4c4f446654786101160014d031c58e3ec9b466d372c6d03f8caa897162894a0101000000610b1d000000000001160014fa0d4d207b8cba79c1e07849621b624a1889b2480101000000610b1d0000000000")
    print(2)
