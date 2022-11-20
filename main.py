import argparse
from utils import *
from method import global_align, block_align4, fast4
import time 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="")
    parser.add_argument("--method", type=str, default="global")
    parser.add_argument("--x", type=str, default="")
    parser.add_argument("--y", type=str, default="")
    parser.add_argument("--t", type=int, default=4)
    parser.add_argument("--score", type=str, default="")
    parser.add_argument("--alpha", type=str, default=None)
    parser.add_argument("--key", type=str, default="default")
    args = parser.parse_args()

    if args.file=="":
        assert args.x!="" and args.y!=""
        str1 = args.x
        str2 = args.y
    else:
        raise NotImplemented
    keys = key_dic[args.key]
    if args.score == "":
        delta = default_score(keys)
    else:
        raise NotImplemented

    t1 = time.time()
    if args.method == "global":
        print(global_align(str1, str2, delta))
    elif args.method == "block":
        print(block_align4(str1, str2, delta, keys, args.t, args.alpha))
    elif args.method == "fast":
        print(fast4(str1, str2, delta, keys, args.t))
    print(time.time()-t1)