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

from enum import Enum

class PokemonBaseType(Enum):
  """An Enum representing a Pokemon type, such as 'Fire' or 'Water'."""
  # Types are ordered by in-game type order, and will sort/print in that order.
  nothing = 0
  Normal = 1
  Fire = 2
  Water = 3
  Electric = 4
  Grass = 5
  Ice = 6
  Fighting = 7
  Poison = 8
  Ground = 9
  Flying = 10
  Psychic = 11
  Bug = 12
  Rock = 13
  Ghost = 14
  Dragon = 15
  Dark = 16
  Steel = 17
  Fairy = 18

  # See "OrderedEnum" example in Python 3 Enum docs (8.13.13.2).
  # This allows ordered comparison of types, so we can use sorted().
  def __ge__(self, other):
    if self.__class__ is other.__class__:
      return self.value >= other.value
    return NotImplemented
  def __gt__(self, other):
    if self.__class__ is other.__class__:
      return self.value > other.value
    return NotImplemented
  def __le__(self, other):
    if self.__class__ is other.__class__:
      return self.value <= other.value
    return NotImplemented
  def __lt__(self, other):
    if self.__class__ is other.__class__:
      return self.value < other.value
    return NotImplemented

  def __str__(self):
    return self.name

# Defense matrix. 0 = normal damage, 1 = weak, -1 = strong, -2 = immune.
# Build it the slow way because it's more readable for humans.
# Build a dummy 0th row and column so we can add a "nothing" second type to a real
# one and get logical results without special logic.
defense = [None] * 19
# HEADER                                  [ n,NO,FR,WA,EL,GR,IC,FG,PO,GR,FL,PS,BU,RO,GH,DR,DA,ST,FA]
defense[PokemonBaseType.nothing.value] =  [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
defense[PokemonBaseType.Normal.value] =   [ 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,-2, 0, 0, 0, 0]
defense[PokemonBaseType.Fire.value] =     [ 0, 0,-1, 1, 0,-1,-1, 0, 0, 1, 0, 0,-1, 1, 0, 0, 0,-1,-1]
defense[PokemonBaseType.Water.value] =    [ 0, 0,-1,-1, 1, 1,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1, 0]
defense[PokemonBaseType.Electric.value] = [ 0, 0, 0, 0,-1, 0, 0, 0, 0, 1,-1, 0, 0, 0, 0, 0, 0,-1, 0]
defense[PokemonBaseType.Grass.value] =    [ 0, 0, 1,-1,-1,-1, 1, 0, 1,-1, 1, 0, 1, 0, 0, 0, 0, 0, 0]
defense[PokemonBaseType.Ice.value] =      [ 0, 0, 1, 0, 0, 0,-1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0]
defense[PokemonBaseType.Fighting.value] = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1,-1,-1, 0, 0,-1, 0, 1]
defense[PokemonBaseType.Poison.value] =   [ 0, 0, 0, 0, 0,-1, 0,-1,-1, 1, 0, 1,-1, 0, 0, 0, 0, 0,-1]
defense[PokemonBaseType.Ground.value] =   [ 0, 0, 0, 1,-2, 1, 1, 0,-1, 0, 0, 0, 0,-1, 0, 0, 0, 0, 0]
defense[PokemonBaseType.Flying.value] =   [ 0, 0, 0, 0, 1,-1, 1,-1, 0,-2, 0, 0,-1, 1, 0, 0, 0, 0, 0]
defense[PokemonBaseType.Psychic.value] =  [ 0, 0, 0, 0, 0, 0, 0,-1, 0, 0, 0,-1, 1, 0, 1, 0, 1, 0, 0]
defense[PokemonBaseType.Bug.value] =      [ 0, 0, 1, 0, 0,-1, 0,-1, 0,-1, 1, 0, 0, 1, 0, 0, 0, 0, 0]
defense[PokemonBaseType.Rock.value] =     [ 0,-1,-1, 1, 0, 1, 0, 1,-1, 1,-1, 0, 0, 0, 0, 0, 0, 1, 0]
defense[PokemonBaseType.Ghost.value] =    [ 0,-2, 0, 0, 0, 0, 0,-2,-1, 0, 0, 0,-1, 0, 1, 0, 1, 0, 0]
defense[PokemonBaseType.Dragon.value] =   [ 0, 0,-1,-1,-1,-1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
defense[PokemonBaseType.Dark.value] =     [ 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,-2, 1, 0,-1, 0,-1, 0, 1]
defense[PokemonBaseType.Steel.value] =    [ 0,-1, 1, 0, 0,-1,-1, 1,-2, 1,-1,-1,-1,-1, 0,-1, 0,-1,-1]
defense[PokemonBaseType.Fairy.value] =    [ 0, 0, 0, 0, 0, 0, 0,-1, 1, 0, 0, 0,-1, 0, 0,-2,-1, 1, 0]

def _get_defense(defense_row,defense_value=0):
  results = []
  for i in range(len(defense_row)):
    if defense_row[i] == defense_value:
      results.append(PokemonBaseType(i))
  return results

class PokemonType:
  global defense

  def __init__(self, type1, type2=PokemonBaseType["nothing"]):
    # TODO: check inputs. For now, assume two valid types as input
    if type(type1) is not PokemonBaseType:
      raise TypeError('input must be of class PokemonBaseType')
    if type(type2) is not PokemonBaseType :
      raise TypeError('input must be of class PokemonBaseType')
    if type2.name == "nothing":
      self.name = type1.name
    elif type1.name == "nothing":
      self.name = type2.name
    else:
      self.name = "{} / {}".format(type1.name, type2.name)
    self.defense = [defense[type1.value][x] + defense[type2.value][x] for x in range(len(defense[type1.value]))]
    self.resist_3x = _get_defense(self.defense,-3)
    self.resist_2x = _get_defense(self.defense,-2)
    self.resist_1x = _get_defense(self.defense,-1)
    self.weak_2x = _get_defense(self.defense,2)
    self.weak_1x = _get_defense(self.defense,1)

  def __str__(self):
    return self.name

  def summary(self):
    """Pretty-print a summary of a PokemonType."""
    output = "Type: {}\n".format(self.name)
    if self.weak_2x:
      output += "  Weakness(2x): {}\n".format(", ".join([str(i) for i in self.weak_2x]))
    if self.weak_1x:
      output += "  Weaknesses:   {}\n".format(", ".join([str(i) for i in self.weak_1x]))
    if self.resist_3x:
      output += "  Resist(3x):   {}\n".format(", ".join([str(i) for i in self.resist_3x]))
    if self.resist_2x:
      output += "  Resist(2x):   {}\n".format(", ".join([str(i) for i in self.resist_2x]))
    if self.resist_1x:
      output += "  Resistances:  {}\n".format(", ".join([str(i) for i in self.resist_1x]))
    return output


#normal_flying = PokemonTypeSet(pokemon_types["Normal"], pokemon_types["Flying"])
#print('try: print(pokemon_types["Ground"])')
if __name__ == '__main__':
  import sys
  if len(sys.argv) == 3:
    print(PokemonType(PokemonBaseType[sys.argv[1]], PokemonBaseType[sys.argv[2]]).summary())
  elif len(sys.argv) == 2:
    print(PokemonType(PokemonBaseType[sys.argv[1]]).summary())
  else:
    print("usage: {} Type1 [Type2]".format(sys.argv[0]))
