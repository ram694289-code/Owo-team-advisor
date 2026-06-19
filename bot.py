import discord
import asyncio
import os
import re
from discord.ext import commands
from parser import parse_pets, parse_weapons
from team_builder import build_team, format_team
from database import calc_stats, find_weapon, find_animal, WEAPONS
from reroll_advisor import parse_weapon_inspect, evaluate_weapon, format_reroll_advice, compare_reroll
from templates import match_templates, format_template_result

# ============================================================
# OwO Team Advisor Bot v3
# - Reads owo pets in ONE command (no dex queue)
# - Handles multiple copies of same animal
# - Full animal base stat database
# ============================================================

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OWO_BOT_ID = 408785106942164992

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# { user_id: { animals, weapons, waiting_for } }
sessions = {}

def get_session(uid):
    if uid not in sessions:
        sessions[uid] = {
            "animals": [],
            "weapons": [],
            "waiting_for": None,
            "pending_reroll": None,
            "weapon_page": 1,
            "weapon_total_pages": 1,
            "weapons_buffer": [],
            "user_mention": None,   # stored when !start is run
        }
    return sessions[uid]

def reset_weapon_scan(session):
    """Reset weapon pagination state before a fresh scan."""
    session["weapons"] = []
    session["weapons_buffer"] = []
    session["weapon_page"] = 1
    session["weapon_total_pages"] = 1

def parse_page_info(content: str) -> tuple[int, int]:
    """
    Extract (current_page, total_pages) from OwO's embed footer/content.
    OwO typically shows: 'Page 1 / 3', '1/3', 'Page 1 of 3', etc.
    Returns (1, 1) if no pagination detected.
    """
    patterns = [
        r'[Pp]age\s*(\d+)\s*/\s*(\d+)',
        r'[Pp]age\s*(\d+)\s+of\s+(\d+)',
        r'\((\d+)\s*/\s*(\d+)\)',
        r'^(\d+)\s*/\s*(\d+)$',
    ]
    for pat in patterns:
        m = re.search(pat, content, re.MULTILINE)
        if m:
            return int(m.group(1)), int(m.group(2))
    return 1, 1

# ============================================================
# OWO MESSAGE WATCHER
# ============================================================

@bot.event
async def on_ready():
    print(f"✅ OwO Team Advisor v3 online as {bot.user}")

@bot.event
async def on_message(message: discord.Message):
    if message.author.id == bot.user.id:
        return
    if message.author.id == OWO_BOT_ID:
        await handle_owo_message(message)
        return
    await bot.process_commands(message)

def extract_owo_text(message: discord.Message) -> str:
    """Pull ALL text out of an OwO message — plain content + every embed field."""
    parts = [message.content or ""]
    for embed in message.embeds:
        if embed.title:
            parts.append(embed.title)
        if embed.description:
            parts.append(embed.description)
        for field in embed.fields:
            parts.append(field.name or "")
            parts.append(field.value or "")
        if embed.footer and embed.footer.text:
            parts.append(embed.footer.text)
    return "\n".join(parts)

