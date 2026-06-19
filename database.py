def calc_stats(level, hp_s, str_s, pr_s, wp_s, mag_s, mr_s):
    hp   = 500 + 2 * level * hp_s
    str_ = 100 + level * str_s
    wp   = 500 + 2 * level * wp_s
    mag  = 100 + level * mag_s
    ipr  = 25 + 2 * level * pr_s
    imr  = 25 + 2 * level * mr_s
    pr   = 0.8 * ipr / (100 + ipr)
    mr   = 0.8 * imr / (100 + imr)
    ehp_phys = hp / (1 - pr) if pr < 1 else float('inf')
    ehp_mag  = hp / (1 - mr) if mr < 1 else float('inf')
    return {
        "hp": round(hp), "str": round(str_), "wp": round(wp),
        "mag": round(mag), "pr": round(pr * 100, 1), "mr": round(mr * 100, 1),
        "ehp_phys": round(ehp_phys), "ehp_mag": round(ehp_mag)
    }

ANIMALS = {
    "bee":        {"hp":1,"str":5,"pr":2,"wp":1,"mag":4,"mr":2, "rank":"common",   "total":15, "aliases":["bee"]},
    "bug":        {"hp":1,"str":6,"pr":2,"wp":1,"mag":2,"mr":3, "rank":"common",   "total":15, "aliases":["bug"]},
    "snail":      {"hp":2,"str":3,"pr":4,"wp":2,"mag":2,"mr":2, "rank":"common",   "total":15, "aliases":["snail"]},
    "beetle":     {"hp":2,"str":4,"pr":4,"wp":1,"mag":2,"mr":2, "rank":"common",   "total":15, "aliases":["beetle"]},
    "butterfly":  {"hp":1,"str":5,"pr":1,"wp":2,"mag":4,"mr":2, "rank":"common",   "total":15, "aliases":["butterfly"]},
    "chick":      {"hp":3,"str":2,"pr":1,"wp":3,"mag":3,"mr":2, "rank":"uncommon", "total":18, "aliases":["chick"]},
    "mouse":      {"hp":2,"str":5,"pr":2,"wp":3,"mag":2,"mr":2, "rank":"uncommon", "total":18, "aliases":["mouse"]},
    "chicken":    {"hp":3,"str":4,"pr":1,"wp":3,"mag":2,"mr":2, "rank":"uncommon", "total":18, "aliases":["chicken"]},
    "rabbit":     {"hp":2,"str":5,"pr":2,"wp":2,"mag":3,"mr":2, "rank":"uncommon", "total":18, "aliases":["rabbit","bunny"]},
    "capybara":   {"hp":3,"str":3,"pr":2,"wp":3,"mag":2,"mr":3, "rank":"uncommon", "total":18, "aliases":["capybara","capy"]},
    "sheep":      {"hp":3,"str":5,"pr":2,"wp":2,"mag":3,"mr":2, "rank":"rare",     "total":17, "aliases":["sheep"]},
    "pig":        {"hp":4,"str":5,"pr":2,"wp":2,"mag":2,"mr":2, "rank":"rare",     "total":17, "aliases":["pig"]},
    "cow":        {"hp":4,"str":4,"pr":2,"wp":3,"mag":2,"mr":2, "rank":"rare",     "total":17, "aliases":["cow"]},
    "dog":        {"hp":3,"str":5,"pr":2,"wp":3,"mag":2,"mr":2, "rank":"rare",     "total":17, "aliases":["dog"]},
    "cat":        {"hp":3,"str":4,"pr":2,"wp":3,"mag":3,"mr":2, "rank":"rare",     "total":17, "aliases":["cat"]},
    "crocodile":  {"hp":3,"str":4,"pr":4,"wp":1,"mag":2,"mr":2, "rank":"epic",     "total":16, "aliases":["crocodile","croc"]},
    "tiger":      {"hp":3,"str":6,"pr":1,"wp":2,"mag":2,"mr":2, "rank":"epic",     "total":16, "aliases":["tiger"]},
    "penguin":    {"hp":2,"str":3,"pr":2,"wp":2,"mag":5,"mr":2, "rank":"epic",     "total":16, "aliases":["penguin"]},
    "elephant":   {"hp":5,"str":4,"pr":2,"wp":1,"mag":2,"mr":2, "rank":"epic",     "total":16, "aliases":["elephant"]},
    "whale":      {"hp":5,"str":2,"pr":2,"wp":1,"mag":4,"mr":2, "rank":"epic",     "total":16, "aliases":["whale"]},
    "dragon":     {"hp":4,"str":6,"pr":1,"wp":2,"mag":4,"mr":2, "rank":"mythical", "total":19, "aliases":["dragon"]},
    "unicorn":    {"hp":3,"str":3,"pr":2,"wp":3,"mag":6,"mr":2, "rank":"mythical", "total":19, "aliases":["unicorn"]},
    "snowman":    {"hp":4,"str":4,"pr":2,"wp":4,"mag":1,"mr":4, "rank":"mythical", "total":19, "aliases":["snowman"]},
    "ghost":      {"hp":2,"str":4,"pr":1,"wp":4,"mag":4,"mr":4, "rank":"mythical", "total":19, "aliases":["ghost"]},
    "devo":       {"hp":4,"str":4,"pr":4,"wp":4,"mag":1,"mr":2, "rank":"mythical", "total":19, "aliases":["devo"]},
    "deer":       {"hp":3,"str":8,"pr":1,"wp":1,"mag":5,"mr":2, "rank":"legendary","total":20, "aliases":["deer"]},
    "fox":        {"hp":4,"str":9,"pr":1,"wp":3,"mag":1,"mr":2, "rank":"legendary","total":20, "aliases":["fox","gfox"]},
    "lion":       {"hp":5,"str":7,"pr":2,"wp":2,"mag":2,"mr":2, "rank":"legendary","total":20, "aliases":["lion","glion"]},
    "owl":        {"hp":3,"str":1,"pr":1,"wp":10,"mag":3,"mr":2,"rank":"legendary","total":20, "aliases":["owl","gowl"]},
    "squid":      {"hp":1,"str":1,"pr":1,"wp":6,"mag":6,"mr":5, "rank":"legendary","total":20, "aliases":["squid","gsquid"]},
    "gfish":      {"hp":0,"str":0,"pr":0,"wp":1,"mag":19,"mr":0,"rank":"gem",      "total":20, "aliases":["gfish","fish","gem fish"]},
    "camel":      {"hp":5,"str":1,"pr":0,"wp":5,"mag":11,"mr":0,"rank":"fabled",   "total":22, "aliases":["camel","gcamel"]},
    "panda":      {"hp":5,"str":2,"pr":9,"wp":5,"mag":9,"mr":0, "rank":"fabled",   "total":30, "aliases":["panda","gpanda"]},
    "shrimp":     {"hp":5,"str":9,"pr":0,"wp":5,"mag":9,"mr":0, "rank":"fabled",   "total":28, "aliases":["shrimp","gshrimp"]},
    "spider":     {"hp":0,"str":9,"pr":1,"wp":0,"mag":10,"mr":3,"rank":"fabled",   "total":23, "aliases":["spider","gspider"]},
    "dinohot":    {"hp":2,"str":12,"pr":0,"wp":4,"mag":0,"mr":0,"rank":"fabled",   "total":18, "aliases":["dinohot","dino"]},
    "glitchflamingo":{"hp":5,"str":9,"pr":2,"wp":1,"mag":1,"mr":2,"rank":"fabled", "total":20, "aliases":["glitchflamingo","flamingo","gflamingo"]},
    "glitchchatter":{"hp":2,"str":1,"pr":2,"wp":1,"mag":10,"mr":2,"rank":"fabled", "total":18, "aliases":["glitchchatter","chatter"]},
    "glitchparrot":{"hp":4,"str":10,"pr":1,"wp":2,"mag":4,"mr":1,"rank":"fabled",  "total":22, "aliases":["glitchparrot","parrot","gparrot"]},
    "glitchraccoon":{"hp":4,"str":7,"pr":3,"wp":4,"mag":2,"mr":5,"rank":"fabled",  "total":25, "aliases":["glitchraccoon","raccoon","graccoon"]},
    "glitchzebra": {"hp":3,"str":5,"pr":4,"wp":6,"mag":3,"mr":5,"rank":"fabled",   "total":26, "aliases":["glitchzebra","zebra","gzebra"]},
    "bear":       {"hp":5,"str":2,"pr":3,"wp":3,"mag":1,"mr":3, "rank":"fabled",   "total":17, "aliases":["bear","gbear"]},
    "eagle":      {"hp":2,"str":11,"pr":2,"wp":2,"mag":12,"mr":3,"rank":"fabled",  "total":32, "aliases":["eagle","geagle"]},
    "frog":       {"hp":1,"str":3,"pr":1,"wp":3,"mag":1,"mr":1, "rank":"fabled",   "total":10, "aliases":["frog","gfrog"]},
    "gorilla":    {"hp":7,"str":2,"pr":3,"wp":3,"mag":7,"mr":3, "rank":"fabled",   "total":25, "aliases":["gorilla","ggorilla"]},
    "wolf":       {"hp":5,"str":17,"pr":2,"wp":3,"mag":3,"mr":3,"rank":"fabled",   "total":33, "aliases":["wolf","gwolf"]},
    "koala":      {"hp":10,"str":4,"pr":2,"wp":11,"mag":2,"mr":2,"rank":"fabled",  "total":31, "aliases":["koala","gkoala","hkoala"]},
    "lizard":     {"hp":5,"str":4,"pr":2,"wp":1,"mag":2,"mr":11,"rank":"fabled",   "total":25, "aliases":["lizard","glizard","hlizard"]},
    "monkey":     {"hp":2,"str":11,"pr":3,"wp":7,"mag":2,"mr":2,"rank":"fabled",   "total":27, "aliases":["monkey","gmonkey","hmonkey"]},
    "snake":      {"hp":2,"str":13,"pr":3,"wp":3,"mag":10,"mr":3,"rank":"fabled",  "total":34, "aliases":["snake","gsnake","hsnake"]},
    "squid2":     {"hp":4,"str":10,"pr":3,"wp":1,"mag":12,"mr":2,"rank":"fabled",  "total":32, "aliases":["squid2","hsquid"]},
    "lobshot":    {"hp":0,"str":14,"pr":9,"wp":5,"mag":0,"mr":9,"rank":"fabled",   "total":37, "aliases":["lobshot","lob"]},
    "slothbot":   {"hp":3,"str":3,"pr":2,"wp":3,"mag":2,"mr":2, "rank":"fabled",   "total":15, "aliases":["slothbot","sloth"]},
    "hedgehot":   {"hp":0,"str":4,"pr":2,"wp":0,"mag":6,"mr":5, "rank":"fabled",   "total":17, "aliases":["hedgehot","hedgehog"]},
    "giantfrog":  {"hp":1,"str":12,"pr":0,"wp":4,"mag":0,"mr":0,"rank":"fabled",   "total":17, "aliases":["giantfrog","gfrog2"]},
    "dinobot":    {"hp":2,"str":5,"pr":4,"wp":7,"mag":8,"mr":0, "rank":"fabled",   "total":26, "aliases":["dinobot"]},
}

