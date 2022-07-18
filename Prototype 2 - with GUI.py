from guizero import *
import os
from turtle import *
from collections import defaultdict

cwd = os.getcwd() #Setting constants
accountsFile = "Accounts.txt"

class ADT(): #Superclass for the Abstract Data Types (ADT)
    def __init__(self,m):
        self.maxSize = m #Defines the maximium capacity of each ADT
        self.front = -1 #Sets the initialisation value of the pointer "front"
        self.items=[] #This attribute will hold each ADTs contents
        for i in range(0,m): #Creates the array with the set number of indexes
            self.items.append("")
    def numItems(self): #Method for returning the number of items within the ADT
        count = 0
        for i in self.items:
            if i != "":
                count += 1
        return count
    def isEmpty(self): #Method for returning whether the ADT is empty or not
        if self.numItems() == 0:
            return True
        else:
            return False
    def isFull(self): #Method for returning whether the ADT is full or not
        if self.numItems() == self.maxSize:
            return True
        else:
            return False
    def peek(self):
        if self.numItems() > 0:
            return self.items[self.front]
        else:
            print("Error - ADT is empty")
class Queue(ADT): #Subclass from the ADT Superclass
    def __init__(self,m):
        super().__init__(m) #Inherits the attributes of the Superclass
        self.rear = -1 #Sets the initialisation value of the pointer "rear"
        self.front = 0 #To save issue with "peeking" the queue front pointer is assigned to index 0 now
    def enqueue(self,item): #Adds an item to the Queue
        if super().numItems() < self.maxSize: #Inherits the lenList() class from the Superclass
            self.rear = (self.rear + 1) % self.maxSize
            self.items[self.rear]=item
        else:
            print("Error - Queue is full")
    def dequeue(self): #Removes an item from the front of the Queue, First In First Out (FIFO)
        if super().numItems() > 0:
            removed = self.items[self.front]
            self.items[self.front] = ""
            self.front = (self.front + 1) % self.maxSize
            return removed
        else:
            print("Error - Queue is empty")            
class Stack(ADT): #Subclass from the ADT Superclass
    def __init__(self,m):
        super().__init__(m)
    def push(self,item): #Adds an item to the Stack
        if super().numItems() < self.maxSize:
            self.front = (self.front + 1) % self.maxSize
            self.items[self.front]=item
        else:
            print("Error - Stack is full")
    def pop(self): #Removes an item from the rear of the Stack, Last In First Out (LIFO)
        if super().numItems() > 0:
            popped = self.items[self.front]
            self.items[self.front] = ""
            self.front = (self.front - 1) % self.maxSize
            return popped
        else:
            print("Error - Stack is empty")

class HashTable():
    def __init__(self,s): 
        self.size = s #Initialised with the size of the Hash Table
        self.__Hashing("None") #Private hashing function
        self.slots = []
        for i in range(0,s):
            self.slots.append("")
        self.inSlots("None")
    def __Hashing(self,key): #This private method contains the hashing algorithm used
        splitKey = list(key) 
        for i in range(0,len(splitKey)):
            item = ord(splitKey[i])
            splitKey[i] = item
        key = 0
        for i in splitKey:
            key += i
        key = key**4
        key = key % self.size
        return key
    def lenSlots(self): #Returns the number of slots filled
        count = 0
        for i in self.slots:
            if i != "" and i != "None":
                count += 1
        return count
    def inSlots(self,key): #Checks whether a specific slot is occupied
        key = self.__Hashing(key)
        if self.slots[key] != "" and self.slots[key] != "None":
            return True
        else:
            return False
    def put(self,key,value): #Puts an item into the Hash Table using the first value as the key
        keyValue = self.__Hashing(key)
        while self.slots[keyValue] != "":
            if self.slots[keyValue] == "None": #FIX LATER 'magic'
                break
            keyValue = (keyValue + 1) % self.size #Defines JUMP value if slot already occupied
        self.slots[keyValue]=value
    def get(self,key): #Returns the item in a specific slot
        key = self.__Hashing(key)
        return self.slots[key]
    def delete(self,key): #Deletes the item in the slot
        keyValue = self.__Hashing(key)
        while self.slots[keyValue] == "" or self.slots[keyValue] == "None":
            keyValue = (keyValue + 1) % self.size #Defines JUMP value if slot already occupied
        self.slots[keyValue] = "None"
        return True #Confirms deletion happened
    def save(self,filename): #Saves the Hash Table into a file
        file = open(filename,"w")
        file.write(str(self.size))
        file.write("\n")
        for i in self.slots:
            file.write(str(i))
            file.write("\n")
        file.close()
    def load(self,filename): #Loads the Hash Table from a file
        file = open(filename,"r")
        count = -1
        for line in file:
            if count == -1:
                self.size = int(line)
                self.slots = []
                for i in range(0,self.size):
                    self.slots.append("")
                count += 1
            else:
                splitLine = list(line)
                subcount = len(splitLine)
                joinLine = []
                for i in splitLine:
                    if subcount != 1 and subcount != 0:
                        joinLine.append(i)
                        subcount += -1
                    else:
                        subcount += -1
                joinLine = "".join(joinLine)
                self.slots[count] = joinLine
                count += 1
        file.close()
    def clear(filename): #Deletes the Hash Table in that file
        os.remove(filename)
    def check(self,key,value):
        keyValue = self.__Hashing(key)
        while self.slots[keyValue] == "" or self.slots[keyValue] == "None":
            keyValue = (keyValue + 1) % self.size #Defines JUMP value if slot already occupied
        if self.slots[keyValue] == value:
            return True
        else:
            return False
