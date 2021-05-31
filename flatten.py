d = {
    "a": 5,
    "b": 6,
    "c": {
        "f": 9,
        "g": {
            "m": 17,
            "n": 3
        }
    }
}

import time

def flatten(in_dict):
    need_flatten = False
    out_dict = dict()
    
    for p_key, p_value in in_dict.items():
        if isinstance(p_value, dict):
            for c_key, c_value in p_value.items():
                out_dict[p_key + '.' + c_key] = c_value
                if (isinstance(c_value, dict)):
                    need_flatten = True
        else:
            out_dict[p_key] = p_value
            continue

    if need_flatten:
        out_dict = flatten(out_dict)
        
    return out_dict
        
start_time = time.time()
print(d)
print()
print(flatten(d))
print( f'\n\n--- { ( time.time() - start_time ) } seconds ---\n' )