async def handle_owo_message(message: discord.Message):
    content = extract_owo_text(message)

    for uid, session in list(sessions.items()):
        waiting = session.get("waiting_for")

        # ── WEAPON INSPECT (reroll advisor) ──
        if waiting == "inspect":
            if "Quality" in content or "quality" in content.lower():
                if "[CURRENT]" in content and "[NEW]" in content:
                    parts = content.split("[NEW]")
                    current_text = parts[0]
                    new_text = "[NEW]" + parts[1]
                    cur_weapon = parse_weapon_inspect(current_text)
                    new_weapon = parse_weapon_inspect(new_text)
                    session["waiting_for"] = None
                    comparison = compare_reroll(cur_weapon, new_weapon)
                    if len(comparison) > 1900:
                        for chunk in [comparison[i:i+1900] for i in range(0, len(comparison), 1900)]:
                            await message.channel.send(chunk)
                    else:
                        await message.channel.send(comparison)
                    break

                weapon = parse_weapon_inspect(content)
                if weapon.get("name"):
                    session["pending_reroll"] = weapon
                    session["waiting_for"] = None
                    result = evaluate_weapon(weapon)
                    advice = format_reroll_advice(weapon, result)
                    if len(advice) > 1900:
                        for chunk in [advice[i:i+1900] for i in range(0, len(advice), 1900)]:
                            await message.channel.send(chunk)
                    else:
                        await message.channel.send(advice)

                    if result["reroll_stat"] or result["reroll_passive"]:
                        wid = weapon.get("id","?")
                        await message.channel.send(
                            f"👆 After rerolling, OwO shows **[CURRENT] vs [NEW]**\n"
                            f"I'll automatically compare them — just use `!reroll` to watch!"
                        )
                    break

        # ── PETS OUTPUT ──
        if waiting == "pets":
            pets_keywords = ["lvl.", "level", "pets", "fabled", "legendary", "mythical",
                             "epic", "rare", "uncommon", "common", "gem", "hp", "str",
                             "mag", "wp", "pr", "mr", "xp", "animal"]
            if any(k in content.lower() for k in pets_keywords):
                animals = parse_pets(content)
                if animals:
                    session["animals"] = animals
                    session["waiting_for"] = "weapons"

                    leveled   = [a for a in animals if a["level"] > 1]
                    unleveled = [a for a in animals if a["level"] <= 1]

                    lines = [
                        f"✅ **Got your pets!** Found **{len(animals)} animals**",
                        f"🔼 Leveled: **{len(leveled)}** | ⬇️ Not leveled: **{len(unleveled)}**",
                        ""
                    ]
                    for a in animals:
                        rank = a.get("rank","?").title()
                        lv   = a.get("level", 1)
                        name = a.get("display_name","?").title()
                        computed = a.get("computed", {})
                        str_v = computed.get("str","?")
                        mag_v = computed.get("mag","?")
                        lines.append(
                            f"• **{name}** ({rank}) Lv.{lv} "
                            f"— STR:{str_v} MAG:{mag_v}"
                        )

                    lines.append("")
                    lines.append("🔍 Now scanning your weapons...")

                    msg = "\n".join(lines)
                    if len(msg) > 1900:
                        for chunk in [msg[i:i+1900] for i in range(0, len(msg), 1900)]:
                            await message.channel.send(chunk)
                    else:
                        await message.channel.send(msg)

                    # Auto-trigger weapon scan — use @mention so OwO shows THIS user's weapons
                    reset_weapon_scan(session)
                    mention = session.get("user_mention", "")
                    await asyncio.sleep(1)
                    cmd = f"owo weapon {mention}".strip()
                    await message.channel.send(cmd)
                    break

                else:
                    # Parser found keywords but couldn't identify pets —
                    # OwO's format might have changed. Tell the user instead of going silent.
                    await message.channel.send(
                        "⚠️ I saw OwO's pets response but couldn't read any pet names.\n"
                        "This can happen if OwO's layout changed. Try again, or let the developer know!\n"
                        "_(Use `!start` to retry)_"
                    )
                    session["waiting_for"] = None
                    break

        # ── WEAPONS OUTPUT ──
        elif waiting == "weapons":
            weapon_keywords = ["legendary","epic","mythical","rare","fabled",
                               "uncommon","common","weapon","quality","wp cost"]
            if any(k in content.lower() for k in weapon_keywords):
                page_weapons = parse_weapons(content)
                cur_page, total_pages = parse_page_info(content)

                # Update session with what we just learned
                session["weapon_total_pages"] = total_pages
                session["weapon_page"] = cur_page

                # Add new weapons (avoid duplicates by name+slot)
                existing_names = {w["name"] for w in session["weapons_buffer"]}
                for w in page_weapons:
                    if w["name"] not in existing_names:
                        session["weapons_buffer"].append(w)
                        existing_names.add(w["name"])

                if cur_page < total_pages:
                    # More pages — request the next one
                    next_page = cur_page + 1
                    await message.channel.send(
                        f"📄 Got page {cur_page}/{total_pages} "
                        f"({len(session['weapons_buffer'])} weapons so far) — fetching page {next_page}..."
                    )
                    await asyncio.sleep(1)
                    await message.channel.send(f"owo weapon {next_page}")
                else:
                    # All pages collected — finalise
                    all_weapons = session["weapons_buffer"]
                    session["weapons"] = all_weapons
                    session["waiting_for"] = None
                    session["weapons_buffer"] = []

                    mention = session.get("user_mention", "")
                    if all_weapons:
                        await auto_suggest_team(message.channel, session, mention)
                    else:
                        await message.channel.send(
                            f"{mention} ⚠️ Couldn't read any weapons. Make sure you have weapons equipped and try `!start` again."
                        )
                break

