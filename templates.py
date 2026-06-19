TEMPLATES = [
    {
        "id": "spider_crune",
        "name": "Spider CRune (Spoon)",
        "tier": "S",
        "style": "streaker",
        "level_min": 60,
        "description": "Best streak team at 60+. Spider attacks, CRune heals lowest HP animal repeatedly.",
        "strategy": "Spider deals damage while CRune keeps the team alive indefinitely. Energize passive on CRune is MANDATORY.",
        "slots": [
            {
                "position": 1,
                "role": "Attacker",
                "ideal_weapons": ["Bow", "Rune"],
                "weapon_stats": "STR close to 160%, WP Cost close to 120",
                "ideal_animals": ["gspider", "spider"],
                "stat_needs": {"str": 9},
                "passive": ["strength", "snail"],
                "notes": "Spider is the ONLY option. Want Bow STR close to 160%."
            },
            {
                "position": 2,
                "role": "CRune Healer",
                "ideal_weapons": ["CRune", "Rune of Celebration"],
                "weapon_stats": "Heal close to 50%, WP Cost close to 100, Replenish close to 40%",
                "ideal_animals": ["capybara", "high WP animal"],
                "stat_needs": {"wp": 3},
                "passive": ["energize"],
                "notes": "Energize passive is REQUIRED. Without it this team doesn't work."
            },
            {
                "position": 3,
                "role": "Tank",
                "ideal_weapons": ["Shield"],
                "weapon_stats": "WP Cost close to 150, Sprout or Energize passive",
                "ideal_animals": ["lobshot", "eagle", "high HP + PR animal"],
                "stat_needs": {"hp": 5, "pr": 2},
                "passive": ["sprout", "energize"],
                "notes": "High HP + PR tank. LobBot is best, Eagle is great F2P option."
            }
        ],
        "requires_weapons": ["CRune", "Rune of Celebration"],
        "requires_animals": ["gspider", "spider"],
        "counters": ["Most teams at 60+"],
        "countered_by": ["Scythe Blitz", "Double Scythe"],
    },
    {
        "id": "pstaff_stall",
        "name": "PStaff Stall (True Stall)",
        "tier": "S",
        "style": "streaker",
        "level_min": 50,
        "description": "Best stall team at 50+. PStaff removes debuffs and heals, SStaff with high WP cost enables Discharge.",
        "strategy": "PStaff removes enemy debuffs keeping team alive. SStaff with 200-250 WP cost maximizes Discharge damage. Sprout shield makes team near unkillable.",
        "slots": [
            {
                "position": 1,
                "role": "Attacker/SStaff",
                "ideal_weapons": ["SStaff", "Spirit Staff"],
                "weapon_stats": "WP Cost 200-250 (for Discharge), Heal 40-50%",
                "ideal_animals": ["gspider", "gfish", "snake", "eagle", "high STR or MAG fabled"],
                "stat_needs": {"str": 7},
                "passive": ["mana_tap", "energize"],
                "notes": "SStaff with HIGH WP cost (200-250) is critical for Discharge damage."
            },
            {
                "position": 2,
                "role": "PStaff Healer",
                "ideal_weapons": ["PStaff", "Purify Staff"],
                "weapon_stats": "Heal close to 100%, WP Cost close to 150",
                "ideal_animals": ["high HP + MAG animal", "gorilla", "glion"],
                "stat_needs": {"mag": 5, "hp": 4},
                "passive": ["energize"],
                "notes": "High MAG + HP animal. Energize passive important."
            },
            {
                "position": 3,
                "role": "Tank",
                "ideal_weapons": ["Shield"],
                "weapon_stats": "Sprout passive REQUIRED",
                "ideal_animals": ["eagle", "lobshot", "high HP + PR animal"],
                "stat_needs": {"hp": 5, "pr": 3},
                "passive": ["sprout"],
                "notes": "Sprout passive on Shield is the core of stall. Eagle is best F2P tank."
            }
        ],
        "requires_weapons": ["PStaff", "Purify Staff", "Shield"],
        "requires_animals": [],
        "counters": ["Most teams at 50+", "RStaff Stall"],
        "countered_by": ["Rare edge compositions at same level"],
    },
    {
        "id": "rstaff_stall",
        "name": "RStaff Stall",
        "tier": "S",
        "style": "streaker",
        "level_min": 1,
        "description": "Best accessible streaker. Revives dead allies and stalls indefinitely. Works at any level.",
        "strategy": "RStaff revives dead teammates giving endless second chances. Attacker deals damage while tank absorbs hits. Very consistent streak team.",
        "slots": [
            {
                "position": 1,
                "role": "Attacker",
                "ideal_weapons": ["Bow", "Scythe", "Sword", "EStaff"],
                "weapon_stats": "Highest damage% possible, low WP cost",
                "ideal_animals": ["gspider", "snake", "wolf", "eagle", "fox", "high STR fabled"],
                "stat_needs": {"str": 7},
                "passive": ["strength", "critical", "mana_tap"],
                "notes": "High STR animal. Spider or Snake are top picks."
            },
            {
                "position": 2,
                "role": "Reviver",
                "ideal_weapons": ["RStaff", "Resurrection Staff"],
                "weapon_stats": "Heal close to 90%, WP Cost close to 300",
                "ideal_animals": ["gorilla", "lobshot", "high HP + WP + some MAG"],
                "stat_needs": {"hp": 5, "mag": 3, "wp": 3},
                "passive": ["energize", "kamikaze", "sacrifice"],
                "notes": "Gorilla is great F2P pick. High HP + some MAG for heal effectiveness."
            },
            {
                "position": 3,
                "role": "Tank",
                "ideal_weapons": ["Shield", "SStaff"],
                "weapon_stats": "Energize or Sprout passive",
                "ideal_animals": ["eagle", "dinobot", "lobshot", "high HP + PR"],
                "stat_needs": {"hp": 5, "pr": 2},
                "passive": ["sprout", "energize", "regeneration"],
                "notes": "Absorbs damage and buys time for reviver. Eagle is top F2P tank."
            }
        ],
        "requires_weapons": ["RStaff", "Resurrection Staff"],
        "requires_animals": [],
        "counters": ["Low-mid level teams", "Double AoE teams"],
        "countered_by": ["PStaff Stall at extreme levels", "Triple Sac Hybrid"],
    },
    {
        "id": "true_stall",
        "name": "True Stall (Holy Trinity)",
        "tier": "A",
        "style": "streaker",
        "level_min": 20,
        "description": "Classic Attacker + SStaff Healer + Shield Tank. Most common stall team. Great at mid levels.",
        "strategy": "Attacker deals damage, healer keeps team alive with SStaff, tank absorbs damage with Sprout shield. Very reliable.",
        "slots": [
            {
                "position": 1,
                "role": "Attacker",
                "ideal_weapons": ["Bow", "Scythe", "EStaff", "Sword", "VStaff"],
                "weapon_stats": "Highest STR% or MAG% damage, low WP cost",
                "ideal_animals": ["gspider", "fox", "snake", "eagle", "wolf", "high STR animal"],
                "stat_needs": {"str": 5},
                "passive": ["strength", "critical", "mana_tap"],
                "notes": "Position 1 goes first — high damage output is key. Spider/Fox are top picks."
            },
            {
                "position": 2,
                "role": "Healer",
                "ideal_weapons": ["SStaff", "Spirit Staff", "HStaff", "Healing Staff"],
                "weapon_stats": "Heal 40-50% MAG, low WP cost, Energize passive",
                "ideal_animals": ["glion", "gowl", "gorilla", "high MAG + HP animal"],
                "stat_needs": {"mag": 4, "hp": 3},
                "passive": ["energize", "sprout"],
                "notes": "MAG > WP stat priority. Energize passive keeps healing going. Lion/Owl work great."
            },
            {
                "position": 3,
                "role": "Tank",
                "ideal_weapons": ["Shield"],
                "weapon_stats": "Sprout passive for stall, or Energize/Regeneration",
                "ideal_animals": ["eagle", "elephant", "glion", "high HP + PR animal"],
                "stat_needs": {"hp": 4, "pr": 2},
                "passive": ["sprout", "energize", "regeneration"],
                "notes": "Sprout Shield is best for stall. Eagle is best F2P tank."
            }
        ],
        "requires_weapons": ["SStaff", "Spirit Staff", "HStaff", "Shield"],
        "requires_animals": [],
        "counters": ["Low level teams", "Double AoE at mid level"],
        "countered_by": ["Scythe Blitz", "Double AoE at high level"],
    },
    {
        "id": "scepter_stall",
        "name": "Scepter Stall",
        "tier": "A",
        "style": "streaker",
        "level_min": 15,
        "description": "Scepter transfers WP to healer and tank giving 2-4 bonus rounds of Taunt + healing.",
        "strategy": "Scepter pet passes WP to allies early. Once WP runs out it switches to attacking. Great at lower levels for extending battle.",
        "slots": [
            {
                "position": 1,
                "role": "Scepter Support",
                "ideal_weapons": ["Scepter"],
                "weapon_stats": "Replenish close to 95%, WP Cost close to 125, Energize passive",
                "ideal_animals": ["eagle", "snake", "fox", "decent WP animal"],
                "stat_needs": {"wp": 3},
                "passive": ["energize", "mana_tap", "critical"],
                "notes": "Eagle or Snake work great. WP transfers to healer+tank then switches to attacking."
            },
            {
                "position": 2,
                "role": "Healer",
                "ideal_weapons": ["SStaff", "Spirit Staff"],
                "weapon_stats": "Heal 40-50%, low WP cost, Energize passive",
                "ideal_animals": ["glion", "gowl", "gorilla", "high MAG animal"],
                "stat_needs": {"mag": 4},
                "passive": ["energize"],
                "notes": "High MAG healer. Gets bonus WP from scepter = more healing turns."
            },
            {
                "position": 3,
                "role": "Tank",
                "ideal_weapons": ["Shield"],
                "weapon_stats": "Energize or Regeneration passive",
                "ideal_animals": ["eagle", "elephant", "high HP + PR animal"],
                "stat_needs": {"hp": 4, "pr": 2},
                "passive": ["energize", "regeneration", "sprout"],
                "notes": "Tank also gets bonus WP from scepter = more Taunt turns."
            }
        ],
        "requires_weapons": ["Scepter", "SStaff", "Spirit Staff", "Shield"],
        "requires_animals": [],
        "counters": ["Low level teams without sustain"],
        "countered_by": ["High damage burst teams"],
    },
    {
        "id": "double_aoe_streak",
        "name": "Double AoE Streaker",
        "tier": "B",
        "style": "streaker",
        "level_min": 1,
        "description": "Two AoE attackers + healer. Easy to build, good at low levels.",
        "strategy": "EStaff + Sword hit all enemies every turn. HStaff keeps team alive. Simple and effective at low level.",
        "slots": [
            {
                "position": 1,
                "role": "MAG AoE Attacker",
                "ideal_weapons": ["EStaff", "Energy Staff", "VStaff"],
                "weapon_stats": "Damage close to 65% MAG, low WP cost",
                "ideal_animals": ["gfish", "penguin", "gowl", "high MAG animal"],
                "stat_needs": {"mag": 5},
                "passive": ["energize", "mana_tap"],
                "notes": "Fish (MAG:19 base) is the ultimate pick here. Owl also works well."
            },
            {
                "position": 2,
                "role": "STR AoE Attacker",
                "ideal_weapons": ["Sword"],
                "weapon_stats": "Damage close to 55% STR, low WP cost",
                "ideal_animals": ["gspider", "snake", "wolf", "fox", "high STR animal"],
                "stat_needs": {"str": 5},
                "passive": ["strength", "critical"],
                "notes": "Spider is top pick for STR AoE. Sword hits all enemies."
            },
            {
                "position": 3,
                "role": "Healer",
                "ideal_weapons": ["HStaff", "Healing Staff", "SStaff"],
                "weapon_stats": "Heal close to 160%, Energize passive",
                "ideal_animals": ["glion", "cow", "gowl", "decent MAG + HP animal"],
                "stat_needs": {"mag": 3, "hp": 3},
                "passive": ["energize"],
                "notes": "Any decent MAG animal works here. Lion/Owl/Cow are accessible options."
            }
        ],
        "requires_weapons": ["EStaff", "Energy Staff", "Sword", "HStaff", "SStaff"],
        "requires_animals": [],
        "counters": ["Low level teams"],
        "countered_by": ["Stall teams at mid-high level", "Single target high DPS"],
    },
    {
        "id": "scythe_blitz",
        "name": "Scythe Blitz",
        "tier": "A",
        "style": "breaker",
        "level_min": 30,
        "description": "Uses Mortality from Scythe to reduce enemy healing. High DPS with Flame Staff + Dagger breaks stall teams.",
        "strategy": "Scythe applies Mortality cutting enemy healing. Dagger/FStaff apply Poison/Flame for DoT. SStaff supports your team while enemies take constant damage.",
        "slots": [
            {
                "position": 1,
                "role": "Scythe Attacker",
                "ideal_weapons": ["Scythe"],
                "weapon_stats": "Damage close to 100% STR, low WP cost",
                "ideal_animals": ["snake", "wolf", "eagle", "fox", "high STR fabled"],
                "stat_needs": {"str": 7},
                "passive": ["strength", "critical"],
                "notes": "Mortality debuff cuts enemy healing significantly. High STR is key."
            },
            {
                "position": 2,
                "role": "DoT Attacker",
                "ideal_weapons": ["FStaff", "Flame Staff", "Dagger"],
                "weapon_stats": "Damage close to 95% MAG (FStaff) or 100% STR (Dagger)",
                "ideal_animals": ["lizard", "high MAG animal", "gfish"],
                "stat_needs": {"mag": 5},
                "passive": ["mana_tap", "critical"],
                "notes": "FStaff applies Flame DoT. Lizard is best holder (high MR). Fish also works."
            },
            {
                "position": 3,
                "role": "Support Healer",
                "ideal_weapons": ["SStaff", "Spirit Staff"],
                "weapon_stats": "Heal 40-50%, Energize passive",
                "ideal_animals": ["glion", "gowl", "gorilla", "decent MAG + HP"],
                "stat_needs": {"mag": 3, "hp": 3},
                "passive": ["energize"],
                "notes": "Keeps your team alive while DoT effects wear down enemies."
            }
        ],
        "requires_weapons": ["Scythe"],
        "requires_animals": [],
        "counters": ["RStaff Stall", "True Stall", "Spider CRune"],
        "countered_by": ["Teams at much higher level"],
    },
    {
        "id": "disruption",
        "name": "Disruption (Axe Freeze)",
        "tier": "B",
        "style": "breaker",
        "level_min": 20,
        "description": "Glacial Axe freezes enemy tank preventing Taunt. Then high DPS weapons hit exposed attacker/healer.",
        "strategy": "Axe freezes the enemy tank so it can't taunt. Dagger/FStaff then target the weaker attacker and healer directly.",
        "slots": [
            {
                "position": 1,
                "role": "Freeze Attacker",
                "ideal_weapons": ["Axe", "Glacial Axe"],
                "weapon_stats": "Damage close to 60% STR, WP Cost close to 160",
                "ideal_animals": ["snake", "wolf", "fox", "high STR animal"],
                "stat_needs": {"str": 6},
                "passive": ["strength", "critical", "mana_tap"],
                "notes": "Freeze stops enemy tank from Taunting. High STR animal needed."
            },
            {
                "position": 2,
                "role": "DPS Attacker",
                "ideal_weapons": ["Dagger", "FStaff", "Scythe"],
                "weapon_stats": "High damage%, low WP cost",
                "ideal_animals": ["gspider", "lizard", "eagle", "high STR/MAG"],
                "stat_needs": {"str": 5},
                "passive": ["strength", "mana_tap", "critical"],
                "notes": "With tank frozen, hits go to attacker and healer. Dagger adds Poison DoT."
            },
            {
                "position": 3,
                "role": "Support",
                "ideal_weapons": ["SStaff", "HStaff"],
                "weapon_stats": "Energize passive, decent heal%",
                "ideal_animals": ["glion", "gowl", "cow", "decent MAG animal"],
                "stat_needs": {"mag": 3},
                "passive": ["energize"],
                "notes": "Keeps your team alive. Some RNG involved with Freeze timing."
            }
        ],
        "requires_weapons": ["Axe", "Glacial Axe"],
        "requires_animals": [],
        "counters": ["Stall teams at low-mid level"],
        "countered_by": ["High level stall teams", "Teams with multiple taunters"],
    },
    {
        "id": "double_aoe_breaker",
        "name": "Double AoE Breaker",
        "tier": "B",
        "style": "breaker",
        "level_min": 1,
        "description": "Two AoE attackers wreck teams that rely on single-target defense. Great against stall teams at low level.",
        "strategy": "Sword + EStaff hit ALL enemies every turn. Hard for any single-target stall team to survive constant multi-hit pressure.",
        "slots": [
            {
                "position": 1,
                "role": "STR AoE Attacker",
                "ideal_weapons": ["Sword"],
                "weapon_stats": "Damage close to 55% STR, low WP cost",
                "ideal_animals": ["gspider", "wolf", "snake", "high STR animal"],
                "stat_needs": {"str": 6},
                "passive": ["strength", "critical"],
                "notes": "Hits all enemies with STR damage every turn."
            },
            {
                "position": 2,
                "role": "MAG AoE Attacker",
                "ideal_weapons": ["EStaff", "Energy Staff", "VStaff"],
                "weapon_stats": "Damage close to 65% MAG, low WP cost",
                "ideal_animals": ["gfish", "gowl", "penguin", "high MAG animal"],
                "stat_needs": {"mag": 5},
                "passive": ["energize", "mana_tap"],
                "notes": "Fish with EStaff is devastating — MAG:19 base shreds everything."
            },
            {
                "position": 3,
                "role": "Support/Healer",
                "ideal_weapons": ["SStaff", "HStaff", "Banner"],
                "weapon_stats": "Energize passive",
                "ideal_animals": ["glion", "cow", "decent MAG + HP"],
                "stat_needs": {"mag": 3},
                "passive": ["energize"],
                "notes": "Banner gives AttUp to both attackers, boosting AoE damage significantly."
            }
        ],
        "requires_weapons": ["Sword", "EStaff", "Energy Staff"],
        "requires_animals": [],
        "counters": ["Single-target defense teams", "Low level stall teams"],
        "countered_by": ["High level stall teams", "Meta stall at 40+"],
    },
]


