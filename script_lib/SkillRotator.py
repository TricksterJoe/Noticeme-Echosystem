import time


class Skill:
    SkillName: str
    SkillKey: str


class SkillGroup:
    Skills: list[Skill]
    LastCasted: float


class SkillRotator:
    def __init__(self, CDTracker, p):
        self.CDTracker = CDTracker
        self.p = p
        self.Groups: dict[str, SkillGroup] = {}

    def CreateGroup(self, GroupName: str):
        if GroupName in self.Groups:
            print("Group already set.")
            return

        skillGroup = SkillGroup()
        skillGroup.Skills = []
        skillGroup.LastCasted = time.time()
        self.Groups[GroupName] = skillGroup

    def AddSkillToGroup(self, GroupName: str, SkillName: str, SkillKey: str):
        if GroupName not in self.Groups:
            print(f"{GroupName} not in Groups!")

        skill = Skill()
        skill.SkillKey = SkillKey
        skill.SkillName = SkillName

        self.Groups[GroupName].Skills.append(skill)

    def CastGroups(self):
        for group, skillgroups in self.Groups.items():
            if time.time() - skillgroups.LastCasted <= 10:
                continue

            flag = False
            for skill in skillgroups.Skills:
                if self.CDTracker.IsActive(skill.SkillName):
                    flag = True
                    break

            if flag == True:
                continue

            for skill in skillgroups.Skills:
                if self.CDTracker.IsReady(skill.SkillName):
                    print(f"Casting {skill.SkillName}")
                    time.sleep(0.5)
                    self.p.press(skill.SkillKey)
                    skillgroups.LastCasted = time.time()
                    return

    # def CastGuildSkills(self):
    #     if time.time() - self.Last_Casted <= 20:
    #         return

    #     Guild_Damage_Ready = self.CDTracker.IsReady('Guild_Damage')
    #     Guild_Damage_Active = self.CDTracker.IsActive('Guild_Damage')

    #     Guild_Crit_Ready = self.CDTracker.IsReady('Guild_Crit')
    #     Guild_Crit_Active = self.CDTracker.IsActive('Guild_Crit')

    #     if Guild_Damage_Active == False and Guild_Crit_Active == False:
    #         if Guild_Crit_Ready == True:
    #             print("Casting Crit")
    #             time.sleep(0.5)
    #             self.p.press(self.Crit_Key)
    #             self.Last_Casted = time.time()
    #             return
    #         elif Guild_Damage_Ready == True:
    #             print("Casting Damage")
    #             time.sleep(0.5)
    #             self.p.press(self.Damage_Key)
    #             self.Last_Casted = time.time()
    #             return
