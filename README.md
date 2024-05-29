# 查看學生是否學會「個不停」這種句構
## 檔案介紹
### `account.info`
  - 這是示範用的檔案，裡面的內容需要自己填寫。
### `preprocessing.py`
  - 將 `Gossiping1-10.txt` 轉寫成 json 檔案
### `parsing.py`
  - 將 comment 利用 Arituct 斷詞
### `selecting`
  - 選出在 comment 中有出現「個不能」pattern 的留言
  - 比對學生的 pattern 是否有符合中文正確 pattern

##執行步驟：
1. 請確認已經下載 `Gossiping1-10.txt` 檔案，並將此檔案直接放在 `SelectingPattern` 這個資料夾中
2. 請確認已經將 `account.info` 填寫好
3. 執行 `preprocessing.py`
4. 執行 `parsing.py`
5. 執行 `selecting.py`
