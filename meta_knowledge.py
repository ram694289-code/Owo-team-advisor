PASSIVES = {
    "energize":       "Regenerates WP each turn — BEST for mana sustain, critical for healers/scepter",
    "mana_tap":       "Steals WP from enemy on hit — great for attackers",
    "sacrifice":      "Deals self-damage for massive damage — used in high-level teams",
    "kamikaze":       "Deals huge damage at cost of HP — endgame offensive passive",
    "strength":       "Boosts STR-based damage",
    "critical":       "Chance to deal critical hits",
    "regeneration":   "Regenerates HP each turn — good for tanks",
    "hgen":           "HP regeneration variant",
    "wgen":           "WP generation — important for CRune teams",
    "sprout":         "Shield that blocks damage — core of Stall teams",
    "physical_res":   "Reduces incoming physical damage",
}

METAS = {
    "rstaff_stall": {
        "name": "RStaff Stall (Best Streaker)",
        "tier": "S",
        "desc": "The best performing RStaff team. Revives dead allies and stalls indefinitely.",
        "style": "streaker",
        "level_range": "Any, best at 40+",
        "slots": [
            {
                "role": "Reviver",
                "weapon": "RStaff (Resurrection Staff)",
                "ideal_animals": ["LobBot", "Gorilla", "high HP + some PR/MR + some WP"],
                "passive": "Kamikaze or Sacrifice",
                "notes": "High HP animal that can survive while reviving. Gorilla is a great free-to-play option."
            },
            {
                "role": "Attacker",
                "weapon": "Any strong STR weapon (Bow, Scythe, Axe)",
                "ideal_animals": ["Spider", "Snake", "Eagle", "high STR fabled"],
                "passive": "Strength or Critical",
                "notes": "Spider (gspider) is top pick — massive STR base."
            },
            {
                "role": "Support/Tank",
                "weapon": "Shield (Defender's Aegis) or Banner",
                "ideal_animals": ["DinoBot", "LobBot", "high HP + PR"],
                "passive": "Energize or Regeneration",
                "notes": "Soaks damage and buys time for reviver to work."
            }
        ],
        "counters": ["Pstaff Stall at high level", "Discharge SStaff teams"],
        "countered_by": ["Triple Sac Hybrid", "Scythe Blitz at small level differences"],
    },
    "spider_crune": {
        "name": "Spider CRune (Spoon) — Best at 60+",
        "tier": "S",
        "desc": "Spider + CRune heals the lowest HP animal repeatedly. Very powerful at high level.",
        "style": "streaker",
        "level_range": "60+",
        "slots": [
            {
                "role": "CRune Holder",
                "weapon": "CRune (Rune of Celebration)",
                "ideal_animals": ["capybara", "high WP animal"],
                "passive": "Energize (REQUIRED) + WGen",
                "notes": "WP Cost close to 100, heal close to 50%, replenish close to 40%. Energize is mandatory."
            },
            {
                "role": "Attacker",
                "weapon": "Bow (close to 160% STR) or Rune of Forgotten",
                "ideal_animals": ["Spider (gspider)", "high STR fabled"],
                "passive": "Strength or Critical",
                "notes": "Spider is the ONLY option for true Spider Crune. WP Cost ~120, max ~135."
            },
            {
                "role": "Tank/Support",
                "weapon": "Shield or SStaff",
                "ideal_animals": ["LobBot", "high HP + PR"],
                "passive": "Energize",
                "notes": "Keeps team alive while CRune heals."
            }
        ],
        "counters": ["Most lower-level teams"],
        "countered_by": ["Scythe Blitz", "Double Scythe teams"],
    },
    "pstaff_stall": {
        "name": "PStaff Stall — Best at 50+",
        "tier": "S",
        "desc": "Uses Staff of Purity (PStaff). One of the best streaking teams, especially at very high level.",
        "style": "streaker",
        "level_range": "50+",
        "slots": [
            {
                "role": "PStaff Healer",
                "weapon": "PStaff (Staff of Purity)",
                "ideal_animals": ["high HP + high MAG + some PR"],
                "passive": "Energize",
                "notes": "High MAG + HP animal."
            },
            {
                "role": "Attacker",
                "weapon": "SStaff (Spirit Staff) with HIGH WP cost 200-250",
                "ideal_animals": ["Spider", "Fish (gfish)", "high MAG/STR fabled"],
                "passive": "Mana Tap or Energize",
                "notes": "SStaff with high WP cost maximizes Discharge damage."
            },
            {
                "role": "Tank",
                "weapon": "Shield with Sprout passive",
                "ideal_animals": ["Eagle (geagle)", "high HP + high PR"],
                "passive": "Sprout (REQUIRED for true stall)",
                "notes": "Sprout shield is core of stall. Eagle has great HP+PR for this."
            }
        ],
        "counters": ["Rstaff stall at extreme levels", "Most teams at 50+"],
        "countered_by": ["Rare compositions at same level"],
    },
    "double_aoe": {
        "name": "Double AoE Team — Beginner/Streak Breaker",
        "tier": "B",
        "desc": "Two AoE attackers + healer. Easy to build, decent at low level, streak breaker at high level.",
        "style": "breaker",
        "level_range": "Low-mid, <40",
        "slots": [
            {
                "role": "MAG AoE Attacker",
                "weapon": "EStaff (Energy Staff)",
                "ideal_animals": ["Fish (gfish)", "Penguin", "high MAG animal"],
                "passive": "Energize or Mana Tap",
                "notes": "Fish is top pick for MAG AoE — MAG:19 base is insane."
            },
            {
                "role": "STR AoE Attacker",
                "weapon": "Sword",
                "ideal_animals": ["Spider (gspider)", "Snake", "Wolf", "high STR animal"],
                "passive": "Strength or Critical",
                "notes": "Spider for STR AoE. Sword hits all enemies."
            },
            {
                "role": "Healer",
                "weapon": "HStaff or SStaff",
                "ideal_animals": ["Owl (gowl)", "Lion (glion)", "decent MAG animal"],
                "passive": "Energize",
                "notes": "Keeps the team alive while AoE attackers work."
            }
        ],
        "counters": ["Low-level teams", "Teams without single-target defense"],
        "countered_by": ["Single-target weapons at higher level", "Meta stall teams"],
    },
    "scythe_blitz": {
        "name": "Scythe Blitz — Counter/Breaker",
        "tier": "A",
        "desc": "Uses Mortality debuff to reduce healing + high DPS to kill enemy tank.",
        "style": "breaker",
        "level_range": "Mid-high",
        "slots": [
            {
                "role": "Scythe Attacker",
                "weapon": "Scythe (Culling Scythe)",
                "ideal_animals": ["Snake", "Eagle", "high STR fabled"],
                "passive": "Strength or Critical",
                "notes": "Mortality cuts enemy healing. High STR is key."
            },
            {
                "role": "FStaff/Dagger",
                "weapon": "FStaff (Flame Staff) or Dagger",
                "ideal_animals": ["Lizard", "high MAG animal"],
                "passive": "Mana Tap",
                "notes": "Best FStaff holder is Lizard (high MR). Flame does consistent pressure."
            },
            {
                "role": "Healer/Tank",
                "weapon": "SStaff or Shield",
                "ideal_animals": ["Healer with good MAG", "Eagle for Shield"],
                "passive": "Energize",
                "notes": "Keeps team alive while Scythe and Flame do damage."
            }
        ],
        "counters": ["RStaff Stall", "PStaff Stall", "Spider CRune"],
        "countered_by": ["Teams at much higher level"],
    },
}

