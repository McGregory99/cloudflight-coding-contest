"""Level 4: flock-level species classifier (hand-made path features + from-scratch random forest; no numpy here)."""
import collections, glob, os, random, math
def num(s):
    try: return float(s)
    except ValueError: return 17.0  # "seventeen" (BOP 287)
def temps():
    t = {}
    for l in open("all_data_from_level_1.in").read().splitlines()[1:]:
        b, tt, h = l.split(","); tt = num(tt)
        if tt > 45: tt = (tt - 32) * 5 / 9  # degF bug
        t[int(b)] = (tt, float(h))
    return t
def read(path):
    fl = collections.OrderedDict(); lab = {}
    for l in open(path).read().splitlines()[1:]:
        p = l.split(",")
        fl.setdefault(int(p[0]), []).append([int(x) for x in p[1].split()])
        if p[2] != "missing": lab[int(p[0])] = p[2]
    return fl, lab
T = temps()
import math, random
T=temps()
def agree(rows, lo, hi):
    # mean pairwise position-wise match over fractional positions in [lo,hi) of the shortest row (rows aligned from start)
    L=min(len(r) for r in rows)
    a=int(L*lo); b=max(a+1,int(L*hi)); b=min(b,L)
    tot=cnt=0
    for i in range(len(rows)):
        for j in range(i+1,len(rows)):
            for k in range(a,b):
                tot+= rows[i][k]==rows[j][k]; cnt+=1
    return tot/cnt if cnt else 0.0
def flock_feats(rows):
    n=len(rows); lens=[len(r) for r in rows]
    nodes=[x for r in rows for x in r]
    ts=[T[x][0] for x in nodes]; hs=[T[x][1] for x in nodes]
    # core of row without the repeated trailing base (padding)
    def strip(r):
        r=list(r)
        while len(r)>1 and r[-1]==r[-2]: r.pop()
        return r
    def pal(r):
        r=strip(r)
        return sum(r[i]==r[-1-i] for i in range(len(r)//2))/max(1,len(r)//2)
    def palset(r):
        r=strip(r); h=len(r)//2
        return len(set(r[:h])&set(r[-h:]))/max(1,len(set(r[:h])))
    def trail(r):
        k=0
        while k<len(r) and r[-1-k]==r[-1]: k+=1
        return k
    sets=[set(r) for r in rows]
    jac=[len(sets[i]&sets[j])/len(sets[i]|sets[j]) for i in range(n) for j in range(i+1,n)] or [1.0]
    f=dict(
        n=n, L=sum(lens)/n, Lstd=(sum((l-sum(lens)/n)**2 for l in lens)/n)**.5,
        T=sum(ts)/len(ts), Tmax_frac=sum(t>=35 for t in ts)/len(ts), Tmin=min(ts), H=sum(hs)/len(hs),
        pal=sum(pal(r) for r in rows)/n, palset=sum(palset(r) for r in rows)/n,
        pal_x=sum(strip(r)==strip(r)[::-1] for r in rows)/n, palx=sum(r==r[::-1] for r in rows)/n,
        loop=sum(r[0]==r[-1] for r in rows)/n,
        dup=1-len(set(map(tuple,rows)))/n if n>1 else 0.5,
        a1=agree(rows,0,.25), a2=agree(rows,.25,.5), a3=agree(rows,.5,.75), a4=agree(rows,.75,1),
        ah=agree(rows,0,.5), aw=agree(rows,0,1),
        jac=sum(jac)/len(jac), trail=sum(trail(r) for r in rows)/n,
        uniq=len(set(nodes))/len(nodes), short=float(sum(lens)/n<=9),
        samelen=float(len(set(lens))==1),
    )
    return f

import random, math, collections
def gini(c,n): return 1-sum((v/n)**2 for v in c.values()) if n else 0
def build(X,y,idx,depth,maxd,rng,mtry):
    c=collections.Counter(y[i] for i in idx)
    if len(c)==1 or depth>=maxd or len(idx)<3: return ('leaf',c)
    best=None; nf=len(X[0])
    for f in rng.sample(range(nf),mtry):
        vals=sorted(set(X[i][f] for i in idx))
        for a,b in zip(vals,vals[1:]):
            t=(a+b)/2; l=collections.Counter(); r=collections.Counter()
            for i in idx: (l if X[i][f]<=t else r)[y[i]]+=1
            nl=sum(l.values()); nr=len(idx)-nl
            g=(nl*gini(l,nl)+nr*gini(r,nr))/len(idx)
            if best is None or g<best[0]: best=(g,f,t)
    if best is None: return ('leaf',c)
    _,f,t=best
    L=[i for i in idx if X[i][f]<=t]; R=[i for i in idx if X[i][f]>t]
    return ('n',f,t,build(X,y,L,depth+1,maxd,rng,mtry),build(X,y,R,depth+1,maxd,rng,mtry))
def pred(t,x):
    while t[0]=='n': t=t[3] if x[t[1]]<=t[2] else t[4]
    return t[1]
def forest(X,y,n=100,maxd=8,seed=0):
    rng=random.Random(seed); mtry=max(1,int(len(X[0])**.5)+1); ts=[]
    for _ in range(n):
        idx=[rng.randrange(len(X)) for _ in X]; ts.append(build(X,y,idx,0,maxd,rng,mtry))
    return ts
def proba(ts,x):
    c=collections.Counter()
    for t in ts:
        for k,v in pred(t,x).items(): c[k]+=v/sum(pred(t,x).values())
    s=sum(c.values()); return {k:v/s for k,v in c.items()}
def f1macro(yt,yp):
    cl=set(yt); s=0
    for c in cl:
        tp=sum(a==b==c for a,b in zip(yt,yp)); fp=sum(b==c and a!=c for a,b in zip(yt,yp)); fn=sum(a==c and b!=c for a,b in zip(yt,yp))
        s+=2*tp/(2*tp+fp+fn) if tp else 0
    return s/len(cl)

files = sorted(glob.glob("in_level-4_*.txt"))
data = {f: read(f) for f in files}
FE = {f: {k: flock_feats(r) for k, r in data[f][0].items()} for f in files}
keys = list(next(iter(FE[files[0]].values())))
vec = lambda d: [d[k] for k in keys]
pool = [(vec(FE[f][k]), s) for f in files for k, s in data[f][1].items()]

def models(pool, n=300):
    return forest([x for x, _ in pool], [s for _, s in pool], n, 8, 0)

def cv(folds=5):
    random.seed(0); P = pool[:]; random.shuffle(P); yt = []; yp = []
    for k in range(folds):
        te = P[k::folds]; tr = [p for j, p in enumerate(P) if j % folds != k]
        m = forest([x for x, _ in tr], [s for _, s in tr], 100, 8, k)
        for x, s in te:
            p = proba(m, x); yt.append(s); yp.append(max(p, key=p.get))
    return f1macro(yt, yp), sum(a == b for a, b in zip(yt, yp)) / len(yt)

if os.environ.get("CV"): print("5-fold CV (macro F1, acc):", cv())
m = models(pool)
for f in files:
    out = ["Flock ID,Species"]
    for k in data[f][0]:
        if k not in data[f][1]:
            p = proba(m, vec(FE[f][k])); out.append(f"{k},{max(sorted(p), key=p.get)}")
    open(f.replace("in_", "", 1).replace(".txt", ".out"), "w").write("\n".join(out) + "\n")
