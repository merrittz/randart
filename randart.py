#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  randart.py
#  
#  Copyright 2018 Zachary Merritt <zfmerritt@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
"""
This is a Rogue-like item generator for Pathfinder, which was inspired primarily by playing too much Dungeon Crawl Stone Soup.
These items are meant to be rolled up when a rare item or (potentially) valuable loot is called for. This script makes use of
exponential probability distributions which are determined by book prices for items. All named items are taken from Ultimate Equipment.

There is a fixed 5% chance that any item will be a cursed item instead.
"""
import random, math

def discrete_exp_fix_N(N, alpha):
	"""This function sets a discrete exponential distribution such that the possible outcomes are 0,1,2, ... , N with
	N having a probability of alpha."""
	
	lamb = -1.0 * (math.log(float(alpha)) / float(N))
	i = int(math.floor(random.expovariate(lamb)))
	if i > N:
		i = N
	return i
	
def d100():
	return random.choice(range(1,101))

def discrete_gauss(m, s):
	n = int(round(random.gauss(m, s)))
	if n > 6:
		n = 6
	if n < -6:
		n = -6
	if n >= 0:
		return "+" + str(n)
	if n < 0:
		return str(n)

class randart:
	artifact_class = ""
	artifact_type = ""
	enchantment_bonus = 0
	brand = ""
	
	def roll_class(self):
		index = random.choice(range(0,len(list_of_items)))
		
		if index == 0:
			self.artifact_class = "Ring"
		elif index == 1:
			self.artifact_class = "Weapon"
		elif index == 2:
			self.artifact_class = "Armor"
		elif index == 3:
			self.artifact_class = "Wonderous"
		elif index == 4:
			self.artifact_class = "Shield"
		elif index == 5:
			self.artifact_class = "Staff"
		elif index == 6:
			self.artifact_class = "Rod"
		
		if d100() < 6:
			self.artifact_class = "Cursed!"
	
	def roll_randart(self):
		index = ["Ring", "Weapon", "Armor", "Wonderous", "Shield", "Staff", "Rod", "Cursed!"].index(self.artifact_class)
		
		if self.artifact_class == "Ring":
			i = discrete_exp_fix_N(len(list(rings.keys()))-1, 0.00125)
			key = sorted(list(rings.keys()))[i]
			if key == '0':
				self.artifact_type = str(random.choice(range(0,10))) + " " + random.choice(rings[key])
			else:
				self.artifact_type = random.choice(rings[key])
		
		if self.artifact_class == "Weapon":
			self.artifact_type = random.choice(list_of_items[index])
			self.enchantment_bonus = discrete_exp_fix_N(5, 0.04)
			self.brand = random.choice(brands[discrete_exp_fix_N(5, 0.04)])
		
		if self.artifact_class == "Armor":
			self.artifact_type = random.choice(list_of_items[index])
			self.enchantment_bonus = discrete_exp_fix_N(5, 0.04)
			self.brand = random.choice(armor_brands[discrete_exp_fix_N(5, 0.04)])
		
		if self.artifact_class == "Wonderous":
			i = discrete_exp_fix_N(len(list(wonders.keys()))-1, 0.00025)
			key = sorted(list(wonders.keys()))[i]
			if key == '0':
				self.artifact_type = str(random.choice(range(0,10))) + " " + random.choice(wonders[key])
			else:
				self.artifact_type = random.choice(wonders[key])
		
		if self.artifact_class == "Shield":
			self.artifact_type = random.choice(list_of_items[index])
			self.enchantment_bonus = discrete_exp_fix_N(5, 0.04)
			self.brand = random.choice(shield_brands[discrete_exp_fix_N(5, 0.04)])
		
		if self.artifact_class == "Staff":
			i = discrete_exp_fix_N(len(list(staves.keys()))-1, 0.0064)
			key = sorted(list(staves.keys()))[i]
			self.artifact_type = random.choice(staves[key])
		
		if self.artifact_class == "Rod":
			i = discrete_exp_fix_N(len(list(rods.keys()))-1, 0.0088)
			key = sorted(list(rods.keys()))[i]
			rod = random.choice(rods[key])
			if not "Rod" in rod and not "rod" in rod and key != '0':
				self.artifact_type = "Rod of " + rod
			else:
				self.artifact_type = rod
		
		if self.artifact_class == "Cursed!":
			self.artifact_type = random.choice(cursed_items)
		
		
		#apply additional bonuses to items. ~50% of items will have no additional bonuses.
		#roll for poison on weapons
		if self.artifact_class == "Weapon" and d100() < 6:
			i = discrete_exp_fix_N(len(list(poisons.keys())), 0.10)
			key = sorted(list(poisons.keys()))[i]
			if not self.brand == "":
				self.brand += ", "
			self.brand += 'Pois: ' + random.choice(poisons[key])
		#roll for energy resistances
		if d100() < 21:
			if self.artifact_class == "Shield" or self.artifact_class == "Armor" or self.artifact_class == "Weapon":
				energy_types = ["fire", "cold", "elec", "acid", "sonic"]
				for i in xrange(discrete_exp_fix_N(5, 0.01)):
					if not self.brand == "":
						self.brand += ", "
					energy = random.choice(energy_types)
					self.brand += "ER " + str(discrete_exp_fix_N(29, 0.05) + 1) + " (" + energy + ")"
					energy_types.remove(energy)
		#roll for spell resistance
		if d100() < 21:
			if self.artifact_class == "Shield" or self.artifact_class == "Armor" or self.artifact_class == "Weapon":
				if not self.brand == "" and not "SR" in self.brand:
					self.brand += ", "
				if not "SR" in self.brand:
					self.brand += "SR " + str(discrete_exp_fix_N(12, 0.01) + 13)
		#roll for damage reduction
		if d100() < 6:
			if self.artifact_class == "Shield" or self.artifact_class == "Armor" or self.artifact_class == "Weapon":
				if not self.brand == "":
					self.brand += ", "
				self.brand += "DR " + str(discrete_exp_fix_N(14, 0.05) + 1)
		#roll for stat bonuses/penalties
		if d100() < 21:
			if self.artifact_class == "Shield" or self.artifact_class == "Armor" or self.artifact_class == "Weapon":
				stat_types = ["Str", "Wis", "Int", "Dex", "Con", "Cha"]
				for i in xrange(discrete_exp_fix_N(6, 0.01)):
					stat = random.choice(stat_types)
					modifier = discrete_gauss(0.0, 2.0)
					if not modifier == "+0":
						if not self.brand == "":
							self.brand += ", "
						self.brand += modifier + " " + stat
					stat_types.remove(stat)
	
	def describe(self):
		if self.artifact_class == "Weapon" or self.artifact_class == "Armor" or self.artifact_class == "Shield":
			desc = "+%s %s {%s}" % (str(self.enchantment_bonus), self.artifact_type, self.brand)
			if '{}' in desc:
				return desc[:-3]
			else:
				return desc
		else:
			return "%s" % (self.artifact_type)
			 
