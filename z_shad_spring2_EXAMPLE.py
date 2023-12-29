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


# SPOT SETTINGS #
start = (155.5, 54.5)
start1 = (25.5, 54.5)
GROUND_Y = 54.5
# SPOT SETTINGS #

minimap = (9, 61, 197, 133)
g = Game(minimap)
p = Player(g)


def multi_match_wrapper(img):
    return multi_match(img)


def capture_screen_wrapper():
    return capture_window()


# BOILERPLATE SET UP #
Utility = Util.Utility(g)
CDTracker = CoolDownTracker.CoolDownTracker(
    multi_match_f=multi_match_wrapper, capture_screen=capture_screen_wrapper, capture_cycle=1.1)
PXFinder = PixelFinder.PixelFinder(
    multi_match_f=multi_match_wrapper, capture_screen=capture_screen_wrapper)
# BOILERPLATE SET UP #


# SETTING UP SKILLS THAT ARE TRACKED IN THE HOTKEY #
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
# SETTING UP SKILLS THAT ARE TRACKED IN THE HOTKEY #


# SETTING UP SKILLS THAT ARE TRACKED IN THE BUFF BAR #
CDTracker.AddBuffbarSkill("Shadow_Walker", 2)
CDTracker.AddBuffbarSkill("Maple_Warrior", 1)
CDTracker.AddBuffbarSkill("2x", 3)
CDTracker.AddBuffbarSkill("Gold_Pot", 3)
CDTracker.AddBuffbarSkill("LEGION_2x", 3)
CDTracker.AddBuffbarSkill("LEGION_meso", 3)
CDTracker.AddBuffbarSkill("LEGION_drop", 3)
CDTracker.AddBuffbarSkill("WAP", 3)
CDTracker.AddBuffbarSkill("dojo_2x", 3) 
CDTracker.AddBuffbarSkill("mvp_15x", 3)
# SETTING UP SKILLS THAT ARE TRACKED IN THE BUFF BAR #


# SETTING UP ITEMS IN GROUPS (FOR EXAMPLE: 2x CAN BE SEVERAL DIFFERENT ITEMS, WE ONLY WANT TO USE ONE OF THEM) #
ItemManager = ItemsManager.ItemManager(
    CDTracker=CDTracker, PXFinder=PXFinder, p=p)
ItemManager.AddItem("mvp_15x", "1.5x")
ItemManager.AddItem("2x", "2x")
ItemManager.AddItem("dojo_2x", "2x")
ItemManager.AddItem("LEGION_2x", "2x")
ItemManager.AddItem("Gold_Pot", "Gold_Pot")
ItemManager.AddItem("LEGION_drop", "drop")
ItemManager.AddItem("WAP", "wap")
ItemManager.AddItem("LEGION_meso", "meso")
ItemManager.FinishSetUp()
# SETTING UP ITEMS IN GROUPS (FOR EXAMPLE: 2x CAN BE SEVERAL DIFFERENT ITEMS, WE ONLY WANT TO USE ONE OF THEM) #




# BOILERPLATE COMMANDBOOK, IF YOU ARE NOT A PROJECTILE CLASS(Shadower, Mecha, etc) REMOVE "MesoExplosion" ARGUMENT #
CommandBook = CommandBookGeneral.CommandBook(
    p=p, Utility=Utility, CDTracker=CDTracker, JUMP="SPACE", FLASH_JUMP="F", ROPE_LIFT="T", MesoExplosion="D")
CommandBook.SetMainAttackSkills(CRUEL_STAB)
# BOILERPLATE COMMANDBOOK, IF YOU ARE NOT A PROJECTILE CLASS(Shadower, Mecha, etc) REMOVE "MesoExplosion" ARGUMENT #



# SETTING UP SKILLS, SECOND AND THIRD ARGUMENT REFER TO AT WHAT X,Y RANGE SHOULD A CAST BE TRIGGERED (DOES NOT WALK TO THE POSITION TO CAST IT, BUT WILL ONLY CAST IT WHEN PLAYER IS THERE) #
CommandBook.AddSkill("Shadow_Veil", SHADOW_VEIL, [
                     0, 44.5], [41.5, 54.5], "HOTKEY", True)  # SHADOW VEIL


#SET UP SUMMONER#
SummonerHandler = Summoner.Summoner(
    p, g, Utility, CommandBook, CDTracker=CDTracker, AllTogether=True)



