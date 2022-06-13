# AI_22_termproj
### Batch Mode with 5 characters (Stage 1)
- `team20_proj1.py`: Python Script
- `wordle-answers-alphabetical.txt`: The given dictionary
- `targets_1.txt`: The given targets
- `rec_1.txt`: Record of guessing process
- Running the script
```BASH
python3 team20_proj1.py wordle-answers-alphabetical.txt targets_1.txt rec_1.txt
```
Model is stored as `pattern_dict_1.p`

### 7 characters (Stage 2)
- `team20_2.py`: Python Script
- `tests2.txt`: The given dictionary (lowercase)
- `ques.txt`: The given targets
- `team20.txt`: Record of guessing process
- Running the script
```BASH
rm ./pattern_dic
python3 team20_2.py tests2.txt ques.txt team20.txt
```
Model is stored as `pattern_dict_2.p`

### Interactive Mode with 7 characters (Stage 3)
- `team20_3.py`: Python Script
- `tests.txt`: The given dictionary (lowercase)
- `team20.txt`: Record of guessing process

Model is stored as `pattern_dict_3.p`