def main():
	print """
	Welcome, stranger. This is a Rogue-like item generator for Pathfinder.
	What type of item would you like to create?
	
	[1] - Any type!
	[2] - Weapon
	[3] - Armor
	[4] - Shield
	[5] - Ring
	[6] - Wonderous Item
	[7] - Staff
	[8] - Rod
	[9] - Cursed Item
	
	[q] - I quit!
	
	"""
	classes = ["Weapon", "Armor", "Shield", "Ring", "Wonderous", "Staff", "Rod", "Cursed!"]
	while True:
		try:
			choice = raw_input(">")
			if choice == 'q':
				print "Ok, bye."
				break
			elif choice == "1":
				print "How many?"
				for j in xrange(0,int(raw_input(">"))):
					my_randart = randart()
					my_randart.roll_class()
					my_randart.roll_randart()
					print my_randart.describe()
			elif choice in "23456789":
				print "How many?"
				for j in xrange(0,int(raw_input(">"))):
					my_randart = randart()
					my_randart.artifact_class = classes[int(choice) - 2]
					my_randart.roll_randart()
					print my_randart.describe()
		except:
			print "Oops. Something went wrong :( Please make a selection from 1 to 9."

#Tables and dictionaries and such. This material is from the Ultimate Equipment guide.
rings = {'0': ["copper coins", "silver coins", "gold coins"], '8500': ['Ring of force shield'], '10000': ['Ring of climbing improved', 'Ring of curing', 'Ring of foe focus', 'Ring of jumping improved', 'Ring of ki mastery', 'Ring of revelation lesser', 'Ring of swimming improved'], '19500': ['Ring of energy shroud'], '66000': ['Ring of inner fortitude greater'], '8600': ['Ring of the ram'], '90000': ['Ring of regeneration'], '44000': ['Ring of energy resistance greater'], '28500': ['Ring of the ecclesiarch'], '3000': ['Ring of ferocious action'], '15000': ['Ring of retribution', 'Ring of water walking'], '13500': ['Ring of spell knowledge III'], '125000': ['Ring of djinni calling'], '250': ["Prisoner's Dungeon Ring"], '42000': ['Ring of inner fortitude major'], '2200': ['Ring of feather falling'], '24000': ['Ring of revelation superior', 'Ring of spell knowledge IV'], '45000': ['Ring of delayed doom'], '6000': ['Ring of sacred mistletoe', 'Ring of spell knowledge II', 'Ring of swarming stabs'], '4000': ['Ring of counterspells'], '18000': ['Ring of inner fortitude minor', 'Ring of protection +3', 'Ring of spell storing minor'], '16000': ["Dungeon ring jailer's", 'Ring of revelation greater'], '27000': ['Ring of blinking'], '40000': ['Ring of freedom of movement', 'Ring of wizardry II'], '1500': ['Ring of spell knowledge I'], '120000': ['Ring of three wishes'], '2500': ['Ring of climbing', 'Ring of jumping', 'Ring of sustenance', 'Ring of swimming'], '200000': ['Ring of elemental command', 'Ring of spell storing major'], '50000': ['Ring of friend shield', 'Ring of protection +5', 'Ring of shooting stars', 'Ring of spell storing'], '5000': ['Ring of maniacal devices', 'Ring of rat fangs'], '25000': ['Ring of evasion', 'Ring of x-ray vision'], '56000': ['Ring of continuation'], '14000': ['Ring of the sea strider'], '33600': ['Ring of return'], '12700': ['Ring of chameleon power'], '20000': ['Ring of arcane mastery', 'Ring of invisibility', 'Ring of wizardry I'], '6840': ['Ring of grit mastery'], '8000': ['Ring of forcefangs', 'Ring of mind shielding', 'Ring of protection +2', 'Ring of strength sapping'], '70000': ['Ring of wizardry III', 'Spiritualist Rings'], '11000': ['Ring of tactical precision', 'Ring of the sophisticate'], '32000': ['Ring of protection +4'], '75000': ['Ring of telekinesis'], '12000': ['Decoy ring', 'Ring of craft magic', 'Ring of ectoplasmic invigoration', 'Ring of energy resistance minor', 'Ring of the troglodyte', 'Steelhand circle'], '28000': ['Ring of energy resistance major'], '2000': ['Ring of protection +1', 'Ring of the grasping grave'], '8700': ["Scholar's ring"], '100000': ['Ring of spell turning', 'Ring of wizardry IV'], '10800': ['Ring of animal friendship', 'Ring of transposition'], '1000': ['Ring of arcane signets']}
wonders = {'0': ['peanut shells', 'pretty pebbles'],'15600': ['Bracers of the merciful knight', "Comfort's cloak"], '110000': ['Manual of bodily health +4', 'Manual of gainful exercise +4', 'Manual of quickness of action +4', 'Tome of clear thought +4', 'Tome of leadership and influence +4', 'Tome of understanding +4', 'Gauntlets of the weaponmaster', 'Eyes of the dragon', 'Shadowform belt'], '21000': ['Figurine of wondrous power (ivory goats)', 'Rope of entanglement', 'Shoes of the firewalker', 'Rainbow lenses', 'Belt of fallen heroes'], '66000': ['Monocle of the investigator'], '13400': ['Mantle of spores'], '28500': ['Figurine of wondrous power (obsidian steed)'], '6126': ['Book of extended summoning (greater)'], '17000': ['Broom of flying', 'Figurine of wondrous power (marble elephant)'], '6480': ['Crown of blasting minor', 'Haunted shoes'], '5500': ['Wind fan', 'Boots of striding and springing'], '50000': ['Crystal ball with see invisibility', 'Horn of Valhalla', 'Cloak of displacement major', 'Amulet of natural armor +5', 'Sniper goggles greater', 'Mantle of immortality'], '6000': ['Coin of the untrodden road', 'Horn of battle clarity', 'Life link badge', "Martyr's tear", 'Pipes of haunting', 'Rope of knots', 'Singing bell of striking', 'Stone familiar', 'Bonebreaker gauntlets', 'Vambraces of defense', 'Verdant vine', 'Cloak of the scuttling rat', 'Seafoam shawl', 'Treeform cloak', 'Amulet of bullet protection +2', 'Feychild necklace', 'Crown of swords', "Magnetist's gloves", 'Horseshoes of a zephyr', 'Eyes of keen sight', "Cackling hag's blouse", 'Deadshot vest', "Prophet's pectoral", 'Tunic of deadly might', 'Vest of the vengeful tracker', 'Eidolon anchoring harness', 'Belt of foraging'], '4900': ['Incense of meditation'], '40000': ['Cauldron of flying', 'Enmity fetish', 'Ioun stone (lavender and green ellipsoid)', 'Ring gates', "Juggernaut's pauldrons", 'Headband of mental prowess +4', 'Headband of seduction', 'Belt of physical might +4'], '76000': ['Mantle of faith'], '13000': ['Gem of brightness', 'Harp of contagion', 'Lyre of building', 'Forge fist amulet', "Monk's robe"], '2400': ['Sovereign glue', 'Boots of friendly terrain', 'Robe of bones'], '400': ['Alluring golden apple', 'Feather token (tree)', 'Key of lock jamming'], '147000': ['Bodywrap of mighty strikes +7'], '184800': ['Truesight goggles'], '95000': ["Mindmaster's eyes"], '180': ['Assisting gloves'], '39000': ["Shifter's headband +6"], '200000': ['Mirror of life trapping'], '6250': ['Gloves of swimming and climbing'], '1100': ['Elixir of fire breath', 'Grave salt'], '14350': ['Demonspike pauldrons'], '78600': ['Wyvern cloak'], '120000': ['Amulet of the planes', 'Robe of eyes'], '17500': ['Symbol of sanguine protection', "Shifter's headband +4"], '1150': ['Pipes of the sewers'], '44000': ['Golem manual (stone guardian)'], '3400': ['Bag of tricks (gray)'], '37500': ['Amulet of bullet protection +5'], '22000': ['Golem manual (stone)', 'Orb of golden heaven', 'Amulet of spell mastery', 'Circlet of mindsight', 'Mask of the skull', 'Corset of dire witchcraft'], '15500': ['Figurine of wondrous power (onyx dog)'], '15750': ['Bracelet of second chances'], '18000': ['Ioun stone (iridescent spindle)', 'Orb of foul Abaddon', 'Stole of justice', 'Amulet of natural armor +3', "Cat's eye crown", 'Maw of the wyrm', 'Mitre of the hierophant', 'Vampiric gloves', 'Monkey belt greater'], '46000': ['Burglar boots major'], '7250': ['Bottle of air'], '14500': ['Bracelet of bargaining'], '9900': ["Seducer's bane"], '4400': ['Wind-caller compass', 'Slippers of cloudwalking'], '50': ['Feather token (anchor)', 'Universal solvent'], '8700': ['Necklace of fireballs (type VII)'], '5850': ['Necklace of fireballs (type V)'], '26000': ['Iron bands of binding', 'Cloak of the bat', 'Batrachian helm', 'Spectral shroud'], '82500': ['Manual of bodily health +3', 'Manual of gainful exercise +3', 'Manual of quickness of action +3', 'Tome of clear thought +3', 'Tome of leadership and influence +3', 'Tome of understanding +3'], '33000': ['Cauldron of resurrection'], '10800': ['Cape of the mountebank', 'Pauldrons of the watchful lion'], '2250': ['Elemental gem', 'Flying ointment'], '200': ['Feather token (fan)', 'Formula alembic', 'Hybridization funnel', 'Soul soap', 'Sleeves of many garments', 'Catching cape', 'Bandages of rapid recovery'], '19200': ['Jellyfish cape'], '52000': ['Last leaves of the autumn dryad'], '11200': ['Plague rat belt greater'], '5600': ['Headband of unshakeable resolve'], '2600': ['Cloak of fiery vanishing', "Pirate's eye patch", 'Aquatic cummerbund'], '2800': ['Cloak of fangs'], '3300': ['Shroud of disintegration'], '4800': ['Slippers of spider climbing'], '12500': ['Blessed book', 'Waters of transfiguration', 'Security belt'], '70000': ['Crystal ball with telepathy', 'Horn of blasting (greater)', 'Pearl of Power (two spells)', "Sea tyrant's patch"], '58000': ["Poisoner's jacket greater", 'Robe of stars'], '8800': ['Goggles of brilliant light'], '45800': ['Strand of prayer beads (standard)'], '1650': ['Necklace of fireballs (type I)'], '1400': ['Elixir of dragon breath', 'Daredevil boots'], '5000': ['Admixture vial', 'Bag of holding (type II)', 'Bone razor', 'Horn of the huntmaster', 'Insistent doorknocker', 'Ioun stone (dusty rose prism)', 'Mallet of building', 'Polymorphic pouch', 'Scabbard of stanching', 'School of eyes', 'Sheath of bladestealth', 'Stone of alliance', 'Summoning shackle', 'Bracers of archery lesser', 'Spellguard bracers', 'Amulet of mighty fists +1', "Grappler's mask", 'Helm of fearsome mien', 'Jingasa of the fortunate soldier', 'Gloves of arcane striking', "Poisoner's gloves", 'Sandals of the lightest step', 'Sipping jacket', 'Tunic of careful casting', 'Mnemonic vestments', 'Robe of components', "Sorcerer's robe", 'Blinkback belt'], '13900': ["Arrowmaster's bracers"], '2750': ['Book of extended summoning (standard)'], '34500': ['Gauntlet of rust greater'], '300': ['Bottle of messages', 'Feather token (bird)', 'Origami swarm'], '60000': ['Carpet of flying (10 ft. by 10 ft.)', 'Darkskull', 'Orb of pure law', 'Merciful baldric', 'Belt of stoneskin'], '9000': ['Boro bead (3rd)', 'Decanter of endless water', 'Loathsome mirror', 'Page of spell knowledge (3rd)', 'Pearl of Power (3rd)', 'Preserving flask (3rd)', 'Bracers of armor +3', 'Cloak of resistance +3', 'Amulet of hidden strength', 'Necklace of adaptation', "Serpent's band", 'Veil of fleeting glances', 'Glyphbane gloves', 'Nightmare horseshoes', 'Serpent belt'], '7900': ['Bracers of the glib entertainer'], '48000': ['Orb of storms', 'Bodywrap of mighty strikes +4', "Smuggler's collapsible robe"], '100': ['Stubborn nail', 'War paint of the terrible visage'], '4350': ['Necklace of fireballs (type III)'], '900': ['Cloak of human guise', 'Hand of the mage', 'Cap of light'], '27500': ['Manual of bodily health +1', 'Manual of gainful exercise +1', 'Manual of quickness of action +1', 'Tome of clear thought +1', 'Tome of leadership and influence +1', 'Tome of understanding +1', 'Headband of knucklebones'], '7700': ["Headband of fortune's favor"], '5400': ['Eversmoking bottle', 'Sustaining spoon', 'Necklace of fireballs (type IV)', 'Stormlure', 'Headband of ki focus'], '3500': ['Dust of disappearance', 'Stonemist cloak', 'Mind sentinel medallion', "Mummer's ruff", "Stalker's mask", 'Boots of the mire', 'Lenses of detection'], '6500': ['Horn of goodness/evil'], '170000': ['Iron flask'], '12000': ['Black soul shard', 'Golem manual (clay)', "Horsemaster's saddle", 'Pipes of dissolution', 'Pipes of pain', "Seeker's sight", 'Lion cloak', 'Crystal of healing hands', 'Guardian gorget', 'Medallion of thoughts', 'Periapt of protection from curses', 'Veiled eye', 'Cap of the free thinker', 'Boots of speed', 'Verdant boots', "Blind man's fold", 'Goggles of night', 'Lenses of figment piercing', "Poisoner's jacket lesser", 'Bodywrap of mighty strikes +2', 'Belt of equilibrium'], '28000': ['Dimensional shackles'], '100000': ["Lord's banner (crusades)", 'Horseshoes of crushing blows +5'], '72000': ['Wings of the gargoyle'], '55000': ['Instant fortress', 'Manual of bodily health +2', 'Manual of gainful exercise +2', 'Manual of quickness of action +2', 'Tome of clear thought +2', 'Tome of leadership and influence +2', 'Tome of understanding +2', 'Cloak of etherealness'], '18900': ['Vambraces of the genie (djinni)', 'Vambraces of the genie (marid)', 'Vambraces of the genie (shaitan)'], '1000': ['Anatomy doll', 'Bead of newt prevention', 'Beast-bond brand', 'Bookplate of recall', 'Boro bead (1st)', 'Concealing pocket', 'Dowsing syrup', 'Incense of transcendence', 'Page of spell knowledge (1st)', 'Pearl of Power (1st)', 'Preserving flask (1st)', 'Pyxes of redirected focus', 'Salve of slipperiness', 'Wasp nest of swarming', 'Bracers of armor +1', "Burglar's bracers", 'Cloak of resistance +1', 'Muleback cords', 'Shawl of life-keeping', 'Shield cloak', 'Phylactery of faithfulness', 'Boots of the cat', "Quick runner's shirt", 'Robe of infinite twine', 'Robe of needles', 'Beneficial bandolier', 'Meridian belt'], '8500': ['Bag of tricks (rust)', 'Helm of the mammoth lord', 'Nightmare boots', 'Goggles of elvenkind'], '39600': ['Horseshoes of glory'], '450': ['Feather token (swan boat)'], '3750': ["Druid's vestment"], '73500': ['Helm of teleportation'], '17200': ["Prestidigitator's cloak"], '90000': ['Apparatus of the crab', 'Bowl of conjuring water elementals', 'Brazier of conjuring fire elementals', 'Censer of conjuring air elementals', 'Stone of conjuring earth elementals', 'Headband of metal prowess +6', 'Mask of giants greater', 'Mantle of spell resistance', 'Belt of physical might +6'], '3800': ['Figurine of wondrous power (silver raven)', 'Volatile vaporizer (3rd)'], '1300': ['Claws of the ice bear'], '164000': ['Cubic gate'], '6600': ['Naga-scale bindi'], '3000': ['Bead of force', 'Cauldron of brewing', 'Chime of opening', 'Philter of love', 'Rope of climbing', 'Volatile vaporizer (2nd)', 'Pauldrons of the serpent', 'Swarmbane clasp', "Miser's mask", "Engineer's workgloves", 'Acrobat slippers', 'Horseshoes of speed', 'Spectacles of understanding', 'Vest of surgery', 'Bodywrap of mighty strikes +1', 'Corset of the vishkanya'], '145000': ['Efreeti bottle'], '15000': ['Book of the loremaster', 'Cauldron of plenty', 'Horn of judgment', 'Horn of the tritons', 'Bracelet of mercy', 'Periapt of wound closure', 'Headband of ninjitsu', 'Gloves of dueling', 'Arachnid goggles', 'Cord of stubborn resolve'], '250': ['Dust of tracelessness', 'Elixir of hiding', 'Elixir of swimming', 'Elixir of tumbling', 'Elixir of vision', 'Nightdrops', 'Oil of silence', 'Silversheen', "Traveler's any-tool"], '2200': ["Knight's pennon (honor)", 'Volatile vaporizer (1st)', "Apprentice's cheating gloves", "Challenger's gloves"], '67000': ['Talons of Leng', 'Otherworldly kimono'], '24000': ['Drinking horn of bottomless valor', 'Cloak of displacement minor', 'Amulet of bullet protection +4', 'Helm of underwater action', 'Dryad sandals', 'Elemental earth belt'], '850': ['Dust of dryness'], '59200': ["Judge's wig"], '32000': ['Amulet of natural armor +4', 'Winter wolf headband', 'Merform belt'], '16800': ['Chime of interruption', 'Brooch of amber sparks'], '5700': ['Hollywreath band'], '1500': ['Bookmark of deception', 'Word bottle', 'Quickchange cloak', 'Aegis of recovery', 'Amulet of bullet protection +1', 'Brooch of shielding', 'Boots of the enduring march', 'Endless bandolier'], '27000': ['Cube of frost resistance', 'Hand of stone', 'Periapt of proof against poison', 'Helm of telepathy', 'Plague mask', 'Gloves of the shortened path', 'Horseshoes of the mist', 'Bodywrap of mighty strikes +3', 'Robe of scintillating colors'], '18500': ["Anaconda's coils"], '16000': ['Bag of tricks (tan)', 'Boro bead (4th)', 'Page of spell knowledge (4th)', 'Pearl of Power (4th)', 'Preserving flask (4th)', 'Scabbard of keen edges', 'Bracers of armor +4', 'Cloak of resistance +4', 'Shawl of the crone', 'Necklace of ki serenity', 'Headband of alluring charisma +4', 'Headband of inspired wisdom +4', 'Headband of mental superiority +2', 'Headband of vast intelligence +4', 'Halo of inner calm', 'Horseshoes of crushing blows +2', 'Winged boots', 'Vest of the cockroach', 'Robe of arcane heritage', 'Belt of giant strength +4', 'Belt of physical perfection +2', 'Belt of incredible dexterity +4', 'Belt of mighty constitution +4'], '9400': ['Monkey belt'], '500': ['Animated portrait', 'Bottled misfortune', 'Elixir of truth', 'Feather token (whip)', 'Scabbard of honing', 'Armbands of the brawler', 'Mask of stony demeanor'], '3600': ['Dust of weighty burdens', "Noble's vigilant pillbox", "Dead man's headband"], '125000': ['Amulet of mighty fists +5', 'Helm of brilliance', 'Helm of electric radiance'], '8100': ['Deck of illusions', 'Necklace of fireballs (type VI)'], '30000': ['Cauldron of the dead', 'Drums of panic', 'Ioun stone (orange prism)', 'Ioun stone (pale green prism)', 'Lantern of revealing', 'Racing broom of flying', 'Gauntlets of skill at arms', 'Soulbound eye', 'Iron circlet of guarded souls', 'Laurel of command', 'Mask of giants lesser', 'Gloves of the commanding conjurer', 'Getaway boots', 'Eyes of eyebite'], '25305': ['Maul of the titans'], '33600': ['Steel-mind cap'], '6800': ["Inquisitor's monocle"], '1200': ['Dust of illusion', 'Goblin skull bomb'], '11000': ["Hunter's band", 'Phylactery of negative channeling', 'Phylactery of positive channeling', 'Blazing robes', 'Shocking robe', 'Voidfrost robes', 'Minotaur belt'], '20000': ['Carpet of flying (5 ft. by 5 ft.)', 'Horn of antagonism', 'Horn of blasting', 'Ioun stone (pale lavender ellipsoid)', 'Ioun stone (pearly white spindle)', "Master's perfect golden bell", "Necromancer's athame", 'Portable hole', 'Stone of good luck', 'Cloak of the diplomat', 'Slashing cloak', 'Stone cloak major', 'Ampoule of false blood', 'Amulet of magecraft', 'Amulet of mighty fists +2', 'Dragonfoe amulet', 'Headband of arcane energy', 'Headband of counterspelling', "Magician's hat", 'Giant fist gauntlets', 'Darklands goggles', 'Sniper goggles', 'Vest of stable mutation', 'Xorn robe', 'Serpent belt greater'], '7000': ['Bottle of shadows', 'Cape of bravado', 'Instant bridge', 'Mirror of guarding reflections', 'Eagle cape', 'Phylactery of the shepherd', 'Headband of intuition', 'Resplendent uniform coat', 'Robe of useful items'], '5100': ['Headband of ponderous recollection'], '22600': ['Howling helm'], '54000': ['Wings of flying'], '92000': ['Mirror of opposition'], '4600': ['Cassock of the clergy'], '3280': ['Shackles of compliance'], '6400': ['Dragonbone divination sticks', 'Headband of deathless devotion', "Treasure hunter's goggles"], '3200': ['Equestrian belt'], '24600': ['Crown of conquest'], '38000': ['Scarab of protection'], '42000': ['Cauldron of seeing', 'Crystal ball', 'Necklace of netted stars', 'Headband of aerial agility +4', 'Belt of mighty hurling greater'], '23000': ['Gorgon belt'], '720': ['Campfire bead'], '108000': ['Bodywrap of mighty strikes +6'], '7400': ['Bag of holding (type III)'], '150000': ['Crown of heaven'], '150': ['Elixir of love', 'Unguent of timelessness'], '82000': ['Well of many worlds'], '10000': ['Bag of holding (type IV)', 'Boundary chalk', 'Chime of resounding silence', 'Construct channel brick', 'Doomharp', 'Drum of advance and retreat', 'Embalming thread', 'Eye of the void', 'Figurine of wondrous power (bronze griffon)', 'Figurine of wondrous power (ebony fly)', 'Figurine of wondrous power (slate spider)', 'Hourglass of last chances', 'Ioun stone (dark blue rhomboid)', 'Ki mat', "Lord's banner (swiftness)", 'Malleable symbol', 'Migrus locker', 'Ornament of healing light', 'Prayer wheel of ethical strength', 'Stone horse (courser)', 'Summon-slave crystal', "Treasurer's seal", 'Cloak of the duskwalker', 'Cocoon cloak', 'Pauldrons of the bull', 'Stone cloak minor', 'Amulet of spell cunning', 'Collar of the true companion', 'Frost fist amulet', 'Headband of mental prowess +2', 'Mask of a thousand tomes', 'Medusa mask', 'Glove of storing', 'Gloves of shaping', 'Pliant gloves', 'Caltrop boots', 'Tremor boots', 'Bane baldric', 'Unfettered shirt', 'Belt of physical might +2', 'Belt of the weasel', 'Belt of thunderous charging'], '600': ['Abjurant salt', 'Arrow magnet', 'Dust of darkness'], '45000': ['Drums of haste', "Charlatan's cape", 'Amulet of mighty fists +3'], '64000': ['Page of spell knowledge (8th)', 'Pearl of Power (8th)', 'Bracers of armor +8', 'Headband of mental resilience', 'Headband of mental superiority +4', 'Horseshoes of crushing blows +4', 'Robe of gates', 'Belt of physical perfection +4'], '550': ["Seer's tea"], '9100': ['Figurine of wondrous power (serpentine owl)'], '16500': ['Figurine of wondrous power (golden lions)'], '13500': ['Amulet of bullet protection +3'], '750': ["Archon's torch", 'Book of extended summoning (lesser)', 'Iron rope', 'Snapleaf'], '8400': ['Candle of invocation', 'Robe of blending'], '23348': ['Mattock of the titans'], '36000': ['Boro bead (6th)', 'Ioun stone (vibrant purple prism)', 'Orb of utter chaos', 'Page of spell knowledge (6th)', 'Pearl of Power (6th)', 'Preserving flask (6th)', 'Bracers of armor +6', 'Headband of alluring charisma +6', 'Headband of inspired wisdom +6', 'Headband of vast intelligence +6', 'Helm of brilliance lesser', 'Horseshoes of crushing blows +3', "Gunman's duster", 'Belt of giant strength +6', 'Belt of incredible dexterity +6', 'Belt of mighty constitution +6'], '62000': ['Cube of force'], '4000': ['Boro bead (2nd)', 'Cautionary creance', 'Escape ladder', 'Far-reaching sight', 'Ioun stone (clear spindle)', 'Marvelous pigments', 'Page of spell knowledge (2nd)', 'Pearl of Power (2nd)', 'Preserving flask (2nd)', 'Restorative ointment', 'Stone salve', 'Bracers of armor +2', "Bracers of falcon's aim", "Inquisitor's bastion vambraces", 'Cloak of resistance +2', 'Amulet of elemental strife', 'Righteous fist amulet', 'Headband of alluring charisma +2', 'Headband of inspired wisdom +2', 'Headband of vast intelligence +2', 'Gauntlets of the skilled maneuver', 'Ghostvision gloves', 'Gloves of arrow snaring', "Trapspringer's gloves", 'Burglar boots minor', 'Horseshoes of crushing blows +1', 'Sandals of quick reaction', 'Eyes of the owl', 'Sash of the war champion', 'Belt of giant strength +2', 'Belt of incredible dexterity +2', 'Belt of mighty constitution +2', 'Belt of teeth'], 'Price': ['Greater Major Slotless Item'], '7200': ['Folding boat', 'Longarm bracers', 'Cloak of the manta ray', 'Carcanet of detention', 'Mask of the krenshar', 'Jaunt boots'], '15300': ['Pearl of the sirines'], '49000': ['Page of spell knowledge (7th)', 'Pearl of Power (7th)', 'Bracers of armor +7', 'Boots of teleportation'], '51000': ['Crystal ball with detect thoughts'], '14800': ['Stone horse (destrier)'], '32500': ["Highwayman's cape"], '175000': ['Mirror of mental prowess'], '95800': ['Strand of prayer beads (greater)'], '5800': ['Grim lantern'], '80000': ['Crystal ball with true seeing', 'Amulet of mighty fists +4', "Swordmaster's blindfold"], '2500': ['Apple of eternal sleep', 'Bag of holding (type I)', 'Candle of truth', 'Hexing doll', 'Cloak of elvenkind', 'Cloak of the hedge wizard', 'Golembane scarab', 'Gloves of larceny', "Healer's gloves", 'Boots of the winterlands', 'Boots of elvenkind', 'Eyes of the eagle', 'Goggles of minute seeing'], '16200': ['Shackles of durance vile'], '9600': ['Strand of prayer beads (lesser)'], '81000': ['Page of spell knowledge (9th)', 'Pearl of Power (9th)', 'Headband of aerial agility +6'], '25000': ['Boro bead (5th)', 'Chaos emerald', 'Page of spell knowledge (5th)', 'Pearl of Power (5th)', 'Preserving flask (5th)', 'Bracers of archery greater', 'Bracers of armor +5', 'Bracers of sworn vengeance', 'Cloak of resistance +5', 'Annihilation spectacles', 'Eyes of doom', 'Sash of flowing water'], '56000': ["Lord's banner (terror)", 'Slippers of the triton', 'Eyes of charming'], '14000': ['Void pennant', 'Cape of effulgent escape', 'Cloak of arachnida', "Gunfighter's poncho", 'Tentacle cloak', 'Band of the stalwart warrior', 'Belt of mighty hurling lesser'], '14900': ['Belt of dwarvenkind'], '144000': ['Headband of mental superiority +6', 'Belt of physical perfection +6'], '2700': ['Stone of alarm', 'Necklace of fireballs (type II)'], '5200': ['Helm of comprehend languages and read magic', 'Vest of escape', 'Plague rat belt'], '75': ['Ioun torch'], '4500': ['Goblin fire drum (greater)', "Knight's pennon (battle)", "Knight's pennon (parley)", 'Void dust', 'Headband of aerial agility +2', "Shifter's headband +2", 'Circlet of persuasion'], '137500': ['Manual of bodily health +5', 'Manual of gainful exercise +5', 'Manual of quickness of action +5', 'Tome of clear thought +5', 'Tome of leadership and influence +5', 'Tome of understanding +5'], '10500': ['Boots of the mastodon', 'Shoes of the lightning leaping'], '23760': ['Crown of blasting major'], '8000': ['Chalice of poison weeping', "Exorcist's aspergillum", 'Golem manual (flesh)', 'Harp of shattering', 'Insignia of valor', 'Ioun stone (deep red sphere)', 'Ioun stone (incandescent blue sphere)', 'Ioun stone (pale blue rhomboid)', 'Ioun stone (pink and green sphere)', 'Ioun stone (pink rhomboid)', 'Ioun stone (scarlet and blue sphere)', 'Needles of fleshgraving', 'Restless lockpicks', 'Werewhistle', 'Charm bracelet', "Duelist's vambraces", 'Merciful vambraces', 'Vambraces of the tactician', 'Amulet of natural armor +2', 'Amulet of proof against petrification', 'Everwake amulet', 'Gravewatch pendant', 'Hand of glory', 'Torc of lionheart fury', 'Headband of havoc', 'Deliquescent gloves', 'Form-fixing gauntlets', 'Iron cobra gauntlet', "Shadow falconer's glove", 'Spellstrike gloves', 'Boots of escape', 'Earth root boots', 'Shirt of immolation', 'Snakeskin tunic'], '84000': ['Halo of menace'], '19000': ['Bracelet of friends'], '75000': ['Gem of seeing', "Lord's banner (victory)", 'Bodywrap of mighty strikes +5', 'Resplendent robe of the thespian', 'Robe of the archmagi'], '1800': ['Dust of appearance', 'Efficient quiver', 'Pipes of sounding', 'Scabbard of vigor', 'Cowardly crouching cloak', 'Hat of disguise', 'All tools vest'], '1600': ['Dust of acid consumption'], '14400': ['Vambraces of the genie (efreeti)'], '11500': ['Bracers of the avenging knight', 'Gauntlet of rust'], '35000': ['Carpet of flying (5 ft. by 10 ft.)', 'Golem manual (iron)', 'Amulet of proof against detection and location', "Stormlord's helm"], '2000': ['Agile alpenstock', 'Blood reservoir of physical prowess', 'Clamor box', 'Dry load powder horn', 'Goblin fire drum (normal)', 'Handy haversack', 'Horn of fog', 'Iron spike of safe passage', 'Bracers of steadiness', 'Manacles of cooperation', 'Amulet of natural armor +1', 'Buffering cap', 'Gloves of reconnaissance', 'Glowing glove', 'Feather step slippers', 'Deathwatch eyes', 'Bladed belt', 'Heavyload belt'], '7500': ['Balm of impish grace', 'Candle of clean air', 'Harp of charming', 'Manual of war', "Hunter's cloak", 'Periapt of health', 'Boots of levitation', 'Kinsight goggles'], '800': ['Bottled yeti fur', 'Defoliant polish', 'Dust of emulation', 'Steadfast gut-stone', 'Cap of human guise', 'Belt of tumbling']}

