"""
MIT License

Copyright (c) 2022 John (BalloonPoodle#1337)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
import csv
import json
import sys

jewels = {
    "Militant Faith": "db/MilitantFaithSeeds.csv",
    "Brutal Restraint": "db/BrutalRestraintSeeds.csv",
    "Glorious Vanity": "db/GloriousVanitySeeds.csv",
    "Elegant Hubris": "db/ElegantHubrisSeeds.csv",
    "Lethal Pride": "db/LethalPrideSeeds.csv",
}

jewel_stats = {
    "Militant Faith": ['Calming Devotion', 'Cloistered', 'Enduring Faith', 'Frenzied Faith',
                       'Heated Devotion', 'Intolerance of Sin', "Martyr's Might", 'Powerful Faith',
                       'Smite the Heretical', 'Smite the Ignorant', 'Smite the Wicked',
                       'Thoughts and Prayers', 'Thundrous Devotion', 'Zealot', 'base_devotion'],
    "Brutal Restraint": ['base_dexterity', 'base_avoid_stun_%', 'evasion_rating_+%',
                         'charges_gained_+%', 'minion_movement_speed_+%', 'elemental_damage_+%',
                         'add_frenzy_charge_on_kill_%_chance', 'base_poison_damage_+%',
                         'projectile_damage_+%', 'base_elemental_status_ailment_duration_+%',
                         'non_curse_aura_effect_+%', 'critical_strike_chance_+%',
                         'global_chance_to_blind_on_hit_%', 'base_cold_damage_resistance_%',
                         'base_movement_velocity_+%', 'attack_and_cast_speed_+%',
                         'minion_damage_+%', 'maximum_life_+%', 'faster_poison_%',
                         'accuracy_rating_+%', 'non_damaging_ailment_effect_+%', 'dexterity_+%',
                         'onslaught_buff_duration_on_kill_ms', 'physical_damage_%_to_add_as_cold',
                         'gain_alchemists_genius_on_flask_use_%'],
    "Glorious Vanity": ['Ancient Hex', 'Automaton Studies', 'Blood-Quenched Bulwark',
                        'Bloody Savagery', 'Commanding Presence', 'Construct Studies',
                        'Cult of Chaos', 'Cult of Fire', 'Cult of Ice', 'Cult of Lightning',
                        'Energy Flow Studies', 'Exquisite Pain', 'Flesh to Flames',
                        'Flesh to Frost', 'Flesh to Lightning', 'Flesh Worship', 'Hierarchy',
                        'Jungle Paths', 'Legacy of the Vaal', 'Might of the Vaal',
                        'Revitalising Darkness', 'Revitalising Flames', 'Revitalising Frost',
                        'Revitalising Lightning', 'Revitalising Winds', 'Ritual of Flesh',
                        'Ritual of Immolation', 'Ritual of Memory', 'Ritual of Might',
                        'Ritual of Shadows', 'Ritual of Stillness', 'Ritual of Thunder',
                        'Soul Worship', 'Temple Paths', 'Thaumaturgical Aptitude',
                        'Thaumaturgical Protection'],
    "Elegant Hubris": ['Axiom Warden', 'Baleful Augmentation', "Bloody Flowers' Rebellion",
                       'Brutal Execution', "Chitus' Heart", 'City Walls', 'Crematorium Worker',
                       "Dialla's Wit", 'Discerning Taste', 'Eternal Adaptiveness',
                       'Eternal Bloodlust', 'Eternal Dominance', 'Eternal Exploitation',
                       'Eternal Fervour', 'Eternal Fortitude', 'Eternal Resilience',
                       'Eternal Separation', 'Eternal Subjugation', 'Flawless Execution',
                       'Freshly Brewed', 'Gemling Ambush', 'Gemling Inquisition',
                       'Gemling Training', "Geofri's End", 'Gleaming Legion', 'Laureate',
                       "Lioneye's Focus", 'Night of a Thousand Ribbons', 'Pooled Resources',
                       'Purity Rebel', "Rigwald's Might", 'Rites of Lunaris', 'Rites of Solaris',
                       'Robust Diet', 'Rural Life', 'Sceptre Pinnacle', 'Secret Tunnels',
                       'Shadowy Streets', 'Slum Lord', 'Street Urchin', 'Superiority',
                       'Virtue Gem Surgery', "Voll's Coup", 'War Games', 'With Eyes Open'],
    "Lethal Pride": ['base_fire_damage_resistance_%',
                     'base_life_leech_from_attack_damage_permyriad', 'base_max_fortification',
                     'base_self_critical_strike_multiplier_-%', 'base_strength',
                     'base_stun_duration_+%', 'base_stun_threshold_reduction_+%', 'burn_damage_+%',
                     'chance_to_deal_double_damage_%', 'chance_to_intimidate_on_hit_%',
                     'endurance_charge_on_kill_%', 'faster_burn_%',
                     'life_regeneration_rate_per_minute_%', 'maximum_life_+%',
                     'melee_critical_strike_chance_+%', 'melee_damage_+%',
                     'melee_weapon_critical_strike_multiplier_+',
                     'physical_damage_%_to_add_as_fire', 'physical_damage_+%',
                     'physical_damage_reduction_rating_+%', 'physical_damage_taken_%_as_fire',
                     'strength_+%', 'summon_totem_cast_speed_+%', 'totem_damage_+%',
                     'warcry_buff_effect_+%'],
}

near = {
    "Cleaving": ["Aggressive Bastion", "Cleaving", "Spiked Bulwark", "Slaughter", "Harpooner",
                 "Savage Wounds", "Hearty", "Robust", "Juggernaut", "Strong Arm", "Stamina",
                 "Barbarism", "Cannibalistic Rite", "Disemboweling", "Lust for Carnage",
                 "Warrior Training", "Diamond Skin"],
    "MoM": ["Asylum", "Enduring Bond", "Arcanist's Dominion", "Anointed Flesh", "Quick Recovery",
            "Essence Infusion", "Fire Walker", "Annihilation", "Essence Extraction"],
    "Supreme Ego": ["Charisma", "Master Sapper", "Dire Torment", "True Strike", "Adder's Touch",
                    "Wasting", "Overcharged", "Void Barrier", "Ballistics",
                    "Replenishing Remedies", "Revenge of the Hunted", "Taste for Blood"],
    "Pain Attunement": ["Nimbleness", "Tolerance", "Vampirism", "Melding", "Undertaker",
                        "Deep Wisdom", "Grave Intentions"],
    "Wind Dancer": ["Quickstep", "Weapon Artistry", "Swift Venoms", "Flash Freeze", "Silent Steps",
                   "Herbalism", "Survivalist", "Aspect of the Lynx", "Careful Conservationist",
                   "Intuition", "Winter Spirit", "Trick Shot", "Fervour", "King of the Hill",
                   "Acuity", "Master Fletcher", "Vengeant Cascade", "Inveterate", "Heartseeker"],
    "Ghost Dance": ["From the Shadows", "Clever Thief", "Backstabbing", "Claws of the Hawk",
                    "One with Evil", "Coldhearted Calculation", "Infused", "Blood Drinker",
                    "Soul Thief", "Will of Blades", "Flaying", "Resourcefulness", "Frenetic",
                    "Elemental Focus", "Mind Drinker", "Fangs of the Viper", "Saboteur",
                    "Master of Blades", "Depth Perception", "Claws of the Magpie",
                    "Sleight of Hand"],
    "Iron Grip": ["Window of Opportunity", "Battle Rouse", "Path of the Warrior", "Sentinel",
                  "Path of the Hunter", "Arcane Chemistry", "Malicious Intent", "Reflexes",
                  "Hired Killer", "Exceptional Performance", "Constitution", "Totemic Zeal"],
    "Unwavering Stance": ['Eagle Eye', 'Berserking', 'Bloodletting', 'Martial Experience',
                         'Admonisher', 'Command of Steel', 'Prismatic Skin'],
    "Iron Will": ['Potency of Will', 'Foresight', 'Dreamer', 'Path of the Warrior', 'Decay Ward',
                  'Forethought', 'Relentless', 'Malicious Intent', 'Path of the Savant',
                  'Inspiring Bond', 'Ash Frost and Storm', 'Veteran Soldier', 'Constitution',
                  'Totemic Zeal', 'Shaper'],
    "Solipsism": ['Potency of Will', 'Foresight', 'Window of Opportunity', 'Path of the Hunter',
                  'Destructive Apparatus', 'True Strike', 'Harrier', 'Path of the Savant',
                  'Reflexes', 'Inspiring Bond', 'Thrill Killer', 'Hired Killer',
                  'Exceptional Performance', 'Leadership'],
    "Elemental Equilibrium": ['Avatar of the Hunt', 'Burning Brutality', 'Crystal Skin',
                              'Profane Chemistry', 'Heavy Draw', 'Art of the Gladiator',
                              'Deadly Draw', 'Weathered Hunter', 'Hardened Scars',
                              "Gladiator's Perseverance"],
    "Zealots Oath": ['Might', 'Arcane Guarding', 'Death Attunement', 'Serpent Stance', 'Acrimony',
                     'Corruption', 'Fearsome Force', 'Hex Master', 'Unnatural Calm', 'Agility',
                     'Prism Weave', 'Blunt Trauma', 'Enigmatic Reach'],
    "Point Blank": ['Twin Terrors', 'Dazzling Strikes', 'Longshot', 'Thick Skin',
                   'Marked for Death', 'Feller of Foes', 'Blade Barrier', 'Fangs of Frost',
                   'Utmost Swiftness', 'Aspect of Stone', 'Bladedancer'],
    "Divine Shield": ['Skull Cracking', 'Vanquisher', 'Sanctum of Thought', 'Counterweight',
                     'Bone Breaker', 'Persistence', 'Whirling Barrier', 'Smashing Strikes',
                     'Shamanistic Fury', 'Disemboweling'],
    "Call To Arms": ['Executioner', 'Steadfast', 'Tribal Fury', 'Lava Lash', 'Blade of Cunning',
                   'Bastion Breaker'],
    "Measured Fury": ['Surveillance', "Golem's Blood", 'Vigour', 'Revelry', 'Deflection',
                     'Assured Strike', 'Cloth and Chain', 'Savagery', 'Ribcage Crusher', 'Dervish',
                     'Titanic Impacts', 'Master of the Arena', 'Destroyer', 'Measured Fury',
                     'Testudo', 'Bravery', 'Art of the Gladiator', 'Adamant', 'Defiance',
                     'Mana Flows', 'Dirty Techniques', 'Fury Bolts'],
    "Perfect Agony": ['From the Shadows', 'Forces of Nature', 'Split Shot', 'Clever Thief',
                     "Hunter's Gambit", 'Silent Steps', 'Piercing Shots', 'Survivalist',
                     'Fatal Toxins', 'Careful Conservationist', 'Trick Shot', 'Vengeant Cascade',
                     'Inveterate', 'Heartseeker'],
    "The Agnostic": ['Endurance', 'Divine Judgement', 'Divine Wrath', 'Runesmith',
                    'Sanctum of Thought', 'Divine Fervour', 'Holy Dominion', 'Overcharge',
                    'Faith and Steel', 'Devotion', 'Divine Fury', 'Arcane Capacitor',
                    'Smashing Strikes', 'Light of Divinity'],
    "Eternal Youth": ['Sanctuary', 'Combat Stamina', 'Dynamo', 'Sanctity', 'Gravepact', 'Expertise',
                     'Steelwood Stance', 'Powerful Bond', 'Deep Breaths', 'Ancestral Knowledge',
                     "Blacksmith's Clout"],
    "Eldritch Battery": ['Arcing Blows', 'Light Eater', 'Physique', 'Influence', 'Fusillade',
                        'Whispers of Doom', 'Alacrity', 'Searing Heat', 'Elder Power',
                        'Efficient Explosives', 'Mysticism', 'Successive Detonations',
                        'Throatseeker', 'Disintegration', 'Cleansed Thoughts', 'Utmost Intellect'],
    "Doomsday": ['Enigmatic Defence', 'Heart of Ice', 'Mental Rapidity', 'Prodigal Perfection',
                 'Breath of Lightning', 'Breath of Flames', 'Skittering Runes', 'Mystic Bulwark',
                 'Instability', 'Breath of Rime', 'Cruel Preparation', 'Wandslinger',
                 'Deep Thoughts', 'Arcane Will', 'Lord of the Dead', 'Golem Commander',
                 'Discord Artisan', 'Infused Flesh', 'Presage', 'Frost Walker', 'Heart of Thunder',
                 'Essence Surge'],
}


def load_jewel(jewel):
    rows = []
    with open(jewels[jewel], newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    return rows


def request_socket():
    jew_keys = list(near.keys())
    for j in enumerate(jew_keys):
        print(j)
    jewel_selected = None
    while True:
        try:
            jewel_selected = int(input(
                f"Select a jewel socket (near selected notable) [0-{len(jew_keys) - 1}]: "))
        except ValueError as e:
            print(f"Please input an integer [0-{len(jew_keys) - 1}]")
            continue
        if jewel_selected > len(jew_keys) or jewel_selected < 0:
            print(f"Please input an integer [0-{len(jew_keys) - 1}]")
            continue
        break

    print()
    return jew_keys[jewel_selected]


def request_jewel():
    jew_keys = list(jewels.keys())
    for j in enumerate(jew_keys):
        print(j)
    jewel_selected = None
    while True:
        try:
            jewel_selected = int(input("Select a jewel [0-4]: "))
        except ValueError as e:
            print("Please input an integer [0-4]")
            continue
        if jewel_selected > 4 or jewel_selected < 0:
            print("Please input an integer [0-4]")
            continue
        break
    print()
    return jew_keys[jewel_selected]


def request_notables(notables):
    n_list = []
    for n in enumerate(notables):
        print(n)
    while True:
        n = input(f"Enter a space delimited list of notable numbers [0-{len(notables) - 1}]: ")
        try:
            n_list = [int(not_num) for not_num in n.split()]
        except ValueError as e:
            print(f"Please input integers [0-{len(notables) - 1}]")
            continue
        for item in n_list:
            if item < 0 or item > len(notables) - 1:
                print(f"Please input integers [0-{len(notables) - 1}]")
                continue
        break

    print(n_list)
    selected = [notables[m] for m in n_list]
    print("Selected: ", selected)
    print()
    return selected


def request_excluded_stats(stats):
    n_list = []
    for n in enumerate(stats):
        print(n)
    while True:
        n = input(f"Enter a space delimited list of stats to exclude "
                  f"from searches [0-{len(stats) - 1}]: ")
        try:
            n_list = [int(not_num) for not_num in n.split()]
        except ValueError as e:
            print(f"Please input integers [0-{len(stats) - 1}]")
            continue
        for item in n_list:
            if item < 0 or item > len(stats) - 1:
                print(f"Please input integers [0-{len(stats) - 1}]")
                continue
        break

    print(n_list)
    selected = [stats[m] for m in n_list]
    print("Selected: ", selected)
    print()
    return selected


def request_stats(stats, num_near):
    mapping = {}
    for n in enumerate(stats):
        print(n)
    while True:
        n = input(
            "Enter the number of a stat followed by the number of times minimum "
            f"it should occur [0-{len(stats) - 1}] [1-{num_near}]. Leave blank to continue: "
        )
        if n == "":
            break
        try:
            n_list = [int(not_num) for not_num in n.split()]
        except ValueError as e:
            print(f"Please input integers [0-{len(stats) - 1}] [0-{num_near}]")
            continue

        if len(n_list) != 2:
            print(f"Please input two integers [0-{len(stats) - 1}] [0-{num_near}]")
            continue
        if n_list[0] < 0 or n_list[0] > len(stats) - 1 or n_list[1] < 0 or n_list[1] > num_near:
            print(f"Please input integers in the range [0-{len(stats) - 1}] [0-{num_near}]")
            continue
        mapping[stats[n_list[0]]] = n_list[1]

    print("Selected: ", mapping)
    print()
    return mapping


def request_info():
    jewel = request_jewel()
    socket = request_socket()

    notables_selected = request_notables(near[socket])
    stats = request_stats(jewel_stats[jewel], len(near[socket]))
    excluded = request_excluded_stats(jewel_stats[jewel])

    return {
        "Jewel": jewel,
        "Socket": socket,
        "Notables Selected": notables_selected,
        "Stats": stats,
        "Excluded": excluded
    }


def calculate(options):
    rows = load_jewel(options["Jewel"])

    for r in rows:
        matches = {}
        skip = False
        for k in r.keys():
            if k in options["Notables Selected"]:
                if r[k] in options["Excluded"]:
                    skip = True
                    break
                if r[k] not in matches.keys():
                    matches[r[k]] = [0, []]
                matches[r[k]][0] = matches[r[k]][0]+1
                matches[r[k]][1].append(k)
        if skip:
            continue
        passes = True
        for k, v in options["Stats"].items():
            if k not in matches.keys():
                passes = False
            if k in matches.keys() and matches[k][0] < v:
                passes = False
        if passes:
            print(f"(seed: {r['Seed']}, matches: {matches})")


def parse_config(args: argparse.Namespace):
    config = None

    with open(args.preset) as c:
        try:
            config = json.loads(c.read())
        except json.decoder.JSONDecodeError as err:
            print(f"{args.config} must be valid json\n{err}", file=sys.stderr)
            exit(1)

    check = ["Jewel", "Socket", "Notables Selected", "Stats"]

    for item in check:
        if config.get(item) is None:
            print(f"Missing '{item}' in {args.preset}", file=sys.stderr)
            exit(1)

    excluded = config.get("Excluded")
    if excluded is None:
        excluded = []

    return {
        "Jewel": config.get("Jewel"),
        "Socket": config.get("Socket"),
        "Notables Selected": config.get("Notables Selected"),
        "Stats": config.get("Stats"),
        "Excluded": excluded
    }


def options(config):
    if config.preset:
        return parse_config(config)
    return request_info()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--preset', default=None)
    return parser.parse_args()


def save_config(opt):
    c = input("To save the inputs you selected for use, input a name to save the file as "
              " Leave blank to skip: ")
    if c == "":
        return

    with open(f"{c}", 'w') as fp:
        json.dump(opt, fp)

    print(f"Saved inputs to {c}")


def main():
    config = parse_arguments()
    opt = options(config)
    calculate(opt)
    if config.preset is None:
        save_config(opt)


if __name__ == "__main__":
    main()
