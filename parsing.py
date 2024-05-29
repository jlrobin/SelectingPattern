#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import json

BASEPATH = os.path.dirname(os.path.abspath(__file__))

from ArticutAPI import Articut
BASEPATH = os.path.dirname(os.path.abspath(__file__))

userDICT = json.load(open(f"{BASEPATH}/account.info", encoding="utf-8"))
username = userDICT["username"]
apikey = userDICT["articut_key"]
articut = Articut(username=username, apikey=apikey, version="v270", level="lv2")



if __name__ == "__main__":

    AllCommentLIST = json.load(open(f"{BASEPATH}/AllCommentLIST.json", "r", encoding="UTF-8"))

    #多加一個 commentLIST 每個 dict 中多一個 key==> res_pos_str
    for post in AllCommentLIST:
        commentLIST = post["commentLIST"]
        for com_d in commentLIST:
            com_d["res_pos_str"] = ""


    # 開始用 Articut 將 comment 斷詞/ 標記上詞性
    for i in range(len(AllCommentLIST)):
        print(i)
        commentLIST = AllCommentLIST[i]["commentLIST"]
        for com_d in commentLIST:
            comment = com_d["comment"]
            try:
                resultDICT = articut.parse(comment)
                if resultDICT["status"]:
                    resPosSTR = "".join(resultDICT["result_pos"])
                    com_d["res_pos_str"] = resPosSTR
            except:
                print("NUM")
                print(f"Error ==> {i}")


    # 將結果存起來
    with open(f"{BASEPATH}/AllCommentLIST_parse.json", "w", encoding="UTF-8") as f:
        json.dump(AllCommentLIST, f, ensure_ascii=False, indent=4)



