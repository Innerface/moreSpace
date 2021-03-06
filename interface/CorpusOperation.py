# Author: YuYuE (1019303381@qq.com) 2018.03.
import os
import re
import docx


def CorpusReform(in_dir, out_dir='./data/corpus.txt', operation=0):
    titles = []
    dict_path = './data/dict.txt'
    f_dict = open(dict_path, 'a', encoding="utf-8")
    for root, dirs, files in os.walk(in_dir):
        for file in files:
            title = os.path.splitext(file)[0]
            titles.append(title)
            print('title', title)
            if len(title) < 6:
                f_dict.write(title + '\n')
            if os.path.splitext(file)[1] == '.txt':
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                with open(out_dir, "a", encoding="utf-8") as f_w:
                    for line in lines:
                        matchStep1 = re.search(r'[！。？]', line)
                        if matchStep1:
                            print('matchStep1', matchStep1.group())
                            sentences = line.split(str(matchStep1.group()))
                            for sentence in sentences:
                                sentence = sentence.replace('　', '')
                                sentence = sentence.replace('\t', '')
                                sentence = sentence.replace('\n', '')
                                if operation == 0:
                                    matchStep2 = re.search(r'[~@#￥%&]', sentence)
                                else:
                                    matchStep2 = re.search(r'[~@#￥%…&{《●]', sentence)
                                if matchStep2:
                                    print('matchStep2', matchStep2.group())
                                    pass
                                else:
                                    if len(sentence) < 3:
                                        continue
                                    f_w.write(sentence + str(matchStep1.group()) + "\n")
                        else:
                            print('NoSence Sentence')
                            pass
    return titles


def getatt(para):
    line = para.text
    if re.match(u'第.+章', line):
        return 0
    if re.match(u'\d\.\d(?=[^\.])', line) \
            or re.match(u'\d\. \d(?=[^\.])', line) \
            or re.match(u'\d\d\.\d(?=[^\.])', line):
        return 1
    if re.match(u"^\d\.+?\d.+?\d", line) or re.match(u"^\d\. \d \.\d", line):
        return 2
    if re.match(u"\d+\.", line) or re.match(u"\d+ \.", line) or re.match(u"\d+．", line):
        return 3
    if re.match(u"\([一二三四五六七八九十]\)*", line) or re.match(u"（[一二三四五六七八九十]）", line):
        return 4
    if re.match(u"[一二三四五六七八九十]+、", line):
        return 5
    if re.match(u"\([0-9]\)*", line) or re.match(u"\s*（[0-9]+）", line) or re.match(u"\.[0-9]+", line):
        return 6
    if re.match(u"第[一二三四五六七八九十]+.*", line):
        return 7
    if re.match(u"\s{4}[a-zA-Z]+\.+", line) or re.match(u"\s{4}[a-zA-Z]+．+", line) or re.match(u"[a-zA-Z]．+", line):
        return 8
    if re.match(u'■\s* ', line):
        return 9
    return 10


def CorpusReformDoc(file_dir, operation=0):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            title = os.path.splitext(file)[0]
            print(title)
            L.append(title)
            if os.path.splitext(file)[1] == '.docx':
                file_path = os.path.join(root, file)
                if operation == 0:
                    file_out = os.path.join('./data/', 'corpusDoc.txt')
                else:
                    file_out = os.path.join('./data/', title + '.txt')
                try:
                    f = docx.Document(file_path)
                    lines = f.paragraphs
                except Exception as error:
                    print('Exception', error)
                    continue
                else:
                    j = 0
                    pretext = ''
                    with open(file_out, "a", encoding="utf-8") as f_w:
                        for i, line in enumerate(lines):
                            if len(line.text) < 3:
                                continue
                            num = getatt(line)
                            if num < 10:
                                # print('num', i, pretext)
                                if len(pretext) > 3:
                                    f_w.write(pretext + '\n')
                                j += 1
                                pretext = line.text
                                if pretext[-1] != "->" and getatt(lines[1+1]) != 10:
                                    pretext += "->"
                                continue
                            else:
                                pretext += line.text

                        # print('num', i, pretext)
                        if len(pretext) > 3:
                            f_w.write(pretext + '\n')
            exit()
    return L


def CorpusReformAdvanced():
    pass


def CorpusReformDocAdvanced(context, file_path=None):
    QA_pairs = {}
    try:
        if file_path is not None:
            context = open(file_path, 'r', encoding='utf-8').readlines()
        if context:
            for i, text in enumerate(context):
                print(text)
    except Exception as error:
        print('Exception', error)
        raise Exception("Exception:", error)
    else:
        return QA_pairs


if __name__ == "__main__":
    # dir_path = './file_set_all'
    # dir_path = './corpus/bank'
    # result = CorpusReform(dir_path)
    dir_path = './test'
    # result = CorpusReformDoc(dir_path, 1)
    result = CorpusReformDocAdvanced('', './data/2012银行从业资格考试教材【风险管理】.txt')
    print(result)
