import os
import sys
import itertools
import pickle
from tqdm import tqdm
from scipy.stats import entropy
from collections import defaultdict, Counter

WORD_LEN = 5

def calculate_pattern(guess, true):
    """
    針對每次的猜測 返回評價 pattern
    沒猜中 = 0
    全對 = 1
    錯位置 = 2
    """

    # enumerate: https://stackoverflow.com/questions/57970751/python-what-does-i-for-i-mean
    # wrong 儲存正確 word 中那些沒被猜中或被猜錯位置的字母的 index
    wrong = [i for (i,v) in enumerate(guess) if v != true[i]]
    # mats = [v for (i,v) in enumerate(guess) if v == true[i]]

    # counts 一個計數器，紀錄正確 word 的那些沒被猜中字母 以及 錯位置字母所出現的次數
    counts = Counter(true[i] for i in wrong)

    # 預設每個字母都猜對
    pattern = [1] * 5 #建立 1*5 的list [1,1,1,1,1]
    for i in wrong: 
        v = guess[i] # 從 wrong 紀錄的位置 refer 該位置我們猜甚麼字母
        if counts[v] > 0: # 查詢我們猜的字母是否有在正確 word 裏面 有(代表錯位)，則counts[v] > 0, othersie counts[v] = 0 (表示沒猜中)  
            pattern[i] = 2 # 標記錯位
            counts[v] -= 1 # 計數器 -1
        else: # 沒中
            pattern[i] = 0 # 標記沒中

    return tuple(pattern)

# 做這花19秒，但只會做一次
def generate_pattern_dict(dictionary):
    """For each word and possible information returned, store a list
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


def calculate_entropies(words, possible_words, pattern_dict):
    """Calculate the entropy for every word in `words`, taking into account
    the remaining `possible_words`"""
    entropies = {}
    for word in words:
        counts = []
        # Generate the possible patterns of information we can get
        all_patterns = list(itertools.product([0, 1, 2], repeat=WORD_LEN)) # 3^5 種可能 

        for pattern in all_patterns:
            matches = pattern_dict[word][pattern]
            matches = matches.intersection(possible_words) #intersection() 方法用於返回兩個或更多集合中都包含的元素
            counts.append(len(matches))
        entropies[word] = entropy(counts)
    return entropies


def main():
    # 接收三個參數。

    # 第一個參數是答案集合的檔案名稱，也就是 wordle-answers-alphabetical.txt
    # sys.argv[1]
    # Load 所有可能解，第一次測試，我們只考慮答案庫裡的2315個單字
    with open(sys.argv[1]) as ifp:
        all_dictionary = list(map(lambda x: x.strip(), ifp.readlines()))

    # 第二個參數是助教出的題目的檔案名稱tests.txt
    # sys.argv[2]
    # Load 助教出的題目(我們要猜的 word)
    with open(sys.argv[2]) as ifp:
        dictionary = list(map(lambda x: x.strip(), ifp.readlines()))

    # 第三個參數是各組程式針對tests.txt所做的答覆的紀錄的檔案名稱
    # sys.argv[3]
    # 將猜測結果寫入檔案 team20_first.txt
    f = open(sys.argv[3], 'w')


    # 第一次測試 不會有不合規格的字
    '''
    error_msg = 'Dictionary contains different length words.'
    assert len({len(x) for x in all_dictionary}) == 1, error_msg
    print(f'Loaded dictionary with {len(all_dictionary)} words...')
    '''


    if 'pattern_dict.p' in os.listdir('.'):
       pattern_dict = pickle.load(open('pattern_dict_1.p', 'rb'))
    else:
        pattern_dict = generate_pattern_dict(all_dictionary)
        pickle.dump(pattern_dict, open('pattern_dict_1.p', 'wb+'))

    for WORD_TO_GUESS in tqdm(dictionary):
        all_words = set(all_dictionary)
        init_round = 1
        g = [] # 儲存我們猜過的字
        t = [] # 儲存我們每次猜所獲評價 patterm

        for n_round in range(init_round, 2316): #最多猜2315次 我們要猜到為止

            candidates = all_dictionary
            entropies = calculate_entropies(candidates, all_words, pattern_dict)

            if max(entropies.values()) < 0.1:
                candidates = all_words
                entropies = calculate_entropies(candidates, all_words, pattern_dict)

            # Guess the candidate with highest entropy
            guess_word = max(entropies.items(), key=lambda x: x[1])[0]
            info = calculate_pattern(guess_word, WORD_TO_GUESS)


            g.append(guess_word);

            # 將 info (a tuple) 轉成 list
            tmp_info = list(info)
            t.append(tmp_info);

            if guess_word == WORD_TO_GUESS:
                print(WORD_TO_GUESS, file=f) # 先印正確答案
                for i in range(n_round): # 印猜的過程
                    times = str(i+1)
                    print(times + '; ' + g[i] + '; "', end="", file=f)
                    print(*t[i], sep=",", end="", file=f)
                    print('"', file=f)
                print(n_round, file=f) # 印猜了幾次
                break

            # 剔除那些不可能的答案
            words = pattern_dict[guess_word][info]
            all_words = all_words.intersection(words) #intersection() 方法用于返回两个或更多集合中都包含的元素
    f.close()
if __name__ == "__main__":
    main()
