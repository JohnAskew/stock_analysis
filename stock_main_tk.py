import os, sys
#from stocks_1 import *
try:
    import tkinter as tk
except:
    os.system('pip install tkinter')
    import tkinter as tk
from tkinter import ttk
try:
    import matplotlib
except:
    os.system("pip install matplotlib")
    import matplotlib
try:
    import subprocess
except:
    os.system("pip install subprocess")
    import subprocess

stock = ""
dir_path = os.path.dirname(os.path.realpath(__file__))
exchange = "S&P500"
DatCounter = 9000
programName = "sp500"
dataPace = "1d"
#######################################
# F U N C T I O N S 
#######################################
def changeTimeFrame(tf):
    global dataPace
    global DatCounter


#-------------------------------------#
def popupmsg(msg):
#-------------------------------------#
    popup = tk.Tk()

    popup.wm_title("!")
    label = ttk.Label(popup, text = msg)
    label.pack(side = "top", fill = "x", pady = 10)
    B1 = ttk.Button(popup, text = "Okay", command = popup.destroy())
    B1.pack()
    popup.mainloop()


#-------------------------------------#
def changeExchange(toWhat, pn):
#-------------------------------------#
    global exchange
    global DatCounter
    global programName

    exchange = toWhat
    programName = pn
    DatCounter = 9000


#######################################
class SeaofBTCapp(tk.Tk):
#######################################
#-------------------------------------#
    def __init__(self, *args, **kwargs): #args = any num variables; same kwargs
#-------------------------------------#    
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default = "py.ico")
        tk.Tk.wm_title(self, "Search Stock client")

        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff = 0)
        filemenu.add_command(label = "Save Settings", command = lambda: popupmsg("Not Supported Yet."))
        filemenu.add_separator()
        filemenu.add_command(label = "Exit", command = quit)
        menubar.add_cascade(label = "File", menu = filemenu)

        exchangeChoice = tk.Menu(menubar, tearoff = 1)
        exchangeChoice.add_command(label = 'S&P 500', command = lambda: changeExchange("SP500", "sp500"))
        exchangeChoice.add_command(label = 'NYSE', command = lambda: changeExchange("NYSE", "nyse"))
        menubar.add_cascade(label = "Exchange", menu = exchangeChoice)

        dataTF = tk.Menu(menubar, tearoff = 1)
        dataTF.add_command(label = "Tick", command = lambda: changeTimeFrame('tick'))
        dataTF.add_command(label = "1 week", command = lambda: changeTimeFrame('7d'))
        dataTF.add_command(label = "1 Month", command = lambda: changeTimeFrame('30d'))
        menubar.add_cascade(label = "TimeSpan", menu = dataTF)               








        tk.Tk.config(self, menu = menubar)




        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageGenerateGraph):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky = "news")

        self.show_frame(StartPage)

#-------------------------------------#    
    def show_frame(self, cont):
#-------------------------------------#    

        frame = self.frames[cont]

        frame.tkraise()


#######################################
class StartPage(tk.Frame):
#######################################
#-------------------------------------#  
    def __init__(self, parent, controller):
#-------------------------------------#  
        tk.Frame.__init__(self, parent)
        #-------------------------------------#
        def get_entryText():
        #-------------------------------------#
            p = e1.get()
            print(p)
            return p

        label = tk.Label(self, text = "Search Stock Tool", font = ("Times", "24", "bold italic underline"))
        

        label.pack(padx = 10, pady = 0)


        

        entryText = tk.StringVar(self)
        entryText.set('GOOG')
        e1 = tk.Entry(self, textvariable = entryText)

        e1.focus_set()
        e1_label = tk.Label(self,text="Enter Stock Symbol", font = ("Courier New", "10", "bold"))#.grid(row=0, column = 0)
        e1_label.pack(side = "top")
        e1.pack(side = "top")
      

        button1 = ttk.Button(self, text = "Accept Choice", command = get_entryText)

        button1.pack(side = 'top')

        button2 = ttk.Button(self, text = "Visit Page 2", command = lambda: controller.show_frame(PageTwo))

        button2.pack(side = "bottom")

        button3 = ttk.Button(self, text = "Generate Graph", command =  lambda: subprocess.call(["python", dir_path + "/" + "stocks_1.py", get_entryText() ]))#lambda: controller.show_frame(PageGenerateGraph))

        button3.pack()

        e2_label = tk.Label(self, text = "--> First daily run takes \n4 minutes to build 500 \nstocks datawarehouse <--", font = ("Monospace, 10"))

        e2_label.pack(side = 'top')


#######################################
class PageOne(tk.Frame):
#######################################
#-------------------------------------# 
    def __init__(self, parent, controller):
#-------------------------------------# 
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Start Page", font = "LARGE_FONT")

        label.pack(padx = 10, pady = 10)

        button1 = ttk.Button(self, text = "Back to Home", command = lambda: controller.show_frame(StartPage))

        button1.pack()

        button2 = ttk.Button(self, text = "Visit PageTwo", command = lambda: controller.show_frame(PageTwo))

        button2.pack()

#######################################
class PageTwo(tk.Frame):
#######################################
#-------------------------------------# 
    def __init__(self, parent, controller):
#-------------------------------------# 
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Start Page", font = "LARGE_FONT")

        label.pack(padx = 10, pady = 10)

        button1 = ttk.Button(self, text = "Back to Home", command = lambda: controller.show_frame(StartPage))

        button1.pack()

        button2 = ttk.Button(self, text = "Visit PageOne", command = lambda: controller.show_frame(PageOne))

        button2.pack()

#######################################
class PageGenerateGraph(tk.Frame):
#######################################
#-------------------------------------# 
    def __init__(self, parent, controller):
#-------------------------------------# 
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Graph Page", font = "LARGE_FONT")

        label.pack(padx = 10, pady = 10)

        button1 = ttk.Button(self, text = "Back to Home", command = lambda: controller.show_frame(StartPage))

        button1.pack()
       







#######################################
# M A I N   L O G I C   S T A R T
#######################################

app = SeaofBTCapp()
app.geometry("360x240")
app.mainloop()





