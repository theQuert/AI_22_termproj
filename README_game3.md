## Team 20 第三戰

### 第三戰
- `team20_game3.py`: 主程式
- `sampled71.txt` / `game2list1.txt` / `game2list2.txt`: 答案集(以下以`ans.txt`表示)
- `team20_third.txt`:  答覆紀錄
- 運行主程式

```BASH
rm ./pattern_dic_3.p
python3 team20_game3.py ans.txt team20_third.txt 
```

最後，答覆紀錄(`team20_third.txt`)內包含有**正確答案**, **當輪猜測的詞**, **當輪回覆的評價** 以及 **共猜了幾次**

#### 備註：
- 程式當猜對當前詞後，會直接再運行下次的input提供輸入，欲離開程式需 *ctrl+c*, 
若在macOS運行，則 *cmd+c* 離開主程式
- 輸入格式為老師先前提供的, 例如：

```
1,1,1,1,1,1,1
```

