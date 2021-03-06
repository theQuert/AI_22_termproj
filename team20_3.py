import os
import sys
import itertools
import pickle
from tqdm import tqdm
from scipy.stats import entropy
from collections import defaultdict, Counter
import string

WORD_LEN = 7


def calculate_pattern(guess, true):
    """
    針對每次的猜測 返回評價 pattern
    沒猜中 = 0
    全對 = 1
    錯位置 = 2
    """

    # enumerate: https://stackoverflow.com/questions/57970751/python-what-does-i-for-i-mean
    # wrong 儲存正確 word 中那些沒被猜中或被猜錯位置的字母的 index
    wrong = [i for (i, v) in enumerate(guess) if v != true[i]]

    # counts 一個計數器，紀錄正確 word 的那些沒被猜中字母 以及 錯位置字母所出現的次數
    counts = Counter(true[i] for i in wrong)

    # 預設每個字母都猜對
    pattern = [1] * WORD_LEN  # 建立 1*7 的list [1,1,1,1,1,1,1]
    for i in wrong:
        v = guess[i]  # 從 wrong 紀錄的位置 refer 該位置我們猜甚麼字母
        if counts[v] > 0:  # 查詢我們猜的字母是否有在正確 word 裏面 有(代表錯位)，則counts[v] > 0, othersie counts[v] = 0 (表示沒猜中)
            pattern[i] = 2  # 標記錯位
            counts[v] -= 1  # 計數器 -1
        else:  # 沒中
            pattern[i] = 0  # 標記沒中

    return tuple(pattern)


def generate_pattern_dict(dictionary):
    """
    Example for wordlen = 5
    For each word and possible information returned, store a list
    of candidate words
    >>> pattern_dict = generate_pattern_dict(['weary', 'bears', 'crane'])
    >>> pattern_dict['crane'][(1, 1, 1, 1, 1)]
    {'crane'}
    >>> sorted(pattern_dict['crane'][(0, 2, 1, 0, 2)])
    ['bears', 'weary']
    """

    # defaultdict(lambda: defaultdict(set)): https://stackoverflow.com/questions/8419401/python-defaultdict-and-lambda
    pattern_dict = defaultdict(lambda: defaultdict(set))
    for word in tqdm(dictionary):
        for word2 in dictionary:
            pattern = calculate_pattern(word, word2)
            pattern_dict[word][pattern].add(word2)
    return dict(pattern_dict)


def calculate_entropies(possible_words, pattern_dict):
    """Calculate the entropy for every word in `words`, taking into account
    the remaining `possible_words`"""
    entropies = {}
    # words = list(set(words).intersection(set(all_dictionary)))
    words = list(possible_words)
    for word in words:
        counts = []
        # Generate the possible patterns of information we can get
        all_patterns = list(itertools.product([0, 1, 2], repeat=WORD_LEN))  # 3^7 種可能

        for pattern in all_patterns:
            matches = pattern_dict[word][pattern]
            matches = matches.intersection(possible_words)  # intersection() 方法用於返回兩個或更多集合中都包含的元素
            counts.append(len(matches))
        entropies[word] = entropy(counts)
    return entropies


