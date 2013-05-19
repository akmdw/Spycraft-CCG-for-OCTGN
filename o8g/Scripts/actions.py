    # Python Scripts for the Spycraft CCG definition for OCTGN
    # Copyright (C) 2013  Konstantine Thoukydides and Lord Nat

    # This python script is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this script.  If not, see <http://www.gnu.org/licenses/>.


import re

#---------------------------------------------------------------------------
# Global Variables
#---------------------------------------------------------------------------

Faction = None

    
#---------------------------------------------------------------------------
# Game Setup
#---------------------------------------------------------------------------

def gameSetup(group, x = 0, y = 0): # WiP
   debugNotify(">>> gameSetup()") #Debug
   mute()
   global Faction
   if Faction and not confirm("Are you sure you want to setup for a new game? (This action should only be done after a table reset)"): return
   debugNotify("Resetting All", 2) #Debug
   resetAll()
   debugNotify("Choosing Side", 2) #Debug
   chooseSide()
   debugNotify("Setting Deck Variables", 2) #Debug
   deck = me.piles['Deck']
   leadersDeck = me.piles['Leaders']
   missionDeck = shared.Missions
   debugNotify("Arranging Leaders",2)
   if len(missionDeck) == 0: 
      delayed_whisper(":::ERROR::: Please load the mission deck before setting up the game")
      return
   if len(leadersDeck) < 4 and not confirm(":::Illegal Deck:::\n\nYou must have at least 4 leaders in your leader deck.\n\nProceed Anyway?"): return
   for leader in leadersDeck:
      debugNotify("Moving {} ({}) to pos {}".format(leader, leader.level, num(leader.level) - 1),2)
      leader.moveTo(leadersDeck,num(leader.level) - 1) # This function will move each leader card at the index of the leader deck, according to its level. So level 1 leader will be top, and level 4 will be bottom
      if not Faction: Faction = leader.Faction
      elif Faction != leader.Faction:
         if not confirm(":::Illegal Deck:::\n\nYou have leader of different factions in your leader deck.\n\nProceed Anyway?"): return
         else: 
            notify(":::Warning::: {}'s Leader deck has different factions!".format(me))
            Faction = leader.Faction
   debugNotify("Setting Reference Cards",2)
   debugNotify("playerside = {}. yaxisMove = {}".format(playerside,yaxisMove()),4)
   if Faction == "Banshee Net": table.create("9f291494-8713-4b7e-bc7c-36b428fc0dd1",playerside * -380, (playerside * 20) + yaxisMove(),1,True) # Creating a the player's faction reference card.
   if Faction == "Bloodvine": table.create("8e2ff010-98b5-4884-a39b-100940d4f702",playerside * -380, (playerside * 20) + yaxisMove(),1,True) # Creating a the player's faction reference card.
   if Faction == "Franchise": table.create("6d131915-cb6a-43ca-b2f1-64ac040b0eec",playerside * -380, (playerside * 20) + yaxisMove(),1,True) # Creating a the player's faction reference card.
   if Faction == "The Krypt": table.create("0d058ed6-51e8-42c7-9cbb-67a3d267c618",playerside * -380, (playerside * 20) + yaxisMove(),1,True) # Creating a the player's faction reference card.
   if Faction == "Nine Tiger": table.create("49f5d0ad-60e2-4810-86b6-5f962f99d9bd",playerside * -380, (playerside * 20) + yaxisMove(),1,True) # Creating a the player's faction reference card.
   if Faction == "Shadow Patriots": table.create("bf4bfecd-1d84-4a6f-a787-0986a0fe06b1",playerside * -380, (playerside * 20) + yaxisMove(),1,True) # Creating a the player's faction reference card.
   debugNotify("Moving First Leader to table",2)
   rnd(1,10) # Delay
   leadersDeck.top().moveToTable(0, (playerside * 130) + yaxisMove()) # Top card in the leaders deck should be the player's level 1 leader.
   debugNotify("Preparing Mission Deck",2)
   currMissionsVar = getGlobalVariable('currentMissions')
   if currMissionsVar != 'CHECKED OUT':
      currentMissions = eval(currMissionsVar)
      if len(currentMissions) == 0: 
         shuffle(missionDeck)
         startingMissions = missionDeck.top(5)
         for mission in startingMissions: prepMission(mission, True)
      else: debugNotify("Missions already setup by another player. Aborting mission deck setup",4)
   else: debugNotify("Missions currently being setup by another player",4)
   shuffle(deck)
   drawMany(deck, 7, silent = True)
   debugNotify("<<< gameSetup()") #Debug
    
