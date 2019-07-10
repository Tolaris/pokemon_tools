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

"""Extract Pokémon Go game data to spreadsheets."""

from collections import defaultdict
from functools import partial
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import argparse
import json
import pickle
import os
import os.path

# Row headers
headerFastMoves = ["Move Name", "Type", "DPT", "EPT", "D+EPT", "PvP Duration", "PvP Power", "PvP Energy", "PvE Power", "PvE Energy", "PvE Duration"]
headerChargeMoves = ["Move Name", "Type", "PvP Power", "PvP Energy", "PvP DPE", "PvE Power", "PvE Energy", "PvE Duration"]
headerPokemonStats = ["Name", "Pokedex ID", "Type", "Type2", "Attack", "Defense", "Stamina", "Family", "3rd Move Stardust", "3rd Move Candy", "km Buddy Distance", "Encounter Capture Rate", "Encounter Flee Rate", "Male %", "Female %", "Genderless %", "Quick Moves", "Charge Moves"]
headerCpMultiplier = ["Level", "CP x"]
headerMovesByPokemon = ["Move Name", "Move Type", "Move Class", "Pokemon Name", "Pokemon Type", "Pokemon Type2"]

# CSV output filenames
csvOutputDirectory = "output"
csvFilenameFastMoves   = "fastMoves.csv"
csvFilenameChargeMoves = "chargeMoves.csv"
csvFilenamePokemonStats = "pokemonStats.csv"
csvFilenameCpMultiplier = "cpMultiplier.csv"

# Google Sheets output
sheetsSpreadsheetId = "1HyxMawsvHyxcKVL9a9GKH2as15qdI9HhSCr0Q_hWYnc"
sheetsTabFastMoves = "Fast"
sheetsTabChargeMoves = "Charge"
sheetsTabPokemonStats = "Pokemon"
sheetsTabCpMultiplier = "CP"

def outputDictAsCsv(datadict, header, filename):
  """Output dict as CSV spreadsheet with header."""
  import csv
  with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.DictWriter(csvfile, fieldnames=header)
    csvwriter.writeheader()
    for k in sorted(datadict.keys()):
      csvwriter.writerow(datadict[k])

def getSheetsService():
  """Returns a Google Sheets service, refreshing credentials if required."""
  # Taken directly from:
  # https://developers.google.com/sheets/api/quickstart/python
  scopes = ['https://www.googleapis.com/auth/spreadsheets']
  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('credentials_token.pickle'):
      with open('credentials_token.pickle', 'rb') as token:
          creds = pickle.load(token)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
          creds = flow.run_local_server()
      # Save the credentials for the next run
      with open('credentials_token.pickle', 'wb') as token:
          pickle.dump(creds, token)
  return build('sheets', 'v4', credentials=creds)

def getRowsFromDictInHeaderOrder(D, order):
  """Given a dict and list of columns, return a 2D list ordered by column.
  D's keys are lost and all k:v pairs become column:cell values.
  Input:
    D: the dictionary of key: dict
    order: a list of column headers
  Returns: a list of lists, sorted by first element, with column headers first.
  """
  # build dict of "heading: columnNumber" pairs
  columnOrder = {}
  for x in range(len(order)):
    columnOrder[order[x]] = x
  # TODO: Figure out the pythonic way to do this with dict or list
  # comprehensions. It'll probably be faster.
  results = []
  for d in D.values():
    row = ['' for _ in range(len(d))]
    for k,v in d.items():
      row[columnOrder[k]] = v
    results.append(row)
  return [order] + sorted(results)

def outputDictAsSheet(datadict, header, spreadsheetId, tabName):
  """Output dict as Google sheet with header. Clears sheet of existing values."""
  rows = getRowsFromDictInHeaderOrder(datadict, header)
  cellrange = '{}!A1:Z'.format(tabName)

  # Call the Sheets API
  service = getSheetsService()
  body = {
      'ranges': [cellrange]
  }
  service.spreadsheets().values().batchClear(
      spreadsheetId=spreadsheetId,
      body=body
  ).execute()
  body = {
      'values': rows
  }
  service.spreadsheets().values().update(
      spreadsheetId=spreadsheetId,
      range=cellrange,
      valueInputOption='USER_ENTERED',
      body=body
  ).execute()

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
  movesByPokemon = []
  formsToBaseForm = {}

  for pokemon in pokemonSettings:
    # Formes have multiple entries, one for the "base" form (not a Pokemon) and
    # one for each form like Normal, Alolan. Collect a mapping.
    if "form" in pokemon.keys():
      pokemonName = pokemon['form'].replace("_"," ").title()
      formsToBaseForm[pokemonName] = pokemon['pokemonId'].replace("_"," ").title()
    else:
      pokemonName = pokemon['pokemonId'].replace("_"," ").title()

    quickMoves = [x.replace("_FAST","").replace("_"," ").title() for x in pokemon['quickMoves']] # non-Legacy
    chargeMoves = [x.replace("_"," ").title() for x in pokemon['cinematicMoves']]                # non-Legacy
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
        'Quick Moves': ", ".join(quickMoves),
        'Charge Moves': ", ".join(chargeMoves),
    }

    # Gender settings are the same for all Formes. Copy the base form gender data
    # to all Formes.
    for genderSetting in genderSettings:
      pokemonName = genderSetting['pokemon'].replace("_"," ").title()
      pokemonStats[pokemonName]['Male %'] = genderSetting['gender']['malePercent']
      pokemonStats[pokemonName]['Female %'] = genderSetting['gender']['femalePercent']
      pokemonStats[pokemonName]['Genderless %'] = genderSetting['gender']['genderlessPercent']
    for pokemonForm, baseForm in formsToBaseForm.items():
      pokemonStats[pokemonForm]['Male %'] = pokemonStats[baseForm]['Male %']
      pokemonStats[pokemonForm]['Female %'] = pokemonStats[baseForm]['Female %']
      pokemonStats[pokemonForm]['Genderless %'] = pokemonStats[baseForm]['Genderless %']

    # Now delete the base form, so we only output one line per Forme.
    for baseForm in formsToBaseForm.values():
      try:
        del pokemonStats[baseForm]
      except KeyError:
        pass

  return pokemonStats


