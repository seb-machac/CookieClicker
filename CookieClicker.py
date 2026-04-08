import tkinter as tk
from tkinter import IntVar, StringVar
import xml.etree.ElementTree as ET
import math

class AppInstance:
    def __init__(self, root):
        self.root = root
        self.root.title("Cookie Clicker")
        self.root.geometry("800x800")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.protocol("WM_CREATE_WINDOW", self.on_create)

        class Building:
            _instances = set()
            def __init__(self, name: str, image: str, cost: int, upgradeAmount: int, buildingFrame, index: int, app):
                self.name = name
                self.image = tk.PhotoImage(file=image)
                self.baseCost = cost
                self.cost = cost
                self.upgradeAmount = upgradeAmount
                self.index = index
                self.purchased = 0
                self.buildingFrame = buildingFrame
                self.app = app

                Building._instances.add(self)

                self.costVar = StringVar(value=f"{self.name} Upgrade Cost: {self.cost}")
                self.purchasedVar = StringVar(value=f"{self.name}s purchased: {self.purchased}")

            def purchase(self):
                if self.app.cookies >= self.cost:
                    self.app.perclick += self.upgradeAmount
                    self.purchased += 1
                    self.app.cookies -= self.cost
                    self.cost = math.ceil(self.baseCost * (1.15**self.purchased))
                    self.updateVars()
                    self.app.updateLabels()

            def updateVars(self):
                self.costVar.set(f"{self.name} Upgrade Cost: {self.cost}")
                self.purchasedVar.set(f"{self.name}s purchased: {self.purchased}")

            def createFrame(self):
                frame = tk.Frame(self.buildingFrame, borderwidth=4, relief="sunken")
                frame.grid(row=self.index, column=1, sticky='W')

                buyButton = tk.Button(frame, text=f'Buy\n{self.name}', command=self.purchase, height=2)
                buyButton.grid(rowspan=2, row=1, column=1)

                imageLabel = tk.Label(frame, image=self.image)
                imageLabel.grid(rowspan=2, row=1, column=2)

                costLabel = tk.Label(frame, textvariable=self.costVar, font=("Arial", 12), anchor="w")
                costLabel.grid(row=1, column=3)

                purchasedLabel = tk.Label(frame, textvariable=self.purchasedVar, font=("Arial", 12), anchor="w")
                purchasedLabel.grid(row=2, column=3)

            @classmethod
            def getAllInstances(cls):
                return list(cls._instances)
            
#=================================User Default Stats=================================

        self.cookies = 0
        self.perclick = 1
        self.persecond = 0
        
#=================================TK Images=================================

        self.cookieImage = tk.PhotoImage(file="Cookie.png").subsample(2)

#=================================TK Vars=================================

        self.cookiesVar = StringVar(value=f"Cookies: {self.cookies}")
        self.perclickVar = StringVar(value=f"Per Click: {self.perclick}")

#=================================TK UI=================================
        self.cookieFrame = tk.Frame(root)
        self.cookieFrame.grid(row=0, column=1)

#--------------------------------Stat Frame-----------------------------
        self.cookieStatFrame = tk.Frame(self.cookieFrame)
        self.cookieStatFrame.grid(row=1)

        #Cookie Stat Label
        self.cookiesLabel = tk.Label(self.cookieStatFrame, textvariable=self.cookiesVar, font=("Arial", 12), anchor="center")
        self.cookiesLabel.grid(row=1, column=1)

        #Per Click Label
        self.perclickLabel = tk.Label(self.cookieStatFrame, textvariable=self.perclickVar, font=("Arial", 12), anchor="center")
        self.perclickLabel.grid(row=1, column=2, padx=5)
        
#------------------------------Cookie Button Frame----------------------
        self.cookieButtonFrame = tk.Frame(self.cookieFrame)
        self.cookieButtonFrame.grid(row=2)

        #Cookie Button
        self.clickButton = tk.Button(self.cookieButtonFrame, text="Click", image=self.cookieImage, command=self.click)
        self.clickButton.pack()
        
#---------------------------------Building Frame------------------------
        self.buildingFrame = tk.Frame(root, bg="lightblue")
        self.buildingFrame.grid(row=0, column=2, sticky="NS")

        #Buildings Inits
        Pointer = Building("Pointer", "Pointer.png", 15, 1, self.buildingFrame,0, self)
        Grandma = Building("Grandma", "Grandma.png", 100, 5, self.buildingFrame, 1, self)
        Grandma = Building("Farm", "Farm.png", 1100, 25, self.buildingFrame, 2, self)
        Grandma = Building("Factory", "Factory.png", 130000, 50, self.buildingFrame, 3, self)

        #Building Frame Gen
        for i, BuildingIter in enumerate(Building.getAllInstances()):
            BuildingIter.createFrame()

#============Functions=================================

    def updateLabels(self):
        self.cookiesVar.set(f"Cookies: {self.cookies}")
        self.perclickVar.set(f"Per Click: {self.perclick}")

    def click(self):
        self.cookies += self.perclick
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