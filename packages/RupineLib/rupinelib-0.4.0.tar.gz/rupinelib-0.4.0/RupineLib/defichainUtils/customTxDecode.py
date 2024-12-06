from dataclasses import asdict
from . import utils
from .CustomTx import CustomTxType

def decodeCustomTx(hex,DfMarker):
    '''
    Hex String without OP_RETURN and DfTx Marker
    ''' 
    DfMarker = utils.hexToString(DfMarker)
    if DfMarker == 'DfTx':
        functionMarker = utils.hexToString(hex[:2])
        if functionMarker == 'j':
            res = decodeSetGovVariable(hex[2:],True)
            if res != None:
                res['name'] = 'setgovheight'
        elif functionMarker == 'G':
            res = decodeSetGovVariable(hex[2:],False)
            if res != None:
                res['name'] = 'setgovvariable'
        elif functionMarker == 's':
            res = decodePoolSwap(hex[2:])
            if res != None:
                res['name'] = 'poolswap'
        elif functionMarker == 'i':
            res = decodePoolSwapV2(hex[2:])
            if res != None:
                res['name'] = 'compositeswap'
        elif functionMarker == 'Q':
            res = decodeDFIP2203(hex[2:])
            if res != None:
                res['name'] = 'dfip2203'
        elif functionMarker == 'l':
            res = decodeAddPoolLiquidity(hex[2:])
            if res != None:
                res['name'] = 'addpoolliquidity'
        elif functionMarker == 'r':
            res = decodeRemovePoolLiquidity(hex[2:])
            if res != None:
                res['name'] = 'removepoolliquidity'
        elif functionMarker == 'p':
            res = decodeCreatePoolPair(hex[2:])
            if res != None:
                res['name'] = 'createpoolpair'
        elif functionMarker == 'u':
            res = decodeUpdatePoolPair(hex[2:])
            if res != None:
                res['name'] = 'updatepoolpair'     
        elif functionMarker == 'B':
            res = decodeAccountToAccount(hex[2:])
            if res != None:
                res['name'] = 'accounttoaccount'
        elif functionMarker == 'X':
            res = decodeTakeLoan(hex[2:])
            if res != None:
                res['name'] = 'takeloan'
        elif functionMarker == 'H':
            res = decodePaybackLoan(hex[2:])
            if res != None:
                res['name'] = 'paybackloan'
        elif functionMarker == 'k':
            res = decodePaybackLoanV2(hex[2:])
            if res != None:
                res['name'] = 'paybackloanv2'
        elif functionMarker == 'a':
            res = decodeAnyAccountsToAccounts(hex[2:])
            if res != None:
                res['name'] = 'anyaccountstoaccounts'
        elif functionMarker == 'e':
            res = decodeCloseVault(hex[2:])
            if res != None:
                res['name'] = 'closevault'
        elif functionMarker == 'V':
            res = decodeVault(hex[2:])
            if res != None:
                res['name'] = 'vault'
        elif functionMarker == 'v':
            res = decodeUpdateVault(hex[2:])
            if res != None:
                res['name'] = 'updatevault'
        elif functionMarker == 'I':
            res = decodeAuctionBid(hex[2:])
            if res != None:
                res['name'] = 'auctionbid'
        elif functionMarker == 'J':
            res = decodeWithdrawFromVault(hex[2:])
            if res != None:
                res['name'] = 'withdrawfromvault'
        elif functionMarker == 'S':
            res = decodeDepositToVault(hex[2:])
            if res != None:
                res['name'] = 'deposittovault'
        elif functionMarker == 'U':
            res = decodeUTXOsToAccount(hex[2:])
            if res != None:
                res['name'] = 'utxostoaccount'          
        elif functionMarker == 'b':
            res = decodeAccountToUTXOs(hex[2:])
            if res != None:
                res['name'] = 'accounttoutxos'                    
        else:
            c = CustomTxType()
            for key, value in asdict(c).items():
                if value == functionMarker:
                    return {
                        'name': str(key).lower(),
                        'hex': hex[2:]
                    }
            return None
        return res
    elif DfMarker == 'DfTS':
        res = decodeDfTxTokenSplit(hex)
        if res != None:
            res['name'] = 'DfTS'
        return res
    else:
        return {
            'txType': DfMarker,
            'hex': hex
        }


