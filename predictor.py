# -*- coding: utf-8 -*-
from data import *

class Predictor():

    def __init__(self):
        self.data = Data()
        self.data.unpickle()                

    # returns the sum of goals of the last 5 years
    def get_goal_sum(self, team1, team2):
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
    
    # returns the scores of the given teams in the given year
    def get_game_scores(self, team1, team2, year):
        try:
            game1 = self.data.kreuz[year][team1][team2]
            game2 = self.data.kreuz[year][team2][team1]
            game2 = list(game2)
            game2.reverse()
        except KeyError:
            return []

        return [game1, game2]

          
    # returns the rank (1,2 or 3) of the given team
    def get_rank(self, team):
        for k,v in self.data.rank_groups.iteritems():
            if team in v:
                return k

   
    # returns the real team name as a string
    def get_team_name(self, team):
        return self.data.names[team]

    # return recent games if team
    def get_recent_games(self, team, number):
        # check if less than 'number' games are played
        games_played = len(self.data.recent_games[team])
        if games_played < number:
            number = games_played

        temp_list = []
        for i in range(0, number):
            temp_list.append(self.data.recent_games[team][i])

        return temp_list

    # checks the recent games and returns 1 if all won, else 0
    def winning_streak(self, team, games):
        games_played = len(games)

        count = 0
        for i in games:
            if i[0] > i[1]:
                count+=1
        
        if count == games_played:
            return 1
        else:
            return 0
                

