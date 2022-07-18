import os
from turtle import *
from collections import defaultdict
main = os.getcwd()
class Plan(): #This class will store the map of the school within it
    def __init__(self): #Defines that the class contains corridors and distances
        self.corridors = defaultdict(list)
        self.distances = {}
    def addCorridor(self, fromRoom, toRoom, distance): #Corridors can be added into the class
        self.corridors[fromRoom].append(toRoom)
        self.corridors[toRoom].append(fromRoom)
        self.distances[(fromRoom, toRoom)] = distance
        self.distances[(toRoom, fromRoom)] = distance
plan = Plan() #Sets the class as being linked to a variable

def BootLoader(): #This function will load the points into the map class from the files where the points are stored
    corridors = []
    os.chdir(os.getcwd()+"/Blocks") #Sets the destination for the program to search for the files in
    blocks = [
"A Block First.txt",
"A Block Ground.txt",
"B Block First.txt",
"B Block Ground.txt",
"C Block First.txt",
"C Block Ground.txt",
"E Block First.txt",
"E Block Ground.txt",
"G Block First.txt",
"G Block Ground.txt",
"Connectors.txt"
] #List that holds the names of the files that need to be loaded into the map class
    for block in blocks: #Works through each file individually
        blockPlan = open(block,"r")
        for line in blockPlan: #A,B,1 #This is how each file's line is formatted: start, end, distance between
            route = []
            data = list(line) #['A',',','B',',','1','\n']
            count = 0
            start = []
            end = []
            dist = []
            for item in data:
                if item == "," or item == "\n": #Checks for "," since files stored as A.B.1 currently
                    count += 1
                elif count == 0:
                    start.append(item)
                elif count == 1:
                    end.append(item)
                elif count == 2:
                    dist.append(item)
                else:
                    None
            start = "".join(start)
            end = "".join(end)
            total = 0
            dot = 0
            count = []
            print(dist)
            for i in dist:#in case a distance of 27 is stored in dist as ['2','7'] #THERE IS AN ERROR HERE!
                if i != ".":
                    i = int(i)
                    if dot == 1:
                        i = str(i)
                        count.append(i)
                    else:
                        total+=1
                else:
                    dot+=1
            total = str(total)
            count = ''.join(count)
            num=total+"."+count
            num=float(num)
            print(num)
            route.append(start)
            route.append(end)
            route.append(num)
            route = tuple(route)
            corridors.append(route)
        blockPlan.close()
    for corridor in corridors:
        plan.addCorridor(*corridor)
    os.chdir(main)
BootLoader()

def Dijsktra(plan,initial,end):
    shortestRoutes = {initial: (None,0)}
    currentPlace = initial
    visited = set()
    while currentPlace != end:
        visited.add(currentPlace)
        destinations = plan.corridors[currentPlace]
        distToCurrentPlace = shortestRoutes[currentPlace][1]
        for nextPlace in destinations:
            distance = plan.distances[(currentPlace,nextPlace)] + distToCurrentPlace
            if nextPlace not in shortestRoutes:
                shortestRoutes[nextPlace] = (currentPlace, distance)
            else:
                currentShortestDist = shortestRoutes[nextPlace][1]
                if currentShortestDist > distance:
                    shortestRoutes[nextPlace] = (currentPlace, distance)
        nextDestinations = {place: shortestRoutes[place] for place in shortestRoutes if place not in visited}
        if not nextDestinations:
            route = "Route not possible"
            return route
        currentPlace = min(nextDestinations, key=lambda k: nextDestinations[k][1])
    route = []
    while currentPlace is not None:
        route.append(currentPlace)
        nextPlace = shortestRoutes[currentPlace][0]
        currentPlace = nextPlace
    route = route[::-1]
    return route

def GraphicDisplay(route,planFile):
    def close():
        bgpic("nopic")
        clearscreen()
        update()
        bye()
    bgpic(planFile)
    screensize(750,1250)
    shape("circle")
    title("Your route")
    shapesize(0.5,0.5,0.5)
    circle(100)
    listen()
    onkeypress(close,"Return")
    mainloop()

while True:
    x=input("Start:")
    y=input("End:")
    route = Dijsktra(plan,x,y)
    if route != "Route not possible":
        planFile = "Plan.png"
        print(route)
        os.chdir(os.getcwd()+"/Textures")
        GraphicDisplay(route,planFile)
        os.chdir(main)
    else:
        print(route)