# ============================================================
# AUTO SUGGEST — called automatically after weapons are done
# ============================================================

async def auto_suggest_team(channel, session, mention):
    """Run after all weapon pages are collected. Posts best team with no extra user steps."""
    animals = session.get("animals", [])
    weapons = session.get("weapons", [])

    # Try streaker first (usually highest tier), then breaker, pick whichever scores better
    streaker_results = match_templates(animals, weapons, "streaker")
    breaker_results  = match_templates(animals, weapons, "breaker")

    all_results = []
    if streaker_results:
        all_results.append(streaker_results[0])
    if breaker_results:
        all_results.append(breaker_results[0])

    # Pick best by score
    all_results.sort(key=lambda r: r.get("score", 0), reverse=True)

    if not all_results:
        await channel.send(f"{mention} ⚠️ Couldn't find a matching team. Try `!start` again.")
        return

    best = all_results[0]

    # ── Team breakdown first ──
    await channel.send(f"{mention} ✅ **Done! Here's your best team:**")
    output = format_template_result(best)
    for chunk in [output[i:i+1900] for i in range(0, len(output), 1900)]:
        await channel.send(chunk)

    # ── Summary card ──
    t      = best["template"]
    tier   = t.get("tier", "B")
    style  = t.get("style", "streaker")
    score  = best.get("score", 0)
    ready  = best.get("ready", False)
    miss_w = best.get("missing_key_weapons", [])
    miss_a = best.get("missing_key_animals", [])

    # Tier info
    tier_data = {
        "S": {"emoji": "🏆", "color": 0xFFD700, "label": "Top-tier",   "pct": "top 5%"},
        "A": {"emoji": "⭐", "color": 0x57F287, "label": "Strong",      "pct": "top 20%"},
        "B": {"emoji": "🔵", "color": 0x5865F2, "label": "Solid",       "pct": "top 40%"},
    }.get(tier, {"emoji": "🔵", "color": 0x5865F2, "label": "Solid", "pct": "top 40%"})

    # Readiness bar  e.g. ████████░░ 80%
    total_slots = len(t.get("slots", [])) or 1
    filled      = total_slots - len(miss_w) - len(miss_a)
    filled      = max(0, min(filled, total_slots))
    bar_filled  = round((filled / total_slots) * 10)
    bar         = "█" * bar_filled + "░" * (10 - bar_filled)
    pct         = round((filled / total_slots) * 100)

    style_label = "🛡️ Streaker (survive & sustain)" if style == "streaker" else "⚔️ Breaker (burst & debuff)"

    if ready:
        status_line = f"✅ **Fully equipped** — run this team now!"
        tip = f"Use `!reroll <id>` to polish your weapon stats."
    elif pct >= 60:
        status_line = f"⚠️ Almost there — missing a couple of pieces."
        tip = f"Still need: {', '.join([f'`{w}`' for w in (miss_w + miss_a)[:4]])}"
    else:
        status_line = f"🔧 Work in progress — keep grinding!"
        tip = f"Priority targets: {', '.join([f'`{w}`' for w in (miss_w + miss_a)[:4]])}"

    embed = discord.Embed(
        title=f"{tier_data['emoji']} Team Report — Tier {tier} · {tier_data['label']}",
        color=tier_data["color"]
    )
    embed.add_field(name="Team",      value=t.get("name", "?"),   inline=True)
    embed.add_field(name="Style",     value=style_label,           inline=False)
    embed.add_field(
        name="Readiness",
        value=f"`{bar}` {pct}%\n{status_line}",
        inline=False
    )
    embed.add_field(
        name="Standing",
        value=f"This is a **{tier_data['pct']}** OwO team composition.",
        inline=False
    )
    embed.add_field(name="Next step", value=tip, inline=False)

    await channel.send(embed=embed)

