"""Regenerates the sensing figures (calibration, transient, enhancement, ratio, selectivity) and the graphical abstract.
Run after analyse_sensing.py:  python code/make_figures.py
Output goes to figures/ (the schematic figures 1, 2 and 11, XRD, FESEM and FTIR panels are not produced here)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import json, os, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sensing_lib import DERIVED, FIGS
res=json.load(open(os.path.join(DERIVED,'results.json')))
plt.rcParams.update({'font.family':'serif','font.serif':['DejaVu Serif'],'font.size':9,'axes.linewidth':0.8,'mathtext.fontset':'dejavuserif','pdf.fonttype':42})
NAVY='#1f3f73'; RED='#a32a2a'; GREY='#8a8a8a'; GREEN='#2e7d32'
NAME={'NO2':r'NO$_2$','VOC':'VOC vapour','NH3':r'NH$_3$','CO':'CO'}
CHL={'NO2':'OX','VOC':'RED','NH3':'OX','CO':'RED'}
SL={'RED':r'$S=R_0/R_s$','OX':r'$S=R_s/R_0$'}
order=['NO2','VOC','NH3','CO']
OUT=FIGS+'/'
def step(g,sn):
    s=res[g][sn]['steps']; C=np.array([float(k) for k in s]); S=np.array([s[k]['S'] for k in s]); sd=np.array([s[k]['sd'] for k in s]); return C,S,sd
# calibration
fig,ax=plt.subplots(2,2,figsize=(7.2,6.6))
for a,g,l in zip(ax.flat,order,'abcd'):
    for sn,col,m,lab in [('COATED',NAVY,'s','Coated'),('UNCOATED',RED,'o','Uncoated')]:
        C,S,sd=step(g,sn); a.errorbar(C,S,sd,fmt=m,color=col,ms=4.5,capsize=2,lw=0.8,label=lab,mec='k',mew=0.4)
        f=res[g][sn]['fit']; xx=np.linspace(C.min(),C.max(),200)
        use_pow = g in('VOC','CO') or (g=='NO2' and sn=='COATED')
        if use_pow:
            A,B=f['pow'][0]; a.plot(xx,A*xx**B,color=col,lw=1.3)
        else:
            a.plot(xx,np.polyval(f['poly'][0],xx),color=col,lw=1.3)
    a.set_title(f'({l}) {NAME[g]} ({CHL[g]} element)',fontsize=9.5,loc='left')
    a.set_xlabel('Concentration (ppm)'); a.set_ylabel(SL[CHL[g]]); a.grid(alpha=0.25,lw=0.4)
    if g=='NO2': a.legend(loc='upper left',frameon=False,fontsize=8)
    elif g=='NH3': a.legend(loc='lower right',frameon=False,fontsize=8)
    else: a.legend(loc='upper left' if g=='VOC' else 'upper left',frameon=False,fontsize=8)
plt.tight_layout(); plt.savefig(OUT+'e_calib.pdf'); plt.close()
# transient
fig,ax=plt.subplots(2,2,figsize=(7.2,6.0))
for a,g,l in zip(ax.flat,order,'abcd'):
    for sn,col,lab in [('COATED',NAVY,'Coated'),('UNCOATED',RED,'Uncoated')]:
        d=res[g][sn]; a.plot(np.array(d['t'])/60,d['y'],color=col,lw=0.8,label=lab)
    a.set_title(f'({l}) {NAME[g]} ({CHL[g]} element)',fontsize=9.5,loc='left'); a.set_xlabel('Time (min)'); a.set_ylabel(r'$R_s/R_0$'); a.grid(alpha=0.25,lw=0.4)
    a.legend(loc='best',frameon=True,framealpha=0.85,fontsize=7.5)
plt.tight_layout(); plt.savefig(OUT+'e_transient.pdf'); plt.close()
# enhancement
fig,ax=plt.subplots(2,2,figsize=(7.2,6.2))
for a,g,l in zip(ax.flat,order,'abcd'):
    c,s,_=step(g,'COATED'); cb,sb,_=step(g,'UNCOATED')
    d={x:(y) for x,y in zip(c,s)}; db={x:y for x,y in zip(cb,sb)}
    cs=[x for x in c if x in db]; E=np.array([(d[x]-db[x])/db[x]*100 for x in cs])
    pos=np.arange(len(cs)); cols=[GREEN if e>=0 else GREY for e in E]
    if g=='NO2':
        EF=np.array([d[x]/db[x] for x in cs]); a.bar(pos,EF,color=[GREEN if e>=1 else GREY for e in EF],edgecolor='k',lw=0.4); a.set_yscale('log'); a.axhline(1,color='k',lw=0.6); a.set_ylabel(r'$S_{coated}/S_{uncoated}$')
        for p_,e in zip(pos,EF): a.text(p_,max(e,1)*1.12 if e>=1 else 1.12, f'{e:.1f}' if e<10 else f'{e:.0f}',ha='center',fontsize=6.5)
        a.set_ylim(0.6,120)
    else:
        a.bar(pos,E,color=cols,edgecolor='k',lw=0.4); a.axhline(0,color='k',lw=0.6); a.set_ylabel(r'Enhancement $E$ (%)')
        for p_,e in zip(pos,E): a.text(p_,e+(1.2 if e>=0 else -1.2),f'{e:+.0f}',ha='center',va='bottom' if e>=0 else 'top',fontsize=6.5)
        lo=min(E.min(),0); hi=max(E.max(),0); a.set_ylim(lo-(hi-lo)*0.15,hi+(hi-lo)*0.15)
    a.set_xticks(pos); a.set_xticklabels([f'{x:g}' for x in cs],rotation=60,fontsize=7); a.set_xlabel(f'{NAME[g]} concentration (ppm)'); a.set_title(f'({l}) {NAME[g]}',fontsize=9.5,loc='left'); a.grid(alpha=0.25,lw=0.4,axis='y')
plt.tight_layout(); plt.savefig(OUT+'e_enh.pdf'); plt.close()
# datasheet ratio
fig,ax=plt.subplots(1,2,figsize=(7.2,3.2))
cols={'CO':'#1565c0','VOC':'#2e7d32','NO2':'#6a1b9a','NH3':'#e65100'}
for g in ['CO','VOC']:
    for sn,ls,al in [('COATED','-',1),('UNCOATED','--',0.55)]:
        C,S,_=step(g,sn); ax[0].plot(C,1/S,ls,color=cols[g],marker='o',ms=3,alpha=al,label=f'{NAME[g]} ({"coated" if sn=="COATED" else "uncoated"})')
for g in ['NO2','NH3']:
    for sn,ls,al in [('COATED','-',1),('UNCOATED','--',0.55)]:
        C,S,_=step(g,sn); ax[1].plot(C,S,ls,color=cols[g],marker='o',ms=3,alpha=al,label=f'{NAME[g]} ({"coated" if sn=="COATED" else "uncoated"})')
for a,t,y in zip(ax,['(a) RED element','(b) OX element'],[r'$R_s/R_0$',r'$R_s/R_0$']):
    a.set_xscale('log'); a.set_yscale('log'); a.set_xlabel('Concentration (ppm)'); a.set_ylabel(y); a.set_title(t,fontsize=9.5,loc='left'); a.grid(alpha=0.25,lw=0.4,which='both'); a.legend(fontsize=7,frameon=False)
ax[0].axhline(1,color='k',lw=0.5); ax[1].axhline(1,color='k',lw=0.5)
plt.tight_layout(); plt.savefig(OUT+'e_ratio.pdf'); plt.close()
# selectivity
fig,a=plt.subplots(figsize=(3.4,2.9))
gs=['NO2','VOC','CO','NH3']; x=np.arange(4); w=0.38
mc=[max(step(g,'COATED')[1]) for g in gs]; mb=[max(step(g,'UNCOATED')[1]) for g in gs]
a.bar(x-w/2,mc,w,color=NAVY,edgecolor='k',lw=0.4,label='Coated'); a.bar(x+w/2,mb,w,color=RED,edgecolor='k',lw=0.4,label='Uncoated')
for xi,v in zip(x-w/2,mc): a.text(xi,v*1.08,f'{v:.2f}',ha='center',fontsize=6.5)
for xi,v in zip(x+w/2,mb): a.text(xi,v*1.08,f'{v:.2f}',ha='center',fontsize=6.5)
a.set_yscale('log'); a.set_ylim(0.8,120); a.set_xticks(x); a.set_xticklabels([NAME[g].replace(' vapour','') for g in gs]); a.set_ylabel('Maximum $S$'); a.set_xlabel('Target gas'); a.legend(frameon=False,fontsize=7,loc='upper right'); a.grid(alpha=0.25,lw=0.4,axis='y')
plt.tight_layout(); plt.savefig(OUT+'e_select.pdf'); plt.close()
print('sensing figures written')


# ---- graphical abstract
plt.rcParams.update({'font.family':'serif','font.serif':['DejaVu Serif'],'font.size':7,'mathtext.fontset':'dejavuserif'})
NAVY='#1f3f73'; RED='#a32a2a'; GREEN='#2e7d32'
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig=plt.figure(figsize=(6.2,3.1))
ax=fig.add_axes([0,0.56,1,0.44]); ax.axis('off'); ax.set_xlim(0,100); ax.set_ylim(0,40)
labels=[("Silver vanadate precursor","hydrothermal, 140 °C"),("In-situ polyaniline","1 M HCl, 0–5 °C"),("Drop-cast coating","1 µL ink on MiCS-4514")]
xs=[2,36,70]
for x,(a,b) in zip(xs,labels):
    ax.add_patch(FancyBboxPatch((x,8),28,24,boxstyle='round,pad=0.4,rounding_size=2',fc='#e8eef7',ec=NAVY,lw=0.9))
    ax.text(x+14,24,a,ha='center',va='center',fontsize=7.5,fontweight='bold',color=NAVY); ax.text(x+14,14.5,b,ha='center',va='center',fontsize=7)
for x in [31.2,65.2]:
    ax.add_patch(FancyArrowPatch((x,20),(x+3.6,20),arrowstyle='-|>',mutation_scale=9,color='k',lw=1))
a1=fig.add_axes([0.09,0.2,0.38,0.27]); a2=fig.add_axes([0.59,0.2,0.38,0.27])
for sn,col,m,lab in [('COATED',NAVY,'s','Coated'),('UNCOATED',RED,'o','Uncoated')]:
    s=res['NO2'][sn]['steps']; C=[float(k) for k in s]; S=[s[k]['S'] for k in s]
    a1.plot(C,S,m+'-',color=col,ms=3.2,lw=1,label=lab)
a1.set_xlabel(r'NO$_2$ (ppm)',fontsize=7); a1.set_ylabel(r'Sensitivity $S$',fontsize=7); a1.legend(frameon=False,fontsize=6.5,loc='upper left'); a1.tick_params(labelsize=6.5); a1.grid(alpha=0.25,lw=0.4)
c=res['VOC']['COATED']['steps']; b=res['VOC']['UNCOATED']['steps']; ks=sorted(c,key=float)
E=[(c[k]['S']-b[k]['S'])/b[k]['S']*100 for k in ks]
a2.bar(range(len(ks)),E,color=GREEN,edgecolor='k',lw=0.3); a2.set_xticks(range(len(ks))); a2.set_xticklabels([f'{float(k):g}' for k in ks],rotation=60,fontsize=6)
a2.set_xlabel('VOC vapour (ppm)',fontsize=7); a2.set_ylabel('Enhancement (%)',fontsize=7); a2.tick_params(axis='y',labelsize=6.5); a2.grid(alpha=0.25,lw=0.4,axis='y')
fig.text(0.28,0.5,'NO$_2$ response',ha='center',fontsize=7.5,fontweight='bold'); fig.text(0.78,0.5,'VOC response',ha='center',fontsize=7.5,fontweight='bold')
fig.savefig(FIGS+'/graphical_abstract.png',dpi=400); fig.savefig(FIGS+'/graphical_abstract.pdf')

