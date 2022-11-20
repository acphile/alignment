from itertools import product
from copy import deepcopy
def global_align(v, w, delta):
    n = len(v)
    m = len(w)
    M = [[None for j in range(m+1)] for i in range(n+1)]
    M[0][0] = 0
    for i in range(n+1):
        for j in range(m+1):
            if i>0:
                M[i][j] = M[i-1][j]+delta[v[i-1]]['-']
            if j>0:
                if M[i][j] is None or M[i][j] < M[i][j-1]+delta['-'][w[j-1]]:
                    M[i][j] = M[i][j-1]+delta['-'][w[j-1]]
            if i>0 and j>0:
                if M[i][j] is None or M[i][j] < M[i-1][j-1]+delta[v[i-1]][w[j-1]]:
                    M[i][j] = M[i-1][j-1] + delta[v[i-1]][w[j-1]]
    score = M[n][m]
    return score

def block_align4(v, w, delta, keys, t, alpha=None):
    n = len(v)
    m = len(w)
    assert n % t == 0
    assert m % t == 0
    possible = ["".join(x) for x in product(keys[:-1], repeat=t)]
    dic = {x:{} for x in possible}
    tot = len(possible)
    assert tot == (len(keys)-1)**t
    for i in range(tot):
        x = possible[i]
        for j in range(tot):
            y = possible[j]
            dic[x][y] = global_align(x, y, delta)
    if alpha is None:
        alpha = {}
        for str1 in possible:
            alpha[str1] = 0
            for x in str1:
                alpha[str1] += delta[x]["-"]
    elif isinstance(alpha, float):
        y = alpha
        alpha = {x: y for x in possible}
    
    n = n // t
    m = m // t
    M = [[None for j in range(m+1)] for i in range(n+1)]
    M[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            if i>0:
                x = v[(i-1)*t:i*t]
            if j>0:
                y = w[(j-1)*t:j*t]
            if i > 0:
                M[i][j] = M[i-1][j] + alpha[x]
            if j > 0:
                if M[i][j] is None or M[i][j] < M[i][j-1] + alpha[y]:
                    M[i][j] = M[i][j-1] + alpha[y]
            if i>0 and j>0:
                if M[i][j] is None or M[i][j] < M[i-1][j-1] + dic[x][y]:
                    M[i][j] = M[i-1][j-1] + dic[x][y]
                
    score = M[n][m]
    return score

def prepare(C, D, R, S, delta, m):
    T = [[None for j in range(m+1)] for i in range(m+1)]
    U = [[None for j in range(m+1)] for i in range(m+1)]
    for i in range(1, m+1):
        T[i][0] = R[i-1]
        U[0][i] = S[i-1]
    for i in range(1, m+1):
        x = C[i-1]
        for j in range(1, m+1):
            y = D[j-1]
            T[i][j] = max(delta[x][y]-U[i-1][j], delta[x]["-"], T[i][j-1]-U[i-1][j] + delta["-"][y])
            U[i][j] = max(delta[x][y]-T[i][j-1], delta[x]["-"] - T[i][j-1] + U[i-1][j], delta["-"][y])
    RR = tuple([T[i][m] for i in range(1,m+1)])
    SS = tuple([U[m][i] for i in range(1,m+1)]) 
    return (RR, SS)

def fast4(v, w, delta, keys, t):
    n = len(v)
    m = len(w)
    assert n % t == 0
    assert m % t == 0
    strs = ["".join(x) for x in product(keys[:-1], repeat=t)]
    values = []
    for x in delta:
        for y in delta:
            values.append(delta[x][y])
    a = max(values)
    b = min(values)
    diff = sorted(list(range(-(a-b), (a-b)+1)))
    steps = [tuple(x) for x in product(diff, repeat=t)]
    tot_strs = len(strs)
    tot_steps = len(steps)
    dic = {}
    for i in range(tot_strs):
        x = strs[i]
        for j in range(tot_strs):
            y = strs[j]
            for k in range(tot_steps):
                R = steps[k]
                for l in range(tot_steps):
                    S = steps[l]
                    dic[(x,y,R,S)] = prepare(x, y, R, S, delta, t)
    
    n = n // t
    m = m // t
    P = [[None for j in range(m+1)] for i in range(n+1)]
    Q = [[None for j in range(m+1)] for i in range(n+1)]
    for i in range(1, n+1):
        P[i][0] = tuple([delta[x]["-"] for x in v[(i-1)*t:i*t]])
    for i in range(1, m+1):
        Q[0][i] = tuple([delta["-"][y] for y in w[(i-1)*t:i*t]])   
    for i in range(1, n+1):
        for j in range(1, m+1):
            P[i][j], Q[i][j] = dic[(v[(i-1)*t:i*t], w[(j-1)*t:j*t], P[i][j-1], Q[i-1][j])]


    score = 0
    for i in range(1, n+1):
        score += sum(P[i][0])
    for j in range(1, m+1):
        score += sum(Q[n][j])
    return score