os.chdir(cwd+"/Accounts")
accounts = HashTable(1) #Creates blank Hash Table
accounts.load(accountsFile) #Loads HashTable for accounts from file 
os.chdir(cwd)

class Graph(): #This class will store the map of the school within it
    def __init__(self): #Defines that the class contains corridors and distances
        self.corridors = defaultdict(list)
        self.distances = {}
    def addCorridor(self, fromRoom, toRoom, distance): #Corridors can be added into the class
        self.corridors[fromRoom].append(toRoom)
        self.corridors[toRoom].append(fromRoom)
        self.distances[(fromRoom, toRoom)] = distance
        self.distances[(toRoom, fromRoom)] = distance
graph = Graph() #creates the 'graph' object

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
            for i in dist:#in case a distance of 27 is stored in dist as ['2','7'] 
                if i != ".":
                    i = int(i)
                    if dot == 1:
                        i = str(i)
                        count.append(i)
                    else:
                        total+=int(i)
                else:
                    dot+=1
            total = str(total)
            count = ''.join(count)
            num=total+"."+count
            num=float(num)
            route.append(start)
            route.append(end)
            route.append(num)
            route = tuple(route)
            corridors.append(route)
        blockPlan.close()
    for corridor in corridors:
        graph.addCorridor(*corridor)
    os.chdir(cwd)
    
def Dijsktra(graph,start,end):
    shortestRoutes = {start: (None,0)}
    currentPlace = start
    visited = set()
    while currentPlace != end:
        visited.add(currentPlace)
        destinations = graph.corridors[currentPlace]
        distToCurrentPlace = shortestRoutes[currentPlace][1]
        for nextPlace in destinations:
            distance = graph.distances[(currentPlace,nextPlace)] + distToCurrentPlace
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
    return route

