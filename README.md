# pokemon_tools

Tools for working with Pokémon Go / Pokémon game data.

Pokémon is Copyright Gamefreak, Nintendo and The Pokémon Company 2001-2019. All images and names owned and trademarked by Nintendo, Niantic, The Pokémon Company, and Gamefreak are property of their respective owners.

## pokemongo_game_master_to_spreadsheet.py

Converts GAME_MASTER.json into spreadsheets (Google Sheets or CSV) for easy analysis. Get a copy of the input here:
https://github.com/pokemongo-dev-contrib/pokemongo-game-master

Example usage:
```
pokemongo_game_master_to_spreadsheet.py -o sheets -s 1AaaAaaaaAaaaAAA1a1AAA1aa11aaA1AaAAa1A_aAAaa ../pokemongo-game-master/versions/latest/GAME_MASTER.json
or
pokemongo_game_master_to_spreadsheet.py -o csv -c output ../pokemongo-game-master/versions/latest/GAME_MASTER.json
```

Open the Google Sheet (-s) or files in the output directory (-c) for results.  If you just want to work with the latest data, make a copy of [this Google
Sheet](https://docs.google.com/spreadsheets/d/1HyxMawsvHyxcKVL9a9GKH2as15qdI9HhSCr0Q_hWYnc/edit).

## pokemon_types.py

Calculate resistances and weaknesses for any combination of two Pokemon types.

Example usage:
```
pokemon_types.py Electric Flying
pokemon_types.py Steel Ghost
pokemon_types.py Fire
```
