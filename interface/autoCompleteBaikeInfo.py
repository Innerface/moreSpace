# Author: YuYuE (1019303381@qq.com) 2018.06.07
import os
import time
import configLoad

baseDir = os.path.dirname(os.path.abspath(__file__))
timeInfo = time.strftime('%Y-%m-%d', time.localtime(time.time()))
configDict = configLoad.getConfig()
print(configDict)