RANK_POWER = {
    "common": 1, "uncommon": 2, "rare": 3, "epic": 4,
    "mythical": 5, "legendary": 6, "gem": 7, "fabled": 8
}

def find_animal(name: str):
    name_lower = name.lower().strip()
    if name_lower in ANIMALS:
        return name_lower, ANIMALS[name_lower]
    for key, data in ANIMALS.items():
        if name_lower in [a.lower() for a in data["aliases"]]:
            return key, data
    return None, None

WEAPONS = {
    101: {"name":"Sword",       "alias":["sword"],                          "wp":(100,200),"stat":"STR","role":"attacker", "aoe":True,  "effect":None,          "desc":"Deals 35-55% STR to ALL enemies"},
    102: {"name":"HStaff",      "alias":["hstaff","heal staff"],            "wp":(150,225),"stat":"MAG","role":"healer",   "aoe":False, "effect":"Overheal",    "desc":"Heals lowest HP ally 110-160% MAG (can overheal to 150% max HP)"},
    103: {"name":"Bow",         "alias":["bow"],                            "wp":(120,220),"stat":"STR","role":"attacker", "aoe":False, "effect":None,          "desc":"Deals 110-160% STR to random enemy"},
    104: {"name":"Rune",        "alias":["rune","forgotten rune"],          "wp":(0,0),    "stat":"BOTH","role":"buffer",  "aoe":False, "effect":"StatBoost",   "desc":"Boosts all stats 5-15%, attacks 65% STR+65% MAG as TRUE DAMAGE"},
    105: {"name":"Shield",      "alias":["shield","aegis"],                 "wp":(150,250),"stat":None, "role":"tank",     "aoe":False, "effect":"Taunt",       "desc":"Applies Taunt to self for 2 turns"},
    106: {"name":"Orb",         "alias":["orb"],                            "wp":(0,0),    "stat":None, "role":"passive",  "aoe":False, "effect":None,          "desc":"No active — has TWO passives. Attacks with no weapon."},
    107: {"name":"VStaff",      "alias":["vstaff","vampire staff"],         "wp":(90,190), "stat":"MAG","role":"hybrid",   "aoe":True,  "effect":"Lifesteal",   "desc":"Deals 25-45% MAG to ALL enemies, heals allies by damage dealt"},
    108: {"name":"Dagger",      "alias":["dagger"],                         "wp":(100,200),"stat":"STR","role":"attacker", "aoe":False, "effect":"Poison",      "desc":"Deals 70-100% STR to random enemy, Poison for 3 turns"},
    109: {"name":"Wand",        "alias":["wand"],                           "wp":(150,250),"stat":"MAG","role":"attacker", "aoe":False, "effect":"WPSteal",     "desc":"Deals 80-115% MAG, steals WP (20-40% of damage) to lowest WP ally"},
    110: {"name":"FStaff",      "alias":["fstaff","flame staff"],           "wp":(100,200),"stat":"MAG","role":"attacker", "aoe":False, "effect":"Flame",       "desc":"Deals 75-95% MAG to random enemy, Flame for 3 turns"},
    111: {"name":"EStaff",      "alias":["estaff","energy staff"],          "wp":(100,200),"stat":"MAG","role":"attacker", "aoe":True,  "effect":None,          "desc":"Deals 35-65% MAG to ALL enemies"},
    112: {"name":"SStaff",      "alias":["sstaff","spirit staff"],          "wp":(150,250),"stat":"MAG","role":"healer",   "aoe":True,  "effect":"DefUp",       "desc":"Heals ALL allies 30-50% MAG + applies DefUp to all for 2 turns"},
    113: {"name":"Scepter",     "alias":["scepter"],                        "wp":(125,200),"stat":"MAG","role":"support",  "aoe":False, "effect":"WPRefill",    "desc":"Replenishes 65-95% MAG as WP to lowest WP ally (can overreplenish 150%)"},
    114: {"name":"RStaff",      "alias":["rstaff","res staff","resurrection staff"],"wp":(300,400),"stat":"MAG","role":"reviver","aoe":False,"effect":"Revive", "desc":"Revives a dead ally and heals them 60-90% MAG"},
    115: {"name":"Axe",         "alias":["axe","glacial axe"],              "wp":(160,260),"stat":"STR","role":"attacker", "aoe":False, "effect":"Freeze",      "desc":"Deals 40-60% STR to random enemy, Freeze for 2 turns"},
    116: {"name":"Banner",      "alias":["banner","vanguard banner"],       "wp":(235,290),"stat":None, "role":"buffer",   "aoe":True,  "effect":"AttUp",       "desc":"Applies AttUp to ALL allies for 2 turns (stronger on recast)"},
    117: {"name":"Scythe",      "alias":["scythe","great scythe"],          "wp":(100,200),"stat":"STR","role":"attacker", "aoe":False, "effect":"Mortality",   "desc":"Deals 70-100% STR to random enemy, Mortality for 2 turns"},
    118: {"name":"CRune",       "alias":["crune","celebration rune"],       "wp":(100,200),"stat":None, "role":"support",  "aoe":False, "effect":"Celebration", "desc":"Applies Celebration to lowest HP ally for 3 turns"},
    119: {"name":"PStaff",      "alias":["pstaff","purify staff"],          "wp":(150,250),"stat":"MAG","role":"healer",   "aoe":False, "effect":"SacredWard",  "desc":"Remove debuff, heal 50-100% MAG, apply Sacred Ward for 2 turns"},
    120: {"name":"LScythe",     "alias":["lscythe","leech scythe"],         "wp":(130,230),"stat":"STR","role":"attacker", "aoe":False, "effect":"Leech",       "desc":"Deals 50-80% STR + Leech 3 turns (+40-60% bonus if Leech already on target)"},
    121: {"name":"FFish",       "alias":["ffish","foul fish"],              "wp":(180,280),"stat":"STR","role":"attacker", "aoe":False, "effect":"Stinky",      "desc":"Deals 50-80% STR to random enemy, Stinky for 2 turns"},
    122: {"name":"LRune",       "alias":["lrune","luck rune"],              "wp":(100,200),"stat":"BOTH","role":"attacker","aoe":False, "effect":None,          "desc":"Hits random enemy 5 times with 1-40% STR or MAG each (random per hit)"},
    123: {"name":"CStaff",      "alias":["cstaff","counter staff"],         "wp":(150,250),"stat":"STR","role":"breaker",  "aoe":False, "effect":"BuffReduce",  "desc":"Reduces enemy buff effectiveness 70-50%, deals 80-120% STR"},
    124: {"name":"Soul Tithe",  "alias":["soultithe","tithe"],              "wp":(50,100), "stat":"MAG","role":"attacker", "aoe":False, "effect":"WPDrain",     "desc":"Absorbs 10-25% of all allies WP, deals 35-45% MAG per 100 WP absorbed"},
    125: {"name":"BHStaff",     "alias":["bhstaff","thorn staff"],          "wp":(140,240),"stat":None, "role":"support",  "aoe":True,  "effect":"ThornTether", "desc":"Applies Thorn Tether to allies for 2 turns"},
    126: {"name":"Arbiter Edge","alias":["arbiter","edge"],                 "wp":(125,225),"stat":"BOTH","role":"hybrid",  "aoe":False, "effect":"SinVirtue",   "desc":"Gains Sin stacks on damage, Virtue stacks on heal/replenish"},
    127: {"name":"Wbow",        "alias":["wbow","war bow","heavy bow"],     "wp":(280,480),"stat":"STR","role":"attacker", "aoe":False, "effect":"HeavyArrow",  "desc":"Load or consume Heavy Arrow (loading free, consuming fires powerful shot)"},
    128: {"name":"Gaze",        "alias":["gaze"],                           "wp":(0,0),    "stat":"MAG","role":"controller","aoe":False,"effect":"MindControl", "desc":"Forces random enemy to attack its own allies at 30-40% effectiveness"},
    129: {"name":"Claw",        "alias":["claw"],                           "wp":(100,200),"stat":"MAG","role":"hybrid",   "aoe":False, "effect":"DebuffSteal", "desc":"Moves debuff from enemy to most-buffed ally (reduced 20-50%), deals 120-170% MAG"},
}

RANK_POWER = {"common":1,"uncommon":2,"rare":3,"epic":4,"mythical":5,"legendary":6,"gem":7,"fabled":8}

def find_weapon(name: str):
    name_lower = name.lower().strip()
    for wid, wdata in WEAPONS.items():
        if name_lower == wdata["name"].lower():
            return wid, wdata
        if name_lower in [a.lower() for a in wdata["alias"]]:
            return wid, wdata
    return None, None

TEAM_TYPES = {
    "streaker": {
        "desc": "Survive long battles with healing, revives and WP sustain",
        "stat_priority": ["mag","wp","hp","pr","mr"],
        "key_weapons": [114,119,112,118,113,116,105],
        "notes": "Focus on MAG animals for healing weapons. RStaff + PStaff combo is top tier."
    },
    "breaker": {
        "desc": "Break enemy streaks with status effects and burst damage",
        "stat_priority": ["str","mag","wp","hp"],
        "key_weapons": [115,108,121,123,128,117,129],
        "notes": "Focus on high STR/MAG animals. Freeze, Poison, Stinky are best debuffs."
    }
}
