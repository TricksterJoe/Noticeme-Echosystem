import pickle
import time
import random
import importlib
import cv2
import threading

import script_lib.Utilitiy as Util
import script_lib.CommandBookGeneral as CommandBookGeneral
import script_lib.Summoner as Summoner
import script_lib.CoolDownTracker as CoolDownTracker
import script_lib.ItemManager as ItemsManager
import script_lib.PixelFinder as PixelFinder
import script_lib.SkillRotator as SkillRotator
importlib.reload(Util)
importlib.reload(CommandBookGeneral)
importlib.reload(Summoner)
importlib.reload(CoolDownTracker)
importlib.reload(ItemsManager)
importlib.reload(PixelFinder)
importlib.reload(SkillRotator)
# KEY BINDINGS #
CRUEL_STAB = "A"
SHADOW_ASSULT = "V"
MESO_EXPLOSION = "D"
# KEY BINDINGS #

# COOLDOWN KEYS#
SHADOW_VEIL = "7"
SUDDEN_RAID = "6"
SSF = "3"
MAPLE_WARRIOR = "N"
# COOLDOWN KEYS#

# SUMMONS #
DARK_FLARE = "8"
ERDA_SHOWERS = "J"
# SUMMONS #

# SPOT SETTINGS #
start = (167.5, 62.5)
start1 = (52.5, 62.5)
# SPOT SETTINGS #

minimap = (9, 61, 231, 140)
g = Game(minimap)
p = Player(g)


def multi_match_wrapper(img):
    return multi_match(img)


def capture_screen_wrapper():
    return capture_window()


Utility = Util.Utility(g)
CDTracker = CoolDownTracker.CoolDownTracker(
    multi_match_f=multi_match_wrapper, capture_screen=capture_screen_wrapper, capture_cycle=1.1)
PXFinder = PixelFinder.PixelFinder(
    multi_match_f=multi_match_wrapper, capture_screen=capture_screen_wrapper)

CDTracker.AddHotkeySkill("Sudden_Raid", 1)
CDTracker.AddHotkeySkill("Dark_Flare", 2)
CDTracker.AddHotkeySkill("Shadow_Veil", 1)
CDTracker.AddHotkeySkill("Erda_Shower", 1)
CDTracker.AddHotkeySkill("SSF", 1)


CDTracker.AddHotkeySkill("Guild_Damage", 3)
CDTracker.AddHotkeySkill("Guild_Crit", 3)

CDTracker.AddBuffbarSkill("Guild_Damage", 3)
CDTracker.AddBuffbarSkill("Guild_Crit", 3)

CDTracker.AddHotkeySkill("Shadow_Walker", 2)
# CDTracker.AddHotkeySkill("Last_Resort", 2)

CDTracker.AddBuffbarSkill("Shadow_Walker", 2)
# CDTracker.AddBuffbarSkill("Last_Resort", 2)


CDTracker.AddBuffbarSkill("Maple_Warrior", 1)
CDTracker.AddBuffbarSkill("2x", 3)
CDTracker.AddBuffbarSkill("Gold_Pot", 3)
CDTracker.AddBuffbarSkill("LEGION_2x", 3)
CDTracker.AddBuffbarSkill("LEGION_meso", 3)

ItemManager = ItemsManager.ItemManager(
    CDTracker=CDTracker, PXFinder=PXFinder, p=p)
# ItemManager.AddItem("2x", "2x")
ItemManager.AddItem("Gold_Pot", "Gold_Pot")
# ItemManager.AddItem("LEGION_2x", "2x")
# ItemManager.AddItem("LEGION_meso", "meso")

ItemManager.FinishSetUp()
CommandBook = CommandBookGeneral.CommandBook(
    p=p, Utility=Utility, CDTracker=CDTracker, JUMP="SPACE", FLASH_JUMP="F", ROPE_LIFT="T")
CommandBook.SetMainAttackSkills(CRUEL_STAB)

# CommandBook.AddSkill("Sudden_Raid", SUDDEN_RAID, [
#    81.5, 124.5], [], "HOTKEY", True)  # SUDDEN RAID
CommandBook.AddSkill("Shadow_Veil", SHADOW_VEIL, [
                     136.5, 156.5], [], "HOTKEY", True)  # SHADOW VEIL
# CommandBook.AddSkill("SSF", SSF, [], [], "HOTKEY", True)  # SSF
CommandBook.AddSkill("Maple_Warrior", MAPLE_WARRIOR, [], [], "BUFFBAR", False)