brands = [[""],
["Frost", "Flaming", "Bane","Thundering", "Impervious", "Glamered", "Shock", "Spell Storing", "Corrosive", "Lucky", "Defending", "Gray Flame", "Ghost Touch", "Mimetic", "Limning", "Merciful", "Mightly Cleaving", "Ominous", "Throwing", "Vicious", "Called", "Dispelling"],
["Anarchic", "Advancing", "Axiomatic", "Anchoring", "Corrosive Burst", "Dispelling Burst", "Disruption", "Flaming Burst", "Holy", "Icy Burst", "Shocking Burst", "Unholy", "Wounding", "Furyborn", "Invigorating", "Negating", "Lifesurge"],
["Nullifying", "Speed", "Spell Stealing", "Repositioning"],
["Brilliant Energy", "Dancing", "Dueling"],
["Vorpal", "Transformative"]]

armor_brands = [[""],
["Benevolent", "Poison Resistant", "Balanced", "Bitter", "Bolstering", "Brawling", "Champion", "Dastard", "Deathless", "Defiant", "Fortification", "Grinding", "Impervious", "Mirrored", "Spell Storing", "Stanching", "Warding"],
["Glamered", "Jousting", "Shadow", "Slick", "Expeditious", "Creeping", "Rallying", "SR 13"],
["Adhesive", "Hosteling", "Radiant", "Delving", "Putrid", "Fortification (moderate)", "Ghost Touch", "Invulnerability", "SR 15", "Titanic", "Wild"],
["Harmonizing", "Shadow, improved", "Slick, improved", "Martyring", "SR 17"],
["Righteous", "Unbound", "Unrighteous", "Vigilant", "Determination", "Greater Shadow", "Greater Slick", "Etherealness", "Undead Controlling", "Heavy Fortification", "SR 19"]]

