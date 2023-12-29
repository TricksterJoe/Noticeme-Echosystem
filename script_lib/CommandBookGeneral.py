import time


class Skill:
    NAME: str
    KEY: str
    X: list[float]
    Y: list[float]
    TYPE: str
    isAttack: bool


class CommandBook:
    def __init__(self, p, Utility, CDTracker, JUMP="SPACE", FLASH_JUMP="F", ROPE_LIFT="T", MesoExplosion="", AutoFeed=False):
        self.__p = p
        self.__Utility = Utility
        self.__JUMP = JUMP
        self.MesoExplosion = MesoExplosion
        self.__FLASH_JUMP = FLASH_JUMP
        self.__ROPE_LIFT = ROPE_LIFT
        self.__skills: list[Skill] = []
        self.__LAST_CASTED = time.time()
        self.__MAIN_ATTACK = ""
        self.CDTracker = CDTracker
        self.AutoFeed = AutoFeed
        self.AutoFeedTimer = time.time()

    def SetMainAttackSkills(self, key: str):
        self.__MAIN_ATTACK = key

    def AddSkill(self, NAME: str, key: str, X: list[float, float], Y: list[float, float], type: str, isAttack: bool):
        skill = Skill()
        skill.KEY = key
        skill.X = X
        skill.Y = Y
        skill.NAME = NAME
        skill.TYPE = type
        skill.isAttack = isAttack
        self.__skills.append(skill)

    def Assault(self, direction=""):
        if direction == "DOWN":
            self.__p.hold("DOWN")
            time.sleep(0.1)
        elif direction == "UP":
            self.__p.hold("UP")
            time.sleep(0.1)
        self.__p.press("V")
        time.sleep(0.5)
        self.__p.release_all()

    def Attack(self):
        if self.__MAIN_ATTACK == "":
            print("No Attack Key Was Set!")
            return
        self.__p.release_all()
        self.__p.press(self.__MAIN_ATTACK)
        time.sleep(0.1)
        if self.MesoExplosion != "":
            self.__p.press(self.MesoExplosion)  # patch
            time.sleep(0.05)

    def JumpDown(self):
        self.__p.hold("DOWN")
        # time.sleep(0.015)
        self.__p.press(self.__JUMP)
        self.__p.release_all()

    def JumpRope(self, hold=True):
        self.__p.press(self.__ROPE_LIFT)
        if hold:
            time.sleep(0.03)
            self.__p.hold(self.__JUMP)
            time.sleep(1)
            self.__p.release(self.__JUMP)
        time.sleep(1)

    def UpJump(self):
        self.__p.release_all()
        self.__p.hold("UP")
        time.sleep(0.015)
        self.__p.press(self.__JUMP)
        time.sleep(0.015)
        self.__p.press(self.__JUMP)
        self.__p.release_all()

    def Jump(self):
        self.__p.release_all()
        self.__p.press(self.__JUMP)
        time.sleep(0.015)

    def FlashJump(self):
        self.__p.release_all()
        time.sleep(0.01)
        self.__p.press(self.__JUMP)
        time.sleep(0.02)
        self.__p.press(self.__FLASH_JUMP)
        time.sleep(0.02)

    def CastSkill(self, skill, HoldDown=False):
        self.__p.release_all()
        time.sleep(0.015)
        if HoldDown:
            self.__p.hold("DOWN")
            time.sleep(0.1)
            self.__p.press(skill)
            time.sleep(0.2)
            self.__p.release("DOWN")
            time.sleep(0.1)
            return
        self.__p.press(skill)
        time.sleep(0.2)

    def CastSkills(self) -> bool:
        if self.AutoFeed:
            if time.time() - self.AutoFeedTimer > 30:
                time.sleep(0.5)
                self.__p.press("=")
                self.AutoFeedTimer = time.time()

        if time.time() - self.__LAST_CASTED <= 3:
            return False
        for skill in self.__skills:
            if len(skill.X) == 2 and not self.__Utility.PlayerBetweenX(skill.X[0], skill.X[1]):
                continue
            if len(skill.Y) == 2 and not self.__Utility.PlayerBetweenY(skill.Y[0], skill.Y[1]):
                continue

            if skill.TYPE == "HOTKEY":
                if self.CDTracker.IsReady(skill.NAME):
                    if skill.NAME == "Dark_Omen":
                        time.sleep(0.5)
                    print(f"Casting {skill.NAME}")
                    if skill.isAttack == False:
                        time.sleep(0.5)
                    self.CastSkill(skill.KEY)
                    self.__LAST_CASTED = time.time()
                    return True
            else:
                if self.CDTracker.IsActive(skill.NAME) == False:
                    print(f"Casting {skill.NAME}")
                    if skill.isAttack == False:
                        time.sleep(0.5)
                    self.CastSkill(skill.KEY)
                    self.__LAST_CASTED = time.time()
                    return True
        return False
