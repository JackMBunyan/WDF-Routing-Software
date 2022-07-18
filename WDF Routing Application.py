from guizero import * #imports all libraries necessary for the program
import os
import sys
from collections import defaultdict

cwd = os.getcwd() #Setting global constants
accountsFile = "Accounts.txt"

class ADT(): #Superclass for the Abstract Data Types (ADT)
    def __init__(self,m):
        self.maxSize = m #Defines the maximium capacity of **each ADT
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
    def peek(self): #Method for peeking at the front item in the ADT
        if self.numItems() > 0:
            return self.items[self.front]
        else:
            print("Error - ADT is empty")
            
class Stack(ADT): #Subclass from the ADT Superclass
    def __init__(self,m):
        super().__init__(m)
    def push(self,item): #Adds an item to the Stack
        if super().numItems() < self.maxSize:
            self.front = (self.front + 1) % self.maxSize
            self.items[self.front]=item
        else:
            print("Error - Stack is full")
    def pop(self): #Removes an item from the front of the Stack, Last In First Out (LIFO)
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
        splitKey = list(key) #Key is split into a list with each character of the string
                             #becoming an element
        for i in range(0,len(splitKey)): #Each item in the list is turned into its unicode
                                         #value
            item = ord(splitKey[i])
            splitKey[i] = item
        key = 0
        for i in splitKey: #Key is generated from the sum of all the unicode value
            key += i
        key = key**4 #The sum is then put to the power of four
        key = key % self.size #Then a modulus operation is used to make sure its value is
        #one within the range of the table
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
            if self.slots[keyValue] == "None":
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
        for line in file: #Each line in the file is reassembled individually
            if count == -1:
                self.size = int(line) #First value in the line is the size of the table
                self.slots = []
                for i in range(0,self.size): #This value is used to create an empty table with
                                             #that many slots
                    self.slots.append("")
                count += 1
            else: #After the first line is used to set the size of the table, the other lines
                #have the contents of the saved table
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
        if value != "":
            keyValue = self.__Hashing(key)
            initial = keyValue
            flag = False
            while (self.slots[keyValue] == "" or self.slots[keyValue] == "None") and flag == True:
                keyValue = (keyValue + 1) % self.size #Defines JUMP value if slot already occupied
                if keyValue == initial:
                    flag = True
            if self.slots[keyValue] == value:
                return True
            else:
                return False
        else:
            return False
os.chdir(cwd+"/Accounts")
accounts = HashTable(1) #Creates blank Hash Table, size arbitrarily set to 1 as it is changed in the
                        #next line based on the size of the saved HashTable
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

def BootLoader(): #This function will load the points into the map class from the files where the
                  #points are stored
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
        for line in blockPlan: #A,B,1 #This is how each file's line is formatted: start, end, distance
                               #between
            route = []
            data = list(line) #['A',',','B',',','1','\n']
            count = 0
            start = []
            end = []
            dist = []
            for item in data:
                if item == "," or item == "\n": #Checks for "," since files stored as A,B,1 currently
                    count += 1
                elif count == 0:
                    start.append(item) #adds the item into the sub list start point
                elif count == 1:
                    end.append(item) #adds the item into the sub list end point
                elif count == 2:
                    dist.append(item) #stores the distance of the connection
                else:
                    None
            start = "".join(start) #joins the lists into single strings
            end = "".join(end)
            total = 0
            dot = 0
            count = []
            for i in dist:#in case a distance of 27 is stored in dist as ['2','7'] 
                if i != ".": #subroutine to store the distance correctly as a float
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
            num=float(num) #the number is now formatted correctly
            route.append(start) 
            route.append(end)
            route.append(num)
            route = tuple(route) #each section of corridor as saved as a tuple route - start, end,
                                 #distance
            corridors.append(route) #each section added to a list of corridors
        blockPlan.close()
    for corridor in corridors: #this loop adds all the corridors loaded from the file into the
                               #object graph which holds the school's map
        graph.addCorridor(*corridor) 
    os.chdir(cwd)
    
