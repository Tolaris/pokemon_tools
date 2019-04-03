# pokemon_tools

Tools for working with Pokémon Go / Pokémon game data. If you just want to work
with the data, make a copy of [my spreadsheet](https://www.tolaris.com/go/pogodata).

## pokemongo_game_master_to_csv.py

Converts GAME_MASTER.json into a set of spreadsheets for easy analysis. See:
https://github.com/pokemongo-dev-contrib/pokemongo-game-master

Example usage:
```
pokemongo_game_master_to_csv.py ../pokemongo-game-master/versions/latest/GAME_MASTER.json
```

See the "output" directory for results.

## pokemon_types.py

Calculate resistances and weaknesses for any combination of two Pokemon types.

Example usage:
```
pokemon_types.py Electric Flying
pokemon_types.py Steel Ghost
pokemon_types.py Fire
```
