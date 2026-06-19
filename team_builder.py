from database import WEAPONS, TEAM_TYPES, RANK_POWER


def score_animal(animal: dict, team_type: str) -> float:
    score = 0.0
    computed = animal.get("computed", {})
    level    = animal.get("level", 1)
    rank     = animal.get("rank", "common")
    base     = animal.get("base_stats", {})

    config = TEAM_TYPES[team_type]
    priority = config["stat_priority"]

    weights = {}
    for i, stat in enumerate(priority):
        weights[stat] = len(priority) - i

    if computed:
        score += computed.get("hp",  0) * weights.get("hp",  0) * 0.01
        score += computed.get("str", 0) * weights.get("str", 0) * 0.05
        score += computed.get("mag", 0) * weights.get("mag", 0) * 0.05
        score += computed.get("wp",  0) * weights.get("wp",  0) * 0.01
        score += computed.get("pr",  0) * weights.get("pr",  0) * 0.5
        score += computed.get("mr",  0) * weights.get("mr",  0) * 0.5
        score += computed.get("ehp_phys", 0) * 0.002
        score += computed.get("ehp_mag",  0) * 0.002
    elif base:
        score += base.get("hp",  0) * weights.get("hp",  0) * 2
        score += base.get("str", 0) * weights.get("str", 0) * 3
        score += base.get("mag", 0) * weights.get("mag", 0) * 3
        score += base.get("wp",  0) * weights.get("wp",  0) * 2
        score += base.get("pr",  0) * weights.get("pr",  0) * 2
        score += base.get("mr",  0) * weights.get("mr",  0) * 2

    score += RANK_POWER.get(rank, 0) * 10
    score += level * 2

    return round(score, 2)


def score_weapon(weapon: dict, team_type: str) -> float:
    wdata = weapon.get("weapon_data", {})
    if not wdata:
        return 0.0

    role   = wdata.get("role", "")
    effect = wdata.get("effect", "")

    streaker_scores = {
        "reviver":   100, "healer":  90, "support": 80,
        "buffer":     70, "tank":    60, "hybrid":  40,
        "attacker":   20, "breaker": 10, "passive": 30, "controller": 10,
    }
    breaker_scores = {
        "attacker":   90, "breaker": 100, "controller": 95,
        "hybrid":     70, "support":  30, "buffer":     20,
        "healer":     20, "reviver":  10, "tank":       15, "passive": 40,
    }

    scores = streaker_scores if team_type == "streaker" else breaker_scores
    score = scores.get(role, 0)

    if team_type == "breaker":
        disrupt = ["Freeze","Poison","Stinky","Mortality","Leech","MindControl","DebuffSteal","BuffReduce"]
        if effect in disrupt:
            score += 20

    return score


def check_weapon_fit(animal: dict, weapon_data: dict) -> tuple[str, str]:
    if not weapon_data:
        return "poor", "⚠️ No weapon assigned!"

    stat_type = weapon_data.get("stat")
    computed  = animal.get("computed", {})
    base      = animal.get("base_stats", {})
    name      = animal.get("display_name", "?").title()
    wname     = weapon_data.get("name", "?")

    if stat_type == "STR":
        base_str = base.get("str", 0)
        if base_str >= 7:
            return "great", f"✅ {name} has high STR ({base_str} base) — {wname} will hit very hard!"
        elif base_str >= 4:
            return "ok",    f"➡️ {name} has decent STR ({base_str} base) — {wname} works fine."
        else:
            return "poor",  f"⚠️ {name} has low STR ({base_str} base) — consider a MAG weapon instead of {wname}."
    elif stat_type == "MAG":
        base_mag = base.get("mag", 0)
        if base_mag >= 7:
            return "great", f"✅ {name} has high MAG ({base_mag} base) — {wname} will be very powerful!"
        elif base_mag >= 4:
            return "ok",    f"➡️ {name} has decent MAG ({base_mag} base) — {wname} works fine."
        else:
            return "poor",  f"⚠️ {name} has low MAG ({base_mag} base) — consider a STR weapon instead of {wname}."
    elif stat_type == "BOTH":
        return "ok", f"➡️ {wname} uses both STR & MAG — {name} can use it."
    else:
        return "ok", f"➡️ {wname} doesn't rely on STR/MAG stats — works on any animal."


