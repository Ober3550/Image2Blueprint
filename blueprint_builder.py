import json
import zlib
import base64

class Blueprint:

    def __init__(self,name):
        self.__lowest_entity_id = 0
        self.__bluestring_json = {}
        self.__bluestring_json["blueprint"] = {}
        self.__bluestring_json["blueprint"]["item"] = "blueprint"
        self.__bluestring_json["blueprint"]["label"] = name+" BP Image"
        self.__bluestring_json["blueprint"]["version"] = 68722819072
        self.__bluestring_json["blueprint"]["entities"] = []
        self.__bluestring_json["blueprint"]["tiles"] = []
        self.__bluestring_json["blueprint"]["icons"] = []
        #iconsDict = {}
        #iconsDict["index"] = 1
        #signal = {}
        #signal["type"] = "item"
        #signal["name"] = "transport-belt"
        #iconsDict["signal"] = signal
        #self.__bluestring_json["blueprint"]["icons"].append(iconsDict)
        #self.__bluestring_json["blueprint"]["icons"].append


    def addEntity(self, objectName, position, eType):
        entityToAdd = {}
        entityToAdd["name"] = objectName
        entityToAdd["position"] = {}
        entityToAdd["position"]["x"] = position[0]
        entityToAdd["position"]["y"] = position[1]
        if eType == "entity":
            entityToAdd["entity_number"] = self.__lowest_entity_id
            self.__lowest_entity_id = self.__lowest_entity_id + 1
            entityToAdd["direction"] = 2
            self.__bluestring_json["blueprint"]["entities"].append(entityToAdd)
        elif eType == "tile":
            self.__bluestring_json["blueprint"]["tiles"].append(entityToAdd)
        else:
            return "Uknown entity type for blueprint."
        return 0

    def getBlueprintString(self):
        stringedBlueprint = json.dumps(self.__bluestring_json)
        compressedBlueprint = zlib.compress(stringedBlueprint.encode("utf8"))
        encodedBlueprint = base64.b64encode(compressedBlueprint)
        encodedBlueprint = "0" + encodedBlueprint.decode("utf8")
        return encodedBlueprint

    def getJsonString(self):
        return json.dumps(self.__bluestring_json)
