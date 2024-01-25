from poke_data import PokeData
import conf.global_settings as gs
import pokemon as pk
import battle as bt
import trainer as tr

PokeData.start()

amount_of_pokemon = input("How many Pokémon do you want to use? (Max 6)\n")

if amount_of_pokemon.isnumeric():
    amount_of_pokemon = int(amount_of_pokemon)
    if (amount_of_pokemon < gs.POKE_NUM_MIN or amount_of_pokemon > gs.POKE_NUM_MAX):
        print("Invalid amount of Pokémon, initialized to 6 Pokémon\n")
        amount_of_pokemon = gs.POKE_NUM_MAX
else:
    print("Invalid amount of Pokémon, initialized to 6 Pokémon\n")
    amount_of_pokemon = gs.POKE_NUM_MAX

trainer_name = input(f"\nWhat is your trainer name?\n")
if trainer_name == "":
    print("Trainer name can't be empty, initialized to \"Ash\"")
    trainer_name = "Ash"
    
poke_list = []

for i in range(amount_of_pokemon):
    is_valid = False
    while(not is_valid):
        name = input(f"\nWhat is the name of Pokémon {i+1}?\n")
        move_list = input(f"\nWhat are the moves of {name}? Enter these moves, separated by a comma and space\n").lower().split(", ")
        try:
            if len(move_list) <= 4:
                poke_list.append(pk.Pokemon(name, move_list))
                is_valid = True
            else:
                print("Too many moves were given, only 4 moves are allowed")
        except Exception as e:
            print(f'{e}')

trainer1 = tr.Trainer(trainer_name, poke_list)
    
trainer_name = input(f"\nWhat is your opponent's trainer name?\n")
if trainer_name == "":
    print("Trainer name can't be empty, initialized to \"Paul\"")
    trainer_name = "Paul"

poke_list = []

for i in range(amount_of_pokemon):
    is_valid = False
    while(not is_valid):
        name = input(f"\nWhat is the name of opponent Pokémon {i+1}?\n")
        move_list = input(f"\nWhat are the moves of {name}? (Max 4) Enter these moves, separated by a comma and space\n").lower().split(", ")
        try:
            if len(move_list) <= 4:
                poke_list.append(pk.Pokemon(name, move_list))
                is_valid = True
            else:
                print("Too many moves were given, only 4 moves are allowed")
        except Exception as e:
            print(f'{e}')
            
trainer2 = tr.Trainer(trainer_name, poke_list)
    
battle = bt.Battle(trainer1, trainer2)
battle.start()

while(not battle.is_finished()):
    print(f"\n{trainer1.name}:")
    current_poke = trainer1.current_poke
    current_opponent_poke = trainer2.current_poke
    print(f"{current_poke.name} HP:{current_poke.cur_hp}/{current_poke.max_hp} VS {current_opponent_poke.name} HP:{current_opponent_poke.cur_hp}/{current_opponent_poke.max_hp}\n")
    valid_action = False
    while valid_action == False:
        action_trainer1 = input("Enter \"S\" if you want to switch, enter anything else if you want to attack\n")
        if action_trainer1 == "S":
            action_trainer1 = ['other', 'switch']
        else:
            is_valid = False
            while not is_valid:
                print(f"\nChoose {current_poke.name}'s attack:")
                print(f"HP: {current_poke.cur_hp}/{current_poke.max_hp}\n")
                amount_of_moves = len(trainer1.current_poke.moves)
                for i in range(amount_of_moves):
                    move = trainer1.current_poke.moves[i]
                    print(f"{i+1}) {move.name} Power:{move.power} PP:{move.cur_pp}\n")
                move_index = input("Which move do you want to use?\n")
                if not move_index.isnumeric() or int(move_index) < 1 or int(move_index) > amount_of_moves:
                    print("invalid move selected")
                else:
                    action_trainer1 = ['move', trainer1.current_poke.moves[int(move_index)-1].name]
                    is_valid = True
        valid_action = trainer1.is_valid_action(action_trainer1)
        if valid_action == False:
            print("\nThe chosen action is invalid due to not being able to switch to a fainted Pokémon or the chosen move not having any PP left")
                
    print(f"\n{trainer2.name}:")
    current_poke = trainer2.current_poke
    current_opponent_poke = trainer1.current_poke
    print(f"{current_poke.name} HP:{current_poke.cur_hp}/{current_poke.max_hp} VS {current_opponent_poke.name} HP:{current_opponent_poke.cur_hp}/{current_opponent_poke.max_hp}\n")
    valid_action = False
    while valid_action == False:
        action_trainer2 = input("Enter \"S\" if you want to switch, enter anything else if you want to attack\n")
        if action_trainer2 == "S":
            action_trainer2 = ['other', 'switch']
        else:
            is_valid = False
            while not is_valid:
                print(f"\nChoose {current_poke.name}'s attack")
                print(f"HP: {current_poke.cur_hp}/{current_poke.max_hp}\n")
                amount_of_moves = len(trainer2.current_poke.moves)
                for i in range(amount_of_moves):
                    move = trainer2.current_poke.moves[i]
                    print(f"{i+1}) {move.name} Power:{move.power} PP:{move.cur_pp}\n")
                move_index = input("Which move do you want to use?\n")
                if not move_index.isnumeric() or int(move_index) < 1 or int(move_index) > amount_of_moves:
                    print("invalid move selected")
                else:
                    action_trainer2 = ['move', trainer2.current_poke.moves[int(move_index)-1].name]
                    is_valid = True
        valid_action = trainer2.is_valid_action(action_trainer2)
        if valid_action == False:
            print("\nThe chosen action is invalid due to not being able to switch to a fainted Pokémon or the chosen move not having any PP left")
                
    battle.turn(action_trainer1, action_trainer2)
    print(battle.get_cur_text())

print(f'Trainer {battle.get_winner().name} won this battle!')