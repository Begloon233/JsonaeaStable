'''
Jsonaea by Begloon (2025)\n
这是一个可以将Arcaea游戏中谱面文件（*.aff）转换为json类字典，亦可将json类字典转换回谱面文件的实用库。\n
内置了Tools实用库

使用示例::

    >>> import jsonaea
    >>> arcPath = input("Please input path of the chart:")
    >>> J = jsonaea.load(arcPath)
    >>> createJson(J,"./")
    >>> input("Already completed.")
    
'''
import re
from json import dumps
from . import Tools
__script__ = 250509

#纠正对照字典
ArcColor = {
    0:"blue",
    1:"red",
    2:"green",
    3:"white",
    "blue":0,
    "red":1,
    "green":2,
    "white":3
}
Boolean = {
    "true":True,
    "false":False,
    True:"true",
    False:"false"
}

#解读arcaea文件（load函数）
def load(arcPath:str) -> dict:
    """
    使用``load()``来加载Arcaea铺面文件（``x.aff``），并使其转换为json文件（字典）\n
    ``arcPath``: Arcaea铺面文件导入路径\n
    此函数将返回一个字典。
    """
    #json总字典
    ArcJson = {
        "META":{},
        "Camera":[],
        "TimingList":[
            {
                "tags":[],
                "notes":[],
                "timing":[],
                "scenecontrol":[]
            }
        ]
    }

    with open(arcPath,'r') as f:
        data = f.readlines()
        tg = 0    #tg:TimingGroup
        noteNum = 0
        for line in data:
            noteNum += 1
            nl = re.split(':|\\n',line)
            if nl[0] == "-":
                break
            else:
                ArcJson["META"].update({nl[0]:int(nl[1])})
        for lineI,line in enumerate(data):
            if lineI <= noteNum - 1:
                continue
            line = line.strip()
            nl = re.split('\(|\)|,|;|:',line)  #nl:NoteList
            fac = nl[0]
            if fac == "timinggroup":
                tg += 1
                ArcJson["TimingList"].append({
                    "tags":[],
                    "notes":[],
                    "timing":[],
                    "scenecontrol":[]
                })
                tags = nl[1].split("_")
                if tags != [""]:
                    for tag in tags:
                        ArcJson["TimingList"][tg]["tags"].append(tag)
            if fac == "AudioOffset":
                ArcJson["META"].update({"AudioOffset":int(nl[1])})
            if fac == "scenecontrol":
                try:
                    ArcJson["TimingList"][tg]["scenecontrol"].append({
                        "time":int(nl[1]),
                        "type":nl[2],
                        "param":[float(nl[3]),int(nl[4])]
                    })
                except:
                    ArcJson["TimingList"][tg]["scenecontrol"].append({
                        "time":int(nl[1]),
                        "type":nl[2]
                    })
            if fac == "camera":
                ArcJson["Camera"].append({
                    "time":int(nl[1]),
                    "transverse":float(nl[2]),
                    "bottomzoom":float(nl[3]),
                    "linezoom":float(nl[4]),
                    "steadyangle":float(nl[5]),
                    "topzoom":float(nl[6]),
                    "angle":float(nl[7]),
                    "easing":nl[8],
                    "lastingtime":int(nl[9])
                })
            if fac == "timing":
                ArcJson["TimingList"][tg]["timing"].append({
                    "time":int(nl[1]),
                    "BPM":float(nl[2]),
                    "metreInfo":float(nl[3])
                })
            if fac == "":
                ArcJson["TimingList"][tg]["notes"].append({
                    "type":"tap",
                    "time":int(nl[1]),
                    "track":int(nl[2])
                })
            if fac == "hold":
                ArcJson["TimingList"][tg]["notes"].append({
                    "type":"hold",
                    "startTime":int(nl[1]),
                    "endTime":int(nl[2]),
                    "track":int(nl[3])
                })
            if fac == "arc":
                ArcJson["TimingList"][tg]["notes"].append({
                    "type":"arc",
                    "startTime":int(nl[1]),
                    "endTime":int(nl[2]),
                    "startPos":[float(nl[3]),float(nl[6])],
                    "endPos":[float(nl[4]),float(nl[7])],
                    "arcType":nl[5],
                    "color":ArcColor[int(nl[8])],
                    "hitsound":nl[9],
                    "IsSkyline":Boolean[nl[10]]
                })
                if nl[11] == "[arctap":
                    noteNum = len(ArcJson["TimingList"][tg]["notes"])-1
                    i = 11
                    ArcJson["TimingList"][tg]["notes"][noteNum].update({"arctap":[]})
                    while True:
                        ArcJson["TimingList"][tg]["notes"][noteNum]["arctap"].append(int(nl[i+1]))
                        if nl[i+3] == "arctap":
                            i += 3
                        else:
                            break
    return ArcJson

