def nvl(obj:dict,key:str,default=None,dataType=None):
    '''
    function takes an object an key and returns the value of it. If the key does not exist, default is returned.
    if function gets a type, the returned value is casted to this datatype

    :param obj: a dictionary
    :param key: the of the value which should be returned
    :param default: optional - default value if the key does not exist. None per default.
    :param dataType: optional - the data type in which the value should be casted. None per default, no casting is done.

    :return: value of the key in obj
    '''
    if key in obj:
        res = obj[key]
    else:
        res = default
        
    if dataType is None or res is None:
        return res
    else:
        return dataType(res)