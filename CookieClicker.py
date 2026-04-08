import tkinter as tk
from tkinter import IntVar, StringVar
import xml.etree.ElementTree as ET
import math
import time

class AppInstance:
    def __init__(self, root):
        self.root = root
        self.root.title("Cookie Clicker")
        self.root.geometry("800x800")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        class Building:
            _instances = set()
            def __init__(self, name: str, image: str, cost: int, perSecond, perClick: int, buildingFrame, index: int, app):
                self.name = name
                self.image = tk.PhotoImage(file=image)
                self.imageStr = image
                self.baseCost = cost
                self.cost = cost
                self.perSecond = perSecond
                self.perClick = perClick
                self.index = index
                self.purchased = 0
                self.buildingFrame = buildingFrame
                self.app = app

                Building._instances.add(self)

                self.costVar = StringVar(value=f"{self.name} Upgrade Cost: {self.cost}")
                self.purchasedVar = StringVar(value=f"{self.name}s purchased: {self.purchased}")

            def purchase(self):
                if self.app.cookies >= self.cost:
                    self.app.perClick += self.perClick
                    self.app.perSecond += self.perSecond
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

        self.Building = Building
            
#=================================User Default Stats=================================

        self.cookies = 0
        self.perClick = 1
        self.perSecond = 0
        self.running = False
        self.timerJob = None
        
#=================================TK Images=================================

        self.cookieImage = tk.PhotoImage(file="Cookie.png").subsample(2)

#=================================TK Vars=================================

        self.cookiesVar = StringVar(value=f"Cookies: {self.cookies}")
        self.perclickVar = StringVar(value=f"Per Click: {self.perClick}")
        self.perSecondVar = StringVar(value=f"Per Second: {self.perSecond}")

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
        
        #Per Second Label
        self.perSecondLabel = tk.Label(self.cookieStatFrame, textvariable=self.perSecondVar, font=("Arial", 12), anchor="center")
        self.perSecondLabel.grid(row=1, column=3, padx=5)
        
#------------------------------Cookie Button Frame----------------------
        self.cookieButtonFrame = tk.Frame(self.cookieFrame)
        self.cookieButtonFrame.grid(row=2)

        #Cookie Button
        self.clickButton = tk.Button(self.cookieButtonFrame, text="Click", image=self.cookieImage, command=self.click)
        self.clickButton.grid(row=1, column=1)

        self.stopTimeButton = tk.Button(self.cookieButtonFrame, text="Toggle Timer", command=self.toggleTime)
        self.stopTimeButton.grid(row=2, column=1)
        
#---------------------------------Building Frame------------------------
        self.buildingFrame = tk.Frame(root, bg="lightblue")
        self.buildingFrame.grid(row=0, column=2, sticky="NS")

        #Buildings Inits
        Pointer = Building("Pointer", "Pointer.png", 15, 0.1, 1, self.buildingFrame,0, self)
        Grandma = Building("Grandma", "Grandma.png", 100, 1, 5, self.buildingFrame, 1, self)
        Grandma = Building("Farm", "Farm.png", 1100, 8, 25, self.buildingFrame, 2, self)
        Grandma = Building("Factory", "Factory.png", 130000, 260, 50, self.buildingFrame, 3, self)

        #Building Frame Gen
        for i, BuildingIter in enumerate(Building.getAllInstances()):
            BuildingIter.createFrame()

