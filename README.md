# AI_22_termproj
### Batch Mode (1$^{st}$ stage)
- `team20_proj1.py`: Python Script
- `wordle-answers-alphabetical.txt`: The given dictionary
- `tests_1.txt`: The given guessing target
- `rec_first.txt`: Record of guessing process
- Running the script
```BASH
python3 team20_proj1.py wordle-answers-alphabetical.txt tests_1.txt rec_first.txt
```
Model is stored as `pattern_dict_1.p

### 7 characters (2$^{nd}$ stage)
- `team20_proj2.py`: Python Script
- `sampled71.txt`: The gien dictionary (lowercase)
- `tests_2.txt`: The given guessing target
- `rec_second.txt`: Record of guessing process
- Running the script
```BASH
python3 team20_proj2.py sampled71.txt tests_2.txt rec_second.txt
```
Model is stored as `pattern_dict_2.p`

### Interactive Mode
- `team20_interactive.py`: Python Script
- `tests.interactive.txt`: The given answer
- `team20_first_interactive.txt`: Record for guessing process
- Running the script
```
python3 team20_interactive.py wordle-answers-alphabetical.txt tests.interactive.txt team20_first_interactive.txt
```
