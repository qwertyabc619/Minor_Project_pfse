import os
import pandas as pd


def aisc_w_sections(units: str) -> pd.DataFrame:
    '''
    Returns the AiSC W Sections from the appropriate csv file (located within the same folder as the python module file) with the desired units
    '''
    
    if units == "si":
        df = pd.read_csv(os.path.abspath('aisc_w_sections_si.csv'))
        #Unscale the data based on the ReadME file
        df.Ix = df.Ix * 1e6
        df.Zx = df.Zx * 1e3
        df.Sx = df.Sx * 1e3
        df.Iy = df.Iy * 1e6
        df.Zy = df.Zy * 1e3
        df.Sy = df.Sy * 1e3
        df.J = df.J * 1e3
        df.Cw = df.Cw * 1e9
    elif units == "us":
        df = pd.read_csv(os.path.abspath('aisc_w_sections_us.csv'))
    df = df.set_index("Section", drop=False)
    return df



    
