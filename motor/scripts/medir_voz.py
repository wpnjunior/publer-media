import sys, json, subprocess, numpy as np, os
SR=16000
def load(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,dtype=np.float32)
CL=[]
def f0_track(x):
    CL.clear()
    fl=int(0.04*SR); hop=int(0.01*SR); out=[]; en=[]
    for i in range(0,len(x)-fl,hop):
        fr=x[i:i+fl]*np.hanning(fl); e=np.sqrt(np.mean(fr**2)); en.append(e)
        if e<1e-3: out.append(0); continue
        ac=np.correlate(fr,fr,'full')[fl-1:]
        lo=int(SR/220); hi=int(SR/65)
        seg=ac[lo:hi]; k=np.argmax(seg)+lo
        cl=ac[k]/ac[0]
        if cl < 0.5: out.append(0); continue
        CL.append(cl)
        # parabolic
        if 1<=k<len(ac)-1:
            a,b,c=ac[k-1],ac[k],ac[k+1]; d=0.5*(a-c)/(a-2*b+c) if (a-2*b+c)!=0 else 0
        else: d=0
        out.append(SR/(k+d))
    f=np.array(out); en=np.array(en)
    thr=np.percentile(en,30)
    return f, en, thr
def spectrum(x):
    n=2048; hop=512; w=np.hanning(n); S=[]
    for i in range(0,len(x)-n,hop):
        fr=x[i:i+n]
        if np.sqrt(np.mean(fr**2))<3e-3: continue
        S.append(np.abs(np.fft.rfft(fr*w))**2)
    S=np.mean(S,0); fr=np.fft.rfftfreq(n,1/SR); return fr,S
def bands(fr,S):
    tot=S[(fr>60)&(fr<8000)].sum()
    B=[(60,250),(250,800),(800,2000),(2000,4000),(4000,8000)]
    return {f'{a}-{b}':round(10*np.log10(S[(fr>=a)&(fr<b)].sum()/tot),1) for a,b in B}
def medir(p, words=None):
    x=load(p); dur=len(x)/SR
    f,en,thr=f0_track(x); v=f[(f>0)]
    st=12*np.log2(v/np.median(v))
    fr,S=spectrum(x)
    cent=float((fr*S).sum()/S.sum())
    r={'arquivo':os.path.basename(p),'dur':round(dur,1),
       'f0_mediana':round(float(np.median(v)),1),'f0_p10':round(float(np.percentile(v,10)),1),'f0_p90':round(float(np.percentile(v,90)),1),
       'variacao_semitons_dp':round(float(np.std(st)),2),'centroide_hz':round(cent),
       'voz_pct':round(100*len(v)/len(f)),'clareza':round(float(np.mean(CL)),3),'bandas_db':bands(fr,S)}
    if words and os.path.exists(words):
        W=json.load(open(words)); W=W if isinstance(W,list) else W.get('words',W)
        if isinstance(W[0],list): W=[{'s':a,'e':b,'w':c} for a,b,c in W]
        n=len(W); fala=sum(w['e']-w['s'] for w in W) if 's' in W[0] else None
        span=W[-1]['e']-W[0]['s']
        gaps=[W[i+1]['s']-W[i]['e'] for i in range(n-1)]
        r['ppm_com_pausas']=round(60*n/span); r['pausas_maiores_0.3s']=sum(g>0.3 for g in gaps)
        r['pausa_media_entre_frases']=round(float(np.mean([g for g in gaps if g>0.25])) if any(g>0.25 for g in gaps) else 0,2)
    return r, (fr,S)
if __name__=='__main__':
    res=[]
    for a in sys.argv[1:]:
        p,_,w=a.partition(',')
        r,_=medir(p,w or None); res.append(r); print(json.dumps(r,ensure_ascii=False))
