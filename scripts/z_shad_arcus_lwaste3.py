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
SHADOW_VEIL = "3"
SUDDEN_RAID = "5"
SSF = "4"
MAPLE_WARRIOR = "N"
# COOLDOWN KEYS#

# SUMMONS #
DARK_FLARE = "2"
ERDA_SHOWERS = "1"
# SUMMONS #
# SPOT SETTINGS #
start = (171.5, 55.5)
start1 = (19.5, 55.5)
# SPOT SETTINGS #

minimap = (9, 61, 201, 135)
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
CDTracker.AddBuffbarSkill("dojo_2x", 3)
CDTracker.AddBuffbarSkill("mvp_15x", 3)

ItemManager = ItemsManager.ItemManager(
    CDTracker=CDTracker, PXFinder=PXFinder, p=p)
ItemManager.AddItem("mvp_15x", "1.5x")
# ItemManager.AddItem("2x", "2x")
ItemManager.AddItem("Gold_Pot", "Gold_Pot")
ItemManager.AddItem("LEGION_2x", "2x")
# ItemManager.AddItem("dojo_2x", "2x")
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
                          93.5, 26.5, [78.5, 108.5], [])
SummonerHandler.AddSummon("Dark_Flare", DARK_FLARE,
                          53.5, 28.5, [35.5, 65.5], [])


SkillsRotator = SkillRotator.SkillRotator(CDTracker=CDTracker, p=p)

SkillsRotator.CreateGroup("Guild_Skills")
SkillsRotator.AddSkillToGroup("Guild_Skills", "Guild_Crit", "Q")
SkillsRotator.AddSkillToGroup("Guild_Skills", "Guild_Damage", "U")

SkillsRotator.CreateGroup("Normal_Buffs")
# SkillsRotator.AddSkillToGroup("Normal_Buffs", "Shadow_Walker", "5")
# SkillsRotator.AddSkillToGroup("Normal_Buffs", "Last_Resort", "4")


rune = 0


y_threshhold = 42.5 + 1

lastMoved = time.time()


def rune_solver():
    global rune
    rune_location = g.get_rune_location()
    if rune_location and rune is not None:
        if checkbox_var5.get():
            print(rune_location)
            if rune_location == (70.0, 10.0):
                rune_location = (64.5, 10.0)
            print("A rune has appeared.")
            p.press("LEFT")
            solve_rune(g, p, rune_location, 1, delay2=1.3)
            lastMoved = time.time()
            rune = rune + 1


def test():
    while 1 == 1:
        time.sleep(0.1)


def auto():
    CDThread = threading.Thread(target=CDTracker.CooldownUpdater, args=())
    CDThread.start()
    direction = 'LEFT'
    time.sleep(1)
    lastMoved = time.time()
    x_value = 0
    while True:

        if not CDThread.is_alive():
            CDThread = None
            CDThread = threading.Thread(
                target=CDTracker.CooldownUpdater, args=())
            CDThread.start()

        isCasting = ItemManager.CheckForRecast()
        if SummonerHandler.PerformSummon():
            lastMoved = time.time()
            continue
        if SummonerHandler.ProcessSummons():
            lastMoved = time.time()
            continue
        rune_solver()

        # SkillsRotator.CastGroups()
        x_player, y_player = g.get_player_location()

        if x_value == x_player:
            if time.time() - lastMoved > 2:
                time.sleep(0.1)
                p.hold("LEFT")
                time.sleep(0.015)
                p.press("SPACE")
                p.release_all()
                time.sleep(0.5)
                lastMoved = time.time()
                continue
        else:
            x_value = x_player
            lastMoved = time.time()
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
        elif y_player == 26.5:
            CommandBook.CastSkill(SUDDEN_RAID)
            time.sleep(0.5)
            CommandBook.JumpDown()
            time.sleep(0.3)
            CommandBook.Assault("DOWN")
            time.sleep(0.1)
            lastMoved = time.time()
            continue
        elif y_player <= y_threshhold+1:
            if x_player >= 99.5:
                p.press("RIGHT")
                direction = "RIGHT"
            else:
                p.press("RIGHT")
                direction = "RIGHT"

            CommandBook.FlashJump()

            # time.sleep(0.1)
            CommandBook.Attack()
            time.sleep(0.2)
            continue

        if x_player <= start1[0]:
            p.release_all()
            time.sleep(0.1)
            direction = 'RIGHT'

        if x_player >= start[0]:
            p.release_all()
            time.sleep(0.1)
            direction = 'LEFT'

        p.press(direction)

        if isCasting == False:
            result = CommandBook.CastSkills()
            if result:
                continue
        if y_player == 55.5:
            CommandBook.FlashJump()

            # time.sleep(0.1)
            CommandBook.Attack()
            time.sleep(0.1)
