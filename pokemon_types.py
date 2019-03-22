#!/usr/bin/env python3

from enum import Enum

class PokemonBaseType(Enum):
  """An Enum representing a Pokemon type, such as 'Fire' or 'Water'."""
  # Types are ordered by in-game type order, and will sort/print in that order.
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

class PokemonType:
  weaknesses = {
      PokemonBaseType.Normal: [PokemonBaseType.Fighting],
      PokemonBaseType.Fire: [PokemonBaseType.Water, PokemonBaseType.Ground, PokemonBaseType.Rock],
      PokemonBaseType.Water: [PokemonBaseType.Electric, PokemonBaseType.Grass],
      PokemonBaseType.Electric: [PokemonBaseType.Ground],
      PokemonBaseType.Grass: [PokemonBaseType.Fire, PokemonBaseType.Ice, PokemonBaseType.Poison, PokemonBaseType.Flying, PokemonBaseType.Bug],
      PokemonBaseType.Ice: [PokemonBaseType.Fire, PokemonBaseType.Fighting, PokemonBaseType.Rock, PokemonBaseType.Steel],
      PokemonBaseType.Fighting: [PokemonBaseType.Flying, PokemonBaseType.Psychic, PokemonBaseType.Fairy],
      PokemonBaseType.Poison: [PokemonBaseType.Ground, PokemonBaseType.Psychic],
      PokemonBaseType.Ground: [PokemonBaseType.Water, PokemonBaseType.Grass, PokemonBaseType.Ice],
      PokemonBaseType.Flying: [PokemonBaseType.Electric, PokemonBaseType.Ice, PokemonBaseType.Rock],
      PokemonBaseType.Psychic: [PokemonBaseType.Bug, PokemonBaseType.Ghost, PokemonBaseType.Dark],
      PokemonBaseType.Bug: [PokemonBaseType.Fire, PokemonBaseType.Flying, PokemonBaseType.Rock],
      PokemonBaseType.Rock: [PokemonBaseType.Water, PokemonBaseType.Grass, PokemonBaseType.Fighting, PokemonBaseType.Ground, PokemonBaseType.Steel],
      PokemonBaseType.Ghost: [PokemonBaseType.Ghost, PokemonBaseType.Dark],
      PokemonBaseType.Dragon: [PokemonBaseType.Ice, PokemonBaseType.Dragon, PokemonBaseType.Fairy],
      PokemonBaseType.Dark: [PokemonBaseType.Fighting, PokemonBaseType.Bug, PokemonBaseType.Fairy],
      PokemonBaseType.Steel: [PokemonBaseType.Fire, PokemonBaseType.Fighting, PokemonBaseType.Ground],
      PokemonBaseType.Fairy: [PokemonBaseType.Poison, PokemonBaseType.Steel],
  }

  resistances = {
      PokemonBaseType.Normal: [],
      PokemonBaseType.Fire: [PokemonBaseType.Fire, PokemonBaseType.Grass, PokemonBaseType.Ice, PokemonBaseType.Bug, PokemonBaseType.Steel, PokemonBaseType.Fairy],
      PokemonBaseType.Water: [PokemonBaseType.Fire, PokemonBaseType.Water, PokemonBaseType.Ice, PokemonBaseType.Steel],
      PokemonBaseType.Electric: [PokemonBaseType.Electric, PokemonBaseType.Flying, PokemonBaseType.Steel],
      PokemonBaseType.Grass: [PokemonBaseType.Water, PokemonBaseType.Electric, PokemonBaseType.Grass, PokemonBaseType.Ground],
      PokemonBaseType.Ice: [PokemonBaseType.Ice],
      PokemonBaseType.Fighting: [PokemonBaseType.Bug, PokemonBaseType.Rock, PokemonBaseType.Dark],
      PokemonBaseType.Poison: [PokemonBaseType.Grass, PokemonBaseType.Fighting, PokemonBaseType.Poison, PokemonBaseType.Bug, PokemonBaseType.Fairy],
      PokemonBaseType.Ground: [PokemonBaseType.Poison, PokemonBaseType.Rock],
      PokemonBaseType.Flying: [PokemonBaseType.Grass, PokemonBaseType.Fighting, PokemonBaseType.Bug],
      PokemonBaseType.Psychic: [PokemonBaseType.Fighting, PokemonBaseType.Psychic],
      PokemonBaseType.Bug: [PokemonBaseType.Grass, PokemonBaseType.Fighting, PokemonBaseType.Ground],
      PokemonBaseType.Rock: [PokemonBaseType.Normal, PokemonBaseType.Fire, PokemonBaseType.Poison, PokemonBaseType.Flying],
      PokemonBaseType.Ghost: [PokemonBaseType.Poison, PokemonBaseType.Bug],
      PokemonBaseType.Dragon: [PokemonBaseType.Fire, PokemonBaseType.Water, PokemonBaseType.Electric, PokemonBaseType.Grass],
      PokemonBaseType.Dark: [PokemonBaseType.Ghost, PokemonBaseType.Dark],
      PokemonBaseType.Steel: [PokemonBaseType.Normal, PokemonBaseType.Grass, PokemonBaseType.Ice, PokemonBaseType.Flying, PokemonBaseType.Psychic, PokemonBaseType.Bug, PokemonBaseType.Rock, PokemonBaseType.Dragon, PokemonBaseType.Steel, PokemonBaseType.Fairy],
      PokemonBaseType.Fairy: [PokemonBaseType.Fighting, PokemonBaseType.Bug, PokemonBaseType.Dark],
  }

  immunities = {
      PokemonBaseType.Normal: [PokemonBaseType.Ghost],
      PokemonBaseType.Fire: [],
      PokemonBaseType.Water: [],
      PokemonBaseType.Electric: [],
      PokemonBaseType.Grass: [],
      PokemonBaseType.Ice: [],
      PokemonBaseType.Fighting: [],
      PokemonBaseType.Poison: [],
      PokemonBaseType.Ground: [PokemonBaseType.Electric],
      PokemonBaseType.Flying: [PokemonBaseType.Ground],
      PokemonBaseType.Psychic: [],
      PokemonBaseType.Bug: [],
      PokemonBaseType.Rock: [],
      PokemonBaseType.Ghost: [PokemonBaseType.Normal, PokemonBaseType.Fighting],
      PokemonBaseType.Dragon: [],
      PokemonBaseType.Dark: [],
      PokemonBaseType.Steel: [PokemonBaseType.Poison],
      PokemonBaseType.Fairy: [PokemonBaseType.Dragon]
    }

  def __init__(self, pokemontype1, pokemontype2=None):
    if type(pokemontype1) is not PokemonBaseType:
      raise TypeError('input must be of class PokemonBaseType')
    #self.type = pokemontype
    self.name = self.type.name
    self.value = self.type.value
    self.weak = self.weaknesses[self.type]
    self.strong = self.resistances[self.type]
    self.immune = self.immunities[self.type]

  def __str__(self):
    return self.name

  def summary(self):
    """Pretty-print a summary of a PokemonType."""
    name = "Type: {}\n".format(self.name)
    if self.weak:
      weak = "  Weak to:   {}\n".format(", ".join([str(i) for i in self.weak]))
    else:
      weak = ""
    if self.strong:
      strong = "  Strong to: {}\n".format(", ".join([str(i) for i in self.strong]))
    else:
      strong = ""
    if self.immune:
      immune = "  Immune to: {}\n".format(", ".join([str(i) for i in self.immune]))
    else:
      immune = ""
    return (name + weak + strong + immune)