def decodeSetGovVariable(hex,withHeight):
    # Only data part of hex string!
    govVariable = hex[2:2+2*int(hex[:2],16)]
    hex = hex[2+2*int(hex[:2],16):]
    if utils.stringToHex('ATTRIBUTES') == govVariable:
        cnt = int(hex[:2],16)
        hex = hex[2:]
        result = {
            'govvariable': 'ATTRIBUTES',
            'attributes': [],
            'hex': ''
        }
        for i in range(0,cnt):
            typeMarker = utils.hexToString(hex[8:10])
            if typeMarker in ['p']:
                variables = [
                    {'bytesCount': 1, 'key': 'type', 'type': str,'endian':None,'abort':['o']},
                    {'bytesCount': 1, 'key': 'typeId', 'type': int,'endian':None},
                    {'bytesCount': 4, 'key': 'key', 'type': str,'endian':'big'},
                    {'bytesCount': 4, 'key': 'keyId', 'type': int,'endian':'little'},
                    {'bytesCount': 4, 'key': 'minuend', 'type': int,'endian':'little'},
                    {'bytesCount': 4, 'key': 'subtractive', 'type': int,'endian':'little'}
                ]
                result['attributes'].append(searchHex(variables,hex[8:44]))
                hex = hex[44:]
            elif typeMarker in ['L']:
                variables = [
                    {'bytesCount': 1, 'key': 'type', 'type': str,'endian':None,'abort':['o']},
                    {'bytesCount': 1, 'key': 'key', 'type': str,'endian':None},
                    {'bytesCount': 4, 'key': 'keyId', 'type': int,'endian':None},
                    {'bytesCount': 4, 'key': 'unknown1', 'type': int,'endian':'little'},
                    {'bytesCount': 1, 'key': 'unknown2', 'type': int,'endian':'little'}
                ]
                result['attributes'].append(searchHex(variables,hex[8:30]))
                hex = hex[30:]
            elif typeMarker in ['o']: 
                variables = [
                    {'bytesCount': 1, 'key': 'type', 'type': str,'endian':None},
                    {'bytesCount': 1, 'key': 'typeId', 'type': str,'endian':None},
                    {'bytesCount': 7, 'key': 'unkown', 'type': 'hex','endian':None},
                    {'bytesCount': 4, 'key': 'splitType', 'type': int,'endian':None},
                    {'bytesCount': 4, 'key': 'tokenId', 'type': int,'endian':'little'},
                    {'bytesCount': 4, 'key': 'multiplier', 'type': int,'endian':'little'}
                ]
                result['attributes'].append(searchHex(variables,hex[8:50]))
                hex = hex[50:]
            elif typeMarker in ['t']: 
                variables = [
                    {'bytesCount': 1, 'key': 'type', 'type': str,'endian':None},
                    {'bytesCount': 4, 'key': 'tokenId', 'type': int,'endian':'little'},
                    {'bytesCount': 1, 'key': 'key', 'type': str,'endian':None},
                    {'bytesCount': 4, 'key': 'keyId', 'type': int,'endian':'little'},
                    {'bytesCount': 4, 'key': 'minuend', 'type': int,'endian':'little'},
                    {'bytesCount': 4, 'key': 'subtractive', 'type': int,'endian':'little'}
                ]
                result['attributes'].append(searchHex(variables,hex[8:44]))
                hex = hex[44:]

        if withHeight: 
            result['height'] = int(utils.convert_hex(hex[-8:],'little','big'),16)
            #{'bytesCount': 4, 'key': 'height', 'type': int,'endian':'little'}
        
        # variables = [
        #     {'key':'govvariable', 'bytesCount':0, 'type': 'constant', 'value': 'ATTRIBUTES','endian':None},
        #     {'key':'attributes', 'type': [
        #         {'bytesCount': 4, 'key': 'unknown', 'type': int,'endian':None},
        #         {'bytesCount': 1, 'key': 'type', 'type': str,'endian':None,'abort':['o']},
        #         {'bytesCount': 1, 'key': 'typeId', 'type': int,'endian':None},
        #         {'bytesCount': 4, 'key': 'key', 'type': str,'endian':'big'},
        #         {'bytesCount': 4, 'key': 'keyId', 'type': int,'endian':'little'},
        #         {'bytesCount': 8, 'key': 'value', 'type': int,'endian':'little'}]
        #     },
        #     {'bytesCount': 4, 'key': 'height', 'type': int,'endian':'little'}
        # ]
        return result 
    elif utils.stringToHex('ICX_TAKERFEE_PER_BTC') == govVariable:
        return {
            'govvariable': 'ICX_TAKERFEE_PER_BTC',
            'hex': hex
        }
    elif utils.stringToHex('LP_LOAN_TOKEN_SPLITS') == govVariable:
        # Anzahl der Splits
        # Token ID und % Anteil an den Rewards
        return {
            'govvariable': 'LP_LOAN_TOKEN_SPLITS',
            'hex': hex
        }
    elif utils.stringToHex('LP_SPLITS') == govVariable:
        return {
            'govvariable': 'LP_SPLITS',
            'hex': hex
        }
    elif utils.stringToHex('ORACLE_DEVIATION') == govVariable:
        return {
            'govvariable': 'ORACLE_DEVIATION',
            'hex': hex
        }
    else:
        return None

