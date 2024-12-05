#!/bin/env python
# -*- coding: utf-8 -*-

""" test_gws.py:  
    2024-04-18, MvdS: initial version.
"""


import colored_traceback
colored_traceback.add_hook()

import numpy as np
import pandas as pd


def main():
    """Main function."""

    test_isco()
    exit(0)

    
def test_isco():
    import sluyspy.gws as gw
    
    df = pd.DataFrame(data=np.linspace(0,31,32), columns=['mass'])
    df.loc[0,'mass'] = 0.1
    df['f_isco'] = gw.isco_frequency_from_mass(df.mass, 0)
    print(df)
    
    df = pd.DataFrame(data=np.linspace(-1,1,11), columns=['spin'])
    df['f_isco'] = gw.isco_frequency_from_mass(10, df.spin)
    print(df)
    
    df['mass']   = np.linspace(5,55,11)
    df['f_isco'] = gw.isco_frequency_from_mass(df.mass, df.spin)
    print(df)
    
    return


if __name__ == '__main__':
    main()

