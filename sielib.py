# file: sielib.py
# content: collection of import, export functions for data files
# Created: 13 December 2024
# Author: Roch Schanen
# comments: this library is in constant development

from numpy import loadtxt

version_history = {}

def import_TorsionOscilla_FreqScan_20241213_112400(fp):

    r"""
    created: 2024/12/13 at 11:24:00
    Oscillator: work-experiments-TorsOsc-2024-2.0
    Measurement test for LN2 Vacuum Can (on the portable setup)
    file copy from: \\luna.lancs.ac.uk\FST\PY\Milikelvin\He4_fridge\TO\202412\    
    file's first 4 lines:
    -->
    % Fsweep 11  at:    09/12/2024  15:14:15    drive_mV 7000.000000    DVM  0.000000
    freq    Vx  Vy  time
    8.8000000000E+1 1.8358300000E-5 3.8731300000E-4 3.8166019067E+9
    8.8007070707E+1 1.8656400000E-5 3.8957800000E-4 3.8166019098E+9
    <--
    """

    fh = open(fp, "r")
    tx = fh.readline()
    fh.close()

    file, date, time, drive, dvm = tx.split("\t")

    def seconds(s):
        t =  float(s[0:2])*3600
        t += float(s[3:5])*60
        t += float(s[6: ])*1
        return t

    info = {
        "filename"  :   fp.split("/")[-1],
        "filenum"   :   int(file[9:].split()[0]),
        "date"      :   date,
        "time"      :   time,
        "seconds"   :   seconds(time),
        "drive"     :   float(drive.split(" ")[-1])*1E-3,
        }

    data = loadtxt(fp,
        comments    = ["%","freq"],
        converters  = {
            0: float,       # freq
            1: float,       # Vx
            2: float,       # Vy
            3: float,       # time
            },
        )

    T  = data[:, 3] - data[0, 3]
    F  = data[:, 0]
    X  = data[:, 1]
    Y  = data[:, 2]

    return info, (T, F, X, Y)


version_history["0.0"] = """
version 0.0 (13 december 2024):
    add import function: "import_TorsionOscilla_FreqScan_20241213_112400()"
"""

### 

if __name__ == "__main__":

    ###  display version ###

    current_version = list(version_history.keys())[-1]

    print(f"sielib current version: {current_version}")
    print(f"-----------------------")

    print()
    print(f"history")
    print(f"-------")
    for v in version_history.values():
        print(v)

    """ example codes """

    if current_version == "0.0":

        ### import test file ###
        
        fp = "./fswp_full_1.dat"
        
        print()
        print(f"import file:")
        print(f"------------")
        print(f"\t'{fp}'")

        Info, Data = import_TorsionOscilla_FreqScan_20241213_112400(fp)

        ### display file info ###

        print()
        print(f"Info:")
        print(f"-----")
        
        for k in Info.keys():
            print(f"{k:>10} = '{Info[k]}'")

        ### display file data ###

        print()
        print(f"Data:")
        print(f"-----")
        
        T, F, X, Y = Data

        print(f"{'line':>5}: {'T[s]':>10}, {'F[Hz]':>10}, {'X[V]':>10}, {'Y[V]':>10}")
        for i in range(3): print(f"{i:5}: {T[i]:10.1f}, {F[i]:10.6f}, {X[i]:10.3e}, {Y[i]:10.3e}")
        print(f"{'...':>5}: {'...':>10}, {'...':>10}, {'...':>10}, {'...':>10}")
        for i in range(T.size-3, T.size): print(f"{i:5}: {T[i]:10.1f}, {F[i]:10.6f}, {X[i]:10.3e}, {Y[i]:10.3e}")

        r"""

        sielib current version: 0.0
        -----------------------

        history
        -------

        version 0.0 (13 december 2024):
            add import function: "import_TorsionOscilla_FreqScan_20241213_112400()"


        import file:
        ------------
            './fswp_full_1.dat'

        Info:
        -----
          filename = 'fswp_full_1.dat'
           filenum = '1'
              date = '17/12/2024'
              time = '16:51:25'
           seconds = '60685.0'
             drive = '7.0'

        Data:
        -----
         line:       T[s],      F[Hz],       X[V],       Y[V]
            0:        0.0,  88.044000,  2.038e-05,  4.380e-04
            1:        8.1,  88.053657,  2.158e-05,  4.410e-04
            2:       16.1,  88.063313,  2.301e-05,  4.460e-04
          ...:        ...,        ...,        ...,        ...
           97:      783.8,  88.980687,  2.325e-06,  3.163e-04
           98:      791.9,  88.990343,  2.682e-06,  3.179e-04
           99:      800.0,  89.000000,  2.563e-06,  3.175e-04

        """