ANIMAL_META_ROLES = {
    "gspider": {
        "best_for": ["Spider CRune attacker", "RStaff Stall attacker", "Double AoE STR"],
        "reason": "Highest STR of all accessible fabled pets (STR base:9). Top tier attacker.",
        "ideal_weapons": ["Bow", "Scythe", "Sword"],
        "ideal_passives": ["Strength", "Critical", "Mana Tap"],
    },
    "gfish": {
        "best_for": ["Double AoE MAG attacker", "PStaff Stall attacker"],
        "reason": "MAG base:19 — literally the highest MAG in the game. Pure magic powerhouse.",
        "ideal_weapons": ["EStaff", "FStaff", "Wand"],
        "ideal_passives": ["Energize", "Mana Tap"],
    },
    "lion": {
        "best_for": ["Healer slot", "Support slot"],
        "reason": "High HP + decent PR. Good survivability for a healer or buffer role.",
        "ideal_weapons": ["HStaff", "SStaff", "Shield"],
        "ideal_passives": ["Energize", "Regeneration"],
    },
    "owl": {
        "best_for": ["WP support", "Scepter holder"],
        "reason": "WP base:10 — highest WP of any legendary. Great for WP replenishment weapons.",
        "ideal_weapons": ["Scepter", "SStaff", "CRune"],
        "ideal_passives": ["Energize", "WGen"],
    },
    "fox": {
        "best_for": ["STR attacker"],
        "reason": "STR base:9 — highest STR of legendary rank. Strong physical attacker.",
        "ideal_weapons": ["Bow", "Scythe", "Axe", "Sword"],
        "ideal_passives": ["Strength", "Critical"],
    },
    "wolf": {
        "best_for": ["Top tier STR attacker"],
        "reason": "STR base:17 — insane physical damage. One of the best attackers in the game.",
        "ideal_weapons": ["Bow", "Scythe", "Axe"],
        "ideal_passives": ["Strength", "Critical", "Kamikaze"],
    },
    "snake": {
        "best_for": ["Scythe Blitz attacker", "RStaff Stall attacker"],
        "reason": "STR:13 + MAG:10 — excellent hybrid attacker.",
        "ideal_weapons": ["Scythe", "Bow", "FStaff"],
        "ideal_passives": ["Strength", "Critical"],
    },
    "eagle": {
        "best_for": ["Stall tank", "Shield holder"],
        "reason": "High HP + good PR. Best free-to-play stall tank.",
        "ideal_weapons": ["Shield", "SStaff"],
        "ideal_passives": ["Sprout", "Energize", "Regeneration"],
    },
    "gorilla": {
        "best_for": ["RStaff Stall tank/support"],
        "reason": "HP:7 + MAG:7 — great hybrid tank. Good for RStaff team.",
        "ideal_weapons": ["RStaff", "Shield"],
        "ideal_passives": ["Kamikaze", "Sacrifice", "Energize"],
    },
    "cow": {
        "best_for": ["Early/mid healer"],
        "reason": "Balanced stats, decent HP. Good starter healer.",
        "ideal_weapons": ["HStaff", "SStaff"],
        "ideal_passives": ["Energize"],
    },
}


