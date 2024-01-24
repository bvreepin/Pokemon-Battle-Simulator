from __future__ import annotations
from random import randrange

from poke_data import PokeData
from move import Move

import pokemon as pk
import battle as bt

import global_settings as gs
import global_data as gd


def process_move(
    attacker: pk.Pokemon,
    defender: pk.Pokemon,
    battle: bt.Battle,
    move_data: Move,
):
    battle.add_text(attacker.nickname + " used " + cap_name(move_data.name) + "!")
    if not _calculate_hit_or_miss(
        attacker, battle, move_data
    ):
        return
    # attacker.last_successful_move_next = move_data
    _calculate_damage(attacker, defender, battle, move_data)
    battle._faint_check()


def _calculate_type_ef(defender: pk.Pokemon, move_data: Move) -> float:
    if move_data.type == "typeless":
        return 1

    t_mult = PokeData.get_type_ef(move_data.type, defender.types[0])
    if defender.types[1]:
        t_mult *= PokeData.get_type_ef(move_data.type, defender.types[1])
    return t_mult


def _calculate_damage(
    attacker: pk.Pokemon,
    defender: pk.Pokemon,
    battle: bt.Battle,
    move_data: Move,
    crit_chance: int = 1/24
) -> int:
    if battle.winner:
        return
    if not defender.is_alive:
        _missed(attacker, battle)
        return
    t_mult = _calculate_type_ef(defender, move_data)
    if not t_mult:
        battle.add_text("It doesn't affect " + defender.nickname)
        return

    cc = crit_chance
    if _calculate_crit(cc):
        crit_mult = 2
        battle.add_text("A critical hit!")
    else:
        crit_mult = 1

    if t_mult < 1:
        battle.add_text("It's not very effective...")
    elif t_mult > 1:
        battle.add_text("It's super effective!")

    a_stat = gs.ATK if move_data.category == gs.PHYSICAL else gs.SP_ATK
    d_stat = gs.DEF if move_data.category == gs.PHYSICAL else gs.SP_DEF

    atk_ig = attacker.stats_actual[a_stat]
    def_ig = defender.stats_actual[d_stat]
    
    ad_ratio = atk_ig / def_ig

    if move_data.type == attacker.types[0] or move_data.type == attacker.types[1]:
        stab = 1.5
    else:
        stab = 1
    random_mult = randrange(85, 101) / 100

    damage = (
        (2 * attacker.level / 5 + 2) * move_data.power * ad_ratio
    ) / 50 + 2
    damage *= crit_mult * random_mult * stab * t_mult
    damage = int(damage)
    
    damage_done = defender.take_damage(damage)
    battle._faint_check()
    
    return damage_done


def _calculate_hit_or_miss(
    attacker: pk.Pokemon,
    battle: bt.Battle,
    move_data: Move,
):
    ma = move_data.acc
    if not ma:
        return True
    elif ma == -1:
        res = randrange(1, 101) <= 30
    else:
        hit_threshold = ma
        res = randrange(1, 101) <= hit_threshold
    if not res:
        _missed(attacker, battle)
    return res


def _calculate_crit(crit_chance: int = None) -> bool:
    if not crit_chance:
        return randrange(16) < 1
    elif crit_chance == 1:
        return randrange(9) < 1
    elif crit_chance == 2:
        return randrange(5) < 1
    elif crit_chance == 3:
        return randrange(4) < 1
    elif crit_chance == 4:
        return randrange(3) < 1
    else:
        return randrange(1000) < crit_chance
    
    
def cap_name(move_name: str) -> str:
    move_name = move_name.replace("-", " ")
    words = move_name.split()
    words = [word.capitalize() for word in words]
    return " ".join(words)


def _missed(attacker: pk.Pokemon, battle: bt.Battle):
    battle.add_text(attacker.nickname + "'s attack missed!")