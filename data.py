# -*- coding: utf-8 -*-
import cPickle as pickle

class Data():

   def __init__(self):
       # team names
       self.names = {65: '1. FC Köln',123: '1899 Hoffenheim',83: 'Arminia Bielefeld',6: 'Bayer Leverkusen',87: 'Bor. Mönchengladbach',7: 'Bor. Dortmund',91: 'Eintracht Frankfurt',93: 'Energie Cottbus',40: 'FC Bayern München',9: 'FC Schalke 04',100: 'Hamburger SV',55: 'Hannover 96',54: 'Hertha BSC',105: 'Karlsruher SC',16: 'VfB Stuttgart',129: 'VfL Bochum',131: 'VfL Wolfsburg',134: 'Werder Bremen',79: '1. FC Nürnberg',102: 'Hansa Rostock',107: 'MSV Duisburg',81: '1. FSV Mainz 05',23: 'Alemannia Aachen',76: '1. FC Kaiserslautern',112: 'SC Freiburg',}

      # kreuztabellen bis 2004
       self.kreuz2009 = {65: {},123: {},83: {},6: {},87: {},7: {},91: {},93: {},40: {},9: {},100: {},55: {},54: {},105: {},16: {},129: {},131: {},134: {},79: {},102: {},107: {},81: {},23: {},76: {},112: {},}
       self.kreuz2008 = {}
       self.kreuz2007 = {}
       self.kreuz2006 = {}
       self.kreuz2005 = {}
       self.kreuz2004 = {}
       self.kreuz = {}

   def unpickle(self):
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

       self.kreuz = {'2004': self.kreuz2004, '2005': self.kreuz2005, '2006': self.kreuz2006, '2007': self.kreuz2007, '2008': self.kreuz2008}

   def get_team_name(self, team):
       return self.names[team]
       
