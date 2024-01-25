from __future__ import annotations

from poke_data import PokeData
from move import Move

import battle as bt
import conf.global_settings as gs


class Pokemon:
    def __init__(
        self,
        name: str,
        moves: [str],
        gender: str = "male",
        level: int = 100,
        nature: str = "adamant",
        cur_hp: int = None,
        stats_actual: [int] = None,
        ivs: [int] = [0]*6,
        evs: [int] = [0]*6,        
        nickname: str = None,
    ):
        self.stats_base = PokeData.get_pokemon(name)
        if not self.stats_base:
            raise Exception("Attempted to create Pokemon with invalid name")

        self.id = int(self.stats_base[gs.NDEX])
        self.name = self.stats_base[gs.NAME]
        self.types = (self.stats_base[gs.TYPE1], self.stats_base[gs.TYPE2])
        self.base = [
            int(self.stats_base[i])
            for i in range(gs.STAT_START, gs.STAT_START + gs.STAT_NUM)
        ]
        self.base_exp = int(self.stats_base[gs.BASE_EXP])
        self.gen = int(self.stats_base[gs.GEN])
        if not isinstance(level, int) or level < gs.LEVEL_MIN or level > gs.LEVEL_MAX:
            raise Exception("Attempted to create Pokemon with invalid level")
        self.level = level
        
        if (
            not gender
            or not isinstance(gender, str)
            or gender.lower() not in gs.POSSIBLE_GENDERS
        ):
            raise Exception("Attempted to create Pokemon with invalid gender")
        self.gender = gender

        if not stats_actual and not ivs and not evs:
            raise Exception("Attempted to create Pokemon without providing stats information")

        if stats_actual and (ivs or evs):
            raise Exception("Attempted to create Pokemon with conflicting stats information")

        if stats_actual:
            if not isinstance(stats_actual, list) or len(stats_actual) != gs.STAT_NUM:
                raise Exception("Attempted to create Pokemon with invalid stats")
            if not all(
                [
                    isinstance(s, int) and gs.STAT_ACTUAL_MIN < s < gs.STAT_ACTUAL_MAX
                    for s in stats_actual
                ]
            ):
                raise Exception("Attempted to create Pokemon with invalid stats")
            self.stats_actual = stats_actual
            self.ivs = ivs
            self.evs = evs
            self.nature = nature
            self.nature_effect = None
        else:
            if (
                not isinstance(ivs, list)
                or not isinstance(evs, list)
                or len(ivs) != gs.STAT_NUM
                or len(evs) != gs.STAT_NUM
            ):
                raise Exception("Attempted to create Pokemon with invalid evs or ivs")
            if not all(
                [isinstance(iv, int) and gs.IV_MIN <= iv <= gs.IV_MAX for iv in ivs]
            ):
                raise Exception("Attempted to create Pokemon with invalid ivs")
            self.ivs = ivs
            if (
                not all(
                    [isinstance(ev, int) and gs.EV_MIN <= ev <= gs.EV_MAX for ev in evs]
                )
                or sum(evs) > gs.EV_TOTAL_MAX
            ):
                raise Exception("Attempted to create Pokemon with invalid evs")
            self.evs = evs
            self.nature_effect = PokeData.nature_conversion(nature.lower())
            if not self.nature_effect:
                raise Exception("Attempted to create Pokemon without providing its nature")
            self.nature = nature.lower()
            self.calculate_stats_actual()

        self.max_hp = self.stats_actual[gs.HP]
        if cur_hp and (not isinstance(cur_hp, int) or cur_hp < 0 or cur_hp > self.max_hp):
            raise Exception("Attempted to create Pokemon with invalid hp value")
        if not cur_hp:
            cur_hp = self.stats_actual[gs.HP]
        self.cur_hp = cur_hp

        moves_data = PokeData.get_move_data(moves)
        if not moves_data:
            raise Exception("Attempted to create Pokemon with invalid moveset")
        self.moves = [Move(move_d) for move_d in moves_data]
        for i in range(len(self.moves)):
            self.moves[i].pos = i
        self.o_moves = self.moves

        if nickname and not isinstance(nickname, str):
            raise Exception("Attempted to create Pokemon with invalid nickname")
        self.nickname = nickname if nickname else self.name
        self.nickname = self.nickname.upper()

        self.original = None
        self.trainer = None

        self.is_alive = self.cur_hp != 0 
        self.in_battle = False
        
    def calculate_stats_actual(self):
        stats_actual = []
        nature_stat_changes = [1.0 for _ in range(6)]
        nature_stat_changes[self.nature_effect[0]] = gs.NATURE_INC
        nature_stat_changes[self.nature_effect[1]] = gs.NATURE_DEC
        stats_actual.append(
            ((2 * self.base[0] + self.ivs[0] + self.evs[0] // 4) * self.level) // 100
            + 10
        )
        for s in range(1, gs.STAT_NUM):
            stats_actual.append(
                (
                    ((2 * self.base[s] + self.ivs[s] + self.evs[s] // 4) * self.level)
                    // 100
                    + 5
                )
                * nature_stat_changes[s]
            )
        self.stats_actual = [int(stat) for stat in stats_actual]
        
    def start_battle(self, battle: bt.Battle):
        self.cur_battle = battle
        self.in_battle = True
        self.enemy = (
            self.cur_battle.t2
            if self.cur_battle.t1 is self.trainer
            else self.cur_battle.t1
        )

    def take_damage(self, damage: int) -> int:
        if not damage or not self.cur_battle:
            return 0
        if self.cur_hp - damage <= 0:
            self.last_damage_taken = self.cur_hp
            if not self.cur_battle:
                return
            self.cur_hp = 0
            self.is_alive = False
            self.cur_battle._faint_check()
            return self.last_damage_taken
        self.turn_damage = True
        self.cur_hp -= damage
        self.last_damage_taken = damage
        return self.last_damage_taken

    def faint(self):
        if not self.is_alive:
            return
        self.cur_hp = 0
        self.is_alive = False
        self.cur_battle._faint_check()

    def get_move_data(self, move_name: str) -> Move:
        for move in self.moves:
            if move.name == move_name:
                return move
            
    def is_move(self, move_name: str) -> bool:
        av_moves = self.get_available_moves()
        for move in av_moves:
            if move.name == move_name:
                return True
        return False

    def get_available_moves(self) -> list | None:
        av_moves = [move for move in self.moves if move.cur_pp]
        return av_moves

    def battle_end_reset(self):
        self.in_battle = False
        self.cur_battle = None
        self.enemy = None

    def no_pp(self) -> bool:
        return all(
            not move.cur_pp
            for move in self.get_available_moves()
        )