class PokemonTypeSet:
  """A class representing a pair of Pokemon types, such as 'Fire / Flying'."""

  def __init__(self, type1=None, type2=None):
    # validate inputs are both PokemonType
    #   valid: PokemonType, PokemonType; PokemonType, None
    # name
    #   if one type, set to type.name
    #   if two types, set to "type1.name / type2.name"
    # for weak:
    #   weak = set symmetric difference
    #   weak_double = set intersection
    # for each strong/immune, take set union of both types
    # print method should print weak_double members first, each followed by " (2x)"
    if type(type1) is not PokemonType:
      raise TypeError('type1 must be of class PokemonType')
    if type(type2) is not PokemonType:
      raise TypeError('type1 must be of class PokemonType')

    self.type1 = type1
    if type2 is None:
      self.type2 = None
      self.name = type1.name
      self.weak = type1.weak
      self.weak_double = []
      self.strong = type1.strong
      self.immune = type1.immune
      self.double_weak = []
    else:
      self.type2 = type2
      self.name = "{} / {}".format(type1.name, type2.name)
      self.weak = sorted(list(set(type1.weak) ^ set(type2.weak)))
      self.weak_double = sorted(list(set(type1.weak) & set(type2.weak)))
      self.strong = sorted(list(set(type1.strong) | set(type2.strong)))
      self.immune = sorted(list(set(type1.immune) | set(type2.immune)))

    self.weak_count = len(self.weak) + len(self.weak_double)*2
    self.strong_count = len(self.strong) + len(self.immune)*2

  def summary(self):
    """Pretty-print a summary of a PokemonType."""
    name = "Type: {}\n".format(self.name)
    if self.weak or self.weak_double:
      weaknesses = [str(i) + " (2x)" for i in self.weak_double]
      #+ self.weak
      weak = "  Weak to:   {}\n".format(", ".join(weaknesses))
    else:
      weak = ""
    if self.strong:
      strong = "  Strong to: {}\n".format(", ".join(self.strong))
    else:
      strong = ""
    if self.immune:
      immune = "  Immune to: {}\n".format(", ".join(self.immune))
    else:
      immune = ""
    return (name + weak + strong + immune)


#normal_flying = PokemonTypeSet(pokemon_types["Normal"], pokemon_types["Flying"])
#print('try: print(pokemon_types["Ground"])')
if __name__ == '__main__':
  import sys
  if len(sys.argv) == 3:
    print(PokemonType(PokemonBaseType[sys.argv[1]], PokemonBaseType[sys.argv[2]]))
  elif len(sys.argv) == 2:
    print(PokemonType(PokemonBaseType[sys.argv[1]]))
  else:
    print("usage: {} Type1 [Type2]".format(sys.argv[0]))