SummonerHandler = Summoner.Summoner(
    p, g, Utility, CommandBook, CDTracker=CDTracker)
SummonerHandler.AddSummon("Erda_Shower", ERDA_SHOWERS,
                          146.5, 30.5, [130.5, 160.5], [])
SummonerHandler.AddSummon("Dark_Flare", DARK_FLARE,
                          69.5, 28.5, [59.5, 79.5], [])


SkillsRotator = SkillRotator.SkillRotator(CDTracker=CDTracker, p=p)

SkillsRotator.CreateGroup("Guild_Skills")
SkillsRotator.AddSkillToGroup("Guild_Skills", "Guild_Crit", "0")
SkillsRotator.AddSkillToGroup("Guild_Skills", "Guild_Damage", "9")

SkillsRotator.CreateGroup("Normal_Buffs")
# SkillsRotator.AddSkillToGroup("Normal_Buffs", "Shadow_Walker", "5")
# SkillsRotator.AddSkillToGroup("Normal_Buffs", "Last_Resort", "4")


rune = 0


y_threshhold = 45.5 + 1


def rune_solver():
    global rune
    rune_location = g.get_rune_location()
    if rune_location and rune is not None:
        if checkbox_var5.get():
            print(rune_location)
            print("A rune has appeared.")
            p.press("LEFT")
            solve_rune(g, p, rune_location, 1)
            rune = rune + 1


def test():
    while 1 == 1:
        print("HELLLLLO")
        time.sleep(0.1)


def auto():
    CDThread = threading.Thread(target=CDTracker.CooldownUpdater, args=())
    CDThread.start()
    direction = 'LEFT'
    time.sleep(1)

    while True:
        if not CDThread.is_alive():
            CDThread = None
            CDThread = threading.Thread(
                target=CDTracker.CooldownUpdater, args=())
            CDThread.start()

        isCasting = ItemManager.CheckForRecast()
        # isCasting = False
        if SummonerHandler.PerformSummon():
            continue
        if SummonerHandler.ProcessSummons():
            continue
        rune_solver()

        SkillsRotator.CastGroups()
        x_player, y_player = g.get_player_location()

        if y_player == 28.5:
            p.press("LEFT")
            time.sleep(0.015)
            direction = "RIGHT"
            CommandBook.FlashJump()
            time.sleep(0.1)
            # CommandBook.CastSkill("2")
            CommandBook.Attack()
            time.sleep(0.8)
            continue
        elif y_player == 30.5:
            p.press("RIGHT")
            time.sleep(0.015)
            direction = "LEFT"
            CommandBook.FlashJump()
            time.sleep(0.1)
            CommandBook.Attack()
            time.sleep(0.3)
            continue
        elif y_player <= y_threshhold+1:
            if 31.5 <= y_player <= 48.5:
                print(f"Pressed Left {y_player}")
                p.press("LEFT")
            else:
                print(f"Pressed Right {y_player}")
                p.press("RIGHT")
            print("Here?")
            time.sleep(0.015)
            CommandBook.JumpDown()
            time.sleep(0.05)
            CommandBook.Attack()
            time.sleep(0.3)
            continue

        # if y_player == 34.5:
        #     if 147.5 <= x_player <= 195.5:
        #         p.press("LEFT")
        #         CommandBook.FlashJump()
        #         time.sleep(0.1)
        #         CommandBook.Attack()
        #         time.sleep(0.2)
        #         continue
        # elif y_player == 32.5 or y_player == 27.5:
        #     if 87.5 <= x_player <= 130.5 or y_player == 27.5:
        #         p.press("LEFT")
        #         CommandBook.FlashJump()
        #         time.sleep(0.1)
        #         if 85.5 <= x_player <= 100.5:
        #             CommandBook.CastSkill("2")
        #             time.sleep(0.1)
        #         else:
        #             CommandBook.Attack()
        #         time.sleep(0.2)
        #         continue
        #     else:
        #         CommandBook.JumpDown()
        #         time.sleep(0.05)
        #         continue
        # if y_player <= y_threshhold:
        #     CommandBook.JumpDown()
        #     time.sleep(0.05)
        #     continue

        if x_player <= start1[0]:
            p.release_all()
            time.sleep(0.1)
            direction = 'RIGHT'

        if x_player >= start[0]:
            p.release_all()
            time.sleep(0.1)
            direction = 'LEFT'

        p.press(direction)

        CommandBook.FlashJump()

        if isCasting == False:
            result = CommandBook.CastSkills()
            if result:
                continue
        # time.sleep(0.1)
        CommandBook.Attack()
        time.sleep(0.2)