#============Functions=================================

    def updateLabels(self):
        self.cookiesVar.set(f"Cookies: {round(self.cookies, 3)}")
        self.perclickVar.set(f"Per Click: {self.perClick}")
        self.perSecondVar.set(f"Per Second: {round(self.perSecond, 3)}")

    def click(self):
        self.cookies += self.perClick
        self.updateLabels()

    def run(self):
        self.root.mainloop()

    def tick(self):
        if not self.running:
            return
        self.cookies += self.perSecond
        self.cookies = round(self.cookies, 3)
        self.updateLabels()
        self.timerJob = self.root.after(1000, self.tick)

    def toggleTime(self):
        if self.running:
            self.running = False
            if self.timerJob is not None:
                self.root.after_cancel(self.timerJob)
                self.timerJob = None
        elif not self.running:
            self.running = True
            self.tick()
        else:
            print("unknown running value")
            self.running = False
        print(self.running)

    def on_close(self):
        self.running = False
        if self.timerJob is not None:
            self.root.after_cancel(self.timerJob)
            self.timerJob = None
        treeroot = ET.Element("root")
        userData = ET.SubElement(treeroot, "userData")
        cookieData = ET.SubElement(userData, "cookies")
        cookieData.text = str(round(self.cookies, 3))

        perClickData = ET.SubElement(userData, "perClick")
        perClickData.text = str(self.perClick)

        perSecondData = ET.SubElement(userData, "perSecond")
        perSecondData.text = str(round(self.perSecond, 3))

        buildingData = ET.SubElement(userData, "buildingData")

        for i, buildingIter in enumerate(self.Building.getAllInstances()):
            buildingIterData = ET.SubElement(buildingData, buildingIter.name)
            buildingIterName = ET.SubElement(buildingIterData, "name")
            buildingIterName.text = str(buildingIter.name)

            buildingIterImage = ET.SubElement(buildingIterData, "image")
            buildingIterImage.text = str(buildingIter.imageStr)

            buildingIterPerClick = ET.SubElement(buildingIterData, "perClick")
            buildingIterPerClick.text = str(buildingIter.perClick)

            buildingIterPerSecond = ET.SubElement(buildingIterData, "perSecond")
            buildingIterPerSecond.text = str(buildingIter.perSecond)

            buildingIterIndex = ET.SubElement(buildingIterData, "index")
            buildingIterIndex.text = str(buildingIter.index)

            buildingIterPurchased = ET.SubElement(buildingIterData, "purchased")
            buildingIterPurchased.text = str(buildingIter.purchased)

            buildingIterCost = ET.SubElement(buildingIterData, "cost")
            buildingIterCost.text = str(buildingIter.cost)

        tree = ET.ElementTree(treeroot)
        tree.write("UserData.xml", encoding="utf-8", xml_declaration=True)
        self.root.destroy()
        
    def on_create(self):
        try:
            tree = ET.parse('UserData.xml')
            treeroot = tree.getroot()
            for data in treeroot.findall('userData'):
                self.cookiesTemp = data.findtext("cookies")
                self.cookies = 0 if self.cookiesTemp == None else float(self.cookiesTemp)
                self.perClickTemp = data.findtext("perClick")
                self.perClick = 0 if self.perClickTemp == None else float(self.perClickTemp)
                self.perSecondTemp = data.findtext("perSecond")
                self.perSecond = 0 if self.perSecondTemp == None else float(self.perSecondTemp)
                print("m")
                for buildingData in data.findall('buildingData'):
                    for building in buildingData:
                        self.Building(str(building.findtext('name')), str(building.findtext("image")), int(building.findtext('cost')), float(building.findtext('perSecond')), int(building.findtext('perClick')), self.buildingFrame, int(building.findtext('index')), self)
                    print(self.Building.getAllInstances())
                        

                # for i, buildingIter in enumerate(self.Building.getAllInstances()):
                #     buildingIterData = ET.SubElement(buildingData, f"{buildingIter.name}Data")
                #     buildingIterPurchased = ET.SubElement(buildingIterData, f"{buildingIter.name}Purchased")
                #     buildingIterPurchased.text = str(buildingIter.purchased)
                #     buildingIterCost = ET.SubElement(buildingIterData, f"{buildingIter.name}Cost")
                #     buildingIterCost.text = str(buildingIter.cost)

                self.updateLabels()
        except Exception as e:
            print(e)
            self.cookies = 0
            self.perClick = 0
            self.perSecond = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = AppInstance(root)
    app.on_create()
    time.sleep(1)
    app.run()