def build_team(animals: list[dict], weapons: list[dict], team_type: str) -> dict:
    if team_type not in TEAM_TYPES:
        return {"error": f"Unknown team type '{team_type}'."}

    scored_animals = sorted(
        [(a, score_animal(a, team_type)) for a in animals],
        key=lambda x: x[1], reverse=True
    )

    top_3 = scored_animals[:3]

    scored_weapons = sorted(
        [(w, score_weapon(w, team_type)) for w in weapons],
        key=lambda x: x[1], reverse=True
    )
    top_weapons = scored_weapons[:3]

    slots = []
    for i, (animal, a_score) in enumerate(top_3):
        if i < len(top_weapons):
            weapon, wdata, w_score = top_weapons[i][0], top_weapons[i][0].get("weapon_data", {}), top_weapons[i][1]
        else:
            weapon, wdata, w_score = None, {}, 0

        fit, tip = check_weapon_fit(animal, wdata)

        slots.append({
            "slot": i + 1,
            "animal": animal,
            "animal_score": a_score,
            "weapon": weapon,
            "weapon_data": wdata,
            "fit": fit,
            "tip": tip,
        })

    owned_ids = {w.get("weapon_id") for w in weapons}
    missing = [WEAPONS[wid]["name"] for wid in TEAM_TYPES[team_type]["key_weapons"]
               if wid in WEAPONS and wid not in owned_ids]

    return {
        "team_type": team_type,
        "slots": slots,
        "strategy": TEAM_TYPES[team_type]["notes"],
        "missing_weapons": missing,
        "total_animals_checked": len(animals),
    }


def format_team(team: dict) -> str:
    if "error" in team:
        return f"❌ {team['error']}"

    tt = team["team_type"]
    emoji = "🛡️" if tt == "streaker" else "⚔️"
    title = "STREAKER" if tt == "streaker" else "BREAKER"

    lines = [
        f"{emoji} **Best {title} Team** (checked {team['total_animals_checked']} animals)",
        ""
    ]

    for slot in team["slots"]:
        animal  = slot["animal"]
        wdata   = slot["weapon_data"]
        computed = animal.get("computed", {})
        base    = animal.get("base_stats", {})

        name   = animal.get("display_name", "?").title()
        rank   = animal.get("rank", "?").title()
        level  = animal.get("level", 1)
        wname  = wdata.get("name", "No Weapon") if wdata else "No Weapon"
        wdesc  = wdata.get("desc", "") if wdata else ""

        lines.append(f"**Slot {slot['slot']}: {name}** | {rank} | Lv.{level}")

        if computed:
            lines.append(
                f"  HP:{computed.get('hp','?')} "
                f"STR:{computed.get('str','?')} "
                f"MAG:{computed.get('mag','?')} "
                f"WP:{computed.get('wp','?')}"
            )
            pr = computed.get('pr','?')
            mr = computed.get('mr','?')
            ehpp = computed.get('ehp_phys','?')
            ehpm = computed.get('ehp_mag','?')
            lines.append(f"  PR:{pr}% MR:{mr}% | eHP(P):{ehpp} eHP(M):{ehpm}")
        elif base:
            lines.append(f"  Base: HP:{base.get('hp')} STR:{base.get('str')} MAG:{base.get('mag')} WP:{base.get('wp')}")

        lines.append(f"  🗡️ **{wname}** — {wdesc}")
        lines.append(f"  {slot['tip']}")
        lines.append("")

    lines.append(f"**Strategy:** {team['strategy']}")

    if team["missing_weapons"]:
        lines.append(f"\n**⬆️ Get these to improve:** {', '.join(team['missing_weapons'])}")

    return "\n".join(lines)
