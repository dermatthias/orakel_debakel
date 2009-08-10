#!/usr/bin/env python
# -*- coding: utf-8 -*-

# socon by matthias
# predicts soccer scores

import sys
import cPickle as pickle
# own classes
from data import *
from predictor import *

DEBUG = 1

class Main():
   def __init__(self):
      self.pred = Predictor()
      self.data = Data()
      # def vars
      self.home_game_bonus = 1.10
      self.home_game_won_bonus = 1.15
      self.last_year = '2008'
      self.last_year_bonus = 1.25

   # returns the sum of goals of all the matches in the database
   # between the two given teams
   def classic(self, team):
      # get scores
      goal_sum = self.pred.resAb(int(team[0]), int(team[1]))
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
      if DEBUG: print '------'
      if DEBUG: print str(self.data.get_team_name(teams[0])) + ' vs. ' + str(self.data.get_team_name(teams[1]))

      goal_sum = list(self.pred.resAb(teams[0], teams[1]))
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
      if home_vics > 2:
         goal_sum[0] *= self.home_game_won_bonus
         print '+ home_game_won_bonus: ' + str(goal_sum)

      # give home games bonus
      goal_sum[0] *= self.home_game_bonus

      
      # last year bonus
      #################
      # check which team won last season, give it bonus
      last_year_score = self.pred.get_game_scores(teams[0], teams[1], self.last_year)
      if last_year_score != []: # have they played each other?
         lys_sum = 0
         
         # give bonus to the better team of the last season
         s1 = last_year_score[0][0] + last_year_score[1][0]
         s2 = last_year_score[0][1] + last_year_score[1][1]
         if s1 > s2:
            goal_sum[0] *= self.last_year_bonus
         else:
            goal_sum[1] *= self.last_year_bonus
            
         if DEBUG: print '+ last_year_bonus: ' + str(goal_sum)

      else: # they haven't played?
         # TODO:
         # bonus to higher team
         pass


      # common bonus to better team (thirds)
      ######################################
      # TODO:
      # if the teams are in a different third of the 'ewige tabelle',
      # give the better team a bonus
      
      

      # calculate diff and goal mean
      ##############################
      goal_diff = goal_sum[0] - goal_sum[1]
      # if teams played each other:
      if goal_sum[2] != 0:
         goal_mean = goal_sum[0]/goal_sum[2], goal_sum[1]/goal_sum[2]
      else:
         # TODO:
         # wenn team noch nie gegeneinander gespielt, dann gewinnt das bessere team
         # aus der ewigen tabelle, bzw. wenn im gleichen drittel, dann 50/50 entscheidung
         # ob unentschieden oder 1:0/2:1
         goal_mean = (0,0)

      if goal_diff > 0:
         if DEBUG: print str(teams[0]) + ' better. ' + 'diff: ' + str(goal_diff)
         if DEBUG: print 'prediction ' + str(goal_mean[0]) + ':' + str(goal_mean[1])
         print str(teams[0]) + ' ' + str(teams[1]) + ' ' \
             + str(int(goal_mean[0])) + ' ' + str(int(goal_mean[1]))
      elif goal_diff == 0:
         if DEBUG: print 'draw. ' + 'diff: ' + str(goal_diff)
         if DEBUG: print 'prediction ' + str(goal_mean[0]) + ':' + str(goal_mean[1])
         print str(teams[0]) + ' ' + str(teams[1]) + ' ' \
             + str(int(goal_mean[0])) + ' ' + str(int(goal_mean[1]))
      else:
         if DEBUG: print str(teams[1]) + ' better. ' + 'diff: ' + str(goal_diff)
         if DEBUG: print 'prediction ' + str(goal_mean[0]) + ':' + str(goal_mean[1])
         print str(teams[0]) + ' ' + str(teams[1]) + ' ' \
             + str(int(goal_mean[0])) + ' ' + str(int(goal_mean[1]))



   # genetic algorithm foo
   def genetic():
      pass



   def main(self):
      # read input
      input = sys.stdin.readlines()

      # calculate every match
      for i in input:
         match = i.replace('\n', '').split(' ')

         # classic mehtod, plain and stupid
         #self.classic(match)

         # classic plus bonus method
         self.classic_plus(match)

         # genetic programming method
         # self.genetic(match)

if __name__ == '__main__':
   main = Main()
   main.main()