# OPTIONALLY: SET UP YOUR OWN SUMMONING FUNCTIONS FOR EACH SUMMON IF YOU WANT TRIGGER SUMMONING ONCE X SUMMONS ARE UP #
def SummonErda():
    location = g.get_player_location()
    if location is None:
        return False
    x_player, y_player = location
    if y_player == GROUND_Y:
        if 115.5 <= x_player <= 129.5:
            CommandBook.Assault("UP")
            time.sleep(0.5)
        else:
            p.go_to((125.5, GROUND_Y))
    elif 15.5 < y_player <= 28.5:  # right platform
        if 120.5 <= x_player <= 129.5:
            CommandBook.CastSkill(ERDA_SHOWERS)
            time.sleep(0.5)
            CommandBook.CastSkill(SUDDEN_RAID)
            time.sleep(0.1)
            return True
        else:
            p.go_to((125.5, y_player))
    else:
        p.go_to((125.5, 28.5))
    return False


def SummonDarkFlare():
    location = g.get_player_location()
    if location is None:
        return False
    x_player, y_player = location
    if 40.5 < y_player <= GROUND_Y:
        if 75.5 <= x_player <= 85.5:
            CommandBook.Assault("UP")
            time.sleep(0.5)
        else:
            p.go_to((77.5, GROUND_Y))
    elif 15.5 < y_player <= 28.5:  # right platform
        if 70.5 <= x_player <= 82.5:
            CommandBook.CastSkill(DARK_FLARE)
            time.sleep(0.5)
            return True
        else:
            p.go_to((77.5, y_player))
    else:
        p.go_to((77.5, 28.5))

    return False



# ALTERNATIVELY, WE COULD JUST REMOVE is_prio AND Func SO SCRIPT WILL SIMPLY SUMMON EACH SUMMON INDIVIDUALLY AT THEIR SPECIFIED [min_x, max_x] RANGE
SummonerHandler.AddSummon("Erda_Shower", ERDA_SHOWERS,
                          81.5, 28.5, [60.5, 100.5], [], is_prio=False, Func=SummonErda)
SummonerHandler.AddSummon("Dark_Flare", DARK_FLARE,
                          131.5, 28.5, [110.5, 141.5], [], Func=SummonDarkFlare, is_prio=True)



# SKILL ROTATOR IS USEFUL FOR ROTATING GUILD SKILLS, CLASS SKILLS (Epic Adventurer ETC), USEFUL FOR WHEN YOU LACK DAMAGE #
SkillsRotator = SkillRotator.SkillRotator(CDTracker=CDTracker, p=p)

SkillsRotator.CreateGroup("Guild_Skills")
SkillsRotator.AddSkillToGroup("Guild_Skills", "Guild_Crit", "Q")
SkillsRotator.AddSkillToGroup("Guild_Skills", "Guild_Damage", "U")

SkillsRotator.CreateGroup("Normal_Buffs")
SkillsRotator.AddSkillToGroup("Normal_Buffs", "Shadow_Walker", "5")
SkillsRotator.AddSkillToGroup("Normal_Buffs", "Last_Resort", "4")


rune = 0


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



# SETTING UP THE GENERAL FLOW OF THE SCRIPT AND SOME MORE BOILERPLATE CODE
def auto():
    CDThread = threading.Thread(target=CDTracker.CooldownUpdater, args=())
    CDThread.start()
    direction = 'RIGHT'
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
        rune_solver()

        # SkillsRotator.CastGroups()
        location = g.get_player_location()
        if location is None:
            continue
        x_player, y_player = location

        if SummonerHandler.PerformSummon():
            lastMoved = time.time()
            continue
        if 68.5 <= x_player <= 96.5:
            if SummonerHandler.ProcessSummons():
                lastMoved = time.time()
                continue

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

        # if y_player == 28.5:
        #     CommandBook.Jump()
        #     time.sleep(0.1)
        #     CommandBook.Assault("DOWN")
        #     time.sleep(0.1)
        #     lastMoved = time.time()
        #     continue
        # elif y_player <= 39.5:
        #     CommandBook.JumpDown()
        #     time.sleep(0.1)
        #     continue

        if x_player >= start[0] and 40.5 < y_player <= GROUND_Y:
            p.release_all()
            if y_player == GROUND_Y:
                CommandBook.JumpDown()
                time.sleep(0.5)
            direction = 'RIGHT'
            continue

        if isCasting == False:
            result = CommandBook.CastSkills()
            if result:
                continue

        if y_player <= 40.5 and x_player <= 60.5:
            CommandBook.JumpDown()
            CommandBook.Attack()
            time.sleep(0.2)
            lastMoved = time.time()
            continue

        if y_player <= GROUND_Y + 3:
            p.press(direction)
            CommandBook.FlashJump()

            # time.sleep(0.1)
            CommandBook.Attack()
            # if x_player < 32.5:
            #     time.sleep(0.3)
            #      continue
            time.sleep(0.15)