def decodePoolSwap(hex):
    variables = [
        {'key': 'from', 'type': 'address','endian':None},
        {'bytesCount':1, 'key': 'fromTokenId', 'type': int,'endian':None, 'canExceedBytesCount': True},
        {'bytesCount': 8, 'key': 'fromAmount', 'type': int,'endian':'little'},
        {'key': 'to', 'type': 'address','endian':None},
        {'bytesCount':1, 'key': 'toTokenId', 'type': int,'endian':None, 'canExceedBytesCount': True},
        {'bytesCount': 8, 'key': 'maxPriceCounter', 'type': int,'endian':'little'},
        {'bytesCount': 8, 'key': 'maxPriceDenominator', 'type': int,'endian':'little'}
    ]
    return searchHex(variables,hex)
def decodePoolSwapV2(hex):
    variables = [
        {'key': 'from', 'type': 'address','endian':None},
        {'bytesCount':1, 'key': 'fromTokenId', 'type': int,'endian':None, 'canExceedBytesCount': True},
        {'bytesCount': 8, 'key': 'fromAmount', 'type': int,'endian':'little'},
        {'key': 'to', 'type': 'address','endian':None},
        {'bytesCount':1, 'key': 'toTokenId', 'type': int,'endian':None, 'canExceedBytesCount': True},
        {'bytesCount': 8, 'key': 'maxPriceCounter', 'type': int,'endian':'little'},
        {'bytesCount': 8, 'key': 'maxPriceDenominator', 'type': int,'endian':'little'},
        {'key':'pools', 'type':
            [{'bytesCount': 1, 'type': int,'endian':None, 'canExceedBytesCount': True}]
        }
    ]
    return searchHex(variables,hex)
def decodeDFIP2203(hex):
    variables = [
        {'key': 'from', 'type': 'address','endian':None},
        {'bytesCount':1, 'key': 'fromTokenId', 'type': int,'endian':None, 'canExceedBytesCount': True},
        {'bytesCount': 8, 'key': 'fromAmount', 'type': int,'endian':'little'},
        {'bytesCount':1, 'key': 'toTokenId', 'type': int,'endian':None, 'canExceedBytesCount': True},
        {'bytesCount':4, 'key': 'direction', 'type': int,'endian':None}
    ]
    return searchHex(variables,hex)
    
def decodeAddPoolLiquidity(hex):
    variables = [
        {'key':'addresses', 'type': [
            {'key': 'from', 'type': 'address','endian':None},
            {'key': 'amounts', 'type': [
                {'bytesCount': 4,'key': 'tokenId', 'type': int,'endian':'little'},
                {'bytesCount': 8, 'key': 'amount', 'type': int,'endian':'little'}
                ]}
        ]},
        {'key': 'shareAddress', 'type': 'address','endian':None}
    ]
    return searchHex(variables,hex)
def decodeRemovePoolLiquidity(hex):
    variables = [
        {'key': 'from', 'type': 'address','endian':None},
        {'bytesCount':1, 'key': 'tokenId', 'type': int,'endian':None, 'canExceedBytesCount': True},
        {'bytesCount': 8, 'key': 'amount', 'type': int,'endian':'little'}
    ]
    return searchHex(variables,hex)
def decodeCreatePoolPair(hex):
    variables = [
        {'bytesCount':1, 'key': 'tokenIdA', 'type': int,'endian':None, 'canExceedBytesCount': True},
        {'bytesCount':1, 'key': 'tokenIdB', 'type': int,'endian':None, 'canExceedBytesCount': True},
        {'bytesCount': 8, 'key': 'commission', 'type': int,'endian':'little'},
        {'key': 'from', 'type': 'address','endian':None},
        {'bytesCount':1, 'key': 'status', 'type': int,'endian':None},
        {'key': 'customRewards', 'type': 'rest' ,'endian':None}
    ]
    return searchHex(variables,hex)
