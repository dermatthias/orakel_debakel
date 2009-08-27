#!/usr/bin/env python
# -*- coding: utf-8 -*-
from suds.client import Client
import sys, codecs

def main():
    # stdout oder fileoutput
    if len(sys.argv) == 4:
        fd = codecs.open(sys.argv[3], mode='w', encoding='latin-1')
    elif len(sys.argv) == 3:
        sys.stdout = codecs.getwriter('utf8')(sys.stdout)
        fd = sys.stdout
    
    # soap kram
    url = 'http://www.openligadb.de/Webservices/Sportsdata.asmx?WSDL'
    client = Client(url)

    # vars
    liga = sys.argv[1]
    jahr = int(sys.argv[2])

    # daten lesen
    result = client.service.GetTeamsByLeagueSaison(liga, jahr)
    for teams in result[0][:]:
        teamID = teams.teamID
        teamName = teams.teamName
        fd.write(str(teamID) + ' ' + teamName + '\n')

# main call und argumente prüfen
if __name__ == "__main__":
    if len(sys.argv) not in (3,4):
        sys.exit("Usage: " +sys.argv[0]+ " <liga> <jahr> [<outfile>]")
    else:
        if int(sys.argv[2]) not in range(2002, 2010):
            sys.exit("Wert für <jahr> ist quatsch.")
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