def match_templates(animals: list, weapons: list, style: str) -> list:
    owned_weapon_names = {w["name"].lower() for w in weapons}
    owned_weapon_names.update({w.get("weapon_data", {}).get("name", "").lower() for w in weapons})

    results = []

    for template in TEMPLATES:
        if template["style"] != style:
            continue

        score = 0
        slot_assignments = []
        missing_key_weapons = []
        missing_key_animals = []

        required_met = False
        for req in template.get("requires_weapons", []):
            if req.lower() in owned_weapon_names:
                required_met = True
                score += 50
                break

        if template.get("requires_weapons") and not required_met:
            missing_key_weapons = template["requires_weapons"]
            score -= 30

        owned_animal_names = {a.get("display_name", "").lower() for a in animals}
        owned_animal_names.update({a.get("name", "").lower() for a in animals})

        for req in template.get("requires_animals", []):
            if req.lower() in owned_animal_names:
                score += 30
            else:
                missing_key_animals.append(req)

        max_level = max((a.get("level", 1) for a in animals), default=1)
        if max_level >= template["level_min"]:
            score += 20
        else:
            score -= 10

        used_animals = set()
        used_weapons = set()

        for slot in template["slots"]:
            best_animal, best_animal_score = None, -1
            best_weapon, best_weapon_score = None, -1

            for a in animals:
                if id(a) in used_animals:
                    continue
                a_score = score_animal_for_slot(a, slot)
                if a_score > best_animal_score:
                    best_animal_score = a_score
                    best_animal = a

            for w in weapons:
                if id(w) in used_weapons:
                    continue
                w_score = score_weapon_for_slot(w, slot)
                if w_score > best_weapon_score:
                    best_weapon_score = w_score
                    best_weapon = w

            if best_animal:
                used_animals.add(id(best_animal))
            if best_weapon:
                used_weapons.add(id(best_weapon))

            score += best_animal_score * 0.3
            score += best_weapon_score * 0.3

            slot_assignments.append({
                "position": slot["position"],
                "role": slot["role"],
                "animal": best_animal,
                "weapon": best_weapon,
                "weapon_data": best_weapon.get("weapon_data", {}) if best_weapon else {},
                "notes": slot["notes"],
                "passive": slot["passive"],
                "ideal_animals": slot["ideal_animals"],
                "ideal_weapons": slot["ideal_weapons"],
            })

        results.append({
            "template": template,
            "score": round(score, 1),
            "slots": slot_assignments,
            "missing_key_weapons": missing_key_weapons,
            "missing_key_animals": missing_key_animals,
            "ready": not missing_key_weapons and not missing_key_animals,
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def score_animal_for_slot(animal: dict, slot: dict) -> float:
    score = 0.0
    computed = animal.get("computed", {})
    base     = animal.get("base_stats", {})
    name     = animal.get("display_name", "").lower()
    rank     = animal.get("rank", "common")
    level    = animal.get("level", 1)

    ideal_animals = [a.lower() for a in slot.get("ideal_animals", [])]
    if name in ideal_animals:
        score += 50

    stat_needs = slot.get("stat_needs", {})
    for stat, min_val in stat_needs.items():
        base_val = base.get(stat, 0)
        if base_val >= min_val:
            score += base_val * 5
        else:
            score -= (min_val - base_val) * 3

    role = slot.get("role", "").lower()
    if "attacker" in role:
        score += computed.get("str", 0) * 0.3
        score += computed.get("mag", 0) * 0.2
    elif "healer" in role or "support" in role:
        score += computed.get("mag", 0) * 0.4
        score += computed.get("wp", 0) * 0.2
        score += computed.get("hp", 0) * 0.1
    elif "tank" in role:
        score += computed.get("hp", 0) * 0.3
        score += computed.get("pr", 0) * 0.5
        score += computed.get("mr", 0) * 0.3

    rank_bonus = {"common":0,"uncommon":2,"rare":4,"epic":8,"mythical":15,"legendary":25,"gem":30,"fabled":35}
    score += rank_bonus.get(rank, 0)
    score += level * 0.5

    return round(score, 2)


def score_weapon_for_slot(weapon: dict, slot: dict) -> float:
    score = 0.0
    wdata = weapon.get("weapon_data", {})
    if not wdata:
        return 0.0

    wname = wdata.get("name", "").lower()
    ideal_weapons = [w.lower() for w in slot.get("ideal_weapons", [])]

    if wname in ideal_weapons:
        score += 50

    role   = slot.get("role", "").lower()
    w_role = wdata.get("role", "").lower()
    role_map = {
        "attacker": ["attacker", "hybrid"],
        "healer":   ["healer", "reviver"],
        "tank":     ["tank"],
        "support":  ["support", "buffer"],
        "reviver":  ["reviver"],
        "crune healer": ["support"],
        "scepter support": ["support"],
        "dot attacker": ["attacker", "hybrid"],
        "freeze attacker": ["attacker"],
        "dps attacker": ["attacker", "hybrid"],
        "mag aoe attacker": ["attacker"],
        "str aoe attacker": ["attacker"],
        "support healer": ["healer", "support"],
        "support/healer": ["healer", "support"],
    }
    compatible = role_map.get(role, [role])
    if w_role in compatible:
        score += 20

    return round(score, 2)


def format_template_result(result: dict) -> str:
    template = result["template"]
    slots    = result["slots"]

    tier_emoji = {"S": "🏆", "A": "⭐", "B": "🔵", "C": "⚪"}.get(template["tier"], "❓")
    style_emoji = "🛡️" if template["style"] == "streaker" else "⚔️"

    lines = [
        f"{style_emoji} {tier_emoji} **{template['name']}** (Tier {template['tier']})",
        f"_{template['description']}_",
        f"Min Level: {template['level_min']}+",
        "",
    ]

    for slot in slots:
        animal   = slot["animal"]
        wdata    = slot["weapon_data"]
        position = slot["position"]
        role     = slot["role"]

        if animal:
            aname   = animal.get("display_name", "?").title()
            alevel  = animal.get("level", 1)
            arank   = animal.get("rank", "?").title()
            comp    = animal.get("computed", {})
            astr    = comp.get("str", "?")
            amag    = comp.get("mag", "?")
            ahp     = comp.get("hp", "?")
            animal_str = f"**{aname}** ({arank} Lv.{alevel}) STR:{astr} MAG:{amag} HP:{ahp}"
        else:
            animal_str = f"⚠️ No animal — need: {', '.join(slot['ideal_animals'][:2])}"

        if wdata:
            wname      = wdata.get("name", "?")
            wdesc      = wdata.get("desc", "")
            weapon_str = f"**{wname}** — {wdesc}"
        else:
            weapon_str = f"⚠️ No weapon — need: {', '.join(slot['ideal_weapons'][:2])}"

        lines.append(f"**Slot {position} [{role}]**")
        lines.append(f"  🐾 {animal_str}")
        lines.append(f"  🗡️ {weapon_str}")
        lines.append(f"  💡 {slot['notes']}")
        lines.append(f"  🎲 Ideal passive: {', '.join(slot['passive'][:2])}")
        lines.append("")

    lines.append(f"**📋 Strategy:** {template['strategy']}")

    if result["missing_key_weapons"]:
        lines.append(f"\n**⚠️ Missing key weapons:** {', '.join(result['missing_key_weapons'])}")
        lines.append("Get these to unlock this team!")

    lines.append(f"\n**Counters:** {', '.join(template['counters'][:2])}")
    lines.append(f"**Weak to:** {', '.join(template['countered_by'][:2])}")

    return "\n".join(lines)