# ============================================================
# COMMANDS
# ============================================================

@bot.command(name="start")
async def start(ctx):
    session = get_session(ctx.author.id)
    session["animals"] = []
    session["weapons"] = []
    session["waiting_for"] = "pets"
    session["user_mention"] = ctx.author.mention

    embed = discord.Embed(
        title="👋 OwO Team Advisor",
        description=(
            f"Hey {ctx.author.mention}! Ready to build your best team?\n\n"
            "**Just type `owo pets` now** — I'll handle everything from there!\n"
            "_(I'll read your pets, scan all your weapons, and post your team automatically)_"
        ),
        color=0x57F287
    )
    await ctx.send(embed=embed)

@bot.command(name="pets")
async def pets_cmd(ctx):
    session = get_session(ctx.author.id)
    session["waiting_for"] = "pets"
    session["user_mention"] = ctx.author.mention
    await ctx.send("✅ Ready — type `owo pets` and I'll read your pets automatically!")

@bot.command(name="weapons")
async def weapons_cmd(ctx):
    session = get_session(ctx.author.id)
    reset_weapon_scan(session)
    session["waiting_for"] = "weapons"
    session["user_mention"] = ctx.author.mention
    await ctx.send("✅ Ready — type `owo weapon` and I'll scan all pages automatically!")

@bot.command(name="debug")
async def debug_cmd(ctx):
    session = get_session(ctx.author.id)
    animals  = session.get("animals", [])
    weapons  = session.get("weapons", [])
    waiting  = session.get("waiting_for")
    wp       = session.get("weapon_page", 1)
    wtp      = session.get("weapon_total_pages", 1)
    buf_len  = len(session.get("weapons_buffer", []))

    embed = discord.Embed(title="🔍 Debug — What I have stored for you", color=0xFEE75C)

    # Status line
    status = f"Currently waiting for: **{waiting or 'nothing'}**"
    if waiting == "weapons" and wtp > 1:
        status += f" | Weapon page **{wp}/{wtp}** (buffer: {buf_len})"
    embed.add_field(name="⏳ State", value=status, inline=False)

    # Pets
    if animals:
        pet_lines = []
        for a in animals:
            name  = a.get("display_name", "?").title()
            rank  = a.get("rank", "?").title()
            lv    = a.get("level", 1)
            c     = a.get("computed", {})
            pet_lines.append(f"• **{name}** ({rank}) Lv.{lv} STR:{c.get('str','?')} MAG:{c.get('mag','?')}")
        value = "\n".join(pet_lines[:20])   # cap at 20 so embed doesn't overflow
        if len(animals) > 20:
            value += f"\n… and {len(animals)-20} more"
        embed.add_field(name=f"🐾 Pets ({len(animals)})", value=value, inline=False)
    else:
        embed.add_field(name="🐾 Pets", value="None stored yet — type `owo pets` after `!start`", inline=False)

    # Weapons
    if weapons:
        wp_lines = []
        for w in weapons:
            name  = w.get("name", "?")
            slot  = w.get("slot", "?")
            qual  = w.get("quality", "?")
            wp_lines.append(f"• **{name}** ({slot}) — {qual}")
        value = "\n".join(wp_lines[:20])
        if len(weapons) > 20:
            value += f"\n… and {len(weapons)-20} more"
        embed.add_field(name=f"🗡️ Weapons ({len(weapons)})", value=value, inline=False)
    else:
        embed.add_field(name="🗡️ Weapons", value="None stored yet — weapons are auto-scanned after pets", inline=False)

    await ctx.send(embed=embed)

