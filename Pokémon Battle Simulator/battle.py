from __future__ import annotations
from random import randrange

from move import Move
from poke_data import PokeData

import trainer as tr

import process_move as pm

import global_settings as gs
import global_data as gd


class Battle:
    def __init__(self, t1: tr.Trainer, t2: tr.Trainer):
        if not isinstance(t1, tr.Trainer) or not isinstance(t2, tr.Trainer):
            raise Exception("Attempted to create Battle with invalid Trainer")
        if t1.in_battle or t2.in_battle:
            raise Exception("Attempted to create Battle with Trainer already in battle")
        for t1_poke in t1.poke_list:
            for t2_poke in t2.poke_list:
                if t1_poke is t2_poke:
                    raise Exception("Attempted to create Battle with Pokemon that is in both Trainers' parties")
        for t1_poke in t1.poke_list:
            if t1_poke.in_battle:
                raise Exception("Attempted to create Battle with Pokemon already in battle")
        for t2_poke in t2.poke_list:
            if t2_poke.in_battle:
                raise Exception("Attempted to create Battle with Pokemon already in battle")

        self.t1 = t1
        self.t2 = t2
        self.battle_started = False
        self.all_text = []
        self.cur_text = []

    def start(self):
        self.t1.start_pokemon(self)
        self.t2.start_pokemon(self)
        self.t1.in_battle = True
        self.t2.in_battle = True
        self.t1_faint = False
        self.t2_faint = False
        self.battle_started = True
        self.winner = None
        self.last_move = None
        self.last_move_next = None
        self.turn_count = 0
        self.add_text(self.t1.name + " sent out " + self.t1.current_poke.nickname + "!")
        self.add_text(self.t2.name + " sent out " + self.t2.current_poke.nickname + "!")

    def turn(self, t1_turn: list[str], t2_turn: list[str]) -> bool | None:
        self.turn_count += 1
        if not self.battle_started:
            raise Exception("Cannot use turn on Battle that hasn't started")
        if self.is_finished():
            return

        t1_move = t1_turn.copy()
        t2_move = t2_turn.copy()
        t1_move_data = None
        t2_move_data = None
        t1_mv_check_bypass = False
        t2_mv_check_bypass = False
        t1_first = None

        t1_move, t1_move_data, t1_mv_check_bypass = self._pre_process_move(
            self.t1, [t1_move, t1_move_data, t1_mv_check_bypass]
        )
        t2_move, t2_move_data, t2_mv_check_bypass = self._pre_process_move(
            self.t2, [t2_move, t2_move_data, t2_mv_check_bypass]
        )

        if (
            not isinstance(t1_move, list)
            or not all(isinstance(t1_move[i], str) for i in range(len(t1_move)))
            or len(t1_move) < 2
            or t1_move[gs.ACTION_TYPE].lower() not in gs.ACTION_PRIORITY
        ):
            raise Exception("Trainer 1 invalid turn action")
        if (
            not isinstance(t2_move, list)
            or not all(isinstance(t2_move[i], str) for i in range(len(t2_move)))
            or len(t2_move) < 2
            or t2_move[gs.ACTION_TYPE].lower() not in gs.ACTION_PRIORITY
        ):
            raise Exception("Trainer 2 invalid turn action")

        self.t1.has_moved = False
        self.t2.has_moved = False
        t1_move = [e.lower() for e in t1_move]
        t2_move = [e.lower() for e in t2_move]
        self.t1_fainted = False
        self.t2_fainted = False
        self.t1.current_poke.turn_damage = False
        self.t2.current_poke.turn_damage = False

        if not t1_move_data and t1_move[gs.ACTION_TYPE] == gd.MOVE:
            t1_move_data = self.t1.current_poke.get_move_data(t1_move[gs.ACTION_VALUE])
            if not t1_move_data:
                t1_move_data = Move(PokeData.get_single_move(t1_move[gs.ACTION_VALUE]))
        if not t2_move_data and t2_move[gs.ACTION_TYPE] == gd.MOVE:
            t2_move_data = self.t2.current_poke.get_move_data(t2_move[gs.ACTION_VALUE])
            if not t2_move_data:
                t2_move_data = Move(PokeData.get_single_move(t2_move[gs.ACTION_VALUE]))

        t1_prio = gs.ACTION_PRIORITY[t1_move[gs.ACTION_TYPE]]
        t2_prio = gs.ACTION_PRIORITY[t2_move[gs.ACTION_TYPE]]
        t1_first = t1_prio >= t2_prio
        if t1_prio == 1 and t2_prio == 1:
            spd_dif = (
                self.t1.current_poke.stats_actual[gs.SPD]
                - self.t2.current_poke.stats_actual[gs.SPD]
            )
            if spd_dif == 0:
                t1_first = randrange(2) < 1
            else:
                t1_first = spd_dif > 0
        self.add_text("Turn " + str(self.turn_count) + ":")
        
        if t1_first:
            if self.t1.current_poke.is_alive:
                # trainer 1 turn
                self._half_turn(self.t1, self.t2, t1_move, t1_move_data)
            self._faint_check()
            if self.t2.current_poke.is_alive:
                # trainer 2 turn
                self._half_turn(self.t2, self.t1, t2_move, t2_move_data)
            self._faint_check()
        else:
            if self.t2.current_poke.is_alive:
                # trainer 2 turn
                self._half_turn(self.t2, self.t1, t2_move, t2_move_data)
            self._faint_check()
            if self.t1.current_poke.is_alive:
                # trainer 1 turn
                self._half_turn(self.t1, self.t2, t1_move, t1_move_data)
            self._faint_check()

        if self.winner:
            return

        dif = (
            self.t1.current_poke.stats_actual[gs.SPD]
            - self.t2.current_poke.stats_actual[gs.SPD]
        )
        if dif > 0:
            faster = self.t1
            slower = self.t2
        elif dif < 0:
            faster = self.t2
            slower = self.t1
        else:
            faster = self.t1 if randrange(2) < 1 else self.t2
            slower = self.t2 if faster is self.t1 else self.t1
            
        self._faint_check()
        if self.winner:
            return
        if not faster.current_poke.is_alive:
            self._process_selection(faster)
        if not slower.current_poke.is_alive:
            self._process_selection(slower)

    def get_cur_text(self) -> list:
        cur_t = self.cur_text
        self.cur_text = []
        return cur_t

    def get_all_text(self) -> list:
        return self.all_text

    def _half_turn(
        self,
        attacker: tr.Trainer,
        defender: tr.Trainer,
        a_move: list[str],
        a_move_data: Move = None,
    ):
        if self.winner:
            return
        if a_move[gs.ACTION_TYPE] == "other":
            self._process_other(attacker, a_move)

        elif self._process_pp(a_move_data):
            pm.process_move(
                attacker.current_poke,
                defender.current_poke,
                self,
                a_move_data.get_tcopy()
            )
            if self.last_move_next:
                self.last_move, self.last_move_next = self.last_move_next, None
        attacker.has_moved = True

    def _process_pp(self, move_data: Move) -> bool:
        if move_data.name == "struggle":
            return True
        if move_data.cur_pp <= 0:
            raise Exception("Trainer attempted to use move that has no pp left")
        move_data.cur_pp -= 1
        return True
    
    def _pre_process_move(self, trainer: tr.Trainer, t_move: list) -> list:
        if (
            t_move[gs.PPM_MOVE][gs.ACTION_TYPE] == gd.MOVE
            and trainer.current_poke.no_pp()
        ):
            t_move[gs.PPM_MOVE] = gd.STRUGGLE
            t_move[gs.PPM_MOVE_DATA] = None
            t_move[gs.PPM_BYPASS] = True
        return t_move

    def _victory(self, winner: tr.Trainer, loser: tr.Trainer):
        self._process_end_battle()
        self.add_text(winner.name + " has defeated " + loser.name + "!")
        self.winner = winner

    def _process_selection(self, selector: tr.Trainer) -> bool:
        if self.winner:
            return True
        old_poke = selector.current_poke
        if selector.selection:
            selector.selection(self)
        if not selector.current_poke.is_alive or selector.current_poke is old_poke:
            for p in selector.poke_list:
                if p.is_alive and not p is old_poke:
                    selector.current_poke = p
                    break
        if not selector.current_poke.is_alive or selector.current_poke is old_poke:
            return True
        self.add_text(selector.name + " sent out " + selector.current_poke.nickname + "!")
        return False
    
    def _process_other(
        self, attacker: tr.Trainer, a_move: list[str]
    ):
        if a_move == gd.SWITCH:
            self._process_selection(attacker)
            

    def _faint_check(self):
        if self.winner:
            return
        if not self.t1_fainted and not self.t1.current_poke.is_alive:
            self.add_text(self.t1.current_poke.nickname + " fainted!")
            self.t1_fainted = True
            self.t1.num_fainted += 1
            if self.t1.num_fainted == len(self.t1.poke_list):
                self._victory(self.t2, self.t1)
                return
        if not self.t2_fainted and not self.t2.current_poke.is_alive:
            self.add_text(self.t2.current_poke.nickname + " fainted!")
            self.t2_fainted = True
            self.t2.num_fainted += 1
            if self.t2.num_fainted == len(self.t2.poke_list):
                self._victory(self.t1, self.t2)
                return

    def _process_end_battle(self):
        for poke in self.t1.poke_list:
            poke.battle_end_reset()
        for poke in self.t2.poke_list:
            poke.battle_end_reset()
        self.t1.in_battle = False
        self.t2.in_battle = False

    def add_text(self, txt: str):
        if not self.winner:
            self.all_text.append(txt)
            self.cur_text.append(txt)

    def _pop_text(self):
        self.all_text.pop()
        self.cur_text.pop()

    def is_finished(self) -> bool:
        return not not self.winner

    def get_winner(self) -> tr.Trainer | None:
        return self.winner