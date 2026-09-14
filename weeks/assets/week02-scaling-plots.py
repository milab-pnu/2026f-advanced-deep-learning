"""노트에 명시한 가상 수식의 교육용 그래프. 실행: MPLCONFIGDIR=/tmp/adl-mpl python3 <이 파일>
실험 데이터나 원논문 그림을 재현하지 않는다. numpy, matplotlib 필요.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path(__file__).parent
plt.rcParams.update({'font.size':13, 'axes.spines.top':False, 'axes.spines.right':False,
                     'axes.labelsize':13, 'figure.facecolor':'white', 'axes.grid':True,
                     'grid.alpha':.18})
def save(fig, name):
    fig.savefig(OUT / name, dpi=190, bbox_inches='tight')
    plt.close(fig)
n=np.geomspace(.25,16,300)
fig,ax=plt.subplots(figsize=(6,4))
ax.plot(n,1+1/np.sqrt(n)+1, color='#334155', lw=2.5)
ax.axhline(2, color='#94a3b8', ls='--', label='Fixed-data floor: E + B/D^0.5 = 2')
ax.scatter([1,4,16],[3,2.5,2.25],color='#0f172a',zorder=3)
ax.set(xlabel='Model size N (billions)',ylabel='Toy loss',ylim=(1.8,4.2))
ax.legend(fontsize=10,loc='upper right')
ax.set_title('Fixed D = 1B: diminishing loss reduction',fontsize=13)
save(fig,'week02-power-law.png')
n=np.geomspace(.125,8,300)
fig,ax=plt.subplots(figsize=(6,4))
ax.plot(n,1+n**-.5+n**.5,color='#334155',lw=2.5)
ax.scatter([.5,1,2],[1+2**.5+2**-.5,3,1+2**.5+2**-.5],color='#0f172a',zorder=3)
for x,y,t in [(.5,3.121,'A'),(1,3,'B'),(2,3.121,'C')]:ax.annotate(t,(x,y),xytext=(0,10),textcoords='offset points',ha='center')
ax.set_xscale('log',base=2)
ax.set_xticks([.125,.25,.5,1,2,4,8],['0.125','0.25','0.5','1','2','4','8'])
ax.set(xlabel='Model size N (billions)',ylabel='Toy loss',ylim=(2.9,4.4))
ax.set_title('Fixed compute: D = 1/N (billions)',fontsize=13)
save(fig,'week02-isoflop.png')
p=np.linspace(0,1,300)
fig,ax=plt.subplots(figsize=(6,4))
ax.plot(p,p,color='#64748b',ls='--',lw=2,label='Per-token success: p')
ax.plot(p,p**5,color='#0f172a',lw=2.5,label='All 5 correct: p^5')
pts=np.array([.4,.6,.8,.9]);ax.scatter(pts,pts**5,color='#0f172a',zorder=3)
ax.set(xlabel='Per-token success probability p',ylabel='Expected score',xlim=(0,1),ylim=(0,1))
ax.legend(fontsize=11,loc='upper left')
ax.set_title('Same predictions, different scoring rules',fontsize=13)
save(fig,'week02-emergence-metric.png')