def decodeUpdatePoolPair(hex):
    variables = [
        {'bytesCount':1, 'key': 'tokenId', 'type': int,'endian':None, 'canExceedBytesCount': True},
        {'bytesCount':4, 'key': 'status', 'type': int,'endian':None},
        {'bytesCount': 8, 'key': 'commission', 'type': int,'endian':'little'},
        {'bytesCount': 'rest', 'key': 'rest', 'type': 'hex','endian':None}
    ]
    return searchHex(variables,hex)
def decodeAccountToAccount(hex):
    variables = [
        {'key': 'from', 'type': 'address','endian':None},
        {'key':'addresses', 'type': [
            {'key': 'to', 'type': 'address','endian':None},
            {'key': 'amounts', 'type': [
                {'bytesCount': 4,'key': 'tokenId', 'type': int,'endian':'little'},
                {'bytesCount': 8, 'key': 'amount', 'type': int,'endian':'little'}
                ]}
        ]}
    ]
    return searchHex(variables,hex)
def decodeTakeLoan(hex):
    variables = [
        {'bytesCount': 32,'key': 'vaultId', 'type': 'hex','endian':'little', 'keepLeadingZeros': True},
        {'key': 'to', 'type': 'address','endian':None},
        {'key': 'amounts', 'type': [
            {'bytesCount': 4,'key': 'tokenId', 'type': int,'endian':'little'},
            {'bytesCount': 8, 'key': 'amount', 'type': int,'endian':'little'}
        ]}
    ]
    return searchHex(variables,hex)
def decodePaybackLoan(hex):
    variables = [
        {'bytesCount': 32,'key': 'vaultId', 'type': 'hex','endian':'little', 'keepLeadingZeros': True},
        {'key': 'from', 'type': 'address','endian':None},
        {'key': 'amounts', 'type': [
            {'bytesCount': 4,'key': 'tokenId', 'type': int,'endian':'little'},
            {'bytesCount': 8, 'key': 'amount', 'type': int,'endian':'little'}
        ]}
    ]
    return searchHex(variables,hex)
def decodePaybackLoanV2(hex):
    variables = [
        {'bytesCount': 32,'key': 'vaultId', 'type': 'hex','endian':'little', 'keepLeadingZeros': True},
        {'key': 'from', 'type': 'address','endian':None},
        {'key': 'tokens', 'type': [
            {'bytesCount': 1,'key': 'tokenId', 'type': int,'endian':None, 'canExceedBytesCount': True},
            {'key': 'amounts', 'type': [
                {'bytesCount': 4,'key': 'tokenId', 'type': int,'endian':'little'},
                {'bytesCount': 8, 'key': 'amount', 'type': int,'endian':'little'}
            ]}
        ]}
    ]
    return searchHex(variables,hex)
def decodeAnyAccountsToAccounts(hex):
    variables = [
        {'key':'fromAddresses', 'type': [
            {'key': 'from', 'type': 'address','endian':None},
            {'key': 'amounts', 'type': [
                {'bytesCount': 4,'key': 'tokenId', 'type': int,'endian':'little'},
                {'bytesCount': 8, 'key': 'amount', 'type': int,'endian':'little'}
                ]}
        ]},
        {'key':'toAddresses', 'type': [
            {'key': 'to', 'type': 'address','endian':None},
            {'key': 'amounts', 'type': [
                {'bytesCount': 4,'key': 'tokenId', 'type': int,'endian':'little'},
                {'bytesCount': 8, 'key': 'amount', 'type': int,'endian':'little'}
                ]}
        ]}
    ]
    return searchHex(variables,hex)
def decodeCloseVault(hex):
    variables = [
        {'bytesCount': 32, 'key': 'vaultId', 'type': 'hex', 'endian':'little', 'keepLeadingZeros': True},
        {'key': 'shareAddress', 'type': 'address','endian':None}
    ]
    return searchHex(variables,hex)
def decodeUpdateVault(hex):
    variables = [
        {'bytesCount': 32, 'key': 'vaultId', 'type': 'hex', 'endian':'little', 'keepLeadingZeros': True},
        {'key': 'ownerAddress', 'type': 'address','endian':None},
        {'bytesCount': 1,'key': 'lengthLoanSchemeName', 'type': int,'endian':'little'},
        {'bytesCount': 'rest', 'key': 'loanScheme', 'type': str,'endian':None}
    ]
    return searchHex(variables,hex)
