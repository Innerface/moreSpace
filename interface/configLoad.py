import os
import time
import json

baseDir = os.path.dirname(os.path.abspath(__file__))
configPath = os.path.dirname(baseDir) + '/.env'
timeInfo = time.strftime('%Y-%m-%d', time.localtime(time.time()))
configDict = {}


def log(message, tag='getConfig', type_='error'):
    if type_ == "error":
        logPath = baseDir + '/log/error.python.log'
    else:
        logPath = baseDir + '/log/access.python.log'
    handle = open(logPath, 'a', encoding='utf-8')
    message = timeInfo + "\t" + tag + "\t" + message
    handle.write(message)


def getConfig():
    if os.path.exists(configPath) is False:
        log("Error: Config Missing", 'getConfig')
        return configDict
    with open(configPath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if line and line.find('=') != -1:
                temp = line.split('=')
                if temp[0] and temp[0] not in configDict:
                    value = temp[1].replace("\n", '')
                    configDict[temp[0]] = value
    log(json.dumps(configDict), 'getConfig', 'access')
    return configDict


if __name__ == "__main__":
    config = getConfig()
    print(config)
