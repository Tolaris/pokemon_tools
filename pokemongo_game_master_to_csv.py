#!/usr/bin/env python3

# Copyright 2019 Google LLC
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

from collections import defaultdict

# CSV row headers
headerFastMoves = ["Move Name", "Type", "DPT", "EPT", "D+EPT", "PvP Duration", "PvP Power", "PvP Energy", "PvE Power", "PvE Energy", "PvE Duration"]
headerChargeMoves = ["Move Name", "Type", "PvP Power", "PvP Energy", "PvP DPE", "PvE Power", "PvE Energy", "PvE Duration"]
headerPokemonStats = ["Name", "Pokedex ID", "Type", "Type2", "Attack", "Defense", "Stamina", "Family", "3rd Move Stardust", "3rd Move Candy", "km Buddy Distance", "Encounter Capture Rate", "Encounter Flee Rate", "Male %", "Female %", "Genderless %", "Quick Moves", "Charge Moves"]

# output filenames
filenameFastMoves   = "output/fastMoves.csv"
filenameChargeMoves = "output/chargeMoves.csv"
filenamePokemonStats = "output/pokemonStats.csv"

def outputDictAsCsv(datadict, header, filename):
  """Output dict as CSV spreadsheet with header."""
  import csv
  with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.DictWriter(csvfile, fieldnames=header)
    csvwriter.writeheader()
    for k in sorted(datadict.keys()):
      csvwriter.writerow(datadict[k])

def getAllFieldsByName(field, gm):
  """Given a field name and GAME_MASTER, return a list of matching dicts."""
  results = []
  for i in gm['itemTemplates']:
    if field in i.keys():
      match = i[field]
      # merge "templateId" into each returned field
      if "templateId" in i.keys():
        match["templateId"] = i["templateId"]
      results.append(match)
  return results

def getCombatMoves(gm):
  """Return two dicts containing fast moves and charge moves."""
  combatMoves = getAllFieldsByName("combatMove", gm)
  moveSettings = getAllFieldsByName("moveSettings", gm)
  fastMoves = defaultdict(dict)
  chargeMoves = defaultdict(dict)

  for pvpMove in combatMoves:
    # automatically create missing fields with 0 instead of default defined in
    # json.load()
    pvpMove = defaultdict(int,pvpMove)

    # Fast moves
    if pvpMove['uniqueId'][-5:] == "_FAST":
      moveName = pvpMove['uniqueId'][0:-5].replace("_"," ").title()
      fastMoves[moveName] = {
          'Move Name': moveName,
          'Type': pvpMove['type'].replace("POKEMON_TYPE_","").title(),
          'PvP Power':  pvpMove['power'],
          'PvP Energy': pvpMove['energyDelta'],
      }
      # "durationTurns" is "number of additional turns". Add 1 to it to count
      # the current turn.
      fastMoves[moveName]['PvP Duration'] = pvpMove['durationTurns'] + 1
      fastMoves[moveName]['DPT'] = fastMoves[moveName]['PvP Power'] / fastMoves[moveName]['PvP Duration']
      fastMoves[moveName]['EPT'] = fastMoves[moveName]['PvP Energy'] / fastMoves[moveName]['PvP Duration']
      fastMoves[moveName]['D+EPT'] = (fastMoves[moveName]['PvP Power'] + fastMoves[moveName]['PvP Energy']) / fastMoves[moveName]['PvP Duration']

    # Charge moves
    else:
      moveName = pvpMove['uniqueId'].replace("_"," ").title()
      chargeMoves[moveName] = {
          'Move Name': moveName,
          'Type': pvpMove['type'].replace("POKEMON_TYPE_","").title(),
          'PvP Power':  pvpMove['power'],
          'PvP Energy': pvpMove['energyDelta'],
      }
      chargeMoves[moveName]['PvP DPE'] = chargeMoves[moveName]['PvP Power'] / -chargeMoves[moveName]['PvP Energy']

  for pveMove in moveSettings:
    # automatically create missing fields with 0 instead of default defined in
    # json.load()
    pveMove = defaultdict(int,pveMove)

    # Fast moves
    if pveMove['movementId'][-5:] == "_FAST":
      moveName = pveMove['movementId'][0:-5].replace("_"," ").title()
      fastMoves[moveName]['Move Name'] = moveName
      fastMoves[moveName]['PvE Power'] = pveMove['power']
      fastMoves[moveName]['PvE Energy'] = pveMove['energyDelta']
      fastMoves[moveName]['PvE Duration'] = pveMove['durationMs']

    # Charge moves
    else:
      moveName = pveMove['movementId'].replace("_"," ").title()
      chargeMoves[moveName]['Move Name'] = moveName
      chargeMoves[moveName]['PvE Power'] = pveMove['power']
      chargeMoves[moveName]['PvE Energy'] = pveMove['energyDelta']
      chargeMoves[moveName]['PvE Duration'] = pveMove['durationMs']

  return fastMoves, chargeMoves