def decodeVault(hex):
    variables = [
        {'key': 'address', 'type': 'address','endian':None},
        {'bytesCount': 1,'key': 'lengthLoanSchemeName', 'type': int,'endian':'little'},
        {'bytesCount': 'rest', 'key': 'loanScheme', 'type': str,'endian':None}
    ]
    return searchHex(variables,hex)
def decodeAuctionBid(hex):
    variables = [
        {'bytesCount': 32, 'key': 'vaultId', 'type': 'hex', 'endian':'little', 'keepLeadingZeros': True},
        {'bytesCount': 4,'key': 'index', 'type': int,'endian':'little'},
        {'key': 'address', 'type': 'address','endian':None},
        {'bytesCount': 1, 'key': 'tokenId', 'type': int,'endian':'little', 'canExceedBytesCount': True},
        {'bytesCount': 8,'key': 'amount', 'type': int,'endian':'little'}
    ]
    return searchHex(variables,hex)
def decodeWithdrawFromVault(hex):
    variables = [
        {'bytesCount': 32, 'key': 'vaultId', 'type': 'hex', 'endian':'little', 'keepLeadingZeros': True},
        {'key': 'to', 'type': 'address','endian':None},
        {'bytesCount': 1, 'key': 'tokenId', 'type': int,'endian':'little', 'canExceedBytesCount': True},
        {'bytesCount': 8,'key': 'amount', 'type': int,'endian':'little'}
    ]
    return searchHex(variables,hex)
def decodeDepositToVault(hex):
    variables = [
        {'bytesCount': 32, 'key': 'vaultId', 'type': 'hex', 'endian':'little', 'keepLeadingZeros': True},
        {'key': 'from', 'type': 'address','endian':None},
        {'bytesCount': 1, 'key': 'tokenId', 'type': int,'endian':'little', 'canExceedBytesCount': True},
        {'bytesCount': 8,'key': 'amount', 'type': int,'endian':'little'}
    ]
    return searchHex(variables,hex)
def decodeUTXOsToAccount(hex):
    variables = [
        {'key': 'tx', 'type': [
            {'key': 'from', 'type': 'address','endian':None},
            {'key': 'amounts', 'type': [
                {'bytesCount': 4,'key': 'placeholder', 'type': int,'endian':'little'},
                {'bytesCount': 8,'key': 'amount', 'type': int,'endian':'little'}
            ]}
        ]}
    ]
    return searchHex(variables,hex)
def decodeAccountToUTXOs(hex):
    variables = [
        {'key': 'from', 'type': 'address','endian':None},
        {'key': 'amounts', 'type': [
            {'bytesCount': 4,'key': 'placeholder', 'type': int,'endian':'little'},
            {'bytesCount': 8,'key': 'amount', 'type': int,'endian':'little'},
            {'bytesCount': 1, 'key': 'mintingOutputStart', 'type': int,'endian':'little'}
        ]}
    ]
    return searchHex(variables,hex)


 
# NOT a DfTx Function!
def decodeDfTxTokenSplit(hex):
    variables = [
        {'bytesCount': 4, 'key': 'typeId', 'type': int,'endian':'little'},
        {'bytesCount': 4,'key': 'tokenId', 'type': int,'endian':'little'},
        {'bytesCount': 4,'key': 'multiplier', 'type': int,'endian':'little'}
    ]
    return searchHex(variables,hex)
    
def recursiveSearchHex(variable,hex):
    abort = False
    if type(variable['type']) == list:
        cnt = int(hex[:2],16)
        hex = hex[2:]
        arr = []
        for i in range(0,cnt):
            res = {}
            for idx,listVariable in enumerate(variable['type']):
                (key,value,hex,abort) = recursiveSearchHex(listVariable,hex)
                if 'abort' in variable['type'][idx] and value in variable['type'][idx]['abort']:
                    abort = True
                    break
                if key is None and idx == len(variable['type']) - 1:
                    res = value
                else:
                    res[key] = value
            arr.append(res)
        return variable['key'],arr,hex,abort
    else:
        (key,value,hex) = getValue(variable,hex)
        return key,value,hex,abort

