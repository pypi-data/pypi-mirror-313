"""
* Written by CK
"""
from copy import deepcopy
import sys

def deepmerge(
    dict1: dict,
    dict2: dict
) -> dict:
    new_dict = deepcopy( dict1 )

    for key, val in dict2.items():

        if key not in new_dict.keys():
            new_dict[ key ] = val
            continue

        dict1_val = new_dict[ key ]
        if isinstance( val, dict ):

            if not isinstance( dict1_val, dict ):
                print( '[error] ckplotlib.deepmerge' )
                print( f'dict2[key] is dict, but dict1[key] is not dict.' )
                sys.exit(1)

            new_dict[ key ] = deepmerge(
                dict1 = dict1_val,
                dict2 = val
            )
        else:
            new_dict[ key ] = val

    return new_dict