#---------------------------------------------------------------------------
# Rest
#---------------------------------------------------------------------------

def defaultAction(card, x = 0, y = 0):
   debugNotify(">>> defaultAction()") #Debug
   mute()
   if not card.isFaceUp: act(card)
   elif card.Type == 'Mission': winMission(card)
   else: ability(card)
   debugNotify("<<< defaultAction()") #Debug
    
def roll6(group, x = 0, y = 0):
    mute()
    n = rnd(1, 6)
    notify("{} rolls {} on a 6-sided die.".format(me, n))

def draw(group = me.piles['Deck'], x = 0, y = 0):
    if len(group) == 0: return
    mute()
    group[0].moveTo(me.hand)
    notify("{} draws a card.".format(me))

def drawMany(group = me.piles['Deck'], count = None, destination = None, silent = False):
   debugNotify(">>> drawMany()") #Debug
   debugNotify("source: {}".format(group.name),2)
   if destination: debugNotify("destination: {}".format(destination.name),2)
   mute()
   if destination == None: destination = me.hand
   SSize = len(group)
   if SSize == 0: return 0
   if count == None: count = askInteger("Draw how many cards?", 5)
   if count == None: return 0
   if count > SSize : 
      count = SSize
      delayed_whisper("You do not have enough cards in your deck to complete this action. Will draw as many as possible")
   for c in group.top(count): 
      c.moveTo(destination)
   if not silent: notify("{} draws {} cards.".format(me, count))
   debugNotify("<<< drawMany() with return: {}".format(count))
   return count

    
def shuffle(group, x = 0, y = 0):
    group.shuffle()

def smartPlay(card, x = 0, y = 0):
    mute()
    if card.Type == 'Gear': playGear(card)
    elif card.Type == 'Action': playAction(card)
    else: playAgent(card)

def playAgent(card, x = 0, y = 0):
    mute()
    card.moveToTable(playerside * -300, yaxisMove(),True)
    notify("{} recruits an agent from their hand.".format(me))

def playGear(card, x = 0, y = 0):
    mute()
    card.moveToTable(playerside * -220, yaxisMove(),True)
    notify("{} requisitions a gear from their hand.".format(me))

def playAction(card, x = 0, y = 0):
    mute()
    card.moveToTable(playerside * 300, yaxisMove() + cwidth())
    if re.search(r'Solo Op',card.Traits):
      notify("{} begins the {} Solo Op.".format(me, card))
      draw()
    else: notify("{} attempts to play {}.".format(me, card))

def winMission(card, x = 0, y = 0):
   mute()
   if card.Type == 'Mission' and confirm("Have you just won {}?".format(card.name)): 
      if scrubMission(card) == 'ABORT': return
      if prepMission(shared.Missions.top()) == 'ABORT': return
      card.moveTo(me.piles['Victory Pile'])
      me.counters['Victory Points'].value += num(card.properties['Victory Points'])
      notify("{} wins {} and gains {} VP.".format(me, card, card.properties['Victory Points']))
   else: whisper(":::ERROR::: You can only win missions")      

def winTargetMission(group, x = 0, y = 0):
   for card in table:
      if card.targetedBy and card.targetedBy == me: winMission(card)

