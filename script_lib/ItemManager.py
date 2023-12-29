import time
import pyautogui


class Item:
    ItemType: str


class Group:
    Items: dict[str, Item]
    LastCasted: float
    HasRanOut: bool


class Steps:
    OpenInventory: bool
    UseTab: bool
    DoubleClick: bool
    SetUp: bool


class ItemManager:
    def __init__(self, CDTracker, PXFinder, p):
        self.item_list: dict[str, Item] = {}
        self.CDTracker = CDTracker
        self.__p = p
        self.item_groups: dict[str, Group] = {}
        self.ActivateGroup: str = None
        self.PXFinder = PXFinder
        self.ActivateSteps: Steps = None

    def AddItem(self, Name: str, ItemType: str):
        if Name in self.item_list:
            return

        item = Item()
        item.ItemType = ItemType

        self.item_list[Name] = item

    def FinishSetUp(self):
        # Create a dictionary to store items grouped by ItemType
        grouped_items = {}

        # Iterate through the items and group them based on ItemType
        for item_name, item in self.item_list.items():
            item_type = item.ItemType  # Corrected attribute name
            if item_type not in grouped_items:
                grouped_items[item_type] = []
            grouped_items[item_type].append(item_name)

        # Create Group objects for each group and add them to the item_groups list
        for item_type, item_names in grouped_items.items():
            group = Group()
            group.Items = {
                item_name: self.item_list[item_name] for item_name in item_names}
            group.LastCasted = time.time() - 5  # Initialize the LastCasted attribute
            group.HasRanOut = False
            self.item_groups[item_type] = group

    def CheckIfGroupActive(self, group: Group):
        if time.time() - group.LastCasted <= 0:
            # print(time.time() - group.LastCasted)
            return True
        for itemName, item in group.Items.items():
            if self.CDTracker.IsActive(itemName):
                return True
        return False

    def FindPixel(self, imageName, click=False):
        loc = self.PXFinder.FindImage(imageName)
        if loc is not None:
            if click:
                self.__p.doubleclick((int(loc[0]), int(loc[1])))
            return (loc[0], loc[1])
        return None

    def ActivateGroupProcedure(self):
        if self.ActivateSteps.OpenInventory == False:
            if self.FindPixel("InventoryHelper/InventoryOpened") is None:
                print("opening inventory...")
                self.__p.press("I")
                time.sleep(0.5)
            else:
                self.ActivateSteps.OpenInventory = True
            return True
        elif self.ActivateSteps.UseTab == False:
            if self.FindPixel("InventoryHelper/UseIdentifier") is None:
                print("Didn't find identifier, clicking Tab.")
                self.__p.press("TAB")
            else:
                print("Use Tab Opened!")
                self.ActivateSteps.UseTab = True
                return True
            return True

        if self.ActivateSteps.DoubleClick == False:
            flag = False
            for itemName, item in self.item_groups[self.ActivateGroup].Items.items():
                loc = self.FindPixel(f"{itemName}/Use")
                if loc is not None:
                    pyautogui.doubleClick(loc[0], loc[1])
                    flag = True
                    time.sleep(0.5)
                    self.ActivateSteps.DoubleClick = True
                    break

            if flag == False:
                print(f"Ran out of group: {self.ActivateGroup}")
                self.ActivateSteps.DoubleClick = True
                self.item_groups[self.ActivateGroup].LastCasted = time.time(
                ) + 60*10
            else:
                print(f"Succesfully Activated {self.ActivateGroup}")
                self.item_groups[self.ActivateGroup].LastCasted = time.time(
                ) + 60*1

            return True

        if self.ActivateSteps.SetUp == False:
            if self.FindPixel("InventoryHelper/UseIdentifier") is None:
                self.ActivateSteps.SetUp = True
                self.ActivateSteps = None
            else:
                self.__p.press("ESCAPE")
                time.sleep(0.2)

    def CheckForRecast(self):
        if self.ActivateSteps is not None:
            self.ActivateGroupProcedure()
            return True

        for groupName, group in self.item_groups.items():
            if self.CheckIfGroupActive(group) == False:
                print(f"Activating {groupName}")
                self.ActivateGroup = groupName
                steps = Steps()
                steps.DoubleClick = False
                steps.OpenInventory = False
                steps.UseTab = False
                steps.SetUp = False
                self.ActivateSteps = steps
                return True

        self.ActivateGroup = None
        self.ActivateSteps = None
        return False