@bot.command(name="suggest")
async def suggest(ctx):
    session = get_session(ctx.author.id)
    animals = session["animals"]
    weapons = session["weapons"]

    if not animals:
        await ctx.send("❌ No pets scanned! Use `!start` then run `owo pets`.")
        return
    if not weapons:
        await ctx.send("❌ No weapons scanned! Use `!weapons` then run `owo weapon`.")
        return

    embed = discord.Embed(title="⚔️ What kind of team?", color=0x7289DA)
    embed.add_field(
        name="🛡️  !streaker",
        value="Survive long battles.\nHealing + revives + WP sustain.",
        inline=True
    )
    embed.add_field(
        name="⚔️  !breaker",
        value="Destroy enemy strategies.\nDebuffs + burst damage.",
        inline=True
    )
    await ctx.send(embed=embed)

@bot.command(name="streaker")
async def streaker(ctx):
    await send_team(ctx, "streaker")

@bot.command(name="breaker")
async def breaker_cmd(ctx):
    await send_team(ctx, "breaker")

async def send_team(ctx, team_type):
    session = get_session(ctx.author.id)
    animals = session["animals"]
    weapons = session["weapons"]

    if not animals:
        await ctx.send("❌ No pets yet! Use `!start` first.")
        return

    await ctx.send(f"🔍 Analysing your animals and weapons against all team templates...")

    results = match_templates(animals, weapons, team_type)

    if not results:
        await ctx.send("❌ No templates found. Make sure you scanned pets and weapons!")
        return

    best = results[0]
    alt  = results[1] if len(results) > 1 else None

    output = format_template_result(best)
    for chunk in [output[i:i+1900] for i in range(0, len(output), 1900)]:
        await ctx.send(chunk)

    if not best["ready"] and alt:
        await ctx.send(
            f"⚠️ You're missing key weapons for **{best['template']['name']}**!\n"
            f"Here's the best team with what you **currently have**:"
        )
        alt_output = format_template_result(alt)
        for chunk in [alt_output[i:i+1900] for i in range(0, len(alt_output), 1900)]:
            await ctx.send(chunk)

    if len(results) > 2:
        other_names = [f"{r['template']['tier']}. {r['template']['name']}" for r in results[1:4]]
        await ctx.send(f"**Other options:** {' | '.join(other_names)}\nUse `!templates` to see all!")

@bot.command(name="info")
async def info_cmd(ctx, *, name: str):
    wid, wdata = find_weapon(name)
    if wdata:
        embed = discord.Embed(title=f"🗡️ {wdata['name']}", color=0x5865F2)
        embed.add_field(name="Role",    value=wdata.get("role","?").title(), inline=True)
        embed.add_field(name="Stat",    value=wdata.get("stat","None") or "None", inline=True)
        embed.add_field(name="WP Cost", value=str(wdata.get("wp",(0,0))), inline=True)
        embed.add_field(name="Effect",  value=wdata.get("effect","None") or "None", inline=True)
        embed.add_field(name="AoE",     value="Yes" if wdata.get("aoe") else "No", inline=True)
        embed.add_field(name="Description", value=wdata.get("desc","?"), inline=False)
        await ctx.send(embed=embed)
        return

    key, adata = find_animal(name)
    if adata:
        embed = discord.Embed(title=f"🐾 {key.title()} ({adata['rank'].title()})", color=0x57F287)
        embed.add_field(name="Stat Total", value=str(adata["total"]), inline=True)
        embed.add_field(name="HP",  value=str(adata["hp"]),  inline=True)
        embed.add_field(name="STR", value=str(adata["str"]), inline=True)
        embed.add_field(name="PR",  value=str(adata["pr"]),  inline=True)
        embed.add_field(name="WP",  value=str(adata["wp"]),  inline=True)
        embed.add_field(name="MAG", value=str(adata["mag"]), inline=True)
        embed.add_field(name="MR",  value=str(adata["mr"]),  inline=True)
        ex = calc_stats(20, adata["hp"], adata["str"], adata["pr"],
                        adata["wp"], adata["mag"], adata["mr"])
        embed.add_field(
            name="At Level 20",
            value=f"HP:{ex['hp']} STR:{ex['str']} MAG:{ex['mag']} WP:{ex['wp']}\nPR:{ex['pr']}% MR:{ex['mr']}%",
            inline=False
        )
        await ctx.send(embed=embed)
        return

    await ctx.send(f"❌ `{name}` not found as a weapon or animal.")

