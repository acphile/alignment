key_dic = {
    "default": ['A', 'C', 'T', 'G', '-']
}

def default_score(keys=None):
    if "-" not in keys:
        keys.append("-")
    default_delta = {}
    for i in range(len(keys)):
        default_delta[keys[i]] = {k : v for (k,v) in zip(keys, [1 if keys[i] == keys[j]  else -1 for j in range(len(keys))])}
    return default_delta