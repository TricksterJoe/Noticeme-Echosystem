import time

from typing import Callable


class Summon:
    NAME: str
    KEY: str
    X: float
    Y: float
    X_TRIGGER: list[float]
    Y_TRIGGER: list[float]
    START_SUMMON_PROCEDURE: bool
    LAST_SUMMONED: float
    IS_UP: bool
    IS_PRIO: bool
    WAS_SUMMONED: bool
    Function: Callable


class Summoner:
    def __init__(self, p, g, Util, CommandBook, CDTracker, AllTogether=False):
        self.__p = p
        self.__g = g
        self.__util = Util
        self.__Command = CommandBook
        self._SUMMONS: list[Summon] = []
        self.CDTracker = CDTracker
        self.AllTogether = AllTogether
        self.SummonForAll = False

    def AddSummon(self, NAME: str, KEY: str, X: float, Y: float, X_TRIGGER: list[float], Y_TRIGGER: list[float], is_prio=False, Func=None):
        summon = Summon()
        summon.NAME = NAME
        summon.KEY = KEY
        summon.X = X
        summon.Y = Y
        summon.X_TRIGGER = X_TRIGGER
        summon.Y_TRIGGER = Y_TRIGGER
        summon.START_SUMMON_PROCEDURE = False
        summon.LAST_SUMMONED = time.time() - 60
        summon.IS_UP = False
        summon.IS_PRIO = is_prio
        summon.WAS_SUMMONED = False
        summon.Function = Func
        self._SUMMONS.append(summon)

    def PerformSummon(self):
        if self.AllTogether == False:
            flag = False
            for Summon in self._SUMMONS:
                if not Summon.START_SUMMON_PROCEDURE:
                    continue
                flag = True

                location = self.__g.get_player_location()
                if location is None:
                    continue
                x_player, y_player = location

                if not Summon.X - 2 <= x_player <= Summon.X + 2 or not Summon.Y - 2 <= y_player <= Summon.Y:
                    if Summon.NAME == "Erda_Shower":
                        self.__p.go_to((Summon.X, Summon.Y))
                    else:
                        self.__p.go_to((Summon.X, Summon.Y))
                    continue

                time.sleep(0.5)
                if Summon.NAME == "Erda_Shower":
                    self.__p.press("LEFT")  # change
                    self.__Command.CastSkill(Summon.KEY)
                else:
                    self.__Command.CastSkill(Summon.KEY)
                time.sleep(0.3)
                Summon.LAST_SUMMONED = time.time()
                Summon.START_SUMMON_PROCEDURE = False
                break

            return flag
        else:
            if self.SummonForAll == False:
                return False
            prio_summon = next(
                (x for x in self._SUMMONS if x.IS_PRIO == True), None)
            non_prio_summon = next(
                (x for x in self._SUMMONS if x.IS_PRIO == False), None)
            if prio_summon == None or non_prio_summon == None:
                print("Couldn't find a prio/non prio summon!!")
                self.ResetSummons()
                return True

            if prio_summon.WAS_SUMMONED == False:
                res = prio_summon.Function()
                if res:
                    prio_summon.WAS_SUMMONED = True
                return True

            if non_prio_summon.WAS_SUMMONED == False:
                res = non_prio_summon.Function()
                if res:
                    non_prio_summon.WAS_SUMMONED = True
                return True
            self.ResetSummons()
            return True

    def ResetSummons(self):
        for Summon in self._SUMMONS:
            Summon.IS_UP = False
            Summon.WAS_SUMMONED = False
            self.SummonForAll = False

    def ProcessSummons(self):
        for Summon in self._SUMMONS:
            if time.time() - Summon.LAST_SUMMONED <= 10:
                continue
            if not self.CDTracker.IsReady(Summon.NAME):
                continue
            Summon.IS_UP = True
            if self.AllTogether == False:
                if len(Summon.X_TRIGGER) == 2 and not self.__util.PlayerBetweenX(Summon.X_TRIGGER[0], Summon.X_TRIGGER[1]):
                    continue
                if len(Summon.Y_TRIGGER) == 2 and not self.__util.PlayerBetweenY(Summon.Y_TRIGGER[0], Summon.Y_TRIGGER[1]):
                    continue
                Summon.START_SUMMON_PROCEDURE = True
                return True

        if self.SummonForAll == True:
            return True

        if self.AllTogether == True:
            if all((SummonCheck.IS_UP == True for SummonCheck in self._SUMMONS)):
                print("Starting procedure")
                self.SummonForAll = True
                return True

        self.ResetSummons()

        return False
