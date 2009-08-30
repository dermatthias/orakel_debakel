#!/usr/bin/env python
# -*- coding: utf-8 -*-

# orakel debakel
# for socon by matthias schneider
# predicts soccer scores

import sys
import random
import cPickle as pickle
# own classes
from data import *
from predictor import *

DEBUG = 1

class Main:
   def __init__(self):
      # init
      self.pred = Predictor()
      self.data = Data()
      self.data.unpickle()

      random.seed()

      # def vars
      self.home_game_bonus = 1.10
      self.home_game_won_bonus = 1.05
      self.home_game_threshold = 2
      self.this_year = '2009'
      self.last_year = '2008'
      self.last_year_bonus = 1.15
      self.not_played_bonus = 1.05
      self.rank_bonus = 1.10
      self.n_recent_games = 3;
      self.recent_games_bonus = 1.10
      self.current_ladder_bonus = 1.10

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

      if DEBUG: print '------'

      if goal_diff > 0:
         if DEBUG: print str(team[0]) + ' better. ' + 'diff: ' + str(goal_diff)
         if DEBUG: print 'prediction ' + str(goal_mean[0]) + ':' + str(goal_mean[1])
         
      elif goal_diff == 0:
         if DEBUG: print 'draw. ' + 'diff: ' + str(goal_diff)
         if DEBUG: print 'prediction ' + str(goal_mean[0]) + ':' + str(goal_mean[1])

      else:
         if DEBUG: print str(team[1]) + ' better. ' + 'diff: ' + str(goal_diff)
         if DEBUG: print 'prediction ' + str(goal_mean[0]) + ':' + str(goal_mean[1])

      print str(team[0]) + ' ' + team[1] + ' ' + \
            str(goal_mean[0]) + ' ' + str(goal_mean[1])



   # classic plus, gives bonus to the 'good' teams and
   # ranks the last season higher than the seasons before
   def classic_plus(self, team):

      teams = [int(team[0]), int(team[1])]
      if DEBUG: print '\33[1;30m------\033[1;m'
      if DEBUG: print str(self.pred.get_team_name(teams[0])) + ' vs. ' + str(self.pred.get_team_name(teams[1]))

      # get sum of all goals in all games
      ###################################
      goal_sum = list(self.pred.get_goal_sum(teams[0], teams[1]))

      # if teams never ever played against each other
      if goal_sum[2] == 0:
         if DEBUG: print 'random score because teams never ever played'

         rank_t1 = self.pred.get_rank(teams[0])
         rank_t2 = self.pred.get_rank(teams[1])
         temp_g = []
         goal_sum = []

         if rank_t1 < rank_t2:
            # team 1 wins random score
            rand_list = [[2,1], [1,0], [1,1]] * 2
            temp_g = random.sample(rand_list, 2)
            goal_sum.append(temp_g[0][0] + temp_g[1][0])
            goal_sum.append(temp_g[0][1] + temp_g[1][1])
            goal_sum.append(len(goal_sum))
         elif rank_t2 < rank_t1:
            # team2 wins random score
            rand_list = [[1,2], [0,1], [1,1]] * 2
            temp_g = random.sample(rand_list, 2)
            goal_sum.append(temp_g[0][0] + temp_g[1][0])
            goal_sum.append(temp_g[0][1] + temp_g[1][1])
            goal_sum.append(len(goal_sum))
         else:
            # complete random if same rank
            rand_list = [[1,0], [0,1], [0,0], [2,1], [1,2]] * 2
            temp_g = random.sample(rand_list, 2)
            goal_sum.append(temp_g[0][0] + temp_g[1][0])
            goal_sum.append(temp_g[0][1] + temp_g[1][1])
            goal_sum.append(len(goal_sum))

      if DEBUG: print '\033[1;32mScore: \033[1;m' + str(goal_sum)

      # home game bonus
      #################
      # check how often won at home
      # give bonus if won often
      games = self.pred.get_history(teams[0], teams[1])
      if DEBUG: print 'History: ' + str(games)

      home_vics = 0
      for g in games:
         if g[0] > g[1]:
            home_vics+=1
      if home_vics > self.home_game_threshold:
         goal_sum[0] *= self.home_game_won_bonus
         if DEBUG: print '\033[1;32m+ home_game_won_bonus: \033[1;m' + str(goal_sum)

      # give home games bonus
      goal_sum[0] *= self.home_game_bonus
      if DEBUG: print '\033[1;32m+ home_game_bonus: \033[1;m' + str(goal_sum)


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
            if DEBUG: print '\033[1;32m+ last_year_bonus: \033[1;m' + str(goal_sum)
         elif s2 > s1:
           goal_sum[1] *= self.last_year_bonus
           if DEBUG: print '\033[1;32m+ last_year_bonus: \033[1;m' + str(goal_sum)

      else: # they haven't played last year?
         # bonus to higher team
         r1 = self.pred.get_rank(teams[0])
         r2 = self.pred.get_rank(teams[1])
         if r1 < r2:
            goal_sum[0] *= self.not_played_bonus
            if DEBUG: print '\033[1;32m+ not_played_bonus: \033[1;m' + str(goal_sum)
         elif r2 < r1:
            goal_sum[1] *= self.not_played_bonus
            if DEBUG: print '\033[1;32m+ not_played_bonus: \033[1;m' + str(goal_sum)


      # common bonus to better team (thirds)
      ######################################
      # if the teams are in a different third of the 'ewige tabelle',
      # give the better team a bonus
      rank_team1 = self.pred.get_rank(teams[0])
      rank_team2 = self.pred.get_rank(teams[1])

      if rank_team1 < rank_team2:
         goal_sum[0] *= self.rank_bonus
         if DEBUG: print '\033[1;32m+ rank_bonus \033[1;m' + \
                self.pred.get_team_name(teams[0]) + ': '  + str(goal_sum)
      elif rank_team2 < rank_team1:
         goal_sum[1] *= self.rank_bonus
         if DEBUG: print '\033[1;32m+ rank_bonus \033[1;m' + \
                self.pred.get_team_name(teams[0]) + ': '  + str(goal_sum)


      # this season bonus
      ###################
      # when x games won in series, give bonus
      rg_t0 = self.pred.get_recent_games(teams[0], self.n_recent_games)
      rg_t1 = self.pred.get_recent_games(teams[1], self.n_recent_games)

      out_temp = 0
      if self.pred.winning_streak(teams[0], rg_t0):
         goal_sum[0] *= self.recent_games_bonus
         out_temp = 1
      if self.pred.winning_streak(teams[1], rg_t1):
         goal_sum[1] *= self.recent_games_bonus
         out_temp = 1

      if out_temp:
         if DEBUG: print '\033[1;32m+ ' + self.this_year + \
                ' winning_streak_bonus \033[1;m' + str(goal_sum)

         
      # give bonus to team which is ranked higher in current season
      ladder = self.pred.generate_ladder_list()
      group_t1 = self.pred.get_ladder_group(teams[0], ladder)
      group_t2 = self.pred.get_ladder_group(teams[1], ladder)

      out_ladder = 0
      if group_t1 < group_t2:
         goal_sum[0] *= self.current_ladder_bonus
         out_ladder = 1
      elif group_t2 < group_t1:
         goal_sum[1] *= self.current_ladder_bonus
         out_ladder = 1

      if DEBUG: 
         if out_ladder:
            print '\033[1;32m+ current_ladder_bonus (' + \
             str(group_t1) + '~' + str(group_t2) + '): \033[1;m' + str(goal_sum)


      # calculate diff and goal mean
      ##############################
      goal_diff = goal_sum[0] - goal_sum[1]
      # if teams played each other:
      if goal_sum[2] != 0:
         goal_mean = [goal_sum[0]/goal_sum[2], goal_sum[1]/goal_sum[2]]


      # output and debug
      ##################
      if goal_diff > 0:
         if DEBUG: print self.pred.get_team_name(teams[0]) + ' better. ' + 'diff: ' + str(goal_diff)
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
         if DEBUG: print self.pred.get_team_name(teams[1]) + ' better. ' + 'diff: ' + str(goal_diff)
         if DEBUG: print '\033[1;31mprediction: \033[1;m ' + str(goal_mean[0]) + ':' + \
                str(goal_mean[1])
         print str(teams[0]) + ' ' + str(teams[1]) + ' ' \
             + str(int(goal_mean[0])) + ' ' + str(int(goal_mean[1]))



   # add new scores and recalculate the stats
   def add_and_do_magic(self, team, gameday):
      # convert to ints
      teams = [int(team[0]), int(team[1]), int(team[2]), int(team[3])]
      # insert into database of 2009
      self.data.kreuz2009[teams[0]][teams[1]] = (teams[2], teams[3])
      # pickle 2009 database
      self.data.save_data()

      # add to recent scores
      try:
         # own score is the first score
         if len(self.data.recent_games[ teams[0] ]) < gameday:
            self.data.recent_games[teams[0]].insert(0, [teams[2], teams[3]])
            self.data.recent_games[teams[1]].insert(0, [teams[3], teams[2]])
            self.data.save_recent()

            # update ladder
            if teams[2] > teams[3]:
               self.data.ladder[teams[0]] += 3
            elif teams[3] > teams[2]:
               self.data.ladder[teams[1]] += 3
            else:
               self.data.ladder[teams[0]] += 1
               self.data.ladder[teams[1]] += 1
            self.data.save_ladder()

         else:
            if DEBUG: print 'gameday ' + str(gameday) + ' schon eingetragen'

      except KeyError:
         print 'KeyError in add_and_do_magic'



   def main(self):            
      # sys args
      if len(sys.argv) != 3:
         print 'arguments wrong. major fuck up detected! called stop() (hammertime!)'
         print 'Usage: ' + sys.argv[0] + ' --predict <gameday> <input'
         print 'Usage: ' + sys.argv[0] + ' --verify <gameday> <input'
         sys.exit(1)
      else:
         mode = sys.argv[1]
         gameday = int(sys.argv[2])

      # read input
      input = sys.stdin.readlines()

      if mode == '--predict':
         # calculate every match
         for i in input:
            match = i.replace('\n', '').split(' ')

            # classic plus bonus method
            self.classic_plus(match)

      # classic mode, secret things are happening here
      elif mode == '--predict2':
         for i in input:
            match = i.replace('\n', '').split(' ')

            # classic method, plain and stupid
            self.classic(match)

      # verify last gameday and enter scores to database
      elif mode == '--verify':
         for i in input:
            match = i.replace('\n', '').split(' ')

            # add live scores to the database and recalculate
            self.add_and_do_magic(match, gameday)

      else:
         print 'ERROR: arguments not recognized.\ndefault method called: solving the answer to the life, the universe and everything. come back in 7.5 million years. and thanks for all the fish!'


if __name__ == '__main__':
   main = Main()
   main.main()
