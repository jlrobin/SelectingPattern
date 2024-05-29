#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from requests import post
import json
import os, sys

from ArticutAPI import Articut
from pprint import pprint
import re

COREPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
userDICT = json.load(open(f"{COREPATH}/ArticutClass/account.info", encoding="utf-8"))

puncLIST = ["！","，","。","？","!",",","\n","；","\u3000",";", "…", " "]
puncPat = re.compile("[{}]+".format("".join(puncLIST)))


username = userDICT["username"] #這裡填入您在 https://api.droidtown.co 使用的帳號 email。若使用空字串，則預設使用每小時 2000 字的公用額度。
apikey   = userDICT["articut_key"] #這裡填入您在 https://api.droidtown.co 登入後取得的 api Key。若使用空字串，則預設使用每小時 2000 字的公用額度。
articut = Articut(username, apikey)


def text2LIST(inputSTR):
    '''
    Converting CV string into a list of sentences.
    '''
    cvLIST = list(filter(None, puncPat.sub("\n", inputSTR).split("\n")))
    return cvLIST





if __name__ == "__main__":

    inputSTR = """
    本週三在紐約的比賽中，馬林魚此戰使用投手車輪戰，4名投手輪番上陣壓制大都會打線，前8局僅被敲出4支安打失1分，讓球隊能帶著2-1的領先優勢進入到9局下半。不過馬林魚推出巴斯登板關門，他面對首名打者麥尼爾，就被打出一發陽春砲，讓大都會追平比數，接下來又分別被敲出2支安打、投出保送，形成滿壘局面，此時輪到康福托上場打擊。在2好1壞的局面下，巴斯投了一顆內角滑球，康福托眼看這顆球越來越	靠近自己的身體，似乎有下意識地將手伸進好球帶內，結果這球就直接碰觸到他的身肘，隨後主審庫爾帕判定這是一記觸身球，讓大都會兵不血刃拿下再見分，最終贏得比賽勝利。
    """

    #inputSTR = "本週三在紐約的比賽中"


    inputLIST = text2LIST(inputSTR)
    print(inputLIST)
    print(len(inputLIST))


    resultDICT = {}
    #for text in saveLIST[i]:
    for text in inputLIST:
        print(text)

        response = articut.parse(text, level="lv2")
        pprint(response)

        if response["status"]:
            resultDICT[text] = "".join(response["result_pos"])

    pprint(resultDICT)