def Dijkstra(graph,start,end): #this subroutine is a variation of Dijsktra's shortest path algorithm
                               #using a stack
    shortestRoutes = {start: (None,0)} #creates a dictionary to begin storing the shortest route,
                                       #current route length is 0
    currentPlace = start #sets the starting location by the parameter start
    visited = set() #this set tracks the nodes already visited on the graph
    while currentPlace != end: #loops until the destination node is located
        visited.add(currentPlace) #adds the current location the visited set
        destinations = graph.corridors[currentPlace] #this is a list of the nodes connected to the
                                                     #start node
        distToCurrentPlace = shortestRoutes[currentPlace][1] #this records the distances between
                                                             #current node and destination node
        for nextPlace in destinations: #iterates through each destination node
            distance = graph.distances[(currentPlace,nextPlace)] + distToCurrentPlace
            #gets the distance to the next node, and totals it with the distance of the whole route
            if nextPlace not in shortestRoutes: #if the node is not already in the list of shortest routes
                shortestRoutes[nextPlace] = (currentPlace, distance) #it is added to that list
            else:
                currentShortestDist = shortestRoutes[nextPlace][1]
                #else this route then becomes the current shortest route
                if currentShortestDist > distance: #if this route is greater then than the current distance
                    shortestRoutes[nextPlace] = (currentPlace, distance) #it is added to the shortest route list
        nextDestinations = {place: shortestRoutes[place] for place in shortestRoutes if place not in visited}
        #from the shortest routes list, the next destinations are calculated
        if not nextDestinations: #if none are available the route is not possible
            route = "Route not possible"
            return route
        currentPlace = min(nextDestinations, key=lambda k: nextDestinations[k][1])
        #the next current node is decided by the next destination with the minimum distance
    routeStack = Stack(100) #using the stack class, a stack of arbitrary size 100 is created
    while currentPlace is not None: #loops through the shorterst route set
        routeStack.push(currentPlace) #each node is pushed onto the stack in order
        nextPlace = shortestRoutes[currentPlace][0] #set is incremented
        currentPlace = nextPlace #loops
    return routeStack #the stack containing the route is returned as the output