shield_brands = [[""],
["Poison Resistant", "Arrow Catching", "Bashing", "Blinding", "Clangorous", "Defiant", "Light Fortification", "Grinding", "Impervious", "Mirrored", "Ramming"],
["Rallying", "Wyrmsbreath", "Animated", "Arrow Deflection", "Merging", "SR 13"],
["Hosteling", "Radiant", "Moderate Fortification", "Ghost Touch", "SR 15", "Wild"],
["SR 17"],
["Determination", "Improved Energy Resistance", "Undead Controlling", "Heavy Fortification", "Reflecting", "SR 19"]]

cursed_items = ['-2 cursed sword', 'Amulet of inescapable location', 'Armor of arrow attraction', 'Armor of rage', 'Arrowbreak bow', 'Bag of devouring', 'Belt of weakness', 'Berserking sword', 'Biting battleaxe', 'Boots of dancing', 'Bracers of defenselessness', 'Broom of animated attack', 'Cape of anchoring', 'Cursed backbiter spear', 'Crystal hypnosis ball', 'Deadly returns throwing axe', 'Drums of lethargy', 'Dust of sneezing and choking', 'Eyes blindness', 'Flask of curses', 'Gauntlets of fumbling', 'Headband of stupidity', 'Heavy hammer', 'Helm of opposite alignment', 'Incense of obsession', 'Mace of blood', 'Mask of ugliness', 'Medallion of thought projection', 'Nearfiring bow', 'Necklace of strangulation', 'Net of snaring', 'Ornery pistol', 'Pauldrons of the jackass', 'Periapt of foul rotting', 'Petrifying cloak', 'Poisonous cloak', 'Potion of poison', 'Ring of clumsiness', 'Ring of life bleed', 'Ring of spell devouring', 'Robe of powerlessness', 'Robe of vermin', 'Rod of foiled magic', 'Scarab of death', 'Scattershot bracers', 'Staff of occasional wonder', 'Stone of weight', 'Unguent of aging', 'Unlucky figurine', 'Unstable musket', 'Unwieldy glaive', 'Vacuous grimoire']

