# AI_22_termproj
### Batch Mode (1$^{st}$ stage)
- `team20_proj1.py`: Python Script
- `wordle-answers-alphabetical.txt`: The given dictionary
- `targets_1.txt`: The given targets
- `rec_1.txt`: Record of guessing process
- Running the script
```BASH
python3 team20_proj1.py wordle-answers-alphabetical.txt targets_1.txt rec_1.txt
```
Model is stored as `pattern_dict_1.p`

### 7 characters (2$^{nd}$ stage)
- `team20_proj2.py`: Python Script
- `sampled71.txt`: The gien dictionary (lowercase)
- `targets_2.txt`: The given targets
- `rec_2.txt`: Record of guessing process
- Running the script
```BASH
python3 team20_proj2.py sampled71.txt targets_2.txt rec_2.txt
```
Model is stored as `pattern_dict_2.p`

### Interactive Mode with 7 characters (3$^{rd}$ stage)
- `team20_proj3.py`: Python Script
- `sampled71.txt`: The given dictionary (lowercase)
- `targets_3.txt`: The given targets
- `rec_3.txt`: Record for guessing process
- Running the script
```BASH
python3 team20_proj3.py sampled71.txt targets_3.txt rec_3.txt
```
Since the guessing process on stage 3 is similar to stage 2, we apply the model from stage 2: `pattern_dict_2.p`
