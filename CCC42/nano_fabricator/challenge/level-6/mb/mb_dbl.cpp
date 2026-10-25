#include <bits/stdc++.h>
using namespace std;
typedef uint64_t u64;
struct Bits{ u64 w[8]; };
static inline Bits zero(){Bits b;for(int i=0;i<8;i++)b.w[i]=0;return b;}
static inline int pc(const Bits&b){int s=0;for(int i=0;i<8;i++)s+=__builtin_popcountll(b.w[i]);return s;}
static inline bool any(const Bits&b){u64 s=0;for(int i=0;i<8;i++)s|=b.w[i];return s!=0;}
static const int DR[6]={0,1,1,0,-1,-1}, DC[6]={2,1,-1,-2,-1,1};
int R,NC,RING;
vector<pair<int,int>> cellrc, ringc;
map<pair<int,int>,int> cid, rid;
vector<vector<Bits>> beam; // [k][p]
vector<vector<int>> qpos; // [k][c]
vector<vector<vector<uint8_t>>> tabD; // [k][p][c]
vector<vector<int>> npline; // [k][p] = NP cells on that beam
int DBL=1; int DBLCAP=4;
Bits P, NP; int Pn;
vector<int> Plist;
double WA=1.0, WF=0.05, WG=8.0; int CAP=10;
struct St{ uint8_t pos[6]; uint8_t act; Bits M; };
struct Cand{ St s; double score; uint16_t combo; int parent; bool done; u64 h; };
static u64 rng_s=88172645463325252ULL;
static inline u64 rnd(){rng_s^=rng_s<<13;rng_s^=rng_s>>7;rng_s^=rng_s<<17;return rng_s;}
void setup(int r, const vector<string>&rows){
  R=r; cellrc.clear(); cid.clear(); ringc.clear(); rid.clear();
  for(int i=0;i<=2*r;i++){int d=abs(i-r); if(d!=r) for(int k=0;k<2*r-1-d;k++){cid[{i,d+2+2*k}]=cellrc.size(); cellrc.push_back({i,d+2+2*k});}}
  NC=cellrc.size();
  ringc.push_back({r,0});
  for(int i=r-1;i>=0;i--)ringc.push_back({i,r-i});
  for(int j=1;j<=r;j++)ringc.push_back({0,r+2*j});
  for(int i=1;i<=r;i++)ringc.push_back({i,3*r+i});
  for(int i=r+1;i<=2*r;i++)ringc.push_back({i,5*r-i});
  for(int j=1;j<=r;j++)ringc.push_back({2*r,3*r-2*j});
  for(int i=2*r-1;i>r;i--)ringc.push_back({i,i-r});
  RING=ringc.size(); for(int i=0;i<RING;i++)rid[ringc[i]]=i;
  beam.assign(6,vector<Bits>(RING)); qpos.assign(6,vector<int>(NC,-1));
  for(int k=0;k<6;k++)for(int p=0;p<RING;p++){Bits b=zero();int a=ringc[p].first+DR[k],c=ringc[p].second+DC[k];
    while(cid.count({a,c})){int id=cid[{a,c}];b.w[id>>6]|=1ULL<<(id&63);a+=DR[k];c+=DC[k];} beam[k][p]=b;}
  for(int k=0;k<6;k++)for(int c=0;c<NC;c++){int a=cellrc[c].first-DR[k],b=cellrc[c].second-DC[k];
    while(cid.count({a,b})){a-=DR[k];b-=DC[k];} auto it=rid.find({a,b}); qpos[k][c]=it==rid.end()?-1:it->second;}
  tabD.assign(6,vector<vector<uint8_t>>(RING,vector<uint8_t>(NC)));
  for(int k=0;k<6;k++)for(int p=0;p<RING;p++)for(int c=0;c<NC;c++){int q=qpos[k][c]; if(q<0){tabD[k][p][c]=100;continue;} int d=abs(p-q); d=min(d,RING-d); tabD[k][p][c]=d;}
  P=zero(); Plist.clear();
  for(int i=0;i<(int)rows.size();i++)for(int j=0;j<(int)rows[i].size();j++)if(rows[i][j]=='M'){int id=cid.at({i,j});P.w[id>>6]|=1ULL<<(id&63);Plist.push_back(id);}
  Pn=Plist.size(); NP=zero();
  static const int NR[6]={0,0,1,1,-1,-1},NCc[6]={2,-2,1,-1,1,-1};
  for(int id:Plist)for(int t=0;t<6;t++){auto it=cid.find({cellrc[id].first+NR[t],cellrc[id].second+NCc[t]}); if(it!=cid.end()){int n=it->second;NP.w[n>>6]|=1ULL<<(n&63);}}
  for(int i=0;i<8;i++)NP.w[i]&=~P.w[i];
  npline.assign(6,vector<int>(RING,0));
  for(int k=0;k<6;k++)for(int p=0;p<RING;p++){int s=0;for(int i=0;i<8;i++)s+=__builtin_popcountll(beam[k][p].w[i]&NP.w[i]);npline[k][p]=s;}
}
// apply combo (2 bits per emitter: 0 stay,1 F,2 B,3 T) returns new state and metrics
struct Res{ St s; int miss, bad; bool done; double score; };
static inline void applyCombo(const St&s,uint16_t combo,St&n){
  n=s;
  for(int k=0;k<6;k++){int o=(combo>>(2*k))&3; if(o==1)n.pos[k]=(s.pos[k]+1)%RING; else if(o==2)n.pos[k]=(s.pos[k]+RING-1)%RING; else if(o==3)n.act^=(1<<k);}
}
static inline void fire(St&n){
  Bits c1=zero(),c2=zero(),c3=zero();
  for(int k=0;k<6;k++) if(n.act>>k&1){const Bits&b=beam[k][n.pos[k]];
    for(int i=0;i<8;i++){u64 bb=b.w[i];u64 t3=c2.w[i]&bb;u64 nc2=(c2.w[i]&~bb)|(c1.w[i]&bb);
      u64 nc1=(c1.w[i]&~bb)|(bb&~c1.w[i]&~c2.w[i]&~c3.w[i]);c3.w[i]|=t3;c2.w[i]=nc2;c1.w[i]=nc1;}}
  // note c1 after: cells with exactly 1; c2 exactly2; c3 >=3
  for(int i=0;i<8;i++)n.M.w[i]=(n.M.w[i]|c2.w[i])&~c3.w[i];
}
static inline void evalState(St&n,Res&r,bool needScore){
  int miss=0,bad=0; Bits ms; 
  for(int i=0;i<8;i++){ms.w[i]=P.w[i]&~n.M.w[i];miss+=__builtin_popcountll(ms.w[i]);bad+=__builtin_popcountll(n.M.w[i]&NP.w[i]);}
  r.miss=miss;r.bad=bad;r.done=(miss==0&&bad==0);
  if(!needScore||r.done){r.score=r.done?-1:0;return;}
  double sf=0;
  for(int i=0;i<8;i++){u64 w=ms.w[i];while(w){int b=__builtin_ctzll(w);w&=w-1;int c=i*64+b;
    int m[3];
    int dbl=1000;
    for(int f=0;f<3;f++){int a=tabD[f][n.pos[f]][c]+((n.act>>f&1)?0:1);int b2=tabD[f+3][n.pos[f+3]][c]+((n.act>>(f+3)&1)?0:1);m[f]=min(a,b2);
      if(DBL){int q=qpos[f][c]; if(q>=0&&npline[f][q]<=DBLCAP){int d=max(a,b2); if(d<dbl)dbl=d;}}}
    if(m[0]>m[1])swap(m[0],m[1]); if(m[1]>m[2])swap(m[1],m[2]); if(m[0]>m[1])swap(m[0],m[1]);
    sf+=min(min(m[1],dbl),CAP);}}
  r.score=WA*miss+WF*sf+WG*bad;
}
static inline u64 hashSt(const St&s){u64 h=1469598103934665603ULL;for(int k=0;k<6;k++)h=(h^s.pos[k])*1099511628211ULL;h=(h^s.act)*1099511628211ULL;for(int i=0;i<8;i++){h^=s.M.w[i]+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);}return h;}
static inline void step(const St&s,uint16_t combo,Res&r,bool sc=true){applyCombo(s,combo,r.s);fire(r.s);evalState(r.s,r,sc);}
// Search from state s0. returns vector of combos; end state (post-fire, pattern still present) in endS. fail -> empty & ok=false
bool search(const St&s0,int W,int Tmax,vector<uint16_t>&out,St&endS,int nrand){
  vector<vector<Cand>> hist; // beams per depth
  vector<Cand> cur(1); cur[0].s=s0;cur[0].parent=-1;cur[0].combo=0;cur[0].score=0;cur[0].done=false;
  hist.push_back(cur);
  for(int t=1;t<=Tmax;t++){
    vector<Cand> pool; pool.reserve(cur.size()*60);
    int doneIdx=-1; 
    for(int ci=0;ci<(int)cur.size();ci++){
      const St&s=cur[ci].s;
      set<uint16_t> seen; 
      auto ev=[&](uint16_t combo)->double{
        Res r; step(s,combo,r);
        if(!seen.count(combo)){seen.insert(combo);
          Cand c; c.s=r.s;c.score=r.score;c.combo=combo;c.parent=ci;c.done=r.done;c.h=0;pool.push_back(c);}
        return r.score; };
      for(int st=0;st<1+nrand;st++){
        uint16_t combo=0;
        if(st>0){for(int k=0;k<6;k++){u64 x=rnd()%10;int o=x<3?0:x<6?1:x<9?2:3; combo|=o<<(2*k);}}
        double best=ev(combo);
        for(int pass=0;pass<2;pass++){bool imp=false;
          int ord[6]={0,1,2,3,4,5};for(int i=5;i>0;i--)swap(ord[i],ord[rnd()%(i+1)]);
          for(int oi=0;oi<6;oi++){int k=ord[oi];int cur_o=(combo>>(2*k))&3;
            for(int o=0;o<4;o++){if(o==cur_o)continue;uint16_t nc=(combo&~(3<<(2*k)))|(o<<(2*k));double sc=ev(nc);
              if(sc<best-1e-9){best=sc;combo=nc;cur_o=o;imp=true;}}}
          if(!imp)break;}
      }
    }
    // check done
    double bs=1e18;for(int i=0;i<(int)pool.size();i++)if(pool[i].done){ if(doneIdx<0||pool[i].s.M.w[0]<pool[doneIdx].s.M.w[0]) doneIdx=i; }
    if(doneIdx>=0){
      // reconstruct
      out.assign(t,0); out[t-1]=pool[doneIdx].combo; int par=pool[doneIdx].parent;
      for(int d=t-1;d>=1;d--){out[d-1]=hist[d][par].combo;par=hist[d][par].parent;}
      endS=pool[doneIdx].s; return true;
    }
    for(auto&c:pool)c.h=hashSt(c.s);
    sort(pool.begin(),pool.end(),[](const Cand&a,const Cand&b){return a.score<b.score;});
    vector<Cand> nxt; unordered_set<u64> hs;
    for(auto&c:pool){ if((int)nxt.size()>=W)break; if(hs.insert(c.h).second)nxt.push_back(c);}
    cur=nxt; hist.push_back(cur);
  }
  return false;
}
string lineOf(uint16_t combo){string s;for(int k=0;k<6;k++){int o=(combo>>(2*k))&3;s+="-FBT"[o];s+=k<5?' ':'\n';}return s;}
uint16_t invCombo(uint16_t c){uint16_t r=0;for(int k=0;k<6;k++){int o=(c>>(2*k))&3;if(o==1)o=2;else if(o==2)o=1;r|=o<<(2*k);}return r;}
// simulate program from initial; returns count, and index (1-based line) of K-th submit
int simulate(const vector<uint16_t>&prog,int K,int&cutLen){
  St s;for(int k=0;k<6;k++)s.pos[k]=k*R;s.act=0;s.M=zero();int cnt=0;cutLen=-1;
  for(int t=0;t<(int)prog.size();t++){
    St n;applyCombo(s,prog[t],n);fire(n);
    int miss=0,bad=0;for(int i=0;i<8;i++){miss+=__builtin_popcountll(P.w[i]&~n.M.w[i]);bad+=__builtin_popcountll(n.M.w[i]&NP.w[i]);}
    if(miss==0&&bad==0){for(int i=0;i<8;i++)n.M.w[i]&=~P.w[i];cnt++;if(cnt==K&&cutLen<0)cutLen=t+1;}
    s=n;}
  return cnt;
}

