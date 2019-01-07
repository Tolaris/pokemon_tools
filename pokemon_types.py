#!/usr/bin/env python3

class PokemonType:
  """A class representing a Pokemon type, such as 'Fire' or 'Water'."""

  def __init__(self, name, weak=None, strong=None, immune=None):
    self.name = name
    self.weak = weak or []
    self.strong = strong or []
    self.immune = immune or []

  def __str__(self):
    """Method for pretty-printing the class."""
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
    # for each strong/immune, take set union of both types
    # for weak:
    #   weak = set symmetric difference
    #   double_weak = set intersection
    # print method should print double_weaks first, each followed by " (2x)"
    if type(type1) is not PokemonType:
      raise TypeError('type1 must be of class PokemonType')
    if type(type2) is not PokemonType:
      raise TypeError('type1 must be of class PokemonType')

    self.type1 = type1
    if type2 is None:
      self.type2 = None
      self.name = type1.name
      self.weak = type1.weak
      self.strong = type1.strong
      self.immune = type1.immune
      self.double_weak = []
    else:
      self.type2 = type2
      self.name = "{} / {}".format(type1.name, type2.name)
      self.weak = 

    self.weak_count = len(self.weak) + len(self.double_weak)*2
    self.strong_count = len(self.strong) + len(self.immune)*2

  def __str__(self):
    """Method for pretty-printing the class."""
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




pokemon_types = {
  "Normal": PokemonType("Normal",
                        weak=["Fighting"],
                        immune=["Ghost"],
                        ),
  "Fire": PokemonType("Fire",
                      weak=["Water", "Ground", "Rock"],
                      strong=["Fire", "Grass", "Ice", "Bug", "Steel", "Fairy"],
                      ),
  "Water": PokemonType("Water",
                       weak=["Electric", "Grass"],
                       strong=["Fire", "Water", "Ice", "Steel"],
                       ),
  "Electric": PokemonType("Electric",
                          weak=["Ground"],
                          strong=["Electric", "Flying", "Steel"],
                          ),
  "Grass": PokemonType("Grass",
                       weak=["Fire", "Ice", "Poison", "Flying", "Bug"],
                       strong=["Water", "Electric", "Grass", "Ground"],
                       ),
  "Ice": PokemonType("Ice",
                     weak=["Fire", "Fighting", "Rock", "Steel"],
                     strong=["Ice"],
                     ),
  "Fighting": PokemonType("Fighting",
                          weak=["Flying", "Psychic", "Fairy"],
                          strong=["Bug", "Rock", "Dark"],
                          ),
  "Poison": PokemonType("Poison",
                        weak=["Ground", "Psychic"],
                        strong=["Grass", "Fighting", "Poison", "Bug", "Fairy"],
                        ),
  "Ground": PokemonType("Ground",
                        weak=["Water", "Grass", "Ice"],
                        strong=["Poison", "Rock"],
                        immune=["Electric"],
                        ),
  "Flying": PokemonType("Flying",
                        weak=["Electric", "Ice", "Rock"],
                        strong=["Grass", "Fighting", "Bug"],
                        immune=["Ground"],
                        ),
  "Psychic": PokemonType("Psychic",
                         weak=["Bug", "Ghost", "Dark"],
                         strong=["Fighting", "Psychic"],
                         ),
  "Bug": PokemonType("Bug",
                     weak=["Fire", "Flying", "Rock"],
                     strong=["Grass", "Fighting", "Ground"],
                     ),
  "Rock": PokemonType("Rock",
                      weak=["Water", "Grass", "Fighting", "Ground", "Steel"],
                      strong=["Normal", "Fire", "Poison", "Flying"],
                      ),
  "Ghost": PokemonType("Ghost",
                       weak=["Ghost", "Dark"],
                       strong=["Poison", "Bug"],
                       immune=["Normal", "Fighting"],
                       ),
  "Dragon": PokemonType("Dragon",
                        weak=["Ice", "Dragon", "Fairy"],
                        strong=["Fire", "Water", "Electric", "Grass"],
                        ),
  "Dark": PokemonType("Dark",
                      weak=["Fighting", "Bug", "Fairy"],
                      strong=["Ghost", "Dark"],
                      ),
  "Steel": PokemonType("Steel",
                       weak=["Fire", "Fighting", "Ground"],
                       strong=["Normal", "Grass", "Ice", "Flying", "Psychic", "Bug", "Rock", "Dragon", "Steel", "Fairy"],
                       immune=["Poison"],
                       ),
  "Fairy": PokemonType("Fairy",
                       weak=["Poison", "Steel"],
                       strong=["Fighting", "Bug", "Dark"],
                       immune=["Dragon"],
                       )
}

normal_flying = PokemonTypeSet(pokemon_types["Normal"], pokemon_types["Flying"])

print('try: print(pokemon_types["Ground"])')