def get_animal_meta_role(animal_name: str) -> dict:
    name = animal_name.lower().strip()
    if name in ANIMAL_META_ROLES:
        return ANIMAL_META_ROLES[name]
    aliases = {
        "glion": "lion", "gowl": "owl", "gspider": "gspider",
        "gfox": "fox", "gwolf": "wolf", "geagle": "eagle",
        "gsnake": "snake", "ggorilla": "gorilla",
    }
    mapped = aliases.get(name)
    if mapped and mapped in ANIMAL_META_ROLES:
        return ANIMAL_META_ROLES[mapped]
    return {}


def suggest_meta_team(animals: list, weapons: list, team_type: str) -> str:
    owned_weapon_names = {w["name"].lower() for w in weapons}
    owned_animal_names = {a["display_name"].lower() for a in animals}

    lines = []

    if team_type == "streaker":
        lines.append("🏆 **Best Streaker Team Options (Wiki Meta)**\n")

        has_rstaff  = "rstaff" in owned_weapon_names
        has_pstaff  = "pstaff" in owned_weapon_names
        has_crune   = "crune" in owned_weapon_names
        has_spider  = "gspider" in owned_animal_names
        has_fish    = "gfish" in owned_animal_names
        has_eagle   = any(n in owned_animal_names for n in ["eagle","geagle"])
        has_shield  = "shield" in owned_weapon_names
        has_sstaff  = "sstaff" in owned_weapon_names

        if has_rstaff:
            lines.append("✅ **You have RStaff!** → Build RStaff Stall (S Tier)")
            meta = METAS["rstaff_stall"]
            for i, slot in enumerate(meta["slots"]):
                lines.append(f"  Slot {i+1} [{slot['role']}]: {slot['weapon']}")
                lines.append(f"    Best animal: {', '.join(slot['ideal_animals'][:2])}")
                lines.append(f"    Passive: {slot['passive']}")
            lines.append(f"  _{meta['desc']}_\n")

        if has_crune and has_spider:
            lines.append("✅ **You have CRune + Spider!** → Spider CRune (S Tier at 60+)")
            meta = METAS["spider_crune"]
            for i, slot in enumerate(meta["slots"]):
                lines.append(f"  Slot {i+1} [{slot['role']}]: {slot['weapon']}")
            lines.append("")

        if has_pstaff:
            lines.append("✅ **You have PStaff!** → PStaff Stall (S Tier at 50+)")

        if not has_rstaff and not has_crune and not has_pstaff:
            lines.append("⚠️ You don't have RStaff, PStaff or CRune yet.")
            lines.append("→ **Best option with your weapons:** Double AoE or HStaff team")
            lines.append("→ **Priority weapon to get:** RStaff (Resurrection Staff)\n")

            if has_sstaff or "hstaff" in owned_weapon_names:
                lines.append("✅ You have a healing staff → run a basic Healer + 2 Attackers team:")
                if has_spider:
                    lines.append("  Slot 1 [Attacker]: gspider + Bow/Scythe/Sword")
                if has_fish:
                    lines.append("  Slot 2 [Attacker]: gfish + EStaff")
                lines.append("  Slot 3 [Healer]: Best MAG animal + HStaff/SStaff with Energize")

    else:
        lines.append("⚔️ **Best Breaker Team Options (Wiki Meta)**\n")
        lines.append("**Recommended: Double AoE or Scythe Blitz**\n")

        has_scythe = "scythe" in owned_weapon_names
        has_estaff = "estaff" in owned_weapon_names
        has_fstaff = "fstaff" in owned_weapon_names
        has_sword  = "sword"  in owned_weapon_names

        if has_scythe:
            lines.append("✅ **You have Scythe!** → Scythe Blitz (A Tier breaker)")
            meta = METAS["scythe_blitz"]
            for i, slot in enumerate(meta["slots"]):
                lines.append(f"  Slot {i+1} [{slot['role']}]: {slot['weapon']}")
                lines.append(f"    Passive: {slot['passive']}")
            lines.append("")

        if has_estaff or has_sword:
            lines.append("✅ **Double AoE** — easiest breaker to build")
            meta = METAS["double_aoe"]
            for i, slot in enumerate(meta["slots"]):
                lines.append(f"  Slot {i+1} [{slot['role']}]: {slot['weapon']}")
            lines.append("")

    lines.append("\n📋 **Your Animals & Their Meta Roles:**")
    for a in animals:
        name = a.get("display_name","?")
        role_info = get_animal_meta_role(name)
        if role_info:
            best = ", ".join(role_info["best_for"][:2])
            ideal_w = ", ".join(role_info["ideal_weapons"][:3])
            lines.append(f"• **{name.title()}** → {best}")
            lines.append(f"  Best weapons: {ideal_w}")
        else:
            rank = a.get("rank","?")
            lines.append(f"• **{name.title()}** ({rank}) — no specific meta role data")

    return "\n".join(lines)
