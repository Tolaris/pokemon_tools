#!/usr/bin/env python3

from enum import Enum

class PokemonType(Enum):
  """An Enum subclass representing a Pokemon type, such as 'Fire' or 'Water'."""
  # Values for each Enum are (SortOrder, weak, strong, immune)
  Normal = (1, ["Fighting"], [], ["Ghost"])
  Fire = (2, ["Water", "Ground", "Rock"], ["Fire", "Grass", "Ice", "Bug", "Steel", "Fairy"], [])

  Water = (3, ["Electric", "Grass"], ["Fire", "Water", "Ice", "Steel"], [])
  Electric = (4, ["Ground"], ["Electric", "Flying", "Steel"], [])
  Grass = (5, ["Fire", "Ice", "Poison", "Flying", "Bug"], ["Water", "Electric", "Grass", "Ground"], [])
  Ice = (6, ["Fire", "Fighting", "Rock", "Steel"], ["Ice"], [])
  Fighting = (7, ["Flying", "Psychic", "Fairy"], ["Bug", "Rock", "Dark"], [])
  Poison = (8, ["Ground", "Psychic"], ["Grass", "Fighting", "Poison", "Bug", "Fairy"], [])
  Ground = (9, ["Water", "Grass", "Ice"], ["Poison", "Rock"], ["Electric"])
  Flying = (10, ["Electric", "Ice", "Rock"], ["Grass", "Fighting", "Bug"], ["Ground"])
  Psychic = (11, ["Bug", "Ghost", "Dark"], ["Fighting", "Psychic"], [])
  Bug = (12, ["Fire", "Flying", "Rock"], ["Grass", "Fighting", "Ground"], [])
  Rock = (13, ["Water", "Grass", "Fighting", "Ground", "Steel"], ["Normal", "Fire", "Poison", "Flying"], [])
  Ghost = (14, ["Ghost", "Dark"], ["Poison", "Bug"], ["Normal", "Fighting"])
  Dragon = (15, ["Ice", "Dragon", "Fairy"], ["Fire", "Water", "Electric", "Grass"], [])
  Dark = (16, ["Fighting", "Bug", "Fairy"], ["Ghost", "Dark"], [])
  Steel = (17, ["Fire", "Fighting", "Ground"], ["Normal", "Grass", "Ice", "Flying", "Psychic", "Bug", "Rock", "Dragon", "Steel", "Fairy"], ["Poison"])
  Fairy = (18, ["Poison", "Steel"], ["Fighting", "Bug", "Dark"], ["Dragon"])

  # See "OrderedEnum" example in Python 3 Enum docs (8.13.13.2).
  # This allows ordered comparison of types, so we can use sorted().
  def __ge__(self, other):
    if self.__class__ is other.__class__:
      return self.value[0] >= other.value[0]
    return NotImplemented
  def __gt__(self, other):
    if self.__class__ is other.__class__:
      return self.value[0] > other.value[0]
    return NotImplemented
  def __le__(self, other):
    if self.__class__ is other.__class__:
      return self.value[0] <= other.value[0]
    return NotImplemented
  def __lt__(self, other):
    if self.__class__ is other.__class__:
      return self.value[0] < other.value[0]
    return NotImplemented

  def __str__(self):
    return self.name

  def __init__(self, *args):
    self.weak = self.value[1]
    self.strong = self.value[2]
    self.immune = self.value[3]

  def summary(self):
    """Pretty-print a summary of a PokemonType."""
    name = "Type: {}\n".format(self.name)
    if self.weak:
      weak = "  Weak to:   {}\n".format(", ".join(self.weak))
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
      weaknesses = [i + " (2x)" for i in self.weak_double] + self.weak
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
