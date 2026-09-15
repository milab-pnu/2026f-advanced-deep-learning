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
fig,(ax,logax)=plt.subplots(1,2,figsize=(8.4,3.9),layout='constrained')
ax.plot(n,2+1/np.sqrt(n), color='#334155', lw=2.5)
ax.axhline(2, color='#94a3b8', ls='--')
ax.text(8,2.10,'Floor = 2',fontsize=12,color='#64748b')
ax.scatter([1,4,16],[3,2.5,2.25],color='#0f172a',zorder=3)
ax.set(xlabel='N (billions)',ylabel='Toy loss',ylim=(1.8,4.2))
ax.set_title('Linear axes: total loss',fontsize=13)
logax.loglog(n,n**-.5,color='#334155',lw=2.5,base=2)
logax.scatter([1,4,16],[1,.5,.25],color='#0f172a',zorder=3)
logax.set_xticks([.25,1,4,16],['0.25','1','4','16'])
logax.set_yticks([.25,.5,1,2],['0.25','0.5','1','2'])
logax.set(xlabel='N (billions)',ylabel='Toy loss − floor')
logax.text(.5,.37,'Slope = −0.5',fontsize=12,color='#64748b')
logax.set_title('Log–log: decreasing term',fontsize=13)
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

# 본문의 교육용 설정을 그대로 그린다. 실제 모델의 recipe가 아니다.
steps=np.arange(1001)
rate=np.where(steps<=100,steps/100,(1000-steps)/900)
fig,ax=plt.subplots(figsize=(6,3.5),layout='constrained')
ax.plot(steps,rate,color='#334155',lw=2.5)
ax.axvline(100,color='#94a3b8',ls='--')
marks=[50,100,550,1000]
ax.scatter(marks,rate[marks],color='#0f172a',zorder=3)
ax.annotate('Warmup ends',(100,1),xytext=(190,.98),fontsize=12)
ax.text(525,.69,'Linear decay',fontsize=12,color='#64748b')
ax.set(xlabel='Optimizer step',ylabel='Learning rate / maximum',xlim=(0,1000),ylim=(-.03,1.1))
ax.set_xticks([0,100,550,1000])
ax.set_yticks([0,.5,1])
save(fig,'week02-learning-rate.png')
