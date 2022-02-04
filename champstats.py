import requests
import re
from functools import lru_cache

GAMEDATA = 'https://127.0.0.1:2999/liveclientdata/allgamedata'
CHAMPINFO = 'https://raw.communitydragon.org/latest/game/data/characters/{champion}/{champion}.bin.json'
DEFRAD = 65.
DEFWINDUP = 0.3

def champname(name):
    return name.split('game_character_displayname_')[1].lower()

class ChampStats():
    def __init__(self):
        gamedata = requests.get(GAMEDATA, verify = False).json()
        champnames = [champname(player['rawChampionName']) for player in gamedata['allPlayers']]
        self.champdata = {}
        for champion in champnames:
            champresponse = requests.get(CHAMPINFO.format(champion=champion)).json()
            self.champdata[champion] = {k.lower(): v for k, v in champresponse.items()}

    @lru_cache(maxsize=None)
    def getatkspd(self, target):
        rootkey = 'characters/{}/characterrecords/root'.format(target.lower())
        atkspdbase = self.champdata[target.lower()][rootkey]['attackSpeed']
        atkspdratio = self.champdata[target.lower()][rootkey]['attackSpeedRatio']
        return atkspdbase, atkspdratio
        
    @lru_cache(maxsize=None)
    def getwindup(self, target):
        rootkey = 'characters/{}/characterrecords/root'.format(target.lower())
        basicatk = self.champdata[target.lower()][rootkey]['basicAttack']
        winduppct = 0.3
        windupmod = 0.
        if 'mAttackDelayCastOffsetPercent' in basicatk:
            winduppct = basicatk['mAttackDelayCastOffsetPercent'] + DEFWINDUP
        if 'mAttackDelayCastOffsetPercentAttackSpeedRatio' in basicatk:
            windupmod = basicatk['mAttackDelayCastOffsetPercentAttackSpeedRatio']
        print("Windup %: {}".format(winduppct))
        print("Windup Modifier: {}".format(windupmod))
        return winduppct, windupmod

    @lru_cache(maxsize=None)
    def getrad(self, target):
        rootkey = 'characters/{}/characterrecords/root'.format(target.lower())
        return self.champdata[target.lower()][rootkey].get('overrideGameplayCollisionRadius',DEFRAD)

    def names(self):
        return self.champdata.keys()

    @lru_cache(maxsize=None)
    def getspells(self,target):
        rootkey = 'characters/{}/characterrecords/root'.format(target.lower())
        return [
            self.champdata[target.lower()]['characters/{}/spells/{}'.format(target.lower(), spell.lower())]['mSpell']
            for spell in self.champdata[target.lower()][rootkey]['spellNames']
        ]

    @lru_cache(maxsize=None)
    def ismelee(self,target):
        rootkey = 'characters/{}/characterrecords/root'.format(target.lower())
        identities = self.champdata[target.lower()][rootkey]['purchaseIdentities']
        return any(identity for identity in identities if identity == 'Melee')
    