@bot.command(name="statcalc")
async def statcalc(ctx, level: int, hp: int, str_: int, pr: int, wp: int, mag: int, mr: int):
    r = calc_stats(level, hp, str_, pr, wp, mag, mr)
    embed = discord.Embed(title=f"📊 Stats at Level {level}", color=0x57F287)
    embed.add_field(name="HP",       value=r["hp"],       inline=True)
    embed.add_field(name="STR",      value=r["str"],      inline=True)
    embed.add_field(name="MAG",      value=r["mag"],      inline=True)
    embed.add_field(name="WP",       value=r["wp"],       inline=True)
    embed.add_field(name="PR",       value=f"{r['pr']}%", inline=True)
    embed.add_field(name="MR",       value=f"{r['mr']}%", inline=True)
    embed.add_field(name="eHP Phys", value=r["ehp_phys"], inline=True)
    embed.add_field(name="eHP Mag",  value=r["ehp_mag"],  inline=True)
    await ctx.send(embed=embed)

@bot.command(name="session")
async def session_cmd(ctx):
    session = get_session(ctx.author.id)
    animals = session["animals"]
    weapons = session["weapons"]

    embed = discord.Embed(title=f"📋 {ctx.author.display_name}'s Session", color=0xFEE75C)

    if animals:
        from collections import defaultdict
        groups = defaultdict(list)
        for a in animals:
            groups[a["display_name"]].append(a["level"])

        lines = []
        for species, levels in groups.items():
            levels_str = ", ".join([f"Lv.{l}" for l in sorted(levels, reverse=True)])
            lines.append(f"**{species.title()}**: {levels_str}")
        embed.add_field(name=f"🐾 Animals ({len(animals)} total)", value="\n".join(lines) or "None", inline=False)
    else:
        embed.add_field(name="🐾 Animals", value="None scanned", inline=False)

    embed.add_field(
        name=f"🗡️ Weapons ({len(weapons)})",
        value=", ".join([w["name"] for w in weapons]) if weapons else "None",
        inline=False
    )
    embed.add_field(name="Waiting for", value=session.get("waiting_for") or "Nothing", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="reset")
async def reset(ctx):
    sessions.pop(ctx.author.id, None)   # wipe entirely; get_session() rebuilds fresh
    await ctx.send("🔄 Session cleared! Use `!start` to begin a fresh scan.")

@bot.command(name="reroll")
async def reroll_cmd(ctx, weapon_id: str = None):
    session = get_session(ctx.author.id)
    session["waiting_for"] = "inspect"

    if weapon_id:
        await ctx.send(f"🔍 Inspecting weapon `{weapon_id}`...")
        await ctx.send(f"owo weapon {weapon_id}")
    else:
        await ctx.send(
            "⚠️ Please provide a weapon ID: `!reroll 42`\n"
            "Check your weapon IDs with `owo weapon`."
        )
        session["waiting_for"] = None

