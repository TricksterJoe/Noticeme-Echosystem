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
QUINT_STAR = "A"
# KEY BINDINGS #

# COOLDOWN KEYS#
DARK_OMEN = "3"
# COOLDOWN KEYS#

# SUMMONS #
ERDA_SHOWERS = "1"
DARK_SERVANT = "2"
# SUMMONS #
# SPOT SETTINGS #
start = (195.5, 42.5)
start1 = (52.5, 42.5)
GROUND_Y = 42.5
# SPOT SETTINGS #

minimap = (9, 61, 227, 127)
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

CDTracker.AddHotkeySkill("Dark_Servant", 1)
CDTracker.AddHotkeySkill("Dark_Omen", 1)
CDTracker.AddHotkeySkill("Erda_Shower", 1)


CDTracker.AddHotkeySkill("Guild_Damage", 3)
CDTracker.AddHotkeySkill("Guild_Crit", 3)

CDTracker.AddBuffbarSkill("Guild_Damage", 3)
CDTracker.AddBuffbarSkill("Guild_Crit", 3)

CDTracker.AddBuffbarSkill("2x", 3)
CDTracker.AddBuffbarSkill("Gold_Pot", 3)
CDTracker.AddBuffbarSkill("LEGION_2x", 3)
CDTracker.AddBuffbarSkill("LEGION_meso", 3)
CDTracker.AddBuffbarSkill("dojo_2x", 3)
CDTracker.AddBuffbarSkill("mvp_15x", 3)

ItemManager = ItemsManager.ItemManager(
    CDTracker=CDTracker, PXFinder=PXFinder, p=p)
ItemManager.AddItem("mvp_15x", "1.5x")
ItemManager.AddItem("2x", "2x")
ItemManager.AddItem("Gold_Pot", "Gold_Pot")
ItemManager.AddItem("LEGION_2x", "2x")
# ItemManager.AddItem("dojo_2x", "2x")
# ItemManager.AddItem("LEGION_meso", "meso")

ItemManager.FinishSetUp()
CommandBook = CommandBookGeneral.CommandBook(
    p=p, Utility=Utility, CDTracker=CDTracker, JUMP="SPACE", FLASH_JUMP="F", ROPE_LIFT="T")
CommandBook.SetMainAttackSkills(QUINT_STAR)


# CommandBook.AddSkill("Dark_Omen", DARK_OMEN, [
#                      108.5, 142.5], [], "HOTKEY", True)  # SHADOW VEIL
SummonerHandler = Summoner.Summoner(
    p, g, Utility, CommandBook, CDTracker=CDTracker)
SummonerHandler.AddSummon("Erda_Shower", ERDA_SHOWERS,
                          184.5, 8.5, [170.5, 193.5], [])
SummonerHandler.AddSummon("Dark_Servant", DARK_SERVANT,
                          156.5, 16.5, [140.5, 165.5], [])


SkillsRotator = SkillRotator.SkillRotator(CDTracker=CDTracker, p=p)

SkillsRotator.CreateGroup("Guild_Skills")
SkillsRotator.AddSkillToGroup("Guild_Skills", "Guild_Crit", "Q")
SkillsRotator.AddSkillToGroup("Guild_Skills", "Guild_Damage", "U")

SkillsRotator.CreateGroup("Normal_Buffs")
# SkillsRotator.AddSkillToGroup("Normal_Buffs", "Shadow_Walker", "5")
# SkillsRotator.AddSkillToGroup("Normal_Buffs", "Last_Resort", "4")


rune = 0


y_threshhold = 9.5 + 1

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
        location = g.get_player_location()
        if location is None:
            continue
        x_player, y_player = location

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

        if y_player != GROUND_Y and y_player < 32.5:
            CommandBook.JumpDown()
            time.sleep(0.3)
            continue

        # if y_player <= y_threshhold+1:
        #     if x_player >= 99.5:
        #         p.press("RIGHT")
        #         direction = "RIGHT"
        #     else:
        #         p.press("RIGHT")
        #         direction = "RIGHT"

        #     CommandBook.FlashJump()

        #     # time.sleep(0.1)
        #     CommandBook.Attack()
        #     time.sleep(0.2)
        #     continue

        if x_player <= start1[0]:
            p.release_all()
            time.sleep(0.1)
            direction = 'RIGHT'

        if x_player >= start[0]:
            p.release_all()
            time.sleep(0.1)
            direction = 'LEFT'

        if isCasting == False:
            result = CommandBook.CastSkills()
            if result:
                continue

        if y_player == GROUND_Y or y_player == 38.5 or (x_player < 32.5):
            p.press(direction)
            CommandBook.FlashJump()

            # time.sleep(0.1)
            CommandBook.Attack()
            if x_player < 32.5:
                time.sleep(0.3)
                continue
            time.sleep(0.15)
