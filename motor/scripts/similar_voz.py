import sys,json,subprocess,numpy as np
exec(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'medir_voz.py')).read().split("if __name__")[0])
def mfcc_stats(x,sr=16000,n=512,hop=160,nm=40,nc=13):
    w=np.hanning(n); fr=[]
    for i in range(0,len(x)-n,hop):
        f=x[i:i+n]
        if np.sqrt(np.mean(f**2))<5e-3: continue
        fr.append(np.abs(np.fft.rfft(f*w))**2)
    P=np.array(fr); freqs=np.fft.rfftfreq(n,1/sr)
    mel=lambda f:2595*np.log10(1+f/700); imel=lambda m:700*(10**(m/2595)-1)
    pts=imel(np.linspace(mel(60),mel(7600),nm+2)); fb=np.zeros((nm,len(freqs)))
    for j in range(nm):
        l,c,r=pts[j],pts[j+1],pts[j+2]
        fb[j]=np.clip(np.minimum((freqs-l)/(c-l),(r-freqs)/(r-c)),0,None)
    E=np.log(P@fb.T+1e-10)
    k=np.arange(nm); D=np.cos(np.pi/nm*(k[None,:]+0.5)*np.arange(nc)[:,None])
    C=E@D.T
    return C[:,1:].mean(0), C[:,1:].std(0)
def gaps(words):
    W=json.load(open(words)); return [round(W[i+1]['s']-W[i]['e'],2) for i in range(len(W)-1) if W[i]['w'][-1:] in '.,?!:']
ref=sys.argv[1]; rm,rs=mfcc_stats(load(ref))
print('ref',ref,'pausas',gaps(ref.rsplit('.',1)[0]+'.words.json'))
for f in sys.argv[2:]:
    m,s=mfcc_stats(load(f))
    d=np.sqrt(np.mean((m-rm)**2)); ds=np.sqrt(np.mean((s-rs)**2))
    r,_=medir(f)
    print(f, 'dist_timbre(MFCC)',round(float(d),2),'dist_var',round(float(ds),2),'F0',r['f0_mediana'],'p90',r['f0_p90'],'var_st',r['variacao_semitons_dp'],'centroide',r['centroide_hz'])
