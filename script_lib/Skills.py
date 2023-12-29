from enum import Enum

class SkillType(Enum):
    MAIN_ATTACK = 1
    COOLDOWN_ATTACK = 2
    SUMMON = 3


class SkillStructure:
    NAME: str
    TYPE: SkillType
    KEY: str

class CooldownAttack:
    X:list[float]
    Y:list[float]
    def __init__(self, skillStructure: SkillStructure):
        self.skillStructure = skillStructure


Sudden_Raid_Structure = SkillStructure()
Sudden_Raid_Structure.KEY = "6"
Sudden_Raid_Structure.NAME = "Sudden_Raid"
Sudden_Raid_Structure.TYPE = SkillType.COOLDOWN_ATTACK
Sudden_Raid = CooldownAttack(Sudden_Raid_Structure)
Sudden_Raid.X = [10,10]
Sudden_Raid.Y = []
