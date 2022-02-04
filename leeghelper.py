import time

LETHALTEMPO = 'ASSETS/Perks/Styles/Precision/LethalTempo/LethalTempo.lua'
HAILOFBLADES = 'ASSETS/Perks/Styles/Domination/HailOfBlades/HailOfBladesBuff.lua'
STACKEDLETHALTEMPO_R = 30.
STACKEDLETHALTEMPO_M = 90.

class leeghelper:

    @staticmethod
    def getattacktime(champion, atkspdbase, atkspdratio, atkspdcap):
        atkspd = min(atkspdcap, (champion.atkspdmult - 1) * atkspdratio + atkspdbase)
        return 1. / atkspd

    @staticmethod
    def getwinduptime(champion, atkspdbase, atkspdratio, winduppct, windupmod, atkspdcap):
        atktime = leeghelper.getattacktime(champion, atkspdbase, atkspdratio, winduppct, windupmod, atkspdcap)
        winduptimebase = (1 / atkspdbase) * winduppct
        winduptime = winduptimebase + ((atktime * winduppct) - winduptimebase) * (1 + windupmod)
        return min(winduptime, atktime)


