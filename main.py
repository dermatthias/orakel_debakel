#!/usr/bin/env python
# -*- coding: utf-8 -*-

# socon by matthias
# predicts soccer scores

import sys
import random
import cPickle as pickle
# own classes
from data import *
from predictor import *

DEBUG = 0

class Main():
   def __init__(self):
      # init 
      self.pred = Predictor()
      self.data = Data()
      random.seed()
      
      # def vars
      self.home_game_bonus = 1.10
      self.home_game_won_bonus = 1.10
      self.home_game_threshold = 2
      self.last_year = '2008'
      self.last_year_bonus = 1.15
      self.not_played_bonus = 1.05
      self.rank_bonus = 1.10

   # returns the sum of goals of all the matches in the database
   # between the two given teams
   def classic(self, team):
      # get scores
      goal_sum = self.pred.get_goal_sum(int(team[0]), int(team[1]))
      goal_diff = goal_sum[0] - goal_sum[1]
      if goal_sum[2] != 0:
         goal_mean = goal_sum[0]/goal_sum[2], goal_sum[1]/goal_sum[2]
      else:
         goal_mean = (0,0)

      print '------'

      if goal_diff > 0:
         print str(team[0]) + ' better. ' + 'diff: ' + str(goal_diff)
         print 'prediction ' + str(goal_mean[0]) + ':' + str(goal_mean[1])

      elif goal_diff == 0:
         print 'draw. ' + 'diff: ' + str(goal_diff)
         print 'prediction ' + str(goal_mean[0]) + ':' + str(goal_mean[1])

      else:
         print str(team[1]) + ' better. ' + 'diff: ' + str(goal_diff)
         print 'prediction ' + str(goal_mean[0]) + ':' + str(goal_mean[1])



   # classic plus, gives bonus to the 'good' teams and
   # ranks the last season higher than the seasons before
   def classic_plus(self, team):

      teams = [int(team[0]), int(team[1])]
      if DEBUG: print '\33[1;30m------\033[1;m'
      if DEBUG: print str(self.data.get_team_name(teams[0])) + ' vs. ' + str(self.data.get_team_name(teams[1]))

      # get sum of all goals in all games
      ###################################
      goal_sum = list(self.pred.get_goal_sum(teams[0], teams[1]))

      # if teams never ever played against each other
      if goal_sum[2] == 0:
         if DEBUG: print 'random score because teams never ever played'

         rank_t1 = self.data.get_rank(teams[0])
         rank_t2 = self.data.get_rank(teams[1])

         if rank_t1 < rank_t2:
            # team 1 wins random score
            rand_list = [[2,1], [1,0], [1,1]] * 2
            goal_sum = random.sample(rand_list, 2)
            goal_sum.append(len(goal_sum))
         elif rank_t2 < rank_t1:
            # team2 wins random score
            rand_list = [[1,2], [0,1], [1,1]] * 2
            goal_sum = random.sample(rand_list, 2)
            goal_sum.append(len(goal_sum))
         else:
            # complete random if same rank
            rand_list = [[1,0], [0,1], [0,0], [2,1], [1,2]] * 2
            goal_sum = random.sample(rand_list, 2)
            goal_sum.append(len(goal_sum))

      if DEBUG: print 'goal_sum: ' + str(goal_sum)

      # home game bonus
      #################
      # check how often won at home
      # give bonus if won often
      games = self.pred.get_history(teams[0], teams[1])
      if DEBUG: print 'hist: ' + str(games)

      home_vics = 0
      for g in games:
         if g[0] > g[1]:
            home_vics+=1
      if home_vics > self.home_game_threshold:
         goal_sum[0] *= self.home_game_won_bonus
         if DEBUG: print '\033[1;32m+ home_game_won_bonus: \033[1;m' + str(goal_sum)

      # give home games bonus
      goal_sum[0] *= self.home_game_bonus


      # last year bonus
      #################
      # check which team won last season, give it bonus
      last_year_score = self.pred.get_game_scores(teams[0], teams[1], self.last_year)
      if last_year_score != []: # have they played each other?

         # give bonus to the better team of the last season
         s1 = last_year_score[0][0] + last_year_score[1][0]
         s2 = last_year_score[0][1] + last_year_score[1][1]
         if s1 > s2:
            goal_sum[0] *= self.last_year_bonus
         else:
            goal_sum[1] *= self.last_year_bonus

         if DEBUG: print '\033[1;32m+ last_year_bonus: \033[1;m' + str(goal_sum)

      else: # they haven't played last year?
         # bonus to higher team
         r1 = self.data.get_rank(teams[0])
         r2 = self.data.get_rank(teams[1])
         if r1 < r2:
            goal_sum[0] *= self.not_played_bonus
            if DEBUG: print '\033[1;32m+ not_played_bonus: \033[1;m' + str(goal_sum)
         elif r2 < r1:
            goal_sum[1] *= self.not_played_bonus
            if DEBUG: print '\033[1;32m+ not_played_bonus: \033[1;m' + str(goal_sum)


      # common bonus to better team (thirds)
      ######################################
      # TODO:
      # if the teams are in a different third of the 'ewige tabelle',
      # give the better team a bonus
      rank_team1 = self.data.get_rank(teams[0])
      rank_team2 = self.data.get_rank(teams[1])

      if rank_team1 < rank_team2:
         goal_sum[0] *= self.rank_bonus
         if DEBUG: print '\033[1;32m+ rank bonus \033[1;m' + \
                self.data.get_team_name(teams[0]) + ': '  + str(goal_sum)
      elif rank_team2 < rank_team1:
         goal_sum[1] *= self.rank_bonus
         if DEBUG: print '\033[1;32m+ rank bonus \033[1;m' + \
                self.data.get_team_name(teams[0]) + ': '  + str(goal_sum)


      # calculate diff and goal mean
      ##############################
      goal_diff = goal_sum[0] - goal_sum[1]
      # if teams played each other:
      if goal_sum[2] != 0:
         goal_mean = [goal_sum[0]/goal_sum[2], goal_sum[1]/goal_sum[2]]


      # output and debug
      ##################
      if goal_diff > 0:
         if DEBUG: print str(teams[0]) + ' better. ' + 'diff: ' + str(goal_diff)
         if DEBUG: print '\033[1;31mprediction: \033[1;m ' + str(goal_mean[0]) + ':' + \
                str(goal_mean[1])
         print str(teams[0]) + ' ' + str(teams[1]) + ' ' \
             + str(int(goal_mean[0])) + ' ' + str(int(goal_mean[1]))

      elif goal_diff == 0:
         if DEBUG: print 'draw. ' + 'diff: ' + str(goal_diff)
         if DEBUG: print '\033[1;31mprediction: \033[1;m ' + str(goal_mean[0]) + ':' + \
                str(goal_mean[1])
         print str(teams[0]) + ' ' + str(teams[1]) + ' ' \
             + str(int(goal_mean[0])) + ' ' + str(int(goal_mean[1]))

      else:
         if DEBUG: print str(teams[1]) + ' better. ' + 'diff: ' + str(goal_diff)
         if DEBUG: print '\033[1;31mprediction: \033[1;m ' + str(goal_mean[0]) + ':' + \
                str(goal_mean[1])
         print str(teams[0]) + ' ' + str(teams[1]) + ' ' \
             + str(int(goal_mean[0])) + ' ' + str(int(goal_mean[1]))



   # genetic algorithm foo
   def genetic():
      pass


   # add new scores and recalculate the stats
   def add_and_do_magic(self, team):
      # convert to ints
      teams = [int(team[0]), int(team[1]), int(team[2]), int(team[3])]
      # insert into database of 2009
      self.data.kreuz2009[teams[0]][teams[1]] = (teams[2], teams[3])
      # pickle 2009 database
      

   def main(self):
      # read input
      input = sys.stdin.readlines()      
      
      # sys args
      if len(sys.argv) != 3:
         print 'arguments wrong. major fuck up detected! called stop(). hammertime!'
         exit(1)
      else:
         mode = sys.argv[1]
         gameday = sys.argv[2]

      if mode == '--predict':         
         # calculate every match
         for i in input:
            match = i.replace('\n', '').split(' ')

            # classic method, plain and stupid
            #self.classic(match)

            # classic plus bonus method
            self.classic_plus(match)

            # genetic programming method
            # self.genetic(match)

      elif mode == '--verify':
         for i in input:
            match = i.replace('\n', '').split(' ')
               
            # add live scores to the database and recalculate
            self.add_and_do_magic(match)

      else: 
         print 'ERROR: arguments not recognized.\ndefault method called: solving the answer to the life, the universe and everything. come back in 7.5 million years. and thanks for all the fish!'
         

if __name__ == '__main__':
   main = Main()
   main.main()
