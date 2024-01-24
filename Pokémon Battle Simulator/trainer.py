from __future__ import annotations

import pokemon as pk
import battle as bt

import global_settings as gs
import global_data as gd


class Trainer:
    def __init__(
        self, name: str, poke_list: list[pk.Pokemon], selection: callable = None
    ):
        """
        Creating a Trainer object requires a name, party, and optional selection function.

        Required

        - name: Trainer's name or nickname
        - poke_List: list of Trainer's Pokemon objects

        Optional

        - selection: function that will be called whenever a selection needs to be made (except for using items)

        If no selection function is provided or the provided selection function does not select a Pokemon correctly,
        the first available Pokemon in the party will be automatically selected.
        """
        if not isinstance(poke_list, list) or not all(
            [isinstance(p, pk.Pokemon) for p in poke_list]
        ):
            raise Exception("Attempted to create Trainer with invalid party")
        if len(poke_list) < gs.POKE_NUM_MIN or len(poke_list) > gs.POKE_NUM_MAX:
            raise Exception(
                "Attempted to create Trainer with invalid number of Pokemon"
            )
        if any([poke.trainer for poke in poke_list]):
            raise Exception(
                "Attempted to create Trainer with Pokemon in another Trainer's party"
            )
        if not name or not isinstance(name, str):
            raise Exception("Attempted to create Trainer without providing name")
        if selection and not isinstance(selection, callable):
            raise Exception(
                "Attempted to create Trainer with invalid selection function"
            )
        self.selection = selection
        self.name = name
        self.poke_list = poke_list
        for poke in self.poke_list:
            poke.trainer = self
        self.in_battle = False

    def start_pokemon(self, battle: bt.Battle):
        for poke in self.poke_list:
            poke.start_battle(battle)
        self.current_poke = self.poke_list[0]
        self.num_fainted = 0
        self.in_battle = False
        self.has_moved = False

    def is_valid_action(self, action: list[str]) -> bool:
        if not isinstance(action, list) or len(action) < 2:
            return False
        if action[gs.ACTION_TYPE] == gd.MOVE:
            return self.can_use_move(action)
        if action == gd.SWITCH:
            return self.can_switch_out()
        return False

    def can_switch_out(self) -> bool:
        return self.num_fainted != len(self.poke_list) - 1

    def can_use_move(self, move_action: list[str]) -> bool:
        if (
            not isinstance(move_action, list)
            or not isinstance(move_action[gs.ACTION_TYPE], str)
            or move_action[gs.ACTION_TYPE] != "move"
        ):
            return False
        if len(move_action) == 2:
            return any(
                [
                    move_action[gs.ACTION_VALUE] == move.name
                    for move in self.current_poke.get_available_moves()
                ]
            )
        return False