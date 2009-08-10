#!/usr/bin/env python
# -*- coding: utf-8 -*-
from suds.client import Client
import sys, codecs
import cPickle as pickle


def kreuz_pickle():
    kreuz = {65: {},123: {},83: {},6: {},87: {},7: {},91: {},93: {},40: {},9: {},100: {},55: {},54: {},105: {},16: {},129: {},131: {},134: {},79: {},102: {},107: {},81: {},23: {},76: {},112: {},}

    # soap kram
    url = 'http://www.openligadb.de/Webservices/Sportsdata.asmx?WSDL'
    client = Client(url)
    
    # vars
    spieltage = int(sys.argv[1])
    jahr = int(sys.argv[2])
    liga = 'bl1'
        
    # daten lesen
    for st in range(1, spieltage+1):
        result = client.service.GetMatchdataByGroupLeagueSaison(st, liga, jahr)
        for spiel in result[0][:]:
            id1 = spiel.idTeam1
            pt1 = spiel.pointsTeam1
            id2 = spiel.idTeam2
            pt2 = spiel.pointsTeam2
            kreuz[id1][id2] = (pt1, pt2)

    filename = 'kreuz' + str(jahr) + '.pkl'
    out_file = open(filename, 'wb')
    pickle.dump(kreuz, out_file)


def main():
    # stdout oder fileoutput
    if len(sys.argv) == 4:
        fd = codecs.open(sys.argv[3], mode='w', encoding='latin-1')
    elif len(sys.argv) == 3:
        sys.stdout = codecs.getwriter('utf8')(sys.stdout)
        fd = sys.stdout    
    
    kreuz_pickle()
    


# main call und argumente prüfen
if __name__ == "__main__":
    if len(sys.argv) not in (3,4):
        sys.exit("Usage: " +sys.argv[0]+ " <spieltage> <jahr> [<outfile>]")
    else:
        main()



# beispieldatensatz
# >>> result[0][0]
# (Matchdata){
#    matchID = 1978
#    matchDateTime = 2008-08-15 20:30:00
#    groupID = 235
#    groupOrderID = 1
#    groupName = "1. Spieltag"
#    leagueID = 18
#    leagueName = "1. Fussball-Bundesliga 2008/2009"
#    leagueSaison = "2008"
#    nameTeam1 = "FC Bayern München"
#    nameTeam2 = "Hamburger SV"
#    idTeam1 = 40
#    idTeam2 = 100
#    iconUrlTeam1 = "http://www.openligadb.de/images/teamicons/Bayern_Muenchen.gif"
#    iconUrlTeam2 = "http://www.openligadb.de/images/teamicons/Hamburger_SV.gif"
#    pointsTeam1 = 2
#    pointsTeam2 = 2
#    lastUpdate = 2008-10-02 22:19:09.290000
#    matchIsFinished = True
#    matchResults = 
#       (matchResults){
#          matchResult[] = 
#             (matchResult){
#                resultName = "Endergebnis"
#                pointsTeam1 = 2
#                pointsTeam2 = 2
#                resultOrderID = 1
#             },
#       }
#  }