def getPokemonStats(gm):
  """Return a dict containing Pokémon base data."""
  pokemonSettings = getAllFieldsByName("pokemonSettings", gm)
  genderSettings = getAllFieldsByName("genderSettings", gm)
  pokemonStats = defaultdict(dict)

  for pokemon in pokemonSettings:
    pokemonName = pokemon['pokemonId'].replace("_"," ").title()
    pokemonStats[pokemonName] = {
        'Name': pokemonName,
        'Pokedex ID': int(pokemon['templateId'][1:5]),
        'Type': pokemon['type'].replace("POKEMON_TYPE_","").title(),
        'Type2': pokemon['type2'].replace("POKEMON_TYPE_","").title(),
        'Attack': pokemon['stats']['baseAttack'],
        'Defense': pokemon['stats']['baseDefense'],
        'Stamina': pokemon['stats']['baseStamina'],
        'Family': pokemon['familyId'][7:].replace("_"," ").title(),
        '3rd Move Stardust': pokemon['thirdMove']['stardustToUnlock'],
        '3rd Move Candy': pokemon['thirdMove']['candyToUnlock'],
        'km Buddy Distance': pokemon['kmBuddyDistance'],
        'Encounter Capture Rate': pokemon['encounter']['baseCaptureRate'],
        'Encounter Flee Rate': pokemon['encounter']['baseFleeRate'],
        'Quick Moves': ", ".join(pokemon['quickMoves']).replace("_FAST","").replace("_"," ").title(), # non-Legacy
        'Charge Moves': ", ".join(pokemon['cinematicMoves']).replace("_"," ").title(),                # non-Legacy
    }
    for genderSetting in genderSettings:
      pokemonName = genderSetting['pokemon'].replace("_"," ").title()
      pokemonStats[pokemonName]['Male %'] = genderSetting['gender']['malePercent']
      pokemonStats[pokemonName]['Female %'] = genderSetting['gender']['femalePercent']
      pokemonStats[pokemonName]['Genderless %'] = genderSetting['gender']['genderlessPercent']

  return pokemonStats


if __name__ == '__main__':
  from functools import partial
  import json
  import pprint
  import sys

  if len(sys.argv) < 2:
    print("usage: {} path/to/GAME_MASTER.json".format(sys.argv[0]))
    print("\n")
    print("try:   pokemongo_game_master_to_csv.py ../pokemongo-game-master/versions/latest/GAME_MASTER.json")
    sys.exit(1)

  with open(sys.argv[1],"r") as fp:
    gm = json.load(fp, object_hook=partial(defaultdict, lambda: ''))
  pp = pprint.PrettyPrinter().pprint

  fastMoves, chargeMoves = getCombatMoves(gm)
  outputDictAsCsv(fastMoves, headerFastMoves, filenameFastMoves)
  outputDictAsCsv(chargeMoves, headerChargeMoves, filenameChargeMoves)

  pokemonStats = getPokemonStats(gm)
  outputDictAsCsv(pokemonStats, headerPokemonStats, filenamePokemonStats)
