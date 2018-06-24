import os
import time
import json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PICKLE_DIR = BASE_DIR + '/toolkit/pickle'
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


def getSynonyms():
    # pickle
    import pickle
    SYNONYMS_FILE = open(PICKLE_DIR + '/synonyms.pickle', "rb+")
    SYNONYMS = pickle.load(SYNONYMS_FILE)
    return SYNONYMS


def getOntology():
    import pickle
    ONTOLOGY_FILE = open(PICKLE_DIR + '/ontology_keywords.pickle', "rb+")
    ONTOLOGY = pickle.load(ONTOLOGY_FILE)
    return ONTOLOGY


def getAttr():
    import pickle
    ATTR_FILE = open(PICKLE_DIR + '/attr_keywords.pickle', "rb+")
    ATTR = pickle.load(ATTR_FILE)
    return ATTR


def getWord2Vec():
    # word2vec
    import gensim
    WORD2VECMODEL = gensim.models.Word2Vec.load(BASE_DIR+"/toolkit/wordVec/faq/faq_origin.model")
    WORD2VECMODEL.init_sims(replace=True)
    return WORD2VECMODEL


def setJieba():
    # jieba
    import jieba
    jieba.load_userdict(BASE_DIR + "/toolkit/chinese/candidatesAll.txt")


if __name__ == "__main__":
    config = getConfig()
    print(config)