def searchHex(variables:list,hex:str):
    res = {}
    for variable in variables:
        (key,value,hex,abort) = recursiveSearchHex(variable,hex)
        res[key] = value
        if abort:
            break
    
    if len(hex) == 0:
        res['hex'] = None
    else:
        res['hex'] = hex
    return res

def getValue(variable,hex):
    # Select subString from hex depending on length info in hex String or length info from variable input
    if variable['type'] == 'address':
        if 'key' in variable and variable['key'] == 'to' and hex[:2] == '00':
            return variable['key'],None,hex[2:]
        # START - Remove leading zeros
        while True:
            if len(hex) >= 2 and hex[:2] == '00':
                hex = hex[2:]
            else:
                break
        if len(hex) < 2:
            return None,None,None
        # END - Remove leading zeros
        hexLength = int(hex[:2],16)
        if hex[2:6] == '76a9' and hexLength == 25:
            addressType = 'base58'
            addressVersion = 18
            addressLength = int(hex[6:8],16)
            hexOfInterest = hex[8:8+2*addressLength]
            hex = hex[2+2*hexLength:]
        elif hex[2:4] == 'a9' and hexLength == 23: 
            addressType = 'base58'
            addressVersion = 90
            addressLength = int(hex[4:6],16)
            hexOfInterest = hex[6:6+2*addressLength]
            hex = hex[2+2*hexLength:]
        else:
            addressType = 'bech32'
            addressVersion = hex[2:4]
            addressLength = int(hex[4:6],16)
            hexOfInterest = hex[6:6+2*addressLength]
            hex = hex[2+2*hexLength:]
    elif variable['type'] == 'rest':
        hexOfInterest = hex
        hex = ''
    else:
        if variable['bytesCount'] == 'rest':
            hexOfInterest = hex
            hex = ''
        elif variable['bytesCount'] == 0:
            hexOfInterest = ''
        else:
            if variable['type'] == int and 'canExceedBytesCount' in variable and variable['canExceedBytesCount']:
                hexTemp = hex
                counter = 0
                while True:
                    counter += 1
                    hexCheck = hexTemp[:2*variable['bytesCount']]
                    if int(hexCheck,16) == 128:
                        hexTemp = hexTemp[2*variable['bytesCount']:]
                    else:
                        hexOfInterest = hex[:counter*2*variable['bytesCount']]
                        hex = hex[counter*2*variable['bytesCount']:]   
                        break
            else:
                hexOfInterest = hex[:2*variable['bytesCount']]
                hex = hex[2*variable['bytesCount']:]

    # Handle Endian Transformation
    hexZeros = ''
    if 'keepLeadingZeros' in variable and variable['keepLeadingZeros'] and hexOfInterest[-2:] == '00':
        counter = 0
        while True:
            search = hexOfInterest[- 2 * (counter + 1):] if counter == 0 else hexOfInterest[- 2 * (counter + 1):-2 * counter]
            if search == '00':
                hexZeros += '00'
                counter += 1
            else:
                break
    if variable['endian'] == 'big':
        hexOfInterest = hexZeros + utils.convert_hex(hexOfInterest,'big','little')
    elif variable['endian'] == 'little':
        hexOfInterest = hexZeros + utils.convert_hex(hexOfInterest,'little','big')

    # Extract Value
    if variable['type'] == int:
        if hexOfInterest == '':
            valueOfInterest = 0
        else:
            if 'canExceedBytesCount' in variable and variable['canExceedBytesCount']:
                valueOfInterest = 0
                for i in range(0,int(len(hexOfInterest)/2/variable['bytesCount'])):
                    valueOfInterest += int(hexOfInterest[i*2*variable['bytesCount']:(i+1)*2*variable['bytesCount']],16)
            else:
                valueOfInterest = int(hexOfInterest,16)
    elif variable['type'] == str:
        if hexOfInterest == '':
            valueOfInterest = hexOfInterest
        else:
            valueOfInterest = utils.hexToString(hexOfInterest)
    elif variable['type'] == 'address':
        valueOfInterest = utils.decodeHexToAddress(hexOfInterest,addressType,addressVersion)
    elif variable['type'] == 'hex':
        valueOfInterest = hexOfInterest
    elif variable['type'] == 'constant':
        valueOfInterest = variable['value']
    else:
        valueOfInterest = None
    
    if 'key' not in variable:
        return None,valueOfInterest,hex
    if variable['key'] != None:
        return variable['key'],valueOfInterest,hex
    return None,None,hex