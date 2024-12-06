from . import bech32
from . import base58

def int2bytes(i:int, enc, length=None):
    if length == None:
        length = (i.bit_length() + 7) // 8

    return i.to_bytes(length, enc)

def int2hex(i:int, enc, cntBytes=None):
    res = int2bytes(i, enc).hex()
    if cntBytes is not None:
        missingBytes = int(cntBytes - len(res)/2)
        if missingBytes < 0:
            return res
    else:
        missingBytes = 0
    
    if enc == 'little':
        return res + ('00' * missingBytes)
    elif enc == 'big':
        return ('00' * missingBytes) + res
    else:
        return res

def convert_hex(str, enc1, enc2):
    '''
    Convert Hex String from enc1 or enc2: e.g. little (Endian) to big (Endian)
    '''
    return int2bytes(int.from_bytes(bytes.fromhex(str), enc1), enc2).hex()

def hexToString(hex):
    if hex[:2] == '0x':
        hex = hex[2:]
    stringValue = bytes.fromhex(hex).decode('utf-8')
    return stringValue

def stringToHex(string):
    hex = string.encode('utf-8').hex()
    if hex[:2] == '0x':
        hex = hex[2:]
    return hex

def generateSequence(hex:str,locktime=0,replacable=False):
    if replacable:
        reducer = 2
    elif locktime > 0:
        reducer = 1
    else:
        reducer = 0

    return int2hex(int(convert_hex(hex,'little','big'),16) - reducer,'little',4)

def encodeBech32AddressToHex(address):
    '''
    DefiChain related Bech32 Encoded Address to Hex.
    '''
    hrp = address.split('1')[0]
    witnessVersion,witnessProgram = bech32.decode(hrp,address)
    # Address MUST be BECH32: Then witnessVersion and witnessProgramm have 22 Bytes together
    res = f'{22:02x}' + f'{witnessVersion:02x}' + f'{len(witnessProgram):02x}'

    for w in witnessProgram:
        res = res + f'{w:02x}'

    return res

def decodeHexToAddress(hex,addressType,addressVersion):
    if addressType == 'bech32':
        witnessVersion = int(addressVersion,16)
        witnessProgram = []
        addressHex = hex
        for i in range(0,int(len(addressHex)/2)):
            witnessProgram.append(int(addressHex[i*2:i*2+2],16))
        #witnessProgram = hex[4:]

        return bech32.encode('df',witnessVersion,witnessProgram)
    elif addressType == 'base58':
        # Add Version 90 (https://bitcoin.stackexchange.com/questions/36623/what-version-byte-will-produce-a-base58-encoding-starting-with-x) Adds "d" to the beginning
        return base58.b58encode_chk(bytes.fromhex(int2hex(addressVersion,'little') + hex))
    else:
        return None