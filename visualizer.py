"""
Executing the programm.
"""

import plot
import dataorganization
import volume


def main():
    ds, us, vs, dcs, lons = dataorganization.dataconverter(range(31, 54))
#    new = plot.interpolator(us, dcs)
#    plot.conplot(new, "u", ds)
    new2, gesdis = plot.interpolator(vs, dcs)
    newvolumes, fullvolume, errors1, fullerror = volume.integrator(new2, gesdis, ds)
    plot.conplot(new2, "v", ds, lons, newvolumes)
    volumes, fullvolume1, errors, fullerror1 = volume.integrator(vs, gesdis, ds)
    print("Gesamt-Volumentransport in [SV]: ", fullvolume/1e6, "±", fullerror/1e6)
    plot.volumeplot(volumes, errors)


if __name__ == "__main__":
    main()
