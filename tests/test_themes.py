from jupyterthemes import install_theme, get_themes
from jupyterthemes import stylefx

def install_themes():
    themes = get_themes()
    for t in themes:
        try:
            install_theme(theme=t, monofont=mf, nbfont=nf, tcfont=tc)
        except Exception:
            return False
    return True

def install_fonts():
    fonts = stylefx.stored_font_dicts('', get_all=True)
    fontvals = [list(fonts[ff]) for ff in ['mono', 'sans', 'serif']]
    monotest, sanstest, seriftest = [fv[:4] for fv in fontvals]
    for i in range(4):
        mono, sans, serif = monotest[i], sanstest[i], seriftest[i]
        try:
            install_theme(theme=t, monofont=mono, nbfont=sans, tcfont=serif)
        except Exception:
            return False
        try:
            install_theme(theme=t, monofont=mono, nbfont=serif, tcfont=sans)
        except Exception:
            return False
    return True

install_themes()
install_fonts()
