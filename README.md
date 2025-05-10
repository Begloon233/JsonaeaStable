<img src=https://github.com/Begloon233/JsonaeaStable/blob/main/imgs/jsonaea.png/>  

# 简介
>*由于前移动设备丢失，主播无法登录原来发布jsonaea项目的账号，所以在此开新项目进行更新/维护。*  
>*前jsonaea项目：[Github](https://github.com/321bug/Jsonaea/tree/main)*   
  
**Jsonaea**为可将Arcaea游戏中铺面文件（``x.aff``）转换为json文件 / 字典，亦可将json文件 / 字典转换回铺面文件的实用库。  
此库使用``Python``编写。  
此库还有一个``Tools``附加库，内含多种不必要但减少代码量的实用函数。  
有关库函数的详细说明等请前往此页面：[Wiki界面](https://github.com/Begloon233/JsonaeaStable/wiki)
  
## 快速使用
打开命令栏，输入以下指令以安装Jsonaea  
```cmd
pip install jsonaea
```
  
如要更新Jsonaea，请输入以下指令
```cmd
pip install --upgrade jsonaea
```

在py文件中导入库：  
```python
import jsonaea
```
使用load函数生成字典：
```python
load(arcPath)
```
``arcPath``: Arcaea铺面文件导入路径  
此函数将返回一个字典。

使用createJson函数生成json文件:
```python
createJson(dict,JsonPath)
```
`dict`:创建json文件的字典  
`JsonPath`:创建json文件的路径
此函数不返回值，会创建一个json文件。  

导出生成的json文件 / 字典为``.aff``文件：
```python
output(arcJson,arcPath)
```
``arcJson``: 提供的json文件（字典）  
``arcPath``: Arcaea铺面文件导出路径  
此函数不返回值，会创建一个``.aff``文件。
### 示例
jsonaea库使用的具体示例，以下代码可将铺面中的arc全部转化为蛇：  
```python
import tkinter as tk
from tkinter import filedialog
from jsonaea import *

#生成铺面导入窗口
root = tk.Tk()
root.withdraw () 
arcPath = filedialog.askopenfilename () 

#导入铺面
arc = load(arcPath)
#设置Tools库全局变量
Tools.arcJson = arc
#检索所有黑线事件
searchedEvent = Tools.searchEventSubject({"type":"arc","IsSkyline": True})
#并将其全部转化为蛇
for se in searchedEvent:
    Tools.changeEvent(se,{"IsSkyline":False})
#导出铺面
output(arc,"./noSkyline.aff")
#导出处理完的Json文件
createJson(arc, "./this.json")
input("已完成")
```
# 支持的谱面信息
**Jsonaea**目前支持的谱面信息有：
- 不含float轨道参数的tap
- 不含float轨道参数的hold
- 所有arc语句（含0123四色）
- 所有timing语句
- 所有camera语句
- 所有scenecontrol语句
- 不同时间组以及标记（如noinput）
- 谱面前元信息（如offset）

特别地，**Jsonaea**目前**不支持**的谱面信息如下：
- 含float轨道参数的tap
- 所有flick语句
- 所有谱面注释
- switch版Arcaea的note染色

# json文件 / 字典格式
```json
{
  "META":{},
  "Camera":[],
  "Scenecontrol":[],
  "TimingList":[
    {
      "tags":[],
      "notes":[],
      "timing":[],
    }
  ]
}
```
- META字典：  
  存储铺面文件头，如:
  ```json
  "AudioOffset": 0,
  "TimingPointDensityFactor":2
  ```
- Camera列表：  
  存储铺面摄像头信息，如：
  ```json
  "time": 0,
  "transverse": 0.0,
  "bottomzoom": 0.0,
  "linezoom": 0.0,
  "steadyangle": 0.0,
  "topzoom": 0.0,
  "angle": 0.0,
  "easing": "reset",
  "lastingtime": 1
  ```
  详见 [ARCAEA中文维基](https://wiki.arcaea.cn/) 中对谱面格式的介绍  
  多个字典以列表形式存储

- Scenecontrol列表：
  存储铺面Scenecontrol事件信息，如：
  ```json
  "time": 0,
  "type": "arcahvdistort",
  "param": [
    1.25,
    0
  ]
  ```
  其中``"param"``项在没有参数时不会生成，详见 [ARCAEA中文维基](https://wiki.arcaea.cn/) 中对谱面格式的介绍  
  多个字典以列表形式存储
- TimingList列表：
  存储无timinggroup与timinggroup组的事件  
  在该列表中无timinggroup的下标为0，timinggroup组的下标≥1（如果铺面中无timinggroup组，则该列表中只有下标为零的字典）  
  多个字典以列表形式存储，字典中存有key为``"tags"``,``"notes"``与``"timing"``的三个列表  
  当在该列表中下标为0的字典中（即无timinggroup的事件），``"tags"``中无参数。
  - tags
    在aff文件``timinggroup(){};``中小括号中的标识，一般用于对timinggroup中的事件达成特殊效果（如noinput）  
    字典格式如：
      ```json
      "noinput",
      "anglex200"
      ```
      
  - notes  
    note事件，分为``tap``、``hold``、``arc``三个类型，由key值``"type"``区分  
    其中``tap``的字典格式如：
    ```json
    "type": "tap",
    "time": 0,
    "track": 1
    ```
    其中track指轨道，目前无法读取track为小数的tap事件  
    
    其中``hold``的字典格式如：
    ```json
    "type": "hold",
    "startTime": 0,
    "endTime": 1000,
    "track": 3
    ```
    其中track指轨道，目前无法读取track为小数的hold事件  
   
    其中``arc``的字典格式如：
    ```json
    "type": "arc",
    "startTime": 0,
    "endTime": 1000,
    "startPos": [
      0.5,
      1.0
    ],
    "endPos": [
      1.0,
      1.0
    ],
    "arcType": "si",
    "color": "blue",
    "hitsound": "none",
    "IsSkyline": true
    ```
    其中``"startPos"``与``"endPos"``列表中下标为0的参数时坐标x,下标为1的为坐标y  
    ``"arcType"``是指该arc的滑动方式  
    ``"hitsound"``为该arc上arctap的打击音，如果有填以铺面的相对路径，如果没有填none  
    ``"IsSkyline"``为该arc是否为黑线，反之为蛇  
    如果该arc上有arctap，那么将在下方添加键值对，如：  
    ```json
    "arctap": [
       200,
       600
    ]
    ```
    列表中存储着该arc上所有arctap的时间，其范围在startTime与endTime之间  
    
  - timing
    控制铺面的bpm（流速）与beat（小节线）
    其格式如：
    ```json
    "time": 0,
    "BPM": 191.0,
    "metreInfo": 4.0
    ```
    其中``"metreInfo"``是指表示每多少个四分拍为一小节，并出现一条小节线  
    多个字典以列表形式存储  
    
  对以上任何信息如有困惑，详见 [ARCAEA中文维基](https://wiki.arcaea.cn/) 中对谱面格式的介绍。  

# 特别声明
**本项目只对Arcaea铺面文件进行解读，关于Arcaea铺面使用与更改的最终解释权归Arcaea版权方lowiro所有。**  
**任何通过通过本项目对游戏内铺面的改写与本项目无关，一切责任归使用者所有。**  
**本项目版权归程序编写者Begloon(321bug)所有。**
