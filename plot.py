"""
Created on Mon Dec 21 14:44:04 2020

@author: theknight
"""

def conplot(veloc):

    cs = plt.contourf(veloc, levels=np.arange(0, 1, 0.01))
    cs.changed()