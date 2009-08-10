# -*- coding: utf-8 -*-
from data import *

class Predictor():

    def __init__(self):
        self.data = Data()
        self.data.unpickle()                

    # returns the sum of goals of the last 5 years
    def resAb(self, team1, team2):
        t1_sum = 0
        t2_sum = 0
        # number of games
        count = 0
        for k,v in self.data.kreuz.iteritems():
            t1_res_home = 0
            t1_res_away = 0
            t2_res_home = 0
            t2_res_away = 0
            # team1
            try:                
                t1_res_home += v[team1][team2][0]
                t1_res_away += v[team2][team1][1]
                # team2
                t2_res_away += v[team1][team2][1]
                t2_res_home += v[team2][team1][0]
             
                t1_sum += t1_res_home + t1_res_away
                t2_sum += t2_res_home + t2_res_away
                count+=2
            except:
                # if no data for that year is available
                pass
            
        return [t1_sum, t2_sum, count]
      
    # returns the game history of the given teams
    # team1 (home team) is always named FIRST
    def get_history(self, team1, team2):
        history = []
        for v in self.data.kreuz.itervalues():            
            try:
                history.append(v[team1][team2])
                vt = v[team2][team1]
                history.append( (vt[1], vt[0]) )
            except KeyError:
                pass

        return history

    def get_game_scores(self, team1, team2, year):
        try:
            game1 = self.data.kreuz[year][team1][team2]
            game2 = self.data.kreuz[year][team2][team1]
        except KeyError:
            return []

        return [game1, game2]
          
