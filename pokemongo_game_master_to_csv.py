#!/usr/bin/env python3

# CSV row headers
headerFastMoves = ["Move Name", "Type", "DPT", "EPT", "D+EPT", "PvP Duration", "PvP Power", "PvP Energy", "PvE Power", "PvE Energy", "PvE Duration"]
headerChargeMoves = ["Move Name", "Type", "PvP Power", "PvP Energy", "PvP DPE", "PvE Power", "PvE Energy", "PvE Duration"]

# output filenames
filenameFastMoves   = "output/fastMoves.csv"
filenameChargeMoves = "output/chargeMoves.csv"

def getAllFieldsByName(field, gm):
  """Given a field name and GAME_MASTER, return a list of matching dicts."""
  results = []
  for i in gm['itemTemplates']:
    if field in i.keys():
      results.append(i[field])
  return results

def getFieldByName(field, gm):
  """Given a field name and GAME_MASTER, return the first matching dict."""
  results = []
  for i in gm['itemTemplates']:
    if field in i.keys():
      return i[field]

def outputCsv(header, rows, filename):
  """Write header and a list of rows to a csv file."""
  import csv
  pass

def getCombatMoves(gm):
  """Return two dicts containing fast moves and charge moves."""
  from collections import defaultdict

  combatMoves = getAllFieldsByName("combatMove", gm)
  moveSettings = getAllFieldsByName("moveSettings", gm)
  fastMoves = defaultdict(dict)
  chargeMoves = defaultdict(dict)

  """
  Fast move:
  >>> combatMoves[130]
  {'uniqueId': 'CONFUSION_FAST', 'type': 'POKEMON_TYPE_PSYCHIC', 'power': 16.0, 'vfxName': 'confusion_fast', 'durationTurns': 3, 'energyDelta': 12}
  >>> moveSettings[130]
  {'movementId': 'CONFUSION_FAST', 'animationId': 4, 'pokemonType': 'POKEMON_TYPE_PSYCHIC', 'power': 20.0, 'accuracyChance': 1.0, 'staminaLossScalar': 0.01, 'trainerLevelMin': 1, 'trainerLevelMax': 100, 'vfxName': 'confusion_fast', 'durationMs': 1600, 'damageWindowStartMs': 600, 'damageWindowEndMs': 1600, 'energyDelta': 15}

  Charge move:
  >>> combatMoves[0]
  {'uniqueId': 'WRAP', 'type': 'POKEMON_TYPE_NORMAL', 'power': 60.0, 'vfxName': 'wrap', 'energyDelta': -45}
  >>> moveSettings[0]
  {'movementId': 'WRAP', 'animationId': 5, 'pokemonType': 'POKEMON_TYPE_NORMAL', 'power': 60.0, 'accuracyChance': 1.0, 'criticalChance': 0.05, 'staminaLossScalar': 0.06, 'trainerLevelMin': 1, 'trainerLevelMax': 100, 'vfxName': 'wrap', 'durationMs': 2900, 'damageWindowStartMs': 2050, 'damageWindowEndMs': 2700, 'energyDelta': -33}
  """

  for pvpMove in combatMoves:
    # automatically create missing fields with value of 0
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
    # automatically create missing fields with value of 0
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

def outputMoves(moves, header, filename):
  """Output a spreadsheet of moves."""
  import csv
  with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.DictWriter(csvfile, fieldnames=header)
    csvwriter.writeheader()
    for k in sorted(moves.keys()):
      csvwriter.writerow(moves[k])


if __name__ == '__main__':
  import sys
  if len(sys.argv) < 2:
    print("usage: {} path/to/GAME_MASTER.json".format(sys.argv[0]))
    print("\n")
    print("try:   pokemongo_game_master_to_csv.py ../pokemongo-game-master/versions/latest/GAME_MASTER.json")
    sys.exit(1)

  import json
  with open(sys.argv[1],"r") as fp:
    gm = json.load(fp)

  import pprint
  pp = pprint.PrettyPrinter()
  fastMoves, chargeMoves = getCombatMoves(gm)
  outputMoves(fastMoves, headerFastMoves, filenameFastMoves)
  outputMoves(chargeMoves, headerChargeMoves, filenameChargeMoves)
