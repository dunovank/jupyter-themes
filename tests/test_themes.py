from jupyterthemes import install_theme, get_themes
from jupyterthemes import stylefx

import numpy as np

def install_themes():
    themes = get_themes()
    pass_list = []
    for t in themes:
        try:
            install_theme(theme=t, monofont=mf, nbfont=nf, tcfont=tc)
            pass_list.append(True)
        except Exception:
            pass_list.append(False)
    return np.all(pass_list)

def install_fonts():
    fonts = stylefx.stored_font_dicts('', get_all=True)
    fontvals = [list(fonts[ff]) for ff in ['mono', 'sans', 'serif']]
    monotest, sanstest, seriftest = [np.array(fv)[:4] for fv in fontvals]
    pass_list = []
    for i in range(4):
        mono, sans, serif = monotest[i], sanstest[i], seriftest[i]
        try:
            install_theme(theme=t, monofont=mono, nbfont=sans, tcfont=serif)
            pass_list.append(True)
        except Exception:
            pass_list.append(False)
        try:
            install_theme(theme=t, monofont=mono, nbfont=serif, tcfont=sans)
            pass_list.append(True)
        except Exception:
            pass_list.append(False)
    return np.all(pass_list)

install_themes()
install_fonts()
