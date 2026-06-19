import re

PASSIVE_THRESHOLDS = {
    "sprout":       {"good": 35.0,  "great": 40.0,  "unit": "%",  "desc": "Increases incoming healing"},
    "energize":     {"good": 30.0,  "great": 40.0,  "unit": "WP", "desc": "Regenerates WP per turn"},
    "strength":     {"good": 25.0,  "great": 35.0,  "unit": "%",  "desc": "Boosts STR damage"},
    "critical":     {"good": 20.0,  "great": 30.0,  "unit": "%",  "desc": "Chance to crit"},
    "regeneration": {"good": 5.0,   "great": 8.0,   "unit": "%",  "desc": "HP regen per turn"},
    "mana_tap":     {"good": 15.0,  "great": 25.0,  "unit": "%",  "desc": "Steals WP on hit"},
    "sacrifice":    {"good": 20.0,  "great": 30.0,  "unit": "%",  "desc": "Self damage for big hit"},
    "kamikaze":     {"good": 30.0,  "great": 45.0,  "unit": "%",  "desc": "Huge damage at HP cost"},
    "physical_res": {"good": 10.0,  "great": 15.0,  "unit": "%",  "desc": "Reduces phys damage taken"},
    "wgen":         {"good": 20.0,  "great": 30.0,  "unit": "WP", "desc": "Extra WP generation"},
}