def getCpMultiplier(gm):
  """Return a dict containing Pokémon base data."""
  playerLevel = getAllFieldsByName("playerLevel", gm)[0]
  cpMultiplier = {}
  for i in range(len(playerLevel["cpMultiplier"])):
    cpMultiplier[i+1] = {
        "Level": i+1,
        "CP x": playerLevel["cpMultiplier"][i],
      }
  return cpMultiplier

# TODO tyler: Don't do this. Instead generate a new structure to return in
# getPokemonStats. Only parse the data once.
#headerMovesByPokemon = ["Move Name", "Move Type", "Move Class", "Pokemon Name", "Pokemon Type", "Pokemon Type2"]
def getMovesByPokemon(fastMoves, chargeMoves, pokemonStats):
  movesByPokemon = None
  pass
  return movesByPokemon


if __name__ == '__main__':
  # argparse
  parser = argparse.ArgumentParser(description=__doc__)

  parser.add_argument("-o", "--output", choices=["csv", "sheets", "test"], help="output csv files or Google Sheets (default {})".format(csvOutputDirectory), default="sheets")
  parser.add_argument("-c", "--csv_dir", help="directory to output CSV files (default {})".format(csvOutputDirectory), default=csvOutputDirectory)
  parser.add_argument("-s", "--sheet", help="the Google Sheet ID to update (default {})".format(sheetsSpreadsheetId), default=sheetsSpreadsheetId)
  parser.add_argument("game_master", help="the path to GAME_MASTER.json")
  args = parser.parse_args()

  if not args.game_master:
    parser.print_help()
    parser.exit(1)

  with open(args.game_master, "r") as fp:
    gm = json.load(fp, object_hook=partial(defaultdict, lambda: ''))

  fastMoves, chargeMoves = getCombatMoves(gm)
  pokemonStats = getPokemonStats(gm)
  #cpMultiplier = getCpMultiplier(gm)
  movesByPokemon = getMovesByPokemon(fastMoves, chargeMoves, pokemonStats)

  if args.output == "csv":
    try:
      os.mkdir(args.csv_dir)
    except FileExistsError:
      pass
    print("Outputing CSV files in {}".format(os.path.abspath(args.csv_dir)))
    outputDictAsCsv(fastMoves, headerFastMoves, os.path.join(args.csv_dir, csvFilenameFastMoves))
    outputDictAsCsv(chargeMoves, headerChargeMoves, os.path.join(args.csv_dir, csvFilenameChargeMoves))
    outputDictAsCsv(pokemonStats, headerPokemonStats, os.path.join(args.csv_dir, csvFilenamePokemonStats))
    #outputDictAsCsv(cpMultiplier, headerCpMultiplier, os.path.join(args.csv_dir, csvFilenameCpMultiplier))
  elif args.output == "sheets":
    print("Updating https://docs.google.com/spreadsheets/d/{}".format(args.sheet))
    outputDictAsSheet(fastMoves, headerFastMoves, args.sheet, sheetsTabFastMoves)
    outputDictAsSheet(chargeMoves, headerChargeMoves, args.sheet, sheetsTabChargeMoves)
    outputDictAsSheet(pokemonStats, headerPokemonStats, args.sheet, sheetsTabPokemonStats)
    #outputDictAsSheet(cpMultiplier, headerCpMultiplier, args.sheet, sheetsTabCpMultiplier)
  else: # else we are in "test" mode, and want to inspect variables interactively
    import pprint
    pp = pprint.PrettyPrinter().pprint
    print("dir():", dir())
    print("Pretty-print with 'pp()'")
