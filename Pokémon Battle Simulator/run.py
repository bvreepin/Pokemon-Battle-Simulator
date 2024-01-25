from poke_data import PokeData
import global_settings as gs
import pokemon as pk
import battle as bt
import trainer as tr

PokeData.start()

amount_of_pokemon = "2" #input("How many Pokémon do you want to use? (Max 6)\n")

trainer_name = "ash" #input(f"What is your trainer name?\n")

if amount_of_pokemon.isnumeric():
    amount_of_pokemon = int(amount_of_pokemon)
    if (amount_of_pokemon < gs.POKE_NUM_MIN or amount_of_pokemon > gs.POKE_NUM_MAX):
        print("Invalid amount of Pokémon, initialized to 6 Pokémon\n")
        amount_of_pokemon = gs.POKE_NUM_MAX
else:
    print("Invalid amount of Pokémon, initialized to 6 Pokémon\n")
    amount_of_pokemon = gs.POKE_NUM_MAX
    
poke_list = []

for i in range(amount_of_pokemon):
    is_valid = False
    while(not is_valid):
        name = input(f"What is the name of Pokémon {i+1}?\n")
        move_list = ["thunderbolt"] #input(f"What are the moves of {name}? Enter these moves, separated by a comma and space\n").lower().split(", ")
        try:
            poke_list.append(pk.Pokemon(name, move_list))
            is_valid = True
        except Exception as e:
            print(f'{e}')

trainer1 = tr.Trainer(trainer_name, poke_list)
    
trainer_name = "paul" #input(f"What is your opponent's trainer name?\n")

poke_list = []

for i in range(amount_of_pokemon):
    is_valid = False
    while(not is_valid):
        name = "infernape" #input(f"What is the name of opponent Pokémon {i+1}?\n")
        move_list = ["fire-blast"] #input(f"What are the moves of {name}? Enter these moves, separated by a comma and space\n").lower().split(", ")
        try:
            poke_list.append(pk.Pokemon(name, move_list))
            is_valid = True
        except Exception as e:
            print(f'{e}')
            
trainer2 = tr.Trainer(trainer_name, poke_list)
    
battle = bt.Battle(trainer1, trainer2)
battle.start()

while(not battle.is_finished()):
    print(f"{trainer1.name}:")
    valid_action = False
    while valid_action == False:
        action_trainer1 = input("Enter \"S\" if you want to switch, enter anything else if you want to attack\n")
        if action_trainer1 == "S":
            action_trainer1 = ['other', 'switch']
        else:
            is_valid = False
            while not is_valid:
                print(f"Choose {trainer1.current_poke}'s attack")
                amount_of_moves = len(trainer1.current_poke.moves)
                for i in range(amount_of_moves):
                    move = trainer1.current_poke.moves[i]
                    print(f"{i+1}) {move.name} Power:{move.power} PP:{move.cur_pp}\n")
                move_index = "1" # input("Which move do you want to use?\n")
                if not move_index.isnumeric() or int(move_index) < 1 or int(move_index) > amount_of_moves:
                    print("invalid move selected")
                else:
                    action_trainer1 = ['move', trainer1.current_poke.moves[int(move_index)-1].name]
                    is_valid = True
        valid_action = trainer1.is_valid_action(action_trainer1)
        if valid_action == False:
            print("The chosen action is invalid due to not being able to switch to a fainted Pokémon or the chosen move not having any PP left")
                
    print(f"{trainer2.name}:")
    valid_action = False
    while valid_action == False:
        action_trainer2 = "1" #input("Enter S if you want to switch, enter anything else if you want to attack\n")
        if action_trainer2 == "S":
            action_trainer2 = ['other', 'switch']
        else:
            is_valid = False
            while not is_valid:
                print(f"Choose {trainer2.current_poke}'s attack")
                amount_of_moves = len(trainer2.current_poke.moves)
                for i in range(amount_of_moves):
                    move = trainer2.current_poke.moves[i]
                    print(f"{i+1}) {move.name} Power:{move.power} PP:{move.cur_pp}\n")
                move_index = "1" # input("Which move do you want to use?\n")
                if not move_index.isnumeric() or int(move_index) < 1 or int(move_index) > amount_of_moves:
                    print("invalid move selected")
                else:
                    action_trainer2 = ['move', trainer2.current_poke.moves[int(move_index)-1].name]
                    is_valid = True
        valid_action = trainer2.is_valid_action(action_trainer2)
        if valid_action == False:
            print("The chosen action is invalid due to not being able to switch to a fainted Pokémon or the chosen move not having any PP left")
                
    battle.turn(action_trainer1, action_trainer2)
    print(battle.get_all_text())

print(f'Trainer {battle.get_winner().name} won this battle!')