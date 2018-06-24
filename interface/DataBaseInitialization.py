# Author: YuYuE (1019303381@qq.com) 2018.06.07
import os
import time
import ConfigLoad as configs
import MySQLdb
import redis
from pymongo import MongoClient


baseDir = os.path.dirname(os.path.abspath(__file__))
timeInfo = time.strftime('%Y-%m-%d', time.localtime(time.time()))
configDict = configs.getConfig()
print(configDict)


def initializationMysql():
    conn = MySQLdb.connect(
        host=str(configDict['DB_HOST']),
        port=int(configDict['DB_PORT']),
        user=str(configDict['DB_USERNAME']),
        passwd=str(configDict['DB_PASSWORD']),
        db=str(configDict['DB_DATABASE']),
        charset='utf8')
    cur = conn.cursor()
    return conn, cur


def sqlFilter(sql, max_length=None):
    # dirty_stuff = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%", "$", "(", ")", "%", "@","!"]
    dirty_stuff = ["\"", "\\", "/", "*", "=", "-", "#", ";", "<", ">", "+", "%", "$", "%", "!"]
    for stuff in dirty_stuff:
        sql = sql.replace(stuff, "")
    if max_length is not None:
        sql = sql[:max_length]
    return sql


def dbOperation(sql, conn=None, cur=None):
    operation = ''
    try:
        sql = sqlFilter(sql)
        if sql.find('select') != -1:
            operation = 'select'
        else:
            operation = 'update'
        if sql:
            if conn is None or cur is None:
                conn, cur = initializationMysql()
            print(sql)
            cur.execute(sql)
    except Exception as error:
        print('Exception', error)
        if operation == 'update':
            conn.rollback()
    else:
        if operation == 'update':
            conn.commit()
        return cur.fetchall()


def initializationRedis(database=0):
    redisConn = redis.Redis(
        configDict['REDIS_HOST'],
        configDict['REDIS_PORT'],
        database,
        configDict['REDIS_PASSWORD'])
    return redisConn


def redisOperation(key, type_='get', value=None, expired=3600, redis_conn=None):
    """

    :param key:
    :param type_:  set get
    :param expired:
    :param value:
    :param redis_conn:
    :return:
    """
    try:
        if key is None:
            raise Exception("invalid key!")
        if redis_conn is None:
            redis_conn = initializationRedis()
        if type_ == 'get':
            values = redis_conn.get(key)
        else:
            redis_conn.set(key, value, expired)
            values = {key: value}
    except Exception as error:
        raise Exception("Exception:", error)
    else:
        return values


def redisListOperation(lst, key=None, operation='Lpush', expired=3600, redis_conn=None):
    """

    :param key:
    :param operation: Lpush Rpush Blpop Brpop
    :param expired:
    :param value:
    :param redis_conn:
    :return:
    """
    try:
        if redis_conn is None:
            redis_conn = initializationRedis()
        if operation == 'Lpush':
            if key is None:
                raise Exception('invalid key')
            # 插入到头部
            values = redis_conn.lpush(lst, key)
        elif operation == 'Rpush':
            if key is None:
                raise Exception('invalid key')
            # 插入到尾部
            values = redis_conn.rpush(lst, key)
        elif operation == 'Blpop':
            # 获取第一个
            values = redis_conn.blpop(lst)
        elif operation == 'Brpop':
            # 获取最后一个
            values = redis_conn.brpop(lst)
        else:
            values = {key: value}
    except Exception as error:
        raise Exception("Exception:", error)
    else:
        return values


def initializationMongo(database='local', dataset='log'):
    client = MongoClient(configDict['REDIS_HOST'], configDict['REDIS_PORT'])
    db = client[database]
    db.authenticate(configDict['REDIS_HOST'], configDict['REDIS_PORT'])
    collection = db[dataset]
    return collection


def mongoOperation(value_dict, type_='find', collection=None):
    try:
        if value_dict is None:
            raise Exception("invalid value!")
        if collection is None:
            collection = initializationMongo()
        if type_ == 'find':
            dict_ = collection.find_one(value_dict)
        else:
            collection.insert_one(value_dict)
            dict_ = value_dict
    except Exception as error:
        raise Exception("Exception:", error)
    else:
        return dict_


if __name__ == "__main__":
    sql = "SELECT username FROM admin_users;"
    sql = "INSERT INTO users(name,email) VALUES('YuYuE','YuYuE@inner.com');"
    result = dbOperation(sql)
    print(result)
    key = 'name'
    value = 'YuYuE'
    result = redisOperation(key, 'set', value)
    print(result)
    result = redisOperation(key)
    print(result)
    print('step1', redisListOperation('words', 'one'))
    print('step2', redisListOperation('words', 'two', 'Rpush'))
    print('step3', redisListOperation('words', 'three'))

