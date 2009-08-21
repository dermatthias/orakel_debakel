# -*- coding: utf-8 -*-
import cPickle as pickle

class Data():

   def __init__(self):
      # team names
      self.names = {65: '1. FC Köln',123: '1899 Hoffenheim',83: 'Arminia Bielefeld',6: 'Bayer Leverkusen',87: 'Bor. Mönchengladbach',7: 'Bor. Dortmund',91: 'Eintracht Frankfurt',93: 'Energie Cottbus',40: 'FC Bayern München',9: 'FC Schalke 04',100: 'Hamburger SV',55: 'Hannover 96',54: 'Hertha BSC',105: 'Karlsruher SC',16: 'VfB Stuttgart',129: 'VfL Bochum',131: 'VfL Wolfsburg',134: 'Werder Bremen',79: '1. FC Nürnberg',102: 'Hansa Rostock',107: 'MSV Duisburg',81: '1. FSV Mainz 05',23: 'Alemannia Aachen',76: '1. FC Kaiserslautern',112: 'SC Freiburg',}
      
      # kreuztabellen bis 2004
      #self.kreuz2009 = {65: {},123: {},83: {},6: {},87: {},7: {},91: {},93: {},40: {},9: {},100: {},55: {},54: {},105: {},16: {},129: {},131: {},134: {},79: {},102: {},107: {},81: {},23: {},76: {},112: {}}
      self.kreuz2009 = {}
      self.kreuz2008 = {}
      self.kreuz2007 = {}
      self.kreuz2006 = {}
      self.kreuz2005 = {}
      self.kreuz2004 = {}
      self.kreuz = {}

       # plus 30 je jahr nicht in 1. bl
      self.eternal_ladder = {65: 159, 123: 175, 83: 181, 6: 260, 87: 165, 7: 244, 91: 185, 93: 167, 40: 355, 9: 306 ,100: 279, 55: 216, 54: 257, 105: 162, 16: 287, 129: 183, 131: 242, 134: 306, 79: 191, 102: 150, 107: 146, 81: 175, 23: 154, 76: 165, 112: 138}
       
      # all teams divided in 3 groups by myself
      self.rank_groups = {1: [40,131,16,134,100,9,7,123], 2: [54,6,91,55,87,129,79,83], 3: [93,81,65,112,105,76,23,102,107]}
      
      # recent games of each team
      # order is important here! first entry in list is most recent game.
      # order of score from view of the team (0:1 is lost, no matter where played)
      self.recent_games = {65: [],123: [],83: [],6: [],87: [],7: [],91: [],93: [],40: [],9: [],100: [],55: [],54: [],105: [],16: [],129: [],131: [],134: [],79: [],102: [],107: [],81: [],23: [],76: [],112: []}

   # load the history pickle files
   def unpickle(self):
      kreuz2009_f = open('kreuz2009.pkl', 'rb')
      self.kreuz2009 = pickle.load(kreuz2009_f)
      kreuz2008_f = open('kreuz2008.pkl', 'rb')
      self.kreuz2008 = pickle.load(kreuz2008_f)
      kreuz2007_f = open('kreuz2007.pkl', 'rb')
      self.kreuz2007 = pickle.load(kreuz2007_f)
      kreuz2006_f = open('kreuz2006.pkl', 'rb')
      self.kreuz2006 = pickle.load(kreuz2006_f)
      kreuz2005_f = open('kreuz2005.pkl', 'rb')
      self.kreuz2005 = pickle.load(kreuz2005_f)
      kreuz2004_f = open('kreuz2004.pkl', 'rb')
      self.kreuz2004 = pickle.load(kreuz2004_f)
      
      # dictionary with all history years
      self.kreuz = {'2004': self.kreuz2004, '2005': self.kreuz2005, '2006': self.kreuz2006, '2007': self.kreuz2007, '2008': self.kreuz2008, '2009': self.kreuz2009}

      # load recent games
      recent_f = open('recent_games.pkl', 'rb')
      self.recent_games = pickle.load(recent_f)



   # save current season data
   def save_data(self):
      kreuz2009_f = open('kreuz2009.pkl', 'wb')
      pickle.dump(self.kreuz2009, kreuz2009_f)

   # save recent games
   def save_recent(self):
      recent_f = open('recent_games.pkl', 'wb')
      pickle.dump(self.recent_games, recent_f)

       
      
   
               
       
