"""
"""

def conplot(veloc):

    cs = plt.contourf(veloc, levels=np.arange(0, 1, 0.01))
    cs.changed()