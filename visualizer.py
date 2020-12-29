"""
Executing the programm.
"""

import plot
import dataorganization


def main():
    ds, us, vs, dcs, lons = dataorganization.dataconverter(range(31, 54))
#    new = plot.interpolator(us, dcs)
#    plot.conplot(new, "u", ds)
    new2 = plot.interpolator(vs, dcs)
    plot.conplot(new2, "v", ds, lons)


if __name__ == "__main__":
    main()