def Application():
    def Quit():
        os.chdir(cwd+"/Accounts")
        accounts.save(accountsFile) #Saves HashTable to accounts file 
        os.chdir(cwd)
        menu.destroy()
    def LoginCheck():
        def Program(box1):
            def Logout():
                box3.hide()
                menu.title = "Login"
                box1.show()
            def FindRoute():
                start = locationEntry.get()
                end = destinationEntry.get()
                route = Dijsktra(graph,start,end)
                print(route)
                routeStack = Stack(len(route))
                for i in route:
                    routeStack.push(i)
                print(routeStack.items)
                print(routeStack.pop())
            menu.title = "WDF Routing Program"
            box3 = Box(menu,layout="grid")
            os.chdir(cwd+"/Textures")
            banner = Picture(box3,image="main_banner.gif",grid=[0,0,4,1])
            headerFinder = Text(box3,text="Route finder:",grid=[0,1,4,1],font="Arial",color="white",bg="black")
            locationText = Text(box3,text="Starting Location:",grid=[0,2],font="Arial")
            locationEntry = TextBox(box3,grid=[1,2],width="15")
            locationEntry.bg = "white"
            destinationText = Text(box3,text="Destination:",grid=[2,2],font="Arial")
            destinationEntry = TextBox(box3,grid=[3,2],width="15")
            destinationEntry.bg = "white"
            dividerOne = Picture(box3, image="divider_1.gif",grid=[0,4,4,1])
            findRoute = PushButton(box3,grid=[0,4,4,1],text="Find Route:",command=FindRoute)
            findRoute.bg = "white"
            headerQueue = Text(box3,text="Routes Queue:",grid=[0,5,4,1],font="Arial",color="white",bg="black")
            dividerTwo = Picture(box3, image="divider_2.gif",grid=[0,6,4,1])
            headerMap = Text(box3,text="The Map",grid=[0,7,4,1],font="Arial",color="white",bg="black")
            dividerThree = Picture(box3, image="divider_3.gif",grid=[0,8,4,1])
            logoutButton=PushButton(box3,grid=[0,9,4,1],text="Logout",command=Logout)
            os.chdir(cwd)
        username=usernameEntry.get()
        password=passwordEntry.get()
        passwordEntry.clear()
        test = accounts.check(username,password)
        if test == True:
            Confirmed = info(title = "Login successful",text="Login attempt was successful")
            usernameEntry.clear()
            box1.hide()
            Program(box1)
        else:
            Error = error(title = "Login unsuccessful",text = "Username or password incorrect, please try again")
    def CreateAccount():
        def Back():
            box2.hide()
            menu.title = "Login"
            box1.show()
        def Create():
            username=userEntry.get()
            password1=passEntry.get()
            password2=confirmEntry.get()
            if password1 != password2:
                errorMessage = error(title="Password error",text="Passwords do not match")
                passEntry.clear()
                confirmEntry.clear()
            else:
                confirmation = yesno(title="Add new account",text="Are you sure you want to add this account?")
                if confirmation == True:
                    accounts.put(username,password1)
                    os.chdir(cwd+"/Accounts")
                    accounts.save(accountsFile)
                    os.chdir(cwd)
                    message = info(title="Success",text="Account added!")
                    box2.hide()
                    box1.show()
                else:
                    message = info(title="Stopped",text="Account not added")
                    passEntry.clear()
                    confirmEntry.clear()
        box1.hide()
        menu.title = "Create Account"
        box2 = Box(menu,layout="grid")
        header2 = Text(box2,text="Please fill in the relevant fields to create a new account",grid=[0,0,2,1],font="Arial",color="blue")
        userText = Text(box2,text="Username:",grid=[0,1])
        passText = Text(box2,text="Password:",grid=[0,2])
        confirmText = Text(box2,text="Confirm Password:",grid=[0,3])
        userEntry=TextBox(box2,grid=[1,1],width="40")
        userEntry.bg = "white"
        passEntry=TextBox(box2,grid=[1,2],width="40")
        passEntry.bg = "white"
        confirmEntry=TextBox(box2,grid=[1,3],width="40")
        confirmEntry.bg = "white"
        createButton=PushButton(box2,grid=[1,4],text="Create",command=Create)
        backButton=PushButton(box2,grid=[0,5,2,1],text="Back to menu",command=Back)
    menu = App(title="Login",bg="#cae8dc")
    box1 = Box(menu,layout="grid")
    os.chdir(cwd+"/Textures")
    menu.tk.wm_iconbitmap("map_icon_transparent.ico")
    logo = Picture(box1,image="blue_map_logo.gif",grid=[1,0])
    os.chdir(cwd)
    header1 = Text(box1, text="Welcome to the WDF Routing Program",grid=[1,1],font="Arial",color="blue")
    quitButton = PushButton(box1,text="Quit",grid=[0,5],command=Quit)
    usernameText=Text(box1,text="Username:",grid=[0,2])
    usernameEntry=TextBox(box1,grid=[1,2],width="40")
    usernameEntry.bg = "white"
    passwordText=Text(box1,text="Password:",grid=[0,3])
    passwordEntry=TextBox(box1,grid=[1,3],width="40")
    passwordEntry.bg = "white"
    loginButton=PushButton(box1,text="Login",grid=[1,4],command=LoginCheck)
    createAccountButton = PushButton(box1,text="Create new\naccount",grid=[2,5],command=CreateAccount)
    menu.display()

BootLoader()
Application()

### BRAINSTORM IDEAS: ###
#Queue - Used for creating a plan for their routes that day etc.
#Stack - Reversing the queue