def main():
    # 接收兩個參數。

    # 第一個參數是答案集合的檔案名稱，也就是 ans.txt
    # sys.argv[1]
    # Load 所有可能解，我們只考慮答案庫裡的所有單字
    with open(sys.argv[1]) as ifp:
        all_dictionary = list(map(lambda x: x.strip(), ifp.readlines()))

    # 第二個參數是各組程式針對team20_third.txt所做的答覆的紀錄的檔案名稱
    # sys.argv[2]
    # 將猜測結果寫入檔案 team20_third.txt
    f = open(sys.argv[2], 'w')

    # if 'pattern_dict_3.p' in os.listdir('.'):
    #     pattern_dict = pickle.load(open('pattern_dict_3.p', 'rb'))

    # else:
    pattern_dict = generate_pattern_dict(all_dictionary)
    pickle.dump(pattern_dict, open('pattern_dict_3.p', 'wb+'))

    while 1:
        all_words = set(all_dictionary)
        init_round = 1
        g = []  # 儲存我們猜過的字
        t = []  # 儲存我們每次猜所獲評價 pattern

        # 用來紀錄字母的大小寫，並且藉此來更改大小寫 0:小寫 1:大寫
        alpha_value = [0] * 26
        alpha_key = list(string.ascii_lowercase)
        alpha_dic = dict(zip(alpha_key, alpha_value))

        # 透過encode來固定位置、大小寫正確（即評價=1）的字母
        fixed_idx = [i for i in range(7)]
        fixed_val = ['#' for _ in range(7)]
        fixed_ans = dict(zip(fixed_idx, fixed_val))

        for n_round in range(init_round, len(all_dictionary)):  # 最多猜完整個答案集 我們要猜到為止

            # all_words = all_words.intersection(set(all_dictionary))
            entropies = calculate_entropies(all_words, pattern_dict)

            # Choose the one with highest entropy
            lower_letter_guess_word = max(entropies.items(), key=lambda x: x[1])[0]

            # guess_word 實際要猜的word
            guess_word = list(lower_letter_guess_word)

            # 查alpha_dictionary，來決定大小寫
            for i in range(7):
                # key = lower_letter_guess_word[i]
                key = guess_word[i]
                if type(fixed_ans[i]) == type('str'):
                    if alpha_dic[key] == 1:  # 大寫
                        # fixed_ans[i] = lower_letter_guess_word[i].upper()
                        fixed_ans[i] = guess_word[i].upper()
                    # else: fixed_ans[i] = lower_letter_guess_word[i]#小寫
                    else:
                        fixed_ans[i] = guess_word[i]  # 小寫

            guess_word_lst = []
            # keys_lst = list(fixed_ans.keys())
            for idx in range(7):
                # if type(fixed_ans[keys_lst[idx]])==type('str'.encode()): # 位置對，字母也對 -> type=='byte'
                if type(fixed_ans[idx]) == type('str'.encode()):  # 位置對，字母也對 -> type=='byte'
                    guess_word_lst.append(fixed_ans[idx].decode())
                else:
                    guess_word_lst.append(fixed_ans[idx])
            guess_word = "".join(guess_word_lst)

            # 紀錄本次答題
            g.append(guess_word)

            if n_round == 1:
                print(f'First guess: {guess_word}')
            else:
                print(f'Current guess: {guess_word}')

            input_pattern = input('response: ')
            feedback = tuple(map(int, input_pattern.split(',')))

            info = list(feedback)
            info2 = list(feedback)
            info3 = list(feedback)
            for i in range(7):
                if info[i] == 4:
                    info[i] = info2[i] = info3[i] = 2
                elif info[i] == 3:
                    info[i] = info2[i] = info3[i] = 1
                elif info[i] == 5:
                    info[i] = 0
                    info2[i] = 1
                    info3[i] = 2
            info = tuple(info)
            info2 = tuple(info2)
            info3 = tuple(info3)

            # 紀錄本次評價
            tmp_feedback = list(feedback)
            t.append(tmp_feedback)

            if input_pattern == "1,1,1,1,1,1,1":
                print(guess_word, file=f)  # 先印正確答案
                for i in range(n_round):  # 印猜的過程
                    times = str(i + 1)
                    print(times + '; ' + g[i] + '; "', end="", file=f)
                    print(*t[i], sep=",", end="", file=f)
                    print('"', file=f)
                print(n_round, file=f)  # 印猜了幾次
                print(n_round)
                break

            # 更新字母大小寫
            seen = []
            for i in range(7):
                # 大小寫錯
                if feedback[i] == 4:
                    key = guess_word[i].lower()
                    # 小寫改大寫
                    if (alpha_dic[key] == 0) or key in seen:
                        alpha_dic[key] = 1
                        seen.append(key)
                    # 大寫改小寫
                    else:
                        alpha_dic[key] = 0
                elif feedback[i] == 3 and guess_word[i].isupper():
                    fixed_ans[i] = guess_word[i].lower().encode()
                elif feedback[i] == 3 and guess_word[i].islower():
                    fixed_ans[i] = guess_word[i].upper().encode()
                elif feedback[i] == 1:
                    fixed_ans[i] = guess_word[i].encode()

            # 剔除那些不可能的答案
            words = pattern_dict[guess_word.lower()][info]
            words2 = pattern_dict[guess_word.lower()][info2]
            words3 = pattern_dict[guess_word.lower()][info3]
            words = words | words2 | words3
            all_words = all_words.intersection(words)  # intersection() 方法用於返回三個或更多集合中都包含的元素
    f.close()


if __name__ == "__main__":
    main()
