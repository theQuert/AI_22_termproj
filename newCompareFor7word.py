from collections import Counter


def compare2words_stage2(ans, guess):
    """
    針對每次的猜測 返回評價 pattern
    0: 答案沒有該字母
    1: 字母正確、位置正確、大小寫正確
    2: 字母正確、位置不正確、大小寫正確
    3: 字母正確、位置正確、大小寫不正確
    4: 字母正確、位置不正確、大小寫不正確
    """

    pattern = [0] * 7  # 建立 1*7 的list [0, 0, 0, 0, 0, 0, 0, 0]: 答案沒有該字母
    counts = Counter(ans[i] for i in range(7))  # 紀錄答案出現了甚麼字母，分別幾次(有大小寫之分)
    for i in range(7):  # 先檢查 1: 字母正確、位置正確、大小寫正確。因為他優先權最大
        if guess[i] == ans[i]:
            pattern[i] = 1
            counts[guess[i]] -= 1  # 配對過了，必須從紀錄消除
    for i in range(7):  # 再檢查 3: 字母正確、位置正確、大小寫不正確
        if pattern[i] == 0:
            if guess[i].islower():  # guess[i]是小寫
                if ans[i].isupper() and guess[i] == ans[i].lower():
                    pattern[i] = 3
                    counts[ans[i]] -= 1
            else:  # guess[i]是大寫
                if ans[i].islower() and guess[i] == ans[i].upper():
                    pattern[i] = 3
                    counts[ans[i]] -= 1
    for i in range(7):  # 再檢查 2: 字母正確、位置不正確、大小寫正確
        if pattern[i] == 0:
            if counts[guess[i]] > 0:
                pattern[i] = 2
                counts[guess[i]] -= 1
    for i in range(7):  # 再檢查 4: 字母正確、位置不正確、大小寫不正確
        if pattern[i] == 0:  # 這時候guess[i]的可能只剩下0(全錯)或是4(字母正確、位置不正確、大小寫不正確)
            if counts[guess[i].lower()] > 0 or counts[guess[i].upper()] > 0:
                pattern[i] = 4
                if guess[i].islower():
                    counts[guess[i].upper()] -= 1
                else:
                    counts[guess[i].lower()] -= 1
    return tuple(pattern)

"""
def main():
    # 老師提供的 sample
    print(compare2words_stage2("cacao", "meCCa"))  # [0, 0, 3, 4, 2]
    print(compare2words_stage2("caCAo", "meCCa"))  # [0, 0, 1, 4, 2]
    print(compare2words_stage2("CACao", "meCCa"))  # [0, 0, 1, 2, 2]
    print(compare2words_stage2("CACAo", "meCCa"))  # [0, 0, 1, 2, 4]

    print(compare2words_stage2("cacao", "mecca"))  # [0, 0, 1, 2, 2]
    print(compare2words_stage2("cacao", "meccA"))  # [0, 0, 1, 2, 4]
    print(compare2words_stage2("cacao", "mecCa"))  # [0, 0, 1, 4, 2]
    print(compare2words_stage2("cacao", "mecCA"))  # [0, 0, 1, 4, 4]
    print(compare2words_stage2("cacao", "meCca"))  # [0, 0, 3, 2, 2]
    print(compare2words_stage2("cacao", "meCcA"))  # [0, 0, 3, 2, 4]
    print(compare2words_stage2("cacao", "meCCa"))  # [0, 0, 3, 4, 2]
    print(compare2words_stage2("cacao", "meCCA"))  # [0, 0, 3, 4, 4]

    print(compare2words_stage2("cACao", "mecca"))  # [0, 0, 3, 2, 2]
    print(compare2words_stage2("cACao", "meccA"))  # [0, 0, 3, 2, 2]
    print(compare2words_stage2("cACao", "mecCa"))  # [0, 0, 3, 4, 2]
    print(compare2words_stage2("cACao", "mecCA"))  # [0, 0, 3, 4, 2]
    print(compare2words_stage2("cACao", "meCca"))  # [0, 0, 1, 2, 2]
    print(compare2words_stage2("cACao", "meCcA"))  # [0, 0, 1, 2, 2]
    print(compare2words_stage2("cACao", "meCCa"))  # [0, 0, 1, 4, 2]
    print(compare2words_stage2("cACao", "meCCA"))  # [0, 0, 1, 4, 2]

    print(compare2words_stage2("furry", "error"))  # [0, 2, 1, 0, 0]
    print(compare2words_stage2("furry", "erroR"))  # [0, 2, 1, 0, 0]
    print(compare2words_stage2("furry", "erRor"))  # [0, 2, 3, 0, 0]
    print(compare2words_stage2("furry", "eRror"))  # [0, 0, 1, 0, 2]
    print(compare2words_stage2("furry", "erRoR"))  # [0, 2, 3, 0, 0]
    print(compare2words_stage2("furry", "eRRor"))  # [0, 0, 3, 0, 2]
    print(compare2words_stage2("furry", "eRroR"))  # [0, 4, 1, 0, 0]
    print(compare2words_stage2("furry", "eRRoR"))  # [0, 4, 3, 0, 0]

    print(compare2words_stage2("droop", "furor"))  # [0, 0, 2, 1, 0]
    print(compare2words_stage2("droop", "furOr"))  # [0, 0, 2, 3, 0]
    print(compare2words_stage2("droop", "fuRor"))  # [0, 0, 0, 1, 2]
    print(compare2words_stage2("droop", "fuROr"))  # [0, 0, 0, 3, 2]
    print(compare2words_stage2("droop", "furoR"))  # [0, 0, 2, 1, 0]
    print(compare2words_stage2("droop", "furOR"))  # [0, 0, 2, 3, 0]
    print(compare2words_stage2("droop", "fuRoR"))  # [0, 0, 4, 1, 0]
    print(compare2words_stage2("droop", "fuROR"))  # [0, 0, 4, 3, 0]


if __name__ == "__main__":
    main()
"""