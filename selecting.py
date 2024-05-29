#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import json
import re

from pprint import pprint
from ArticutAPI import Articut
BASEPATH = os.path.dirname(os.path.abspath(__file__))

userDICT = json.load(open(f"{BASEPATH}/account.info", encoding="utf-8"))
username = userDICT["username"]
apikey = userDICT["articut_key"]
articut = Articut(username=username, apikey=apikey)


geBuTingPAT = re.compile("<(ACTION_verb|VerbP)>[^<]+</(ACTION_verb|VerbP)><(ACTION_eventQuantifier|ENTITY_classifier)>個</(ACTION_eventQuantifier|ENTITY_classifier)>(<(MODIFIER|ModifierP)>不停</(MODIFIER|ModifierP)>|<ENTITY_nouny>不停</ENTITY_nouny>)")

if __name__ == "__main__":

    # 讀檔
    allCommentLIST = json.load(open(f"{BASEPATH}/AllCommentLIST_parse.json"))

    # 找在 PPT 中 「個不停」 所在的 comment
    for comment_d in allCommentLIST:
        commentLIST = comment_d["commentLIST"]
        for com in commentLIST:
            resPosSTR = com["res_pos_str"]
            if geBuTingPAT.search(resPosSTR):
                print(com["comment"])
                #print(com["res_pos_str"])

    # 看看學生的造樣造句是否符合正確 pattern
    studentSTR = "滾個不停"
    #studentSTR = "一個不停"

    studentResPosDICT = articut.parse(studentSTR)
    if studentResPosDICT["status"]:
        studentResPosSTR = "".join(studentResPosDICT["result_pos"])
        print(studentResPosSTR)
        if geBuTingPAT.search(studentResPosSTR):
            print("符合句法")
        else:
            print("不符合句法")