def Application(): #this procedure contains all the program's graphical user interface
                   #and functions
    def Quit(): #this function closes the application
        os.chdir(cwd+"/Accounts") #the directory is changed to the accounts file
        accounts.save(accountsFile) #Saves HashTable to accounts file 
        os.chdir(cwd) #returns the directory to its initial place
        menu.destroy() #closes the GUI window
        sys.exit() #prevents additional commands to be input, closes the program
    def LoginCheck(): #this function checks the login credentials input
        def Program(loginBox): #this function contains the main menu and links to the
                               #various functions of my application
            def Logout(): #this function logs out the user and returns them to the login screen
                menuBox.hide()
                menu.title = "Login"
                loginBox.show()
            def FindRoute(): #this function runs the Dijsktra Algorithm for the user
                def Print(): #this function allows the user to save the route into a text
                             #file to be printed later
                    def Continue(): #a validation check function
                        def Done(): #reuturns the user to the main menu
                            finalBox.hide()
                            menu.title = "WDF Routing Program"
                            menuBox.show()
                        filename = printEntry.get() #the user decides the filename
                                                             #for the route to be saved under
                                                             #but the .txt has to be added
                        printEntry.clear()
                        fileline = list(filename)
                        flag = True
                        if fileline == []:
                            flag = False
                        for f in fileline:
                            if f in ["/",",",".","?"]:
                                flag = False
                        if flag == False:
                            failed = info(title = "Invalid Input",text="Please enter a valid filename")
                        else:
                            confirmation = yesno(title="Save To File",text="Are you sure you want to save this into a file?")
                            if confirmation == False:
                                None
                            else:
                                filename = filename + ".txt"
                                printBox.hide()
                                finalBox = Box(menu,layout="grid")
                                os.chdir(cwd+"/Routes")
                                file = open(filename,"w")
                                file.write("Here's your route:\n\n")
                                file.write(theRoute) #the route that the user asked to be calculated
                                                     #is written into the file
                                file.write("\n\n")
                                file.write(routeAdvice) #along with advice for how to follow the route
                                file.close()
                                os.chdir(cwd)
                                message = Text(finalBox,text="""Your route has been saved to the file
        inside of\nthe folder 'Routes' in your directory, thank you""",grid=[0,0])
                                finished = PushButton(finalBox,text="Finished",grid=[0,1],command=Done)
                    routeBox.hide()
                    printBox = Box(menu,layout="grid")
                    printPrompt = Text(printBox,text="""Please enter a name for the saved file:""",
                                       grid=[0,0]) #the user enters what they would like the file to be called
                    printEntry = TextBox(printBox,grid=[0,1],width="15")
                    printEntry.bg = "white"
                    printConfirm = PushButton(printBox,text="Enter",grid=[0,2],command=Continue)
                def BackOut(): #returns the user to the main menu
                    routeBox.hide()
                    menu.title="WDF Routing Program"
                    menuBox.show()
                start = locationEntry.get()
                end = destinationEntry.get()
                if start == end or start == "" or end == "":
                    failed = info(title = "Invalid Input",text="Please enter valid start and endpoints")
                    locationEntry.clear()
                    destinationEntry.clear()
                else:
                    locationEntry.clear()
                    destinationEntry.clear()
                    routeStack = Dijkstra(graph,start,end) #runs the Dijsktra function and returns the
                                                           #route in a stack
                    if routeStack == "Route not possible":
                        failed = info(title = "Invalid Input",text="Please enter valid start and endpoints")
                    else:
                        menuBox.hide()
                        menu.title="Your Route"
                        routeBox = Box(menu,layout="grid")
                        theRoute = ""
                        routeAdvice = """Advice for using the route:\n
        1. Follow the route by following the rooms as you walk down each corridor
        2. If the first number changes, use the staircase you should be adjacent to
        3. The rooms aren't always in a logical order in each block\n"""
                        for i in range(0,routeStack.numItems()): #converts the route stack into a string for output
                            theRoute = (theRoute + (routeStack.pop()) + "\n")
                        headerRoute = Text(routeBox,text="Here is your route:",grid=[0,0],font="Arial",bg="black",color="white")
                        displayRoute = Text(routeBox,text=theRoute,grid=[0,1],font="Arial",bg="white")
                        infoRoute = Text(routeBox,text=(routeAdvice+"""\nYou can have your route saved into a printable
        text file if you would like?"""),grid=[0,2],font="Arial",color="blue")
                        printRoute = PushButton(routeBox,text="Print Route",grid=[0,3],command=Print)
                        backOut = PushButton(routeBox,text="Return to Menu",grid=[0,4],command=BackOut)
            def ShowMap(): #this function displays a map of the school for the user
                def Back(): #returns the user to the main menu
                    os.chdir(cwd)
                    mapBox.hide()
                    menu.title = "WDF Routing Program"
                    menuBox.show()
                os.chdir(cwd+"/Textures")
                menuBox.hide()
                menu.title = "The Map of William De Ferrers"
                mapBox = Box(menu,layout="grid")
                theMap = Picture(mapBox,image="theMap.gif",grid = [0,0],width=725,height=950)
                hideMap = PushButton(mapBox,text="Return to Menu",grid=[0,1],command=Back)
            menu.title = "WDF Routing Program"
            menuBox = Box(menu,layout="grid")
            os.chdir(cwd+"/Textures")
            banner = Picture(menuBox,image="main_banner.gif",grid=[0,0,4,1])
            headerFinder = Text(menuBox,text="Route finder:",grid=[0,1,4,1],font="Arial",color="white",bg="black")
            locationText = Text(menuBox,text="Starting Location:",grid=[0,2],font="Arial")
            locationEntry = TextBox(menuBox,grid=[1,2],width="15")
            locationEntry.bg = "white"
            destinationText = Text(menuBox,text="Destination:",grid=[2,2],font="Arial")
            destinationEntry = TextBox(menuBox,grid=[3,2],width="15")
            destinationEntry.bg = "white"
            dividerOne = Picture(menuBox, image="divider_1.gif",grid=[0,4,4,1])
            findRoute = PushButton(menuBox,grid=[0,4,4,1],text="Find Route:",command=FindRoute)
            findRoute.bg = "white"
            dividerThree = Picture(menuBox, image="divider_2.gif",grid=[0,5,4,1])
            showMap = PushButton(menuBox,text="Show Map",grid=[0,5,4,1],command=ShowMap)
            showMap.bg = "white"
            logoutButton=PushButton(menuBox,grid=[0,6,4,1],text="Logout",command=Logout)
            os.chdir(cwd)
        username=usernameEntry.get()
        password=passwordEntry.get()
        passwordEntry.clear()
        test = accounts.check(username,password) #uses the HashTable method to return whether the login credentials
                                                 #entered are correct
        if test == True: #if they are, the user is moved into the main menu of the program
            Confirmed = info(title = "Login successful",text="Login attempt was successful")
            usernameEntry.clear()
            loginBox.hide()
            Program(loginBox)
        else:
            Error = error(title = "Login unsuccessful",text = "Username or password incorrect, please try again")
    def CreateAccount(): #this function allows the user to create a new account for the application
        def Back(): #returns the user to the login screen
            accountBox.hide()
            menu.title = "Login"
            loginBox.show()
        def Create(): #attempts to create the new account based on the user's input
            username=userEntry.get()
            password1=passEntry.get()
            password2=confirmEntry.get()
            flag1 = False
            flag2 = False
            passtest = list(password1)
            for p in passtest:
                if p in ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]:
                    flag1 = True
                elif p in ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]:
                    flag2 = True
            if password1 != password2 or username == "" or password1 == "" or len(password1) < 8 or flag1 == False or flag2 == False:
                #if the user entered the password differently in the inputs, an error is shown and the user must try again
                errorMessage = error(title="Error",text="""Please enter valid inputs and ensure that the passwords match. The password
must be at least 8 characters long and contain one lower and one upper case character""")
                passEntry.clear()
                confirmEntry.clear()
            else:
                confirmation = yesno(title="Add new account",text="Are you sure you want to add this account?")
                #the user is then shown the credentials and asked to confirm if they want to create the account
                if confirmation == True: #if so, the HashTable class is used with its methods to add the account
                                         #to the table and then saves it
                    accounts.put(username,password1) #puts the new details into the table
                    os.chdir(cwd+"/Accounts")
                    accounts.save(accountsFile) #saves the new hash table
                    os.chdir(cwd)
                    message = info(title="Success",text="Account added!")
                    accountBox.hide()
                    loginBox.show()
                else: #else nothing happens and the user is told that they account was not added
                    message = info(title="Stopped",text="Account not added")
                    passEntry.clear()
                    confirmEntry.clear()
        loginBox.hide()
        menu.title = "Create Account"
        accountBox = Box(menu,layout="grid")
        header2 = Text(accountBox,text="""Please fill in the relevant fields to create a new
account""",grid=[0,0,2,1],font="Arial",color="blue")
        userText = Text(accountBox,text="Username:",grid=[0,1])
        passText = Text(accountBox,text="Password:",grid=[0,2])
        confirmText = Text(accountBox,text="Confirm Password:",grid=[0,3])
        userEntry=TextBox(accountBox,grid=[1,1],width="40")
        userEntry.bg = "white"
        passEntry=TextBox(accountBox,grid=[1,2],width="40")
        passEntry.bg = "white"
        confirmEntry=TextBox(accountBox,grid=[1,3],width="40")
        confirmEntry.bg = "white"
        createButton=PushButton(accountBox,grid=[1,4],text="Create",command=Create)
        backButton=PushButton(accountBox,grid=[0,5,2,1],text="Back to menu",command=Back)
    menu = App(title="Login",bg="#cae8dc")
    #guizero commands to create a window, fill it with widgets for text and command buttons
    loginBox = Box(menu,layout="grid")
    #each of my applications functions uses a different guizero Box object which can be easily
    #hidden or shown to make navigating windows in my program easy
    os.chdir(cwd+"/Textures")
    #certain images need to be loaded from the correct file and so the directory must be changed
    menu.tk.wm_iconbitmap("map_icon_transparent.ico")
    logo = Picture(loginBox,image="blue_map_logo.gif",grid=[1,0])
    os.chdir(cwd)
    header1 = Text(loginBox, text="Welcome to the WDF Routing Program",grid=[1,1],font="Arial",color="blue")
    quitButton = PushButton(loginBox,text="Quit",grid=[0,5],command=Quit)
    usernameText=Text(loginBox,text="Username:",grid=[0,2])
    usernameEntry=TextBox(loginBox,grid=[1,2],width="40")
    usernameEntry.bg = "white"
    passwordText=Text(loginBox,text="Password:",grid=[0,3])
    passwordEntry=TextBox(loginBox,grid=[1,3],width="40")
    passwordEntry.bg = "white"
    loginButton=PushButton(loginBox,text="Login",grid=[1,4],command=LoginCheck)
    createAccountButton = PushButton(loginBox,text="Create new\naccount",grid=[2,5],command=CreateAccount)
    menu.display()

BootLoader()
Application()
