"""봉우리가 둘인 p에 정규분포 q 하나를 forward KL과 reverse KL로 각각 맞춘 교육용 그림.
실행: MPLCONFIGDIR=/tmp/adl-mpl python3 <이 파일>
p와 q는 설명을 위해 정한 가상 분포다. numpy, scipy, matplotlib 필요.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import norm

OUT = Path(__file__).parent
plt.rcParams.update({'font.size':13, 'axes.spines.top':False, 'axes.spines.right':False,
                     'axes.labelsize':13, 'figure.facecolor':'white'})

x = np.linspace(-8, 8, 4001)
dx = x[1] - x[0]
p = 0.5*norm.pdf(x, -2.5, 0.7) + 0.5*norm.pdf(x, 2.5, 0.7)
eps = 1e-300

def kl(a, b):
    return np.sum(a*(np.log(a+eps) - np.log(b+eps)))*dx

def gauss(theta):
    return norm.pdf(x, theta[0], np.exp(theta[1]))

fwd = minimize(lambda t: kl(p, gauss(t)), [0.5, 0.0], method='Nelder-Mead').x
rev = minimize(lambda t: kl(gauss(t), p), [1.5, 0.0], method='Nelder-Mead').x
for name, t in [('forward', fwd), ('reverse', rev)]:
    print(f'{name}: mean={t[0]:.3f}, sd={np.exp(t[1]):.3f}, '
          f'KL(p||q)={kl(p, gauss(t)):.3f}, KL(q||p)={kl(gauss(t), p):.3f}')

fig, axes = plt.subplots(1, 2, figsize=(9, 3.4), layout='constrained', sharey=True)
for ax, t, title in [(axes[0], fwd, 'Forward KL(p || q)'), (axes[1], rev, 'Reverse KL(q || p)')]:
    ax.fill_between(x, p, color='#cbd5e1', label='p (target)')
    ax.plot(x, gauss(t), color='#0f172a', lw=2.5, label='q (fitted Gaussian)')
    ax.set(xlim=(-6, 6), ylim=(0, 0.62), xlabel='x')
    ax.set_yticks([])
    ax.set_title(title, fontsize=13)
axes[0].legend(fontsize=11, loc='upper left', frameon=False)
fig.savefig(OUT / 'week05-kl-direction.png', dpi=190, bbox_inches='tight')
