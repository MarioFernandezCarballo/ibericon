import requests
import json


def addNewTournament(database, form):
    pass


eventId = "uuoZa6AwEC"
leagueId = "TCGI2aHBcX"
teamId = "JRWxbboEYy"
userId = "0UlBBMiQ5H"

urlEvent = f'https://pnnct8s9sk.execute-api.us-east-1.amazonaws.com/prod/eventplacings?sortAscending=false&eventId={eventId}&leagueId={leagueId}&expand%5B%5D=user&expand%5B%5D=team&expand%5B%5D=army&expand%5B%5D=subFaction&expand%5B%5D=character'
urlUser = f'https://pnnct8s9sk.execute-api.us-east-1.amazonaws.com/prod/eventplacings?sortAscending=false&userId={userId}&leagueId={leagueId}&expand%5B%5D=user&expand%5B%5D=team&expand%5B%5D=army&expand%5B%5D=subFaction&expand%5B%5D=character'
urlFaction = f'https://pnnct8s9sk.execute-api.us-east-1.amazonaws.com/prod/eventplacings?sortAscending=false&userId={eventId}&leagueId={leagueId}&expand%5B%5D=user&expand%5B%5D=team&expand%5B%5D=army&expand%5B%5D=subFaction&expand%5B%5D=character'
urlTeam = f'https://pnnct8s9sk.execute-api.us-east-1.amazonaws.com/prod/eventplacings?sortAscending=false&teamId={teamId}&leagueId={leagueId}&expand%5B%5D=user&expand%5B%5D=team&expand%5B%5D=army&expand%5B%5D=subFaction&expand%5B%5D=character'


data = requests.get(urlEvent)
major = json.loads(data.text)
data = requests.get(urlTeam)
hellfizz = json.loads(data.text)
data = requests.get(urlUser)
nil = json.loads(data.text)


f = "https://pnnct8s9sk.execute-api.us-east-1.amazonaws.com/prod/eventplacings?limit=100&teamId=WcHn0yrvy9&expand%5B%5D=event&expand%5B%5D=user&expand%5B%5D=army&leagueId=TCGI2aHBcX"
g = "https://pnnct8s9sk.execute-api.us-east-1.amazonaws.com/prod/eventplacings?sortAscending=false&eventId=uuoZa6AwEC&leagueId=TCGI2aHBcX&expand%5B%5D=user&expand%5B%5D=team&expand%5B%5D=army&expand%5B%5D=subFaction&expand%5B%5D=character"