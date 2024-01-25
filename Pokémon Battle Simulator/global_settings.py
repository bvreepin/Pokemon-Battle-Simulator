# CSV Paths
DATA_DIR = 'data'
NATURES_CSV = 'natures.csv'
POKEMON_STATS_CSV = 'pokemon_stats.csv'
MOVES_CSV = 'move_list.csv'
TYPE_EF_CSV = 'type_effectiveness.csv'

# Stat Ranges
LEVEL_MIN, LEVEL_MAX = 1, 100
STAT_ACTUAL_MIN, STAT_ACTUAL_MAX = 1, 500
IV_MIN, IV_MAX = 0, 31
EV_MIN, EV_MAX = 0, 255
EV_TOTAL_MAX = 510
NATURE_DEC, NATURE_INC = 0.9, 1.1

# Misc Settings
POKE_ID_MIN, POKE_ID_MAX = 1, 493
POKE_NUM_MIN, POKE_NUM_MAX = 1, 6
POSSIBLE_GENDERS = ['male', 'female', 'genderless']

# Stat Ordering Format
HP = 0
ATK = 1
DEF = 2
SP_ATK = 3
SP_DEF = 4
SPD = 5
STAT_NUM = 6
ACC = 6
EVA = 7

STAT_TO_NAME = ['Health', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'accuracy', 'evasion']

# Move Categories
PHYSICAL = 1
SPECIAL = 2

# Base Pokemon Stats Formatting
NDEX = 0
NAME = 1
TYPE1 = 2
TYPE2 = 3
STAT_START = 4
# HP = 4, ATK = 5, DEF = 6, SP_ATK = 7, SP_DEF = 8, SPD = 9
BASE_EXP = 10
GEN = 11

# Move Data Formatting
MOVE_ID = 0
MOVE_NAME = 1
MOVE_TYPE = 3
MOVE_POWER = 4
MOVE_PP = 5
MOVE_ACC = 6
MOVE_TARGET = 7
MOVE_CATEGORY = 8

# CSV Numerical Columns
POKEMON_STATS_NUMS = [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
MOVES_NUM = [0, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

# Player Turn Actions
ACTION_PRIORITY = {
    'other': 2,
    'move': 1
}

# Turn Data
ACTION_TYPE = 0
ACTION_VALUE = 1

# Pre-process Move Data
PPM_MOVE = 0
PPM_MOVE_DATA = 1
PPM_BYPASS = 2