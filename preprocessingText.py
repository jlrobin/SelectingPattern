#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import json
import re
from pprint import pprint

titleNtimePAT = re.compile("(.+)時間([a-zA-Z]{3}\s[a-zA-Z]{3}\s\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\s\d{4})") #u)看板Gossiping標題Re: (問題)華航空難留言時間Mon Jun 20 07:28:27
opinionTagNameIDPAT = re.compile("([推噓→])\s([A-z0-9]+)[:：]([一-龥\s]+)(\s\d+.\d+.\d+.\d+\s\d{2}/\d{2})") #推 nori:樓上的 請解釋 140.113.4.15 06/20

endingFull = re.compile("--\s※\s發信站:\s批踢踢實業坊\(ptt\.cc\)\s◆\sFrom:\s\d+\.\d+\.\d+\.\d+") #-- ※ 發信站: 批踢踢實業坊(ptt.cc) ◆ From: 61.62.240.128
endingMissingNum = re.compile("--\s※\s發信站:\s批踢踢實業坊\(ptt\.cc\)\s◆\sFrom:\s\d+\.\d+\.\d+") #-- ※ 發信站: 批踢踢實業坊(ptt.cc) ◆ From: 218.162.7
endingMissingHalf = re.compile("--\s※\s發信站:\s批踢踢實業坊\(p") #-- ※ 發信站: 批踢踢實業坊(p


SayPAT = re.compile("說[：:]")

BASEPATH = os.path.dirname(os.path.abspath(__file__))

def separateTitleNFullComment(Lines):
    """
    將語料中的 title (在奇數行) 和 full comment (在偶數行) 分開儲存
    """
    count = 0
    titleLIST = []
    contentLIST = []
    # Strips the newline character
    for line in Lines:
        count += 1
        #print(count % 2)
        if count % 2 != 0:
            #print("Line{}: {}".format(count, line.strip()))
            titleLIST.append(line)
        else:
            #print("Line{}: {}".format(count, line.strip()))
            contentLIST.append(line)
    return titleLIST, contentLIST

def getOpinionNameCommentID(fullCommentDICT, content):
    """
    將 full comment (留言) 中的 人 (person)、opinion tag (推或是噓), 留言 (comment), 和 id 儲存下來
    如果只有 comment ，就只存 comment
    """
    for pat in opinionTagNameIDPAT.finditer(content): #content ==> contentLIST[i]
        commentDICT = {
                "person": "",
                "opinion_tag": "",
                "comment": "",
                "id": "",
            }
        commentDICT["person"] = pat.group(2)
        commentDICT["opinion_tag"] = pat.group(1)
        commentDICT["comment"] = pat.group(3)
        commentDICT["id"] = pat.group(4)
        fullCommentDICT["commentLIST"].append(commentDICT)

    commentDICT = {
            "person": "",
            "opinion_tag": "",
            "comment": "",
            "id": "",
        }
    realContent = titleNtimePAT.sub("", content)
    realContent = opinionTagNameIDPAT.sub("", realContent)
    commentDICT["comment"] = realContent
    fullCommentDICT["commentLIST"].append(commentDICT)
    return fullCommentDICT

def getNoNameComment(fullCommentDICT, content):
    """
    如果留言本身就沒有 person, id, opinion tag
    但是有冒號，那就用冒號來區分不同的留言
    """
    realContentSTR = titleNtimePAT.sub("", content)
    realContentSTR = SayPAT.sub("sAY", realContentSTR)
    comLIST = realContentSTR.split(":")
    fullCommentDICT["commentLIST"] = []
    for i in range(len(comLIST)):
        comLIST[i] = comLIST[i].replace("sAY", "說:")
        commentDICT = {
                "person": f"comment_{i}",
                "opinion_tag": "",
                "comment": "",
                "id": "",
            }
        commentDICT["comment"] = comLIST[i]
        fullCommentDICT["commentLIST"].append(commentDICT)

    return fullCommentDICT


if __name__ == "__main__":

    # 用 readlines() 來讀檔，所以偶數行和奇數行可以分開儲存
    file1 = open(f"{BASEPATH}/Gossiping1-10.txt", encoding="UTF-8")
    Lines = file1.readlines()

    # 將標題和 留言內容存起來
    titleLIST, contentLIST = separateTitleNFullComment(Lines)


    AllCommentLIST = []

    for i in range(len(contentLIST)):
        fullCommentDICT = {
            "title": "",
            "time": "",
            "commentLIST": [],
            "serial_num": "",
        }

        #刪掉明顯不是留言的內容
        contentLIST[i] = endingFull.sub("", contentLIST[i])
        contentLIST[i] = endingMissingHalf.sub("", contentLIST[i])
        contentLIST[i] = endingMissingNum.sub("", contentLIST[i])

        print(i)

        #如果留言只有「此區域為限制級」的內容，那就只把這部分內容存起來
        if "此區域為限制級" in contentLIST[i]:
            commentDICT = {
                "person": "",
                "opinion_tag": "",
                "comment": contentLIST[i],
                "id": "",
            }
            fullCommentDICT["commentLIST"] = [commentDICT]
            fullCommentDICT["serial_num"] = i
            AllCommentLIST.append(fullCommentDICT)
            continue

        # 取得留言中的 title, time; 另外把語料中的留言按處理順序儲存其序號 (e.g., 處理的第一個留言就是第 0 則 留言)
        fullCommentDICT["title"] = titleNtimePAT.search(contentLIST[i]).group(1)
        fullCommentDICT["time"] = titleNtimePAT.search(contentLIST[i]).group(2)
        fullCommentDICT["serial_num"] = i
        #print(fullCommentDICT)

        try:
            # 如果留言中有出現 opinion tag, person, id 等資訊，就把 opinion tag, person, id 等資訊都存起來
            if opinionTagNameIDPAT.search(contentLIST[i]):
                fullCommentDICT = getOpinionNameCommentID(fullCommentDICT, contentLIST[i])
                AllCommentLIST.append(fullCommentDICT)

            # 如果沒有出現 opinion tag, person, id 等資訊，就把留言用冒號分開，然後依序儲存
            else:
                fullCommentDICT = getNoNameComment(fullCommentDICT, contentLIST[i])
                AllCommentLIST.append(fullCommentDICT)

        except:
            print("NUMBER")
            print(i)

    # 把結果存起來
    with open(f"{BASEPATH}/AllCommentLIST.json", "w", encoding="UTF-8") as f:
        json.dump(AllCommentLIST, f, ensure_ascii=False, indent=4)








