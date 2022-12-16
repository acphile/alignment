from method import global_align, block_align4, fast4
from utils import *
import argparse
import numpy as np
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
    length = 500

    keys = key_dic[args.key]
    if args.score == "":
        delta = default_score(keys)
    else:
        raise NotImplemented
    
    f = open("./data.txt")
    seq = []
    line = f.readline()
    while line:
        # seq.append(str(line[:-1]))
        seq.append(str(line[:length]))
        line = f.readline()
    f.close()
    
    score_g = []
    t1 = time.time()
    for i in range(len(seq)):
        for j in range(i, len(seq)):
            score_g.append(global_align(seq[i], seq[j], delta))
    print("global: time=%.2fs, score=%d" % (time.time() - t1, np.mean(score_g)))

    score_b = []
    t = 2
    t1 = time.time()
    for i in range(len(seq)):
        for j in range(i, len(seq)):
            score_b.append(block_align4(seq[i], seq[j], delta, keys, t, args.alpha))
    print("block: time=%.2fs, score=%d" %  (time.time() - t1, np.mean(score_b)))

    
    score_f = []
    t = 2
    t1 = time.time()
    for i in range(len(seq)):
        for j in range(i, len(seq)):
            score_f.append(fast4(seq[i], seq[j], delta, keys, t))
    print("fast: time=%.2fs, score=%d" % (time.time() - t1, np.mean(score_f)))
