from __future__ import annotations

import global_settings as gs


class Move:
    def __init__(self, move_data: list):
        self.md = move_data
        self.id = move_data[gs.MOVE_ID]
        self.name = move_data[gs.MOVE_NAME]
        self.type = move_data[gs.MOVE_TYPE]
        self.o_power = move_data[gs.MOVE_POWER]
        self.power = move_data[gs.MOVE_POWER]
        self.max_pp = move_data[gs.MOVE_PP]
        self.acc = move_data[gs.MOVE_ACC]
        self.target = move_data[gs.MOVE_TARGET]
        self.category = move_data[gs.MOVE_CATEGORY]
        self.cur_pp = self.max_pp
        self.pos = None
        self.disabled = 0
        self.encore_blocked = False

    def reset(self):
        self.cur_pp = self.max_pp
        self.pos = None
        self.disabled = 0
        self.encore_blocked = False
        self.power = self.md[gs.MOVE_POWER]
        self.max_pp = self.md[gs.MOVE_PP]
        self.acc = self.md[gs.MOVE_ACC]
        self.category = self.md[gs.MOVE_CATEGORY]

    def get_tcopy(self) -> Move:
        copy = Move(self.md)
        copy.cur_pp = self.cur_pp
        copy.pos = self.pos
        copy.disabled = self.disabled
        return copy