def discard(card, x = 0, y = 0):
   mute()
   if fetchProperty(card, 'Type') != 'Mission': 
      card.moveTo(card.owner.Discard)
      if card.Type == 'Agent' or card.Type == 'Leader': notify("{} retires {}.".format(me, card))
      else: notify("{} trashes {}.".format(me, card))
   else: 
      if scrubMission(card) == 'ABORT': return
      if prepMission(shared.Missions.top()) == 'ABORT': return
      card.moveTo(shared.piles['Mission Discard'])
      notify("{} discards {}.".format(me, card))
      
def discardFromHand(card):
   mute()
   card.moveTo(me.Discard)
   notify("{} discards {}.".format(me, card))

def shuffleIntoDeck(group = me.Discard):
   mute()
   Deck = me.Deck
   for c in group: c.moveTo(Deck)
   random = rnd(100, 1000)
   Deck.shuffle()
   notify("{} shuffles his {} into his Deck.".format(me, group.name))

def act(card, x = 0, y = 0):
   debugNotify(">>> act()") #Debug
   mute()
   if card.isFaceUp:
      notify("{} Deactivates {}".format(me, card))
      card.isFaceUp = False
   else:
      card.isFaceUp = True
      rnd(1,10) 
      if card.Type == 'Mission': 
         notify("{} Reveals {}".format(me, card))
         card.orientation = Rot0
      else: notify("{} Activates {}".format(me, card))
   debugNotify("<<< act()") #Debug

def wound(card, x = 0, y = 0):
    mute()
    card.orientation ^= Rot90
    if card.orientation & Rot90 == Rot90:
        notify('{} is wounded.'.format(card))
    else:
        notify('{} is unwounded.'.format(card))

def clear(card, x = 0, y = 0):
    notify("{} clears {}.".format(me, card))
    card.highlight = None
    card.target(False)

def expose(card, x = 0, y = 0):
    mute()
    if card.markers[mdict['exposed']] == 0:
        notify("{} becomes Exposed.".format(card))
        card.markers[mdict['exposed']] = 1
    else:
        notify("{} is not Exposed anymore.".format(card))
        card.markers[mdict['exposed']] = 0


def baffle(card, x = 0, y = 0):
    mute()
    if card.markers[mdict['baffled']] == 0:
       notify("{} becomes Baffled and is considered Exposed until the end of the mission.".format(card))
       card.markers[mdict['exposed']] += 1
       card.markers[mdict['baffled']] += 1
    else:
       notify("{} is not baffled anymore.".format(card))
       card.markers[mdict['exposed']] -= 1
       card.markers[mdict['baffled']] -= 1

def ability(card, x = 0, y = 0):
    mute()
    card.highlight = AbilityColor
    notify('{} activates the ability on {}'.format(me, card))

def download_o8c(group,x=0,y=0):
   openUrl("http://dbzer0.com/pub/SpycraftCCG/sets/SpycraftCCG-Sets-Bundle.o8c")

def inspectCard(card, x = 0, y = 0): # This function shows the player the card text, to allow for easy reading until High Quality scans are procured.
   debugNotify(">>> inspectCard()") #Debug
   #if debugVerbosity > 0: finalTXT = 'AutoScript: {}\n\n AutoAction: {}'.format(CardsAS.get(card.model,''),CardsAA.get(card.model,''))
   if card.Type == 'Reference':
      information("This is the {} Leader Ability Reference card.\
                 \nIt does not have any abilities itself but it informs you which built-in ability your leaders have.".format(card.Faction))
   else:          
      finalTXT = "{}\n\nTraits:{}\n\nCard Text: {}".format(card.name, card.Traits, card.Rules)
      information("{}".format(finalTXT))

def inspectTargetCard(group, x = 0, y = 0): # This function shows the player the card text, to allow for easy reading until High Quality scans are procured.
   debugNotify(">>> inspectTargetCard()") #Debug
   for card in table:
      if card.targetedBy and card.targetedBy == me: inspectCard(card)
   
