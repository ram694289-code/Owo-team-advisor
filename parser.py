import re
from database import calc_stats, find_animal, find_weapon, ANIMALS


def _strip_line(line: str) -> str:
    """Remove emojis, markdown bold/italic, and misc symbols for cleaner parsing."""
    line = re.sub(r'[^\x00-\x7F]+', ' ', line)   # strip non-ASCII (emojis)
    line = re.sub(r'\*+', '', line)                # remove ** bold **
    line = re.sub(r'[|,:/\\#!?]', ' ', line)       # punctuation → space
    return line.strip()


def _extract_level(text: str):
    """Try several OwO level formats, return (level, xp_cur, xp_max)."""
    # Lvl.14 [500/1,000]  or  Lvl 14 [500/1000]
    m = re.search(r'Lvl?\.?\s*(\d+)\s*\[([0-9,]+)/([0-9,]+)\]', text, re.IGNORECASE)
    if m:
        return int(m.group(1)), int(m.group(2).replace(',', '')), int(m.group(3).replace(',', ''))
    # [Lv.14]
    m = re.search(r'\[Lv\.?\s*(\d+)\]', text, re.IGNORECASE)
    if m:
        return int(m.group(1)), 0, 0
    # Lv.14  or  Lvl.14  or  Level 14
    m = re.search(r'Lvl?\.?\s*(\d+)', text, re.IGNORECASE)
    if m:
        return int(m.group(1)), 0, 0
    return 1, 0, 0


def _extract_stats(text: str) -> dict:
    """Pull HP/STR/MAG/WP/PR/MR values from any line format."""
    stats = {}
    for stat, pattern in [
        ('hp',  r'HP\s*:?\s*(\d+)'),
        ('str', r'STR\s*:?\s*(\d+)'),
        ('mag', r'MAG\s*:?\s*(\d+)'),
        ('wp',  r'WP\s*:?\s*(\d+)'),
        ('pr',  r'PR\s*:?\s*(\d+(?:\.\d+)?)'),
        ('mr',  r'MR\s*:?\s*(\d+(?:\.\d+)?)'),
    ]:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            stats[stat] = (float(m.group(1)) if stat in ('pr', 'mr')
                           else int(m.group(1)))
    return stats


def _find_animal_in_line(line: str):
    """
    Try to find a known animal name anywhere in a cleaned line.
    Returns (raw_name, db_key, base_data) or (raw_name, None, None).
    """
    SKIP = {
        'pets', 'your', 'the', 'and', 'alone', 'battle', 'all', 'animals',
        'hp', 'str', 'pr', 'wp', 'mag', 'mr', 'lvl', 'lv', 'level', 'xp',
        'total', 'page', 'none', 'equipment', 'no', 'not', 'info', 'weapon',
        'common', 'rare', 'epic', 'mythical', 'legendary', 'fabled',
        'uncommon', 'gem', 'for', 'with', 'has', 'have', 'you', 'is',
        'are', 'at', 'to', 'in', 'of', 'team', 'slot', 'set', 'get',
    }
    clean = _strip_line(line)
    # Remove level info and bracket text before splitting
    clean = re.sub(r'Lvl?\.?\s*\d+', '', clean, flags=re.IGNORECASE)
    clean = re.sub(r'\[.*?\]', '', clean)
    clean = re.sub(r'\(.*?\)', '', clean)

    words = [w.strip() for w in clean.split() if w.strip().isalpha() and len(w.strip()) > 1]

    for word in words:
        if word.lower() in SKIP:
            continue
        k, b = find_animal(word.lower())
        if k:
            return word.lower(), k, b

    # No database match — return the first non-skip word as a raw name anyway
    for word in words:
        if word.lower() not in SKIP and len(word) >= 3:
            return word.lower(), None, None

    return None, None, None


def parse_pets(content: str) -> list[dict]:
    animals = []
    seen = set()
    lines = content.split('\n')

    # Quick reject: clearly not a pets message
    STAT_PREFIXES = re.compile(r'^(HP|STR|PR|WP|MAG|MR|XP|Lvl|Page|Total)', re.IGNORECASE)

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Skip pure stat / header lines
        if STAT_PREFIXES.match(line):
            i += 1
            continue

        raw_name, key, base = _find_animal_in_line(line)

        if not raw_name or raw_name in seen:
            i += 1
            continue

        # Pull level + stats from current line AND the next few lines
        combined = line
        j = i + 1
        while j < min(i + 8, len(lines)):
            nxt = lines[j].strip()
            if not nxt:
                j += 1
                continue
            # Stop if we hit another animal line
            next_name, _, _ = _find_animal_in_line(nxt)
            if next_name and next_name != raw_name and next_name not in seen:
                break
            combined += '\n' + nxt
            j += 1

        level, xp_cur, xp_max = _extract_level(combined)
        computed = _extract_stats(combined)

        # Fill missing stats from the base database using calc_stats
        if base:
            try:
                full = calc_stats(level, base['hp'], base['str'], base['pr'],
                                  base['wp'], base['mag'], base['mr'])
                for stat in ('hp', 'str', 'mag', 'wp', 'pr', 'mr', 'ehp_phys', 'ehp_mag'):
                    computed.setdefault(stat, full.get(stat, 0))
            except Exception:
                pass

        seen.add(raw_name)
        animals.append({
            'name':         key or raw_name,
            'display_name': raw_name,
            'level':        level,
            'xp_current':   xp_cur,
            'xp_max':       xp_max,
            'rank':         base['rank'] if base else 'unknown',
            'base_stats':   {
                'hp': base['hp'], 'str': base['str'], 'pr': base['pr'],
                'wp': base['wp'], 'mag': base['mag'], 'mr': base['mr']
            } if base else {},
            'computed':     computed,
            'is_leveled':   level > 1,
        })

        i = j

    return animals


def parse_weapons(content: str) -> list[dict]:
    from database import WEAPONS
    weapons = []

    for line in content.split('\n'):
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
            for alias in wdata.get('alias', []):
                if alias.lower() in line.lower():
                    found_wid, found_wdata = wid, wdata
                    break
            if found_wid:
                break

        if found_wdata:
            weapons.append({
                'slot':        int(slot_match.group(1)) if slot_match else len(weapons) + 1,
                'rarity':      rarity_match.group(1).lower() if rarity_match else 'unknown',
                'name':        found_wdata['name'],
                'weapon_id':   found_wid,
                'weapon_data': found_wdata,
                'quality':     rarity_match.group(1).title() if rarity_match else 'Unknown',
            })

    return weapons
