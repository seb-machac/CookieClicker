import tkinter as tk
from tkinter import IntVar, StringVar
import xml.etree.ElementTree as ET

class AppInstance:
    def __init__(self, root):
        self.root = root
        self.root.title("Cookie Clicker")
        self.root.geometry("800x800")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.protocol("WM_CREATE_WINDOW", self.on_create)

        # class Building:
        #     _instances = set()
        #     def __init__(self, name: str, image: str, cost: int, upgradeAmount: int):
        #         self.name = name
        #         self.image = tk.PhotoImage(file=image)
        #         self.cost = cost
        #         self.upgradeAmount = upgradeAmount
        #         self.purchased = 0

        #         Building._instances.add(self)

        #         self.costVar = StringVar(value=f"{self.name} Upgrade Cost: {self.cost}")
        #         self.purchasedVar = StringVar(value=f"{self.name}s purchased: {self.purchased}")

        #     @classmethod
        #     def getAllInstances(cls):
        #         return list(cls._instances)

        #     #create stat labels
        #     #buy button
        #     #increase per click
#=================================App Default Stats=================================
        #User Stats
        self.cookies = 0
        self.perclick = 1
        self.persecond = 0
        
        #Building Stats
        self.buildings = ["Pointer", "Grandma", "Farm", "Factory"]
        self.buildingsPurchased = {
            "Pointer": 0,
            "Grandma": 0,
            "Farm": 0,
            "Factory": 0
        }
        self.upgradeCosts = {
            "Pointer": 5,
            "Grandma": 25,
            "Farm": 100,
            "Factory": 1000
        }
        self.upgradeAmount = {
            "Pointer": 1,
            "Grandma": 5,
            "Farm": 25,
            "Factory": 50
        }
        # Grandma = Building("Grandma", "Grandma.png", 5, 5)

#        for i in Building._instances:
#iterate through instances of Building and create neccessary labels and buttons for it
#use two frames, one for main cookie and cookie stats, other for Building stats and buying
#in second frame could potentailly add extra frame per building instance for organisation
#https://www.pythontutorial.net/tkinter/tkinter-frame/
#currently moving buildings into single sub-class
#currently working as intended, no bugs known
#=================================TK Images=================================

        self.cookieImage = tk.PhotoImage(file="Cookie.png").subsample(2)
        self.pointerImage = tk.PhotoImage(file="Pointer.png")
        self.grandmaImage = tk.PhotoImage(file="Grandma.png")
        self.farmImage = tk.PhotoImage(file="Farm.png")
        self.factoryImage = tk.PhotoImage(file="Factory.png")


#=================================TK Vars=================================

        self.cookiesVar = StringVar(value=f"Cookies: {self.cookies}")
        self.perclickVar = StringVar(value=f"Per Click: {self.perclick}")
        
        self.pointerUpgradeCostVar = StringVar(value=f"Pointer Upgrade Cost: {self.upgradeCosts["Pointer"]}")
        self.pointersPurchasedVar = StringVar(value=f"Pointers Purchased: {self.buildingsPurchased["Pointer"]}")

        self.grandmaUpgradeCostVar = StringVar(value=f"Grandma Upgrade Cost: {self.upgradeCosts["Grandma"]}")
        self.grandmasPurchasedVar = StringVar(value=f"Grandmas Purchased: {self.buildingsPurchased["Grandma"]}")

        self.farmUpgradeCostVar = StringVar(value=f"Farm Upgrade Cost: {self.upgradeCosts["Farm"]}")
        self.farmsPurchasedVar = StringVar(value=f"Farms Purchased: {self.buildingsPurchased["Farm"]}")

        self.factoryUpgradeCostVar = StringVar(value=f"Factory Upgrade Cost: {self.upgradeCosts["Factory"]}")
        self.factoriesPurchasedVar = StringVar(value=f"Factories Purchased: {self.buildingsPurchased["Factory"]}")

