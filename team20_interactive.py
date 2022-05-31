import os
import sys
import itertools
import pickle
from tqdm import tqdm
from scipy.stats import entropy
from collections import defaultdict, Counter

WORD_LEN = 5

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
            pattern = compare2words_stage2(word, word2)
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


   #if 'pattern_dict.p' in os.listdir('.'):
       # pattern_dict = pickle.load(open('pattern_dict.p', 'rb'))
    #else:
    pattern_dict = generate_pattern_dict(all_dictionary)
    pickle.dump(pattern_dict, open('pattern_dict.p', 'wb+'))

    for WORD_TO_GUESS in tqdm(dictionary):
        all_words = set(all_dictionary)
        init_round = 1
        g = [] # 儲存我們猜過的字
        t = [] # 儲存我們每次猜所獲評價 pattern

        for n_round in range(init_round, 2316): #最多猜2315次 我們要猜到為止

            candidates = all_dictionary
            entropies = calculate_entropies(candidates, all_words, pattern_dict)

            if max(entropies.values()) < 0.1:
                candidates = all_words
                entropies = calculate_entropies(candidates, all_words, pattern_dict)

            # Guess the candidate with highest entropy
            guess_word = max(entropies.items(), key=lambda x: x[1])[0]
            info = compare2words_stage2(guess_word, WORD_TO_GUESS)

            if n_round==1: print(f'First guess: {guess_word}')
            else: print(f'Current guess: {guess_word}')
            
            input_pattern = input('response: ')
            info = tuple(map(int, input_pattern.split(',')))
            g.append(guess_word);

            # 將 info (a tuple) 轉成 list
            tmp_info = list(info)
            # Add L130-L134, L141 for interactive mode
            t.append(tmp_info);
            print(list(tmp_info))

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