@bot.command(name="shards")
async def shards_cmd(ctx):
    embed = discord.Embed(title="💎 Weapon Shards", color=0xA855F7)
    embed.add_field(name="Check shards",      value="`owo ws` or `owo weaponshards`", inline=False)
    embed.add_field(name="Reroll stats",       value="`owo weapon rr {id} stat`\nRerolls ALL stats (dmg%, WP cost, passive values)", inline=False)
    embed.add_field(name="Reroll passive",     value="`owo weapon rr {id} passive`\nRerolls passive TYPE (random new passive)", inline=False)
    embed.add_field(name="Dismantle weapon",   value="`owo dismantle {id}`\nBreaks weapon into shards", inline=False)
    embed.add_field(name="Buy weapon crate",   value="Costs **40 shards**", inline=False)
    embed.add_field(name="⚠️ Warning",         value="Every reroll **degrades weapon wear** by 1 stage!\nPristine→Fine→Decent→Worn\nEmpowered weapons **cannot** be rerolled!", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="wearinfo")
async def wearinfo_cmd(ctx):
    embed = discord.Embed(title="🔧 Weapon Wear", color=0xEB459E)
    embed.add_field(name="Pristine", value="1% chance | +5% quality bonus", inline=True)
    embed.add_field(name="Fine",     value="5% chance | +3% quality bonus", inline=True)
    embed.add_field(name="Decent",   value="10% chance | +1% quality bonus", inline=True)
    embed.add_field(name="Worn",     value="Default | No bonus", inline=True)
    embed.add_field(name="Unknown",  value="Pre-update weapons | No bonus", inline=True)
    embed.add_field(
        name="⚠️ Important",
        value="Each reroll degrades wear by 1 stage. A Pristine weapon becomes Fine after one reroll!",
        inline=False
    )
    await ctx.send(embed=embed)

@bot.command(name="templates")
async def templates_cmd(ctx, style: str = "all"):
    from templates import TEMPLATES
    style = style.lower()

    embed = discord.Embed(
        title="📋 All OwO Team Templates",
        description="Bot knows these compositions and auto-selects the best one for you!",
        color=0x5865F2
    )

    streakers = [t for t in TEMPLATES if t["style"] == "streaker"]
    breakers  = [t for t in TEMPLATES if t["style"] == "breaker"]

    if style in ("all", "streaker"):
        val = ""
        for t in streakers:
            tier_e = {"S":"🏆","A":"⭐","B":"🔵"}.get(t["tier"],"❓")
            val += f"{tier_e} **{t['name']}** (Tier {t['tier']}, Lv.{t['level_min']}+)\n"
            val += f"  _{t['description'][:60]}..._\n"
        embed.add_field(name="🛡️ Streaker Templates", value=val or "None", inline=False)

    if style in ("all", "breaker"):
        val = ""
        for t in breakers:
            tier_e = {"S":"🏆","A":"⭐","B":"🔵"}.get(t["tier"],"❓")
            val += f"{tier_e} **{t['name']}** (Tier {t['tier']}, Lv.{t['level_min']}+)\n"
            val += f"  _{t['description'][:60]}..._\n"
        embed.add_field(name="⚔️ Breaker Templates", value=val or "None", inline=False)

    embed.set_footer(text="Use !suggest to auto-pick the best one for YOUR animals + weapons!")
    await ctx.send(embed=embed)