#=================================TK UI=================================

        #Cookie Frame
        self.cookieFrame = tk.Frame(root)
        self.cookieFrame.grid(row=1)
        #Cookie Stat Label
        self.cookiesLabel = tk.Label(root, textvariable=self.cookiesVar, font=("Arial", 12), anchor="center")
        self.cookiesLabel.place(x=40, y=100, width=100, height=24)

        #Per Click Label
        self.perclickLabel = tk.Label(root, textvariable=self.perclickVar, font=("Arial", 12), anchor="center")
        self.perclickLabel.place(x=190, y=100, width=100, height=24)
        
        #Cookie Button
        self.clickButton = tk.Button(root, text="Click", image=self.cookieImage, command=self.click)
        self.clickButton.place(x=20, y=140, width=300, height=300)

        #-----------------Pointer-----------------
        #Pointer Upgrade Cost Label
        self.PointerUpgradeCostLabel = tk.Label(root, textvariable=self.pointerUpgradeCostVar, font=("Arial", 12), anchor="w")
        self.PointerUpgradeCostLabel.place(x=510, y=170, width=250, height=20)
        
        #Pointer Upgrade Button
        self.PointerUpgradeButton = tk.Button(root, text="Buy\nPointer", command=lambda: self.upgradeBuilding("Pointer"), font=("Arial", 12))
        self.PointerUpgradeButton.place(x=340, y=150, width=100, height=50)

        #Pointer Image
        self.PointerImageLabel = tk.Label(root, image=self.pointerImage)
        self.PointerImageLabel.place(x=450, y=150, width=50, height=50)

        #Pointers Purchased Label
        self.PointersPurchasedLabel = tk.Label(root, textvariable=self.pointersPurchasedVar, font=("Arial", 12), anchor="w")
        self.PointersPurchasedLabel.place(x=510, y=150, width=200, height=20)


        #-----------------Grandma-----------------
        #Grandma Upgrade Cost Label
        self.GrandmaUpgradeCostLabel = tk.Label(root, textvariable=self.grandmaUpgradeCostVar, font=("Arial", 12), anchor="w")
        self.GrandmaUpgradeCostLabel.place(x=510, y=250, width=250, height=20)

        #Grandma Upgrade Button
        self.GrandmaUpgradeButton = tk.Button(root, text="Buy\nGrandma", command=lambda: self.upgradeBuilding("Grandma"), font=("Arial", 12))
        self.GrandmaUpgradeButton.place(x=340, y=230, width=100, height=50)

        #Grandma Image
        self.GrandmaImageLabel = tk.Label(root, image=self.grandmaImage)
        self.GrandmaImageLabel.place(x=450, y=230, width=50, height=50)
        
        #Grandmas Purchased Label
        self.GrandmasPurchasedLabel = tk.Label(root, textvariable=self.grandmasPurchasedVar, font=("Arial", 12), anchor="w")
        self.GrandmasPurchasedLabel.place(x=510, y=230, width=200, height=20)


        #-----------------Farm-----------------
        #Farm Upgrade Cost Label
        self.FarmUpgradeCostLabel = tk.Label(root, textvariable=self.farmUpgradeCostVar, font=("Arial", 12), anchor="w")
        self.FarmUpgradeCostLabel.place(x=510, y=330, width=250, height=20)

        #Farm Upgrade Button
        self.FarmUpgradeButton = tk.Button(root, text="Buy\nFarm", command=lambda: self.upgradeBuilding("Farm"), font=("Arial", 12))
        self.FarmUpgradeButton.place(x=340, y=310, width=100, height=50)

        #Farm Image Label
        self.FarmImageLabel = tk.Label(root, image=self.farmImage)
        self.FarmImageLabel.place(x=450, y=310, width=50, height=50)

        #Farms Purchased Label
        self.FarmsPurchasedLabel = tk.Label(root, textvariable=self.farmsPurchasedVar, font=("Arial", 12), anchor="w")
        self.FarmsPurchasedLabel.place(x=510, y=310, width=200, height=20)


        #-----------------Factory-----------------
        #Factory Upgrade Cost Label
        self.FactoryUpgradeCostLabel = tk.Label(root, textvariable=self.factoryUpgradeCostVar, font=("Arial", 12), anchor="w")
        self.FactoryUpgradeCostLabel.place(x=510, y=410, width=250, height=20)

        #Factory Upgrade Button
        self.FactoryUpgradeButton = tk.Button(root, text="Buy\nFactory", command=lambda: self.upgradeBuilding("Factory"), font=("Arial", 12))
        self.FactoryUpgradeButton.place(x=340, y=390, width=100, height=50)

        #Factory Image Label
        self.FactoryImageLabel = tk.Label(root, image=self.factoryImage)
        self.FactoryImageLabel.place(x=450, y=390, width=50, height=50)

        #Factories Purchased Label
        self.FactoriesPurchasedLabel = tk.Label(root, textvariable=self.factoriesPurchasedVar, font=("Arial", 12), anchor="w")
        self.FactoriesPurchasedLabel.place(x=510, y=390, width=200, height=20)

