try: # if intalling brawlPY from pip, this should happen automatically
    from dotenv import load_dotenv
    from requests import get
except ImportError:
    raise ImportError("Unable to find requests and dotenv library: Use pip to download these libraries")
import os

class AuthorizationError(Exception):
    pass

class APIClient:
    def __init__(self, key: str = None):
        # looks for api key in .env file and if there is no key provided in param
        load_dotenv()
        self.key = os.getenv("API_KEY") or key
        if not self.key:
            raise ValueError("Unable to access .env file: please provide API key")
    
    def __get_json(self, url: str):
        # using the requests library, attempts to access the data from the url given as a param
        responce = get(url, headers = {"Authorization": f"Bearer {self.key}"})

        # status code 200 is given when the data is successfully sent to the user
        if responce.status_code == 200:
            return responce.json()
        else:
            raise AuthorizationError(responce.json())
    
    # methods that return json of specific data from the api. some of these are useless i know
    def get_brawler_list(self):
        return self.__get_json("https://api.brawlstars.com/v1/brawlers")

    def get_brawler_info(self, tag: str):
        return self.__get_json(f"https://api.brawlstars.com/v1/brawlers/{tag}")

    def get_club_info(self, tag: str):
        return self.__get_json(f"https://api.brawlstars.com/v1/clubs/%23{tag}")

    def get_club_members(self, tag: str):
        return self.__get_json(f"https://api.brawlstars.com/v1/clubs/%23{tag}/members")

    def get_event_list(self):
        return self.__get_json("https://api.brawlstars.com/v1/events/rotation")

    def get_player_battlelog(self, tag: str):
        return self.__get_json(f"https://api.brawlstars.com/v1/players/%23{tag}/battlelog")

    def get_player_info(self, tag: str):
        return self.__get_json(f"https://api.brawlstars.com/v1/players/%23{tag}")

class Player:
    def __init__(self, tag: str, client: APIClient):
        # stores all data for specific player
        self.__json = client.get_player_info(tag)

        # creates a class for each brawler that is available in the "brawler" section of the player's json file
        self.brawler = {brawler["name"].lower(): self.Brawler(brawler) for brawler in self.__json["brawlers"]}

    def getName(self) -> str: # returns a string of the nickname that the player is using
        return self.__json["name"]
    
    def getTrophies(self) -> int: # returns an integer of the current amount of trophies
        return self.__json["trophies"]
    
    def getExpLevel(self) -> int: # returns an integer of the current level
        return self.__json["expLevel"]
    
    def getExpPoints(self) -> int: 
        return self.__json["expPoints"]
    
    def getHighestTrophies(self) -> int: # returns an integer the highest trophy count
        return self.__json["highestTrophies"]
    
    def isQualifiedFromChampionshipChallenge(self) -> bool: # returns a boolean 
        return self.__json["isQualifiedFromChampionshipChallenge"]
    
    def getThreeVictories(self) -> int: # returns an integer of current total of 3v3 victories
        return self.__json["3vs3Victories"]

    def getSoloVictories(self) -> int: # returns an integer of current total of solo showdown victories
        return self.__json["soloVictories"]
    
    def getDuoVictories(self) -> int: # returns an integer of current total of duo showdown victories
        return self.__json["duoVictories"]
    
    def getBestRoboRumbleTime(self) -> int: 
        return self.__json["bestRoboRumbleTime"]
    
    def getBestTimeAsBigBrawler(self) -> int:
        return self.__json["bestTimeAsBigBrawler"]

    def getNameColor(self): # returns a color code of the user's name color
        try:
            return self.__json["nameColor"]
        except KeyError:
            return None

    class Brawler:
        def __init__(self, json):
            self.__json = json
        
        def getId(self): # returns the ID of the brawler
            return self.__json["id"]
        
        def getPower(self):
            return self.__json["power"]
        
        def getRank(self): # returns an integer of the current rank of the brawler
            return self.__json["rank"]
        
        def getTrophies(self): # returns an integer of the current total trophies of the brawler
            return self.__json["trophies"]
        
        def getHighestTrophies(self): # returns an integer of the highest amount of trophies of the brawler
            return self.__json["highestTrophies"]
        
        def getGears(self): # returns a dictionary with the gears the player has for the brawler
            return self.__json["gears"]
        
        def getStarPowers(self): # returns a dictionary with the star powers the player has for the brawler
            return self.__json["starPowers"]
        
        def getGadgets(self): # returns a dictionary with the gadgets the player has for the brawler
            return self.__json["gadgets"]
        
class Club:
    def __init__(self, tag: str, client: APIClient):
        self.__json = client.get_club_info(tag)
    
    def getName(self): # returns a string of the club name
        return self.__json["name"]
    
    def getDescription(self): # returns a string of the club description
        return self.__json["description"]
    
    def getTrophies(self): # returns the total trophies of the club
        return self.__json["trophies"]
    
    def getRequiredTrophies(self): # returns the required amount of trophies to get in the club
        return self.__json["requiredTrophies"]
    
    def getMembers(self): # returns a list of the players in the club
        return self.__json["members"]
    
    def getType(self):
        return self.__json["type"]
    
    def getBadgeId(self):
        return self.__json["badgeId"]