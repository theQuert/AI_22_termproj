## Team 20

### 第二戰
- `team20_game2.py`: 主程式
- `sampled71.txt` / `game2list1.txt` / `game2list2.txt`: 答案集(以下以`ans.txt`稱)`
- 助教出的題目 (以下以`ques.txt`)
- `team20_second.txt`:  答覆紀錄
- 運行

```BASH
python3 team20_game2.py ans.txt ques.txt team20_second.txt 
```
因此，輸出包含 `patter_dict_2.p`(此為pickle檔), 若測試過程中有替換過答案集，需運行：

```BASH
rm ./pattern_dic_2.p
```
最後，答覆紀錄(`team20_second.txt`)內包含有**正確答案**, **當輪猜測的詞**, **當輪回覆的評價** 以及 **共猜了幾次**
