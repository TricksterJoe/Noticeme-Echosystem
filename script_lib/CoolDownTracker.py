import time
import cv2
import numpy as np
import win32gui
import pyautogui


class Verify:
    RoundNumber: int
    ValueToVerify: bool
    VerificationCount: int


class Skill:
    ImageTop: cv2.Mat
    ImageBot: cv2.Mat
    Type: str
    Ready: bool
    Active: bool
    VerifyCount: int
    PendingVerification: Verify


class CoolDownTracker:
    def __init__(self, multi_match_f, capture_screen, capture_cycle=1.0, imageFolder="script_lib/images/"):
        self.SkillListHotKey: dict[str, Skill] = {}
        self.SkillListBuffBar: dict[str, Skill] = {}
        self.imageFolder = imageFolder
        self.multi_match = multi_match_f
        self.capture_screen = capture_screen
        self.game_image = None
        self.last_captured = time.time() - 10
        self.new_image = False
        self.capture_cycle = capture_cycle

    def GetPosition(self, x, y):
        # hwnd of the specific window, it could be whatever you what
        the_window_hwnd = win32gui.GetForegroundWindow()
        # get the position of window you gave.
        left_top_x, left_top_y, * \
            useless_position = win32gui.GetWindowRect(the_window_hwnd)

        print(left_top_x, left_top_y)
        pos_in_window_x, pos_in_window_y = (x + left_top_x), (y + left_top_y)

        return (pos_in_window_x, pos_in_window_y)

    def AddHotkeySkill(self, SkillName: str, VerifyCount=0):
        if SkillName in self.SkillListHotKey:
            return

        skill = Skill()
        skill.Type = "HOTKEY"
        imgTop = cv2.imread(f'{self.imageFolder}HOTKEYS/{SkillName}.png')
        if imgTop is None:
            print(f'Image of {SkillName} not found!')
            return
        skill.ImageTop = imgTop
        skill.PendingVerification = None
        skill.Ready = False
        skill.VerifyCount = VerifyCount
        self.SkillListHotKey[SkillName] = skill
        print(f"Succesfully loaded {SkillName} as HOTKEY")

    def AddBuffbarSkill(self, SkillName: str, VerifyCount=0):
        if SkillName in self.SkillListBuffBar:
            return

        skill = Skill()
        skill.Type = "BUFFBAR"
        imgTop = cv2.imread(f'{self.imageFolder}{SkillName}/Top.png')
        if imgTop is None:
            print(f'Image of {SkillName} not found!')
            return
        skill.ImageTop = imgTop
        imgBot = cv2.imread(f'{self.imageFolder}{SkillName}/Bottom.png')
        if imgBot is None:
            print(f'Image of {SkillName}_Bottom not found!')
            return
        skill.ImageBot = imgBot
        skill.Active = True
        skill.PendingVerification = None
        skill.VerifyCount = VerifyCount
        self.SkillListBuffBar[SkillName] = skill
        print(f"Succesfully loaded {SkillName} as BUFFBAR")

    def GetMatch(self, findIm, type="ALL"):
        # Read Main and Needle Image
        img_rgb = self.game_image
        template = findIm
        h_img, w_img = img_rgb.shape[:-1]
        # CV_TM_SQDIFF
        if type == "HOTKEY":
            img_rgb = img_rgb[int(h_img/2):int(h_img), 0:int(w_img)]
        if type == "BUFFBAR":
            img_rgb = img_rgb[0:int(h_img/3), 0:int(w_img)]

        # HOTKEY = img_rgb[int(h_img/2):int(h_img), 0:int(w_img)]
        # BUFFBAR = img_rgb[0:int(h_img/3), int(w_img/3):int(w_img)]

        # cv2.imwrite("HOTKEY.png", HOTKEY)
        # cv2.imwrite("BUFFBAR.png", BUFFBAR)

        w, h = template.shape[:-1]
        # cv2.TM_SQDIFF
        res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.95
        loc = np.where(res >= threshold)

        # for pt in zip(*loc[::-1]):  # Switch columns and rows
        #    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255),2)
        # return loc[0] if len(loc[0]) == 1 else None

        if len(loc[0]) <= 0:
            return None

        return [list(zip(*loc[::-1]))[0][0], list(zip(*loc[::-1]))[0][1] + h/2]

    def IsReady(self, SkillName: str):
        if SkillName not in self.SkillListHotKey:
            print(
                f'Please add {SkillName} as Hotkey to CoolDownTracker class.')
            return False

        skill = self.SkillListHotKey[SkillName]

        return skill.Ready

    def IsActive(self, SkillName: str):
        if SkillName not in self.SkillListBuffBar:
            print(
                f'Please add {SkillName} as BuffBar to CoolDownTracker class.')
            return True

        skill = self.SkillListBuffBar[SkillName]

        return skill.Active

    def CaptureScreen(self):
        if time.time() - self.last_captured >= self.capture_cycle:
            self.game_image = self.capture_screen()
            self.last_captured = time.time()

    # Add an option to add 3 seconds delay to a skill to turn from false to true
    def CooldownUpdater(self):
        self.CaptureScreen()
        if self.game_image is None:
            return
        for skillName, skillInfo in self.SkillListBuffBar.items():

            state = None
            locateBot = self.GetMatch(skillInfo.ImageBot, "BUFFBAR")
            if locateBot is not None:
                state = True
            else:
                locateTop = self.GetMatch(skillInfo.ImageTop, "BUFFBAR")
                if locateTop is not None:
                    state = True
            if state is None:
                state = False

            verify = skillInfo.PendingVerification
            if verify is not None:
                if verify.ValueToVerify == state:
                    if verify.VerificationCount >= skillInfo.VerifyCount:
                        skillInfo.Active = state
                        skillInfo.PendingVerification = None
                        continue
                    else:
                        verify.VerificationCount = verify.VerificationCount + 1
                    continue
                skillInfo.Active = True
                skillInfo.PendingVerification = None
                continue
            if skillInfo.Active != state:
                if state == True:
                    skillInfo.Active = True
                verification = Verify()
                verification.ValueToVerify = state
                verification.VerificationCount = 0
                skillInfo.PendingVerification = verification
                continue
            skillInfo.Active = state

        for skillName, skillInfo in self.SkillListHotKey.items():
            state = None
            locate = self.GetMatch(skillInfo.ImageTop, "HOTKEY")
            if locate is not None:
                state = True

            if state is None:
                state = False

            verify = skillInfo.PendingVerification
            if verify is not None:
                if verify.ValueToVerify == state:
                    if verify.VerificationCount >= skillInfo.VerifyCount:
                        skillInfo.Ready = state
                        skillInfo.PendingVerification = None
                        continue
                    else:
                        verify.VerificationCount = verify.VerificationCount + 1
                    continue
                skillInfo.Ready = False
                skillInfo.PendingVerification = None
                continue
            if skillInfo.Ready != state:
                if state == False:
                    skillInfo.Ready = False

                verification = Verify()
                verification.ValueToVerify = state
                verification.VerificationCount = 0
                skillInfo.PendingVerification = verification
                continue
            skillInfo.Ready = state

        self.game_image = None
        return
