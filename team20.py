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
    沒中 = 0
    全對 = 1
    錯位置 = 2
    """

    # enumerate 解釋 https://stackoverflow.com/questions/57970751/python-what-does-i-for-i-mean
    # wrong 儲存某些答案字母的位置 (而該位置是沒中 或 錯位置)
    wrong = [i for (i,v) in enumerate(guess) if v != true[i]] #for (i,v) in enumerate(guess): wrong.append(i)
	mats = [v for (i,v) in enumerate(guess) if v==true[i]]

    # counts 儲存答案字母 (那些沒中字母 以及 錯位置字母)
    counts = Counter(true[i] for i in wrong)

    # 預設每個字母都猜對
    pattern = [1] * 5 #建立1*5的list [1,1,1,1,1]
    for i in wrong:
        v = guess[i] #從wrong紀錄的位置refer猜的字母
        if counts[v] > 0 and v not in mats: #從該字母反查有沒有在答案裏面 有：1 沒有：0  #所以>0 字母對但錯位
            pattern[i] = 2 #標記錯位
            counts[v] -= 1 #看過標記0
        else: #沒中
            pattern[i] = 0 #標記沒中

    return tuple(pattern)

#做這花19秒，但只會做一次
def generate_pattern_dict(dictionary):
    """For each word and possible information returned, store a list
    of candidate words
    >>> pattern_dict = generate_pattern_dict(['weary', 'bears', 'crane'])
    >>> pattern_dict['crane'][(1, 1, 1, 1, 1)]
    {'crane'}
    >>> sorted(pattern_dict['crane'][(0, 2, 1, 0, 2)])
    ['bears', 'weary']
    """

    # defaultdict(lambda: defaultdict(set)) 解釋 https://stackoverflow.com/questions/8419401/python-defaultdict-and-lambda
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
        all_patterns = list(itertools.product([0, 1, 2], repeat=WORD_LEN)) #3^5種可能 

        for pattern in all_patterns:
            matches = pattern_dict[word][pattern]
            matches = matches.intersection(possible_words) #intersection() 方法用於返回兩個或更多集合中都包含的元素
            counts.append(len(matches))
        entropies[word] = entropy(counts)
    return entropies


def main():
    #接收三個參數。

    #第一個參數是答案集合的檔案名稱，也就是 wordle-answers-alphabetical.txt
    #sys.argv[1]
    # Load 所有可能解，第一次測試，我們只考慮答案庫裡的2315個單字
    with open(sys.argv[1]) as ifp:
        all_dictionary = list(map(lambda x: x.strip(), ifp.readlines()))

    #第二個參數是考題的檔案名稱tests.txt
    #sys.argv[2]
    # Load 助教出的題目
    with open(sys.argv[2]) as ifp:
        dictionary = list(map(lambda x: x.strip(), ifp.readlines()))

    #第三個參數是各組程式針對tests.txt所做的答覆的紀錄的檔案名稱
    #sys.argv[3]
    #將猜測結果寫入檔案 team20_first.txt
    f = open(sys.argv[3], 'w')


    '''第一次測試 不會有不合規格的字 先略
    error_msg = 'Dictionary contains different length words.'
    assert len({len(x) for x in all_dictionary}) == 1, error_msg
    print(f'Loaded dictionary with {len(all_dictionary)} words...')
    '''


    # Calculate the pattern_dict and cache it 花了19秒
    pattern_dict = generate_pattern_dict(all_dictionary)
    pickle.dump(pattern_dict, open('pattern_dict.p', 'wb+'))

    # or load the cache if it already exists 建議自己測試的時候 做過上面那兩行一次之後 把它隱藏 跑下面這兩行
    '''
    if 'pattern_dict.p' in os.listdir('.'):
    pattern_dict = pickle.load(open('pattern_dict.p', 'rb'))
    '''

    for WORD_TO_GUESS in tqdm(dictionary):
        all_words = set(all_dictionary)
        init_round = 1
        g = [] #儲存我們猜過的字
        t = [] #儲存我們每次猜所獲評價

        for n_round in range(init_round, 2315): #最多猜2315次 我們要猜到為止

            candidates = all_dictionary
            entropies = calculate_entropies(candidates, all_words, pattern_dict)

            if max(entropies.values()) < 0.1:
                candidates = all_words
                entropies = calculate_entropies(candidates, all_words, pattern_dict)

            # Guess the candidate with highest entropy
            guess_word = max(entropies.items(), key=lambda x: x[1])[0]
            info = calculate_pattern(guess_word, WORD_TO_GUESS)


            g.append(guess_word);

            # 將info (是tuple) 轉成 list
            tmp_info = list(info)
            t.append(tmp_info);

            if guess_word == WORD_TO_GUESS:
                print(WORD_TO_GUESS, file=f) #先印正確答案
                for i in range(n_round): #印猜的過程
                    times = str(i+1)
                    print(times + '; ' + g[i] + '; "', end="", file=f)
                    print(*t[i], sep=",", end="", file=f)
                    print('"', file=f)
                print(n_round, file=f) #印猜了幾次
                break

            # 剔除那些不可能的答案
            words = pattern_dict[guess_word][info]
            all_words = all_words.intersection(words) #intersection() 方法用于返回两个或更多集合中都包含的元素
    f.close()
if __name__ == "__main__":
    main()