poisons = {'150': ['Medium spider venom'], '200': ['Large scorpion venom'], '210': ['Giant wasp poison'], '1800': ['Deathblade'], '700': ['Purple worm poison'], '120': ['Black adder venom', 'Blue whinnis'], '75': ['Drow poison'], '3000': ['Wyvern poison'], '90': ['Small centipede poison'], '100': ['Bloodroot', 'Greenblood oil'], '250': ['Shadow essence']}

staves = {'0': ['A large wooden stick', 'An exceptionally large twig'], '23200': ['Staff of radiance'], '48800': ['Staff of performance'], '82000': ['Staff of abjuration', 'Staff of conjuration', 'Staff of divination', 'Staff of enchantment', 'Staff of evocation', 'Staff of illusion', 'Staff of necromancy', 'Staff of transmutation'], '19200': ['Staff of courage'], '63960': ['Staff of the planes'], '41400': ['Staff of frost'], '180200': ['Staff of one hundred hands'], '56925': ['Staff of traps'], '47000': ['Staff of dark flame'], '41600': ['Staff of bolstering'], '18950': ['Staff of fire'], '62000': ['Staff of defense'], '26150': ['Staff of size alteration'], '32000': ["Heretic's bane", 'Musical staff'], '7200': ['Staff of blessed relief'], '31900': ['Staff of electricity'], '14800': ['Staff of accompaniment'], '58000': ['Staff of mithral might'], '16000': ['Staff of understanding'], '8800': ['Staff of tricks'], '81766': ['Staff of slumber'], '81000': ['Dragon staff'], '51600': ['Staff of obstacles'], '34200': ['Staff of toxins'], '28600': ['Staff of acid'], '27200': ['Staff of Journeys'], '43500': ['Staff of curses'], '57200': ['Staff of many rays'], '9600': ['Staff of the scout'], '109400': ['Staff of life'], '54400': ['Staff of travel'], '30000': ['Staff of the master'], '28800': ['Staff of shrieking'], '54000': ['Staff of heaven and earth'], '100400': ['Staff of the woodlands'], '69300': ['Staff of hungry shadows'], '220000': ['Staff of the hierophant'], '85800': ['Staff of earth and stone'], '17600': ['Staff of charming'], '22800': ['Staff of swarming insects'], '51500': ['Staff of illumination'], '47200': ['Staff of cackling wrath'], '20000': ['Staff of belittling'], '8000': ['Staff of minor arcana'], '55866': ['Staff of hoarding'], '39600': ['Staff of speaking'], '32800': ['Staff of souls'], '86666': ['Staff of vision'], '36800': ['Staff of stealth'], '235000': ['Staff of power'], '49800': ['Animate staff'], '51008': ['Staff of revelations'], '14400': ['Staff of eidolons'], '206900': ['Staff of passage'], '23000': ['Staff of authority'], '30200': ['Staff of spiders'], '29600': ['Chaotic staff', 'Holy staff', 'Lawful staff', 'Staff of healing', 'Unholy staff'], '37600': ['Staff of aspects'], '37310': ['Staff of the avenger'], '84066': ['Staff of weather'], '20800': ['Staff of feast and famine', 'Staff of rigor']}