vector<uint16_t> build(int K,int W,int nrand,bool&okout){
  okout=false;
  St s0;for(int k=0;k<6;k++)s0.pos[k]=k*R;s0.act=0;s0.M=zero();
  vector<uint16_t> prog,A,B;St e1,e2;
  if(!search(s0,W,1500,A,e1,nrand))return prog;
  prog=A; for(int i=0;i<8;i++)e1.M.w[i]&=~P.w[i];
  if(K>=2){
    if(!search(e1,W,1500,B,e2,nrand))return prog;
    prog.insert(prog.end(),B.begin(),B.end());
    int L=B.size(),jmin=0;
    for(int j=1;j<L;j++){St t=e1;for(int x=0;x<L;x++){applyCombo(t,B[x],t);if(x>=j)fire(t);}
      int miss=0,bad=0;for(int i=0;i<8;i++){miss+=__builtin_popcountll(P.w[i]&~t.M.w[i]);bad+=__builtin_popcountll(t.M.w[i]&NP.w[i]);}
      if(miss==0&&bad==0)jmin=j;else break;}
    vector<uint16_t> seg(B.begin()+jmin+1,B.end());int nl=seg.size();bool dirR=true;
    for(int c=3;c<=K;c++){prog.push_back(0);
      if(dirR){for(int i=nl-1;i>=0;i--)prog.push_back(invCombo(seg[i]));}else for(int i=0;i<nl;i++)prog.push_back(seg[i]);
      dirR=!dirR;}
  }
  int cut;int cnt=simulate(prog,K,cut);
  if(cnt<K||cut<0){
    prog=A;St cs=e1;
    for(int c=2;c<=K;c++){vector<uint16_t> X;St e;if(!search(cs,W,1500,X,e,nrand))return prog;
      prog.insert(prog.end(),X.begin(),X.end());for(int i=0;i<8;i++)e.M.w[i]&=~P.w[i];cs=e;}
    cnt=simulate(prog,K,cut);
  }
  if(cut<0)return prog;
  prog.resize(cut);okout=true;return prog;
}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r");int a=atoi(argv[2]),b=atoi(argv[3]);int W=atoi(argv[5]);int nrand=atoi(argv[6]);int trials=atoi(argv[7]); if(argc>8)DBL=atoi(argv[8]); if(argc>9)DBLCAP=atoi(argv[9]);
  int N;fscanf(f,"%d",&N);
  FILE*fo=fopen(argv[4],"w");long total=0;
  static const double wfs[]={0.05,0.02,0.1,0.05,0.03,0.2,0.05,0.01};
  static const int caps[]={10,6,20,10,8,12,5,10};
  static const double was[]={1,1,2,0.5,1,1,3,1};
  for(int pi=0;pi<N;pi++){
    int r,rows,cols,K;fscanf(f,"%d %d %d %d",&r,&rows,&cols,&K);vector<string> pat(rows);
    for(int i=0;i<rows;i++){char buf[256];fscanf(f,"%s",buf);pat[i]=buf;}
    if(pi<a||pi>=b)continue;
    setup(r,pat);
    vector<uint16_t> best;bool have=false;
    for(int tr=0;tr<trials||!have;tr++){
      int q=tr%8;WF=wfs[q];CAP=caps[q];WA=was[q];int w2=W*(1+tr/8);
      if(tr>40){fprintf(stderr,"pattern %d giving up\n",pi);break;}
      rng_s=88172645463325252ULL+tr*7919;
      bool ok;auto p=build(K,w2,nrand,ok);
      if(ok&&(!have||p.size()<best.size())){best=p;have=true;}
    }
    if(!have){fprintf(fo,"FAIL %d\n",pi);continue;}
    fprintf(fo,"PAT %d %d\n",pi,(int)best.size());
    for(auto c:best)fputs(lineOf(c).c_str(),fo);
    fprintf(fo,"END\n");total+=best.size();
  }
  fprintf(stderr,"TOTAL %ld\n",total);
}