#=================================Functions=================================

    def updateLabels(self):
        self.cookiesVar.set(f"Cookies: {self.cookies}")
        self.perclickVar.set(f"Per Click: {self.perclick}")
        self.pointerUpgradeCostVar.set(f"Pointer Upgrade Cost: {self.upgradeCosts["Pointer"]}")
        self.pointersPurchasedVar.set(f"Pointers Purchased: {self.buildingsPurchased["Pointer"]}")
        self.grandmaUpgradeCostVar.set(f"Grandma Upgrade Cost: {self.upgradeCosts["Grandma"]}")
        self.grandmasPurchasedVar.set(f"Grandmas Purchased: {self.buildingsPurchased["Grandma"]}")
        self.farmUpgradeCostVar.set(f"Farm Upgrade Cost: {self.upgradeCosts["Farm"]}")
        self.farmsPurchasedVar.set(f"Farms Purchased: {self.buildingsPurchased["Farm"]}")
        self.factoryUpgradeCostVar.set(f"Factory Upgrade Cost: {self.upgradeCosts["Factory"]}")
        self.factoriesPurchasedVar.set(f"Factories Purchased: {self.buildingsPurchased["Factory"]}")


    def click(self):
        self.cookies += self.perclick
        self.updateLabels()


    def upgradeBuilding(self, building):
        if self.cookies >= self.upgradeCosts[building]:
            self.perclick += self.upgradeAmount[building]
            self.buildingsPurchased[building] += 1
            self.cookies = self.cookies - self.upgradeCosts[building]
            self.upgradeCosts[building] *= 2
            self.updateLabels()

    def run(self):
        self.root.mainloop()

    def on_close(self):
        treeroot = ET.Element("root")
        UserData = ET.SubElement(treeroot, "UserData")
        cookie_data = ET.SubElement(UserData, "Cookies")
        cookie_data.text = str(self.cookies)
        perclick_data = ET.SubElement(UserData, "PerClick")
        perclick_data.text = str(self.perclick)
        persecond_data = ET.SubElement(UserData, "PerSecond")
        persecond_data.text = str(self.persecond)

        tree = ET.ElementTree(treeroot)
        tree.write("UserData.xml", encoding="utf-8", xml_declaration=True)
        root.destroy()
        
    def on_create(self):
        try:
            tree = ET.parse('UserData.xml')
            treeroot = tree.getroot()
            for data in treeroot.findall('UserData'):
                self.cookiesTemp = data.findtext("Cookies")
                self.cookies =  0 if self.cookiesTemp == None else int(self.cookiesTemp)
                print(self.cookies)
                self.perClickTemp = data.findtext("PerClick")
                self.perclick =  0 if self.perClickTemp == None else int(self.perClickTemp)
                self.perSecondTemp = data.findtext("PerSecond")
                self.persecond =  0 if self.perSecondTemp == None else int(self.perSecondTemp)
        except FileNotFoundError:
            self.cookies = 0
            self.perclick = 0
            self.persecond = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = AppInstance(root)
    app.run()