WEAPON_IDEAL = {
    "Spirit Staff": {
        "heal_pct":      {"want": "high", "range": (30, 50),   "good_pct": 0.85},
        "defense_up":    {"want": "high", "range": (20, 35),   "good_pct": 0.80},
        "wp_cost":       {"want": "low",  "range": (150, 250), "good_pct": 0.85},
        "good_passives": ["sprout", "energize", "regeneration"],
        "bad_passives":  ["kamikaze", "sacrifice", "strength"],
        "notes": "Sprout passive is BEST for stall teams. Want heal% close to 50% and low WP cost."
    },
    "SStaff": {
        "heal_pct":      {"want": "high", "range": (30, 50),   "good_pct": 0.85},
        "defense_up":    {"want": "high", "range": (20, 35),   "good_pct": 0.80},
        "wp_cost":       {"want": "low",  "range": (150, 250), "good_pct": 0.85},
        "good_passives": ["sprout", "energize", "regeneration"],
        "bad_passives":  ["kamikaze", "sacrifice"],
        "notes": "Same as Spirit Staff. Sprout is king for stall. For Discharge meta: want HIGH WP cost."
    },
    "RStaff": {
        "heal_pct":      {"want": "high", "range": (60, 90),   "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (300, 400), "good_pct": 0.85},
        "good_passives": ["energize", "kamikaze", "sacrifice"],
        "bad_passives":  ["sprout", "regeneration"],
        "notes": "Want heal% close to 90% and WP cost close to 300. Energize is best passive."
    },
    "Resurrection Staff": {
        "heal_pct":      {"want": "high", "range": (60, 90),   "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (300, 400), "good_pct": 0.85},
        "good_passives": ["energize", "kamikaze", "sacrifice"],
        "bad_passives":  ["sprout", "regeneration"],
        "notes": "Want heal% close to 90% and WP cost close to 300. Energize is best passive."
    },
    "Bow": {
        "dmg_pct":       {"want": "high", "range": (110, 160), "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (120, 220), "good_pct": 0.85},
        "good_passives": ["strength", "critical", "mana_tap", "kamikaze"],
        "bad_passives":  ["sprout", "regeneration", "energize"],
        "notes": "Want damage% close to 160% and WP cost close to 120."
    },
    "Healing Staff": {
        "heal_pct":      {"want": "high", "range": (110, 160), "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (150, 225), "good_pct": 0.85},
        "good_passives": ["energize", "sprout", "regeneration"],
        "bad_passives":  ["kamikaze", "sacrifice", "strength"],
        "notes": "Want heal% close to 160% and WP cost close to 150."
    },
    "HStaff": {
        "heal_pct":      {"want": "high", "range": (110, 160), "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (150, 225), "good_pct": 0.85},
        "good_passives": ["energize", "sprout", "regeneration"],
        "bad_passives":  ["kamikaze", "sacrifice"],
        "notes": "Want heal% close to 160% and WP cost close to 150."
    },
    "Energy Staff": {
        "dmg_pct":       {"want": "high", "range": (35, 65),   "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (100, 200), "good_pct": 0.85},
        "good_passives": ["energize", "mana_tap", "strength"],
        "bad_passives":  ["sprout", "regeneration"],
        "notes": "Want damage% close to 65% and WP cost close to 100."
    },
    "EStaff": {
        "dmg_pct":       {"want": "high", "range": (35, 65),   "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (100, 200), "good_pct": 0.85},
        "good_passives": ["energize", "mana_tap", "strength"],
        "bad_passives":  ["sprout"],
        "notes": "Want damage% close to 65% and WP cost close to 100."
    },
    "Sword": {
        "dmg_pct":       {"want": "high", "range": (35, 55),   "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (100, 200), "good_pct": 0.85},
        "good_passives": ["strength", "critical", "mana_tap"],
        "bad_passives":  ["sprout", "regeneration"],
        "notes": "Want damage% close to 55% and WP cost close to 100."
    },
    "Scythe": {
        "dmg_pct":       {"want": "high", "range": (70, 100),  "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (100, 200), "good_pct": 0.85},
        "good_passives": ["strength", "critical", "kamikaze"],
        "bad_passives":  ["sprout", "regeneration"],
        "notes": "Want damage% close to 100% and WP cost close to 100."
    },
    "Shield": {
        "wp_cost":       {"want": "low",  "range": (150, 250), "good_pct": 0.85},
        "good_passives": ["sprout", "energize", "regeneration", "physical_res"],
        "bad_passives":  ["kamikaze", "sacrifice", "strength"],
        "notes": "Sprout passive is REQUIRED for stall teams!"
    },
    "Axe": {
        "dmg_pct":       {"want": "high", "range": (40, 60),   "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (160, 260), "good_pct": 0.85},
        "good_passives": ["strength", "critical", "mana_tap"],
        "bad_passives":  ["sprout", "regeneration"],
        "notes": "Want damage% close to 60% and WP cost close to 160."
    },
    "Dagger": {
        "dmg_pct":       {"want": "high", "range": (70, 100),  "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (100, 200), "good_pct": 0.85},
        "good_passives": ["mana_tap", "strength", "critical"],
        "bad_passives":  ["sprout", "regeneration"],
        "notes": "Want damage% close to 100% and WP cost close to 100."
    },
    "Flame Staff": {
        "dmg_pct":       {"want": "high", "range": (75, 95),   "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (100, 200), "good_pct": 0.85},
        "good_passives": ["mana_tap", "energize", "critical"],
        "bad_passives":  ["sprout", "regeneration"],
        "notes": "Want damage% close to 95%. Lizard is best holder."
    },
    "FStaff": {
        "dmg_pct":       {"want": "high", "range": (75, 95),   "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (100, 200), "good_pct": 0.85},
        "good_passives": ["mana_tap", "energize", "critical"],
        "bad_passives":  ["sprout"],
        "notes": "Want damage% close to 95%."
    },
    "Scepter": {
        "replenish_pct": {"want": "high", "range": (65, 95),   "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (125, 200), "good_pct": 0.85},
        "good_passives": ["energize", "mana_tap"],
        "bad_passives":  ["kamikaze", "sacrifice"],
        "notes": "Want replenish% close to 95% and WP cost close to 125."
    },
    "Purify Staff": {
        "heal_pct":      {"want": "high", "range": (50, 100),  "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (150, 250), "good_pct": 0.85},
        "good_passives": ["energize", "sprout"],
        "bad_passives":  ["kamikaze", "sacrifice"],
        "notes": "Want heal% close to 100%. Energize passive is important."
    },
    "PStaff": {
        "heal_pct":      {"want": "high", "range": (50, 100),  "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (150, 250), "good_pct": 0.85},
        "good_passives": ["energize", "sprout"],
        "bad_passives":  ["kamikaze", "sacrifice"],
        "notes": "Want heal% close to 100%. Energize passive is important."
    },
    "Banner": {
        "wp_cost":       {"want": "low",  "range": (235, 290), "good_pct": 0.85},
        "good_passives": ["energize", "strength"],
        "bad_passives":  ["sprout", "kamikaze"],
        "notes": "Want WP cost close to 235."
    },
    "Rune of Celebration": {
        "heal_pct":      {"want": "high", "range": (45, 50),   "good_pct": 0.85},
        "replenish_pct": {"want": "high", "range": (35, 40),   "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (100, 200), "good_pct": 0.85},
        "good_passives": ["energize", "wgen"],
        "bad_passives":  ["kamikaze", "sacrifice", "strength"],
        "notes": "Energize is REQUIRED. Want heal% close to 50%, replenish% close to 40%."
    },
    "CRune": {
        "heal_pct":      {"want": "high", "range": (45, 50),   "good_pct": 0.85},
        "replenish_pct": {"want": "high", "range": (35, 40),   "good_pct": 0.85},
        "wp_cost":       {"want": "low",  "range": (100, 200), "good_pct": 0.85},
        "good_passives": ["energize", "wgen"],
        "bad_passives":  ["kamikaze", "sacrifice"],
        "notes": "Energize is REQUIRED. Want heal% close to 50%, replenish% close to 40%."
    },
}


def parse_weapon_inspect(content: str) -> dict:
    weapon = {}

    if "[NEW]" in content:
        weapon["is_new"] = True
    elif "[CURRENT]" in content:
        weapon["is_current"] = True

    name_match = re.search(r'Name:\s*(.+)', content)
    if name_match:
        weapon["name"] = name_match.group(1).strip()
    else:
        title_match = re.search(
            r"(?:(?:\w+'s|\[NEW\]|\[CURRENT\])\s+)([\w\s]+Staff|[\w\s]+Bow|[\w\s]+Axe|[\w\s]+Shield|[\w\s]+Sword|[\w\s]+Scythe|[\w\s]+Dagger|[\w\s]+Scepter|[\w\s]+Banner|[\w\s]+Rune|[\w\s]+Orb|[\w\s]+Wand|[\w\s]+Claw|[\w\s]+Gaze)",
            content
        )
        if title_match:
            weapon["name"] = title_match.group(1).strip()

    id_match = re.search(r'ID:\s*([A-Z0-9]+)', content)
    if id_match:
        weapon["id"] = id_match.group(1).strip()

    quality_match = re.search(r'Quality:.*?([\d]+\.[\d]+)%', content)
    if quality_match:
        weapon["quality"] = float(quality_match.group(1))

    wear_match = re.search(r'Wear:\s*(PRISTINE|FINE|DECENT|WORN|UNKNOWN)', content, re.IGNORECASE)
    if wear_match:
        weapon["wear"] = wear_match.group(1).upper()

    cost_match = re.search(r'Weapon Cost:\s*(\d+)', content, re.IGNORECASE)
    if cost_match:
        weapon["wp_cost"] = int(cost_match.group(1))

    heal_match = re.search(r'[Hh]eal(?:\s+all\s+allies)?\s+for\s+([\d.]+)%', content)
    if heal_match:
        weapon["heal_pct"] = float(heal_match.group(1))

    dmg_match = re.search(r'[Dd]eals?\s+([\d.]+)%\s+of\s+your\s+(STR|MAG)', content)
    if dmg_match:
        weapon["dmg_pct"]  = float(dmg_match.group(1))
        weapon["dmg_type"] = dmg_match.group(2)

    replenish_match = re.search(r'[Rr]eplenish\w*\s+([\d.]+)%', content)
    if replenish_match:
        weapon["replenish_pct"] = float(replenish_match.group(1))

    defup_match = re.search(r'Defense Up.*?([\d.]+)%', content)
    if defup_match:
        weapon["defense_up"] = float(defup_match.group(1))

    passive_match = re.search(
        r'(Sprout|Energize|Strength|Critical|Regeneration|Mana Tap|Sacrifice|Kamikaze|Physical Res|WGen)\s*[-–]\s*[^+\n]*\+([\d.]+)%?',
        content, re.IGNORECASE
    )
    if passive_match:
        weapon["passive_name"]  = passive_match.group(1).strip().lower().replace(" ", "_")
        weapon["passive_value"] = float(passive_match.group(2))

    reroll_match = re.search(r'Reroll Changes:\s*(\d+)\s*\|\s*Reroll Attempts:\s*(\d+)', content)
    if reroll_match:
        weapon["reroll_changes"]  = int(reroll_match.group(1))
        weapon["reroll_attempts"] = int(reroll_match.group(2))

    sell_match = re.search(r'Sell Value:.*?(\d[\d,]*)\s*(?:cowoncy|💰).*?(\d[\d,]*)\s*(?:shards|✏️)', content, re.IGNORECASE)
    if sell_match:
        weapon["sell_cowoncy"] = int(sell_match.group(1).replace(",",""))
        weapon["sell_shards"]  = int(sell_match.group(2).replace(",",""))

    return weapon


def evaluate_weapon(weapon: dict) -> dict:
    name = weapon.get("name", "")
    ideal = WEAPON_IDEAL.get(name)

    if not ideal:
        for key in WEAPON_IDEAL:
            if key.lower() in name.lower() or name.lower() in key.lower():
                ideal = WEAPON_IDEAL[key]
                break

    if not ideal:
        return {
            "verdict": "UNKNOWN",
            "action": f"⚠️ No ideal data for **{name}**. Can't fully evaluate yet.",
            "stat_notes": [],
            "passive_note": "Unknown weapon type.",
            "reroll_stat": False,
            "reroll_passive": False,
            "notes": "",
            "good_passives": [],
            "avg_score": 0,
        }

    good_passives = ideal.get("good_passives", [])
    bad_passives  = ideal.get("bad_passives", [])

    stat_notes  = []
    stat_scores = []

    def eval_stat(label, value, cfg):
        lo, hi = cfg["range"]
        want    = cfg["want"]
        good_pct = cfg.get("good_pct", 0.85)
        if want == "high":
            ratio = (value - lo) / (hi - lo) if hi != lo else 1.0
        else:
            ratio = 1.0 - (value - lo) / (hi - lo) if hi != lo else 1.0
        ratio = max(0.0, min(1.0, ratio))

        if ratio >= good_pct:
            return ratio, f"✅ {label}: **{value}** — great!"
        elif ratio >= 0.60:
            target = hi if want == "high" else lo
            return ratio, f"➡️ {label}: **{value}** — okay (want closer to {target})"
        else:
            target = hi if want == "high" else lo
            return ratio, f"❌ {label}: **{value}** — low (want closer to {target})"

    for stat_key, cfg in ideal.items():
        if stat_key in ("good_passives", "bad_passives", "notes"):
            continue
        val = weapon.get(stat_key)
        if val is not None:
            score, note = eval_stat(stat_key.replace("_", " ").title(), val, cfg)
            stat_scores.append(score)
            stat_notes.append(note)

    avg_score   = sum(stat_scores) / len(stat_scores) if stat_scores else 0
    stats_good  = avg_score >= 0.80

    passive_name  = weapon.get("passive_name", "")
    passive_value = weapon.get("passive_value")
    passive_good  = any(gp in passive_name for gp in good_passives)
    passive_bad   = any(bp in passive_name for bp in bad_passives)

    if passive_name:
        threshold = PASSIVE_THRESHOLDS.get(passive_name, {})
        great_val = threshold.get("great", 0)
        good_val  = threshold.get("good", 0)
        unit      = threshold.get("unit", "")

        if passive_bad:
            passive_note = (
                f"❌ Passive **{passive_name}** ({passive_value}{unit}) — bad for this weapon!\n"
                f"   Best passives: {', '.join(good_passives[:3])}"
            )
            passive_good = False
        elif passive_good and passive_value and passive_value >= great_val:
            passive_note = f"✅ Passive **{passive_name}** ({passive_value}{unit}) — excellent!"
        elif passive_good and passive_value and passive_value >= good_val:
            passive_note = f"➡️ Passive **{passive_name}** ({passive_value}{unit}) — good but could be higher (want {great_val}+{unit})"
            passive_good = False
        elif passive_good:
            passive_note = f"✅ Passive **{passive_name}** — correct type!"
        else:
            passive_note = (
                f"❌ Passive **{passive_name}** — not ideal for this weapon.\n"
                f"   Best passives: {', '.join(good_passives[:3])}"
            )
    else:
        passive_note = "⚠️ Couldn't read passive from output."
        passive_good = False

    if stats_good and passive_good:
        verdict        = "✅ KEEP"
        action         = "This weapon is great! No reroll needed."
        reroll_stat    = False
        reroll_passive = False
    elif stats_good and not passive_good:
        verdict        = "🔄 REROLL PASSIVE"
        action         = (
            f"Stats are great but passive is wrong.\n"
            f"Run: `owo rr {weapon.get('id','?')} passive`\n"
            f"Cost: ~100 shards per attempt\n"
            f"⚠️ Wear degrades each reroll! New passive values will be random."
        )
        reroll_stat    = False
        reroll_passive = True
    elif not stats_good and passive_good:
        verdict        = "🔄 REROLL STATS"
        action         = (
            f"Passive is good but stats are weak.\n"
            f"Run: `owo rr {weapon.get('id','?')} stat`\n"
            f"⚠️ This rerolls passive VALUES too (not type). Passive type stays same."
        )
        reroll_stat    = True
        reroll_passive = False
    else:
        verdict        = "🔄 REROLL STATS FIRST"
        action         = (
            f"Both stats and passive need work. Start with stats.\n"
            f"Run: `owo rr {weapon.get('id','?')} stat`\n"
            f"After getting good stats → reroll passive if still wrong."
        )
        reroll_stat    = True
        reroll_passive = True

    return {
        "verdict":        verdict,
        "action":         action,
        "stat_notes":     stat_notes,
        "passive_note":   passive_note,
        "reroll_stat":    reroll_stat,
        "reroll_passive": reroll_passive,
        "notes":          ideal.get("notes", ""),
        "good_passives":  good_passives,
        "avg_score":      round(avg_score * 100, 1),
    }


def compare_reroll(current: dict, new: dict) -> str:
    lines = ["⚔️ **Reroll Comparison**\n"]

    cur_q = current.get("quality", 0)
    new_q = new.get("quality", 0)
    if new_q > cur_q:
        lines.append(f"📈 Quality: {cur_q}% → **{new_q}%** (+{round(new_q-cur_q,1)}%) ✅")
    elif new_q < cur_q:
        lines.append(f"📉 Quality: {cur_q}% → **{new_q}%** ({round(new_q-cur_q,1)}%) ❌")
    else:
        lines.append(f"➡️ Quality: {cur_q}% → {new_q}% (same)")

    cur_wp = current.get("wp_cost")
    new_wp = new.get("wp_cost")
    if cur_wp and new_wp:
        if new_wp < cur_wp:
            lines.append(f"📈 WP Cost: {cur_wp} → **{new_wp}** (lower = better ✅)")
        elif new_wp > cur_wp:
            lines.append(f"📉 WP Cost: {cur_wp} → **{new_wp}** (higher = worse ❌)")
        else:
            lines.append(f"➡️ WP Cost: {cur_wp} → {new_wp} (same)")

    for stat_key, label in [("heal_pct", "Heal %"), ("dmg_pct", "Damage %"), ("replenish_pct", "Replenish %")]:
        cur_v = current.get(stat_key)
        new_v = new.get(stat_key)
        if cur_v and new_v:
            if new_v > cur_v:
                lines.append(f"📈 {label}: {cur_v}% → **{new_v}%** ✅")
            elif new_v < cur_v:
                lines.append(f"📉 {label}: {cur_v}% → **{new_v}%** ❌")
            else:
                lines.append(f"➡️ {label}: same ({cur_v}%)")

    cur_p  = current.get("passive_name", "?")
    new_p  = new.get("passive_name", "?")
    cur_pv = current.get("passive_value", "?")
    new_pv = new.get("passive_value", "?")

    if cur_p != new_p:
        lines.append(f"🔄 Passive: **{cur_p}** ({cur_pv}) → **{new_p}** ({new_pv})")
    elif cur_pv != new_pv:
        try:
            diff = round(float(new_pv) - float(cur_pv), 1)
            arrow = "✅" if diff > 0 else "❌"
            lines.append(f"Passive value: {cur_pv} → **{new_pv}** ({'+' if diff>0 else ''}{diff}) {arrow}")
        except:
            lines.append(f"Passive: {cur_p} ({cur_pv} → {new_pv})")
    else:
        lines.append(f"➡️ Passive: same ({cur_p} {cur_pv})")

    lines.append("")
    text = "\n".join(lines)
    good_count = text.count("✅")
    bad_count  = text.count("❌")

    if good_count > bad_count:
        lines.append("**🎯 VERDICT: CONFIRM** ✅")
        lines.append("The new roll is better overall!")
    elif bad_count > good_count:
        lines.append("**🎯 VERDICT: CANCEL** ❌")
        lines.append("The new roll is worse — keep your current weapon.")
    else:
        lines.append("**🎯 VERDICT: YOUR CALL** ➡️")
        lines.append("Mixed results — check passive type. If passive is better, confirm!")

    lines.append(f"\n**Buttons to press:**")
    lines.append(f"✅ **Confirm** — accept new roll")
    lines.append(f"❌ **Cancel** — keep current weapon")
    lines.append(f"🔄 **Reroll** — spend more shards to try again")

    return "\n".join(lines)


def format_reroll_advice(weapon: dict, eval_result: dict) -> str:
    name    = weapon.get("name", "?")
    wid     = weapon.get("id", "?")
    quality = weapon.get("quality", "?")
    wear    = weapon.get("wear", "WORN")
    reroll_changes  = weapon.get("reroll_changes", 0)
    reroll_attempts = weapon.get("reroll_attempts", 0)

    lines = [
        f"🗡️ **{name}** (ID: `{wid}`)",
        f"Quality: **{quality}%** | Wear: **{wear}**",
        f"Reroll History: {reroll_changes} changes, {reroll_attempts} attempts",
        "",
        "**📊 Stat Analysis:**",
    ]

    for note in eval_result["stat_notes"]:
        lines.append(f"  {note}")

    if not eval_result["stat_notes"]:
        lines.append("  ⚠️ Couldn't read detailed stats — make sure to run `owo weapon {id}`")

    lines.append("")
    lines.append("**🎲 Passive:**")
    lines.append(f"  {eval_result['passive_note']}")
    lines.append("")
    lines.append(f"💡 **{eval_result['notes']}**")
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━")
    lines.append(f"**🎯 {eval_result['verdict']}**")
    lines.append(eval_result["action"])

    if eval_result["reroll_stat"] or eval_result["reroll_passive"]:
        lines.append("")
        lines.append("After rerolling → OwO shows **[CURRENT]** vs **[NEW]**")
        lines.append("Share that output and I'll tell you **Confirm or Cancel!**")

    return "\n".join(lines)