rods = {'0': ['An oak paintbrush', 'A twig', 'Some sort of long bone'], '8500': ['Rod of ice'], '9000': ['Metamagic (+2 spell level) minor'], '3000': ['Metamagic (+1 spell level) minor'], '15000': ['Rod of balance', 'Rod of escape', 'Rod of flame extinguishing'], '13500': ["Trap-stealer's rod"], '64305': ['Rod of shadows'], '5500': ['Metamagic merciful normal'], '50000': ['Rod of absorption', 'Rod of flailing'], '67000': ['Rod of mind mastery'], '33000': ['Rod of thunder and lightning'], '12250': ['Metamagic merciful greater'], '54000': ['Metamagic (+3 spell level) normal'], '1500': ['Metamagic merciful minor'], '37000': ['Rod of negation'], '74000': ['Scepter of heaven'], '32500': ['Metamagic (+2 spell level) normal'], '16000': ['Rod of ruin'], '13000': ['Rod of the python'], '22305': ['Fiery nimbus rod'], '80000': ['Rod of dwarven might'], '75500': ['Metamagic quicken normal'], '5000': ['Immovable rod'], '25000': ['Rod of splendor', 'Rod of withering'], '30000': ["Liberator's rod"], '73000': ['Metamagic (+2 spell level) greater'], '14000': ['Metamagic (+3 spell level) minor'], '170000': ['Metamagic quicken greater'], '16650': ['Sapling rod'], '60000': ['Rod of rulership'], '24500': ['Metamagic (+1 spell level) greater'], '20000': ['Suzerain scepter'], '26500': ['Earthbind rod'], '10500': ['Rod of metal and mineral detection'], '23500': ['Rod of enemy detection'], '18000': ['Rod of beguiling', 'Rod of nettles'], '121500': ['Metamagic (+3 spell level) greater'], '29000': ['Rod of the aboleth'], '70000': ['Rod of lordly might'], '11000': ['Metamagic (+1 spell level) normal', 'Rod of cancellation'], '5400': ['Rod of thunderous force'], '12000': ['Conduit rod', 'Grounding rod', 'Rod of the wayang', 'Rod of wonder'], '38305': ['Rod of steadfast resolve'], '35000': ['Metamagic quicken minor'], '61000': ['Rod of security'], '85000': ['Rod of alertness'], '19000': ['Rod of the viper']}

list_of_items = [rings,
["Dagger", "Sword Cane", "Brass Knuckles", "Punching Dagger", "Spiked Gauntlet", "Light Mace", "Club", "Heavy Mace", "Whip", "Morning Star", "Spear", "Heavy Crossbow", "Light Hammer", "Hand Axe", "Short Sword", "Long Sword", "Battle Axe", "Flail", "Scimitar", "Rapier", "Trident", "Warhammer", "Falchion", "Greataxe", "Heavy Flail", "Great Sword", "Halberd", "Scythe", "Longbow"],
["Robe", "Cloak", "Leather Boots", "Leather Gloves", "Bracers", "Greaves", "Great Helm", "Wizard's Hat", "Bassinet", "Leather Armor", "Chainmail", "Hide", "Breastplate", "Banded Mail", "Half-Plate", "Full Plate"],
wonders,
["Buckler", "Light Steel Shield", "Light Steel Quickdraw Shield", "Light Wooden Shield", "Light Wooden Quickdraw Shield", "Heavy Steel Shield", "Heavy Wooden Shield", "Tower Shield"],
staves,
rods]

if __name__ == '__main__':
	main()