#写入arcaea文件（output函数）
def output(arcJson:dict,arcPath:str):
    '''
    使用``output()``来将json文件（字典）写入Arcaea铺面文件（``x.aff``）中\n
    ``arcJson``: 提供的json文件（字典）\n
    ``arcPath``: Arcaea铺面文件导出路径\n
    此函数不返回值，会创建一个Arcaea铺面文件。
    '''
    with open(arcPath,"w") as f:
        for k,v in arcJson["META"].items():
            f.write("%s:%s\n"%(k,v))
        f.write("JsonaeaVersion:%d\n-\n"%__script__)
        #字典排序
        old_dict0 = []
        #print(arcJson)
        for i in [arcJson["TimingList"][0]["notes"],arcJson["TimingList"][0]["timing"],arcJson["Camera"],arcJson["TimingList"][0]["scenecontrol"]]:
            #print(i)
            for d in i:
                old_dict0.append(d)
        new_dict0 = Tools.sort(old_dict0)
        createJson(new_dict0,"testJJ.json")

        #处理无timinggroup
        for de in new_dict0:    #de:DictEvent
            if "BPM" in de:
                f.write("timing(%r,%.2f,%.2f);\n"%(de["time"],float(de["BPM"]),de["metreInfo"]))
            elif len(de.keys()) == 2:
                f.write("scenecontrol(%r,%s);\n"%(de["time"],de["type"]))
            elif "param" in de:
                f.write("scenecontrol(%r,%s,%.2f,%d);\n"%(de["time"],de["type"],de["param"][0],de["param"][1]))
                
            elif "transverse" in de: 
                f.write("camera(%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f,%s,%d);\n"%(de["time"],de["transverse"],de["bottomzoom"],de["linezoom"],de["steadyangle"],
                de["topzoom"],de["angle"],de["easing"],de["lastingtime"]))
            elif de["type"] == "tap":
                f.write("(%d,%r);\n"%(de["time"],de["track"]))
            elif de["type"] == "hold":
                f.write("hold(%d,%d,%r);\n"%(de["startTime"],de["endTime"],de["track"]))
            elif de["type"] == "arc":
                f.write("arc(%d,%d,%.2f,%.2f,%s,%.2f,%.2f,%d,%s,%s)"%(de["startTime"],de["endTime"],de["startPos"][0],de["endPos"][0],de["arcType"],
                de["startPos"][1],de["endPos"][1],ArcColor[de["color"]],de["hitsound"],Boolean[de["IsSkyline"]]))
                if "arctap" in de and not de["arctap"] == []:
                    f.write("[")
                    for index,i in enumerate(de["arctap"]):
                        f.write("arctap(%d)"%i)
                        try: 
                            de["arctap"][index+1] 
                            f.write(",")
                        except:pass
                    f.write("]")
                f.write(";\n")
        #处理timinggroup
        for index,i in enumerate(arcJson["TimingList"]):
            if index == 0:
                continue
            tags = ""
            for iT,tag in enumerate(i["tags"]):
                tags += tag
                if iT+1 < len(i["tags"]):
                    tags += "_"
            old_dict = []
            f.write("timinggroup(%s){\n"%tags)
            for a in [arcJson["TimingList"][index]["notes"],arcJson["TimingList"][index]["timing"],arcJson["TimingList"][index]["scenecontrol"]]:
                for d in a:
                  old_dict.append(d)
            new_dict = Tools.sort(old_dict)
            for de in new_dict:
                if "BPM" in de:
                    f.write("   timing(%r,%.2f,%.2f);\n"%(de["time"],float(de["BPM"]),de["metreInfo"]))
                elif len(de.keys()) == 2:
                    f.write("   scenecontrol(%r,%s);\n"%(de["time"],de["type"]))
                elif "param" in de:
                    f.write("   scenecontrol(%r,%s,%.2f,%d);\n"%(de["time"],de["type"],de["param"][0],de["param"][1]))
                elif de["type"] == "tap":
                    f.write("   (%r,%r);\n"%(de["time"],de["track"]))
                elif de["type"] == "hold":
                    f.write("   hold(%d,%d,%r);\n"%(de["startTime"],de["endTime"],de["track"]))
                elif de["type"] == "arc":
                    f.write("   arc(%d,%d,%.2f,%.2f,%s,%.2f,%.2f,%d,%s,%s)"%(de["startTime"],de["endTime"],de["startPos"][0],de["endPos"][0],de["arcType"],
                    de["startPos"][1],de["endPos"][1],ArcColor[de["color"]],de["hitsound"],Boolean[de["IsSkyline"]]))
                    if "arctap" in de:
                        f.write("[")
                        for index,i in enumerate(de["arctap"]):
                            f.write("arctap(%d)"%i)
                            try: 
                                de["arctap"][index+1] 
                                f.write(",")
                            except:pass
                        f.write("]")
                    f.write(";\n")
            f.write("};\n")

def createJson(dict,JsonPath:str):
    """
    将字典创建为json文件\n
    `dict`:创建json文件的字典\n
    `JsonPath`:创建json文件的路径\n
    此函数不返回值，会创建一个json文件。
    """
    jsonData = dumps(dict,indent=4)
    w = open(JsonPath,"w")
    w.write(jsonData)
    w.close()