@bot.command(name="top")
async def top_cmd(ctx, stat: str = "overall"):
    """Rank your scanned pets. Stats: str | mag | hp | wp | overall"""
    session = get_session(ctx.author.id)
    animals = session.get("animals", [])
    if not animals:
        await ctx.send("❌ No pets scanned yet. Use `!start` then type `owo pets`.")
        return

    stat = stat.lower()
    valid = ("str", "mag", "hp", "wp", "overall")
    if stat not in valid:
        await ctx.send(f"❓ Unknown stat `{stat}`. Choose from: {', '.join(valid)}")
        return

    def score(a):
        c = a.get("computed", {})
        if stat == "overall":
            return (c.get("str", 0) or 0) + (c.get("mag", 0) or 0) + (c.get("hp", 0) or 0)
        return c.get(stat, 0) or 0

    ranked = sorted(animals, key=score, reverse=True)

    stat_label = {"str": "STR", "mag": "MAG", "hp": "HP",
                  "wp": "WP", "overall": "STR+MAG+HP"}[stat]

    embed = discord.Embed(
        title=f"🏆 Your Top Pets — by {stat_label}",
        color=0x57F287
    )
    lines = []
    medals = ["🥇", "🥈", "🥉"]
    for i, a in enumerate(ranked[:15]):
        c  = a.get("computed", {})
        nm = a.get("display_name", "?").title()
        rk = a.get("rank", "?").title()
        lv = a.get("level", 1)
        if stat == "overall":
            val = f"{(c.get('str',0) or 0)+(c.get('mag',0) or 0)+(c.get('hp',0) or 0)}"
        else:
            val = str(c.get(stat, "?"))
        prefix = medals[i] if i < 3 else f"`{i+1}.`"
        lines.append(f"{prefix} **{nm}** ({rk}) Lv.{lv} — {stat_label}:{val}")
    embed.description = "\n".join(lines)
    embed.set_footer(text=f"Showing top {min(15, len(ranked))} of {len(ranked)} pets • !top str / mag / hp / wp / overall")
    await ctx.send(embed=embed)


@bot.command(name="missing")
async def missing_cmd(ctx):
    """Show which weapons you still need for the best team templates."""
    from templates import TEMPLATES
    session = get_session(ctx.author.id)
    animals = session.get("animals", [])
    weapons = session.get("weapons", [])

    if not animals:
        await ctx.send("❌ No pets scanned yet. Use `!start` then type `owo pets`.")
        return

    owned_names = {w["name"].lower() for w in weapons}

    embed = discord.Embed(
        title="🎯 Weapons You're Still Missing",
        description="Based on your top team templates — listed from highest-priority to lowest.",
        color=0xED4245
    )

    added = 0
    for t in TEMPLATES[:6]:            # check top 6 templates
        missing = []
        for slot in t.get("slots", []):
            for wp in slot.get("ideal_weapons", []):
                if wp.lower() not in owned_names and wp not in missing:
                    missing.append(wp)
        if missing:
            tier_e = {"S": "🏆", "A": "⭐", "B": "🔵"}.get(t["tier"], "❓")
            style_e = "🛡️" if t["style"] == "streaker" else "⚔️"
            embed.add_field(
                name=f"{tier_e}{style_e} {t['name']} (Tier {t['tier']})",
                value="Missing: " + ", ".join([f"`{w}`" for w in missing]),
                inline=False
            )
            added += 1
        if added >= 5:
            break

    if added == 0:
        embed.description = "✅ You have all the key weapons for the top templates! Use `!suggest` to get your team."

    embed.set_footer(text="Use !info <weapon> to learn what each weapon does")
    await ctx.send(embed=embed)


@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(
        title="📖 OwO Team Advisor",
        description=(
            "Only 3 commands you need to know:\n\n"
            "**`!start`**\n"
            "Begins the scan. Then just type `owo pets` — the bot reads your pets and all weapon pages automatically and posts your best team.\n\n"
            "**`!reroll <weapon id>`**\n"
            "Get advice on whether a weapon is worth rerolling. Example: `!reroll 42`\n\n"
            "**`!reset`**\n"
            "Clears everything and starts fresh."
        ),
        color=0x5865F2
    )
    embed.set_footer(text="That's it! Type !start to begin.")
    await ctx.send(embed=embed)

if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: DISCORD_BOT_TOKEN environment variable not set!")
        exit(1)
    print("Starting OwO Team Advisor v3...")
    bot.run(TOKEN)
