import re
from database import calc_stats, find_animal, find_weapon, ANIMALS


def parse_pets(content: str) -> list[dict]:
    animals = []
    lines = content.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        name_match = re.match(r'^.{1,3}\s*([a-zA-Z][a-zA-Z0-9]*)\s*$', line)

        if name_match and not re.match(r'^(HP|STR|PR|WP|MAG|MR|Lvl)', line, re.IGNORECASE):
            raw_name = name_match.group(1).strip().lower()
            key, base = find_animal(raw_name)

            if raw_name in ['pets', 'alone', 'your', 'the', 'and']:
                i += 1
                continue

            level, xp_cur, xp_max = 1, 0, 0
            computed = {}
            j = i + 1

            while j < len(lines) and j < i + 6:
                stat_line = lines[j].strip()

                lv_m = re.match(r'Lvl\.(\d+)\s*\[([0-9,]+)/([0-9,]+)\]', stat_line)
                if lv_m:
                    level   = int(lv_m.group(1))
                    xp_cur  = int(lv_m.group(2).replace(',',''))
                    xp_max  = int(lv_m.group(3).replace(',',''))
                    j += 1
                    continue

                hp_m = re.search(r'HP\s*:?\s*(\d+)', stat_line, re.IGNORECASE)
                wp_m = re.search(r'WP\s*:?\s*(\d+)', stat_line, re.IGNORECASE)
                if hp_m: computed['hp'] = int(hp_m.group(1))
                if wp_m: computed['wp'] = int(wp_m.group(1))

                str_m = re.search(r'STR\s*:?\s*(\d+)', stat_line, re.IGNORECASE)
                mag_m = re.search(r'MAG\s*:?\s*(\d+)', stat_line, re.IGNORECASE)
                if str_m: computed['str'] = int(str_m.group(1))
                if mag_m: computed['mag'] = int(mag_m.group(1))

                pr_m = re.search(r'PR\s*:?\s*(\d+)', stat_line, re.IGNORECASE)
                mr_m = re.search(r'MR\s*:?\s*(\d+)', stat_line, re.IGNORECASE)
                if pr_m: computed['pr'] = float(pr_m.group(1))
                if mr_m: computed['mr'] = float(mr_m.group(1))

                if re.match(r'^.{1,3}\s*[a-zA-Z][a-zA-Z]+\s*$', stat_line) and not any(
                    k in stat_line.upper() for k in ['HP','STR','PR','WP','MAG','MR','LVL']
                ):
                    break

                j += 1

            if base and level:
                full = calc_stats(level, base['hp'], base['str'], base['pr'],
                                  base['wp'], base['mag'], base['mr'])
                computed['ehp_phys'] = full['ehp_phys']
                computed['ehp_mag']  = full['ehp_mag']

            if key and level > 0 and computed:
                animals.append({
                    'name': key,
                    'display_name': raw_name,
                    'level': level,
                    'xp_current': xp_cur,
                    'xp_max': xp_max,
                    'rank': base['rank'] if base else 'unknown',
                    'base_stats': {
                        'hp': base['hp'], 'str': base['str'], 'pr': base['pr'],
                        'wp': base['wp'], 'mag': base['mag'], 'mr': base['mr']
                    } if base else {},
                    'computed': computed,
                    'is_leveled': level > 1,
                })

            i = j
        else:
            i += 1

    return animals


def parse_weapons(content: str) -> list[dict]:
    from database import WEAPONS
    weapons = []
    lines = content.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        slot_match   = re.search(r'\[(\d+)\]', line)
        rarity_match = re.search(
            r'(Common|Uncommon|Rare|Epic|Mythical|Legendary|Fabled|Gem)',
            line, re.IGNORECASE
        )

        found_wid, found_wdata = None, None
        for wid, wdata in WEAPONS.items():
            if wdata['name'].lower() in line.lower():
                found_wid, found_wdata = wid, wdata
                break
            for alias in wdata['alias']:
                if alias.lower() in line.lower():
                    found_wid, found_wdata = wid, wdata
                    break
            if found_wid:
                break

        if found_wdata:
            weapons.append({
                'slot': int(slot_match.group(1)) if slot_match else len(weapons)+1,
                'rarity': rarity_match.group(1).lower() if rarity_match else 'unknown',
                'name': found_wdata['name'],
                'weapon_id': found_wid,
                'weapon_data': found_wdata,
            })

    return weapons
