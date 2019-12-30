import os, sys
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
try:
    import configparser
except:
    os.system('pip install configparser')
    import configparser
from tools_parse_config import ParseConfig
try:
    from tools_config_manager import ConfigUpdater
except:
    msg = "Unable to find config file. Using defaults"
    
    print(msg)
    
    movavg_window_days_short_term = 10                                         #Moving Average 10 days (quick)
    
    movavg_window_days_long_term = 30                                         #Moving Average 30 days (slow)
    
    macd_periods_long_term = 26
    
    macd_periods_short_term = 12
    
    expma_periods = 9 

try:
    from tools_parse_config import ParseConfig
except:
    
    msg = "Unable to find config file. Using defaults"
    
    print(msg)
    
    movavg_window_days_short_term = 10                                         #Moving Average 10 days (quick)
    
    movavg_window_days_long_term = 30                                         #Moving Average 30 days (slow)
    
    macd_periods_long_term = 26
    
    macd_periods_short_term = 12
    
    expma_periods = 9 

stock = ""

dir_path = os.path.dirname(os.path.realpath(__file__))


#######################################
# F U N C T I O N S 
#######################################
#-------------------------------------#
def popupmsg(msg):
#-------------------------------------#
    popup = tk.Tk()
    
    popup.wm_title(" Warning!")
    
    label = ttk.Label(popup, text = msg)
    
    label.grid(row = 3, column = 5)
    
    B1 = ttk.Button(popup, text = "Okay", command = lambda: popup.destroy())
    
    B1.grid(row = 5, column = 5)
    
    popup.mainloop()




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
    
        #container.pack(side = "top", fill = "both", expand = True)
        container.grid(row =0, column = 0)
    
        container.grid_rowconfigure(0, weight = 1)
    
        container.grid_columnconfigure(0, weight = 1)

        

        self.frames = {}

        for F in (StartPage, PageGenerateGraph):

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
        def update_mAST_config():
        #-------------------------------------#
            variable = mAST.get()
            
            a =  ConfigUpdater('movavg_window_days_short_term', variable)
            
            a.run()

        #-------------------------------------#
        def update_mALT_config():
        #-------------------------------------#
            variable = mALT.get()
            
            a =  ConfigUpdater('movavg_window_days_long_term', variable)
            
            a.run()
        
        #-------------------------------------#
        def update_mcST_config():
        #-------------------------------------#
            variable = mcST.get()
            
            a =  ConfigUpdater('macd_periods_short_term', variable)
            
            a.run()

        #-------------------------------------#
        def update_mcLT_config():
        #-------------------------------------#
            variable = mcLT.get()
            
            a =  ConfigUpdater('macd_periods_long_term', variable)
            
            a.run()
            
        #-------------------------------------#
        def update_eMAT_config():
        #-------------------------------------#
            variable = eMAT.get()
            
            a =  ConfigUpdater('expma_periods', variable)
            
            a.run()
            
            
        #-------------------------------------#
        def update_rHT_config():
        #-------------------------------------#
            variable = rHT.get()
            
            a =  ConfigUpdater('rsi_overbought', variable)
            
            a.run()
            
            
        #-------------------------------------#
        def update_rLT_config():
        #-------------------------------------#
            variable = rLT.get()
            
            a =  ConfigUpdater('rsi_oversold', variable)
            
            a.run()

        #-------------------------------------#
        def get_entryText():
        #-------------------------------------#
            p = eT1.get()

            if len(p) < 1:

                msg = "Accepted input must be Characters"

                popupmsg(msg)

                return

            p = ''.join(p)

            p = str.upper(p).split()

            p = str(p[0])



            if p.isalpha():

                pass 

            else:

                msg = "Input must be all Alphabetic Characters without spaces"

                popupmsg(msg) 

                return
            
            if len(p) > 5:

                msg = "Stock Ticker must be 5 Characters or less"

                popupmsg(msg)

                return

            return p


        label = tk.Label(self, text = "Stock Tracker Tool", font = ("Times", "24", "bold italic underline"))
        
        label.grid(row = 1, column = 0, sticky = 'w')

        eT1_label = tk.Label(self,text="    Enter Stock here ", font = ("Courier New", "10", "bold"), width = 18)
        
        eT1_label.grid(row = 4, column = 0, sticky = "w")

        entryText        = tk.StringVar(self)
        maShort_Tentry   = tk.StringVar(self)
        maLong_Tentry    = tk.StringVar(self)
        macdShort_Tentry = tk.StringVar(self)
        macdLong_Tentry  = tk.StringVar(self)
        ema_Tentry       = tk.StringVar(self)
        rsiLow_Tentry    = tk.StringVar(self)
        rsiHigh_Tentry   = tk.StringVar(self)



        maShort_label   = tk.Label(self,text=" Mov. Avg. short:", font = ("Courier New", "8")).grid(row = 20, column = 0, sticky = 'nw')
        maLong_label    = tk.Label(self,text="  Mov. Avg. long:", font = ("Courier New", "8")).grid(row = 22, column = 0, sticky = 'nw')
        macdShort_label = tk.Label(self,text="     MACD  short:", font = ("Courier New", "8")).grid(row = 24, column = 0, sticky = 'nw')
        macdLong_label  = tk.Label(self,text="       MACD long:", font = ("Courier New", "8")).grid(row = 26, column = 0, sticky = 'nw')
        ema_label       = tk.Label(self,text="Expon. Mov. Avg.:", font = ("Courier New", "8")).grid(row = 28, column = 0, sticky = 'nw')
        rsiLow_label    = tk.Label(self,text="         RSI low:", font = ("Courier New", "8")).grid(row = 30, column = 0, sticky = 'nw')
        rsiHigh_label   = tk.Label(self,text="        RSI high:", font = ("Courier New", "8")).grid(row = 32, column = 0, sticky = 'nw')
        
 
        a = ParseConfig()
        movavg_window_days_short_term, movavg_window_days_long_term, macd_periods_long_term, macd_periods_short_term, expma_periods, rsi_overbought, rsi_oversold = a.run()

        entryText.set('GOOG')
        maShort_Tentry.set(movavg_window_days_short_term)
        maLong_Tentry.set(movavg_window_days_long_term)
        macdShort_Tentry.set(macd_periods_short_term)
        macdLong_Tentry.set(macd_periods_long_term)
        ema_Tentry.set(expma_periods)
        rsiLow_Tentry.set(rsi_oversold)
        rsiHigh_Tentry.set(rsi_overbought)
        

        eT1  = tk.Entry(self, textvariable = entryText,        width = 8)
        mAST = tk.Entry(self, textvariable = maShort_Tentry,   width = 4)
        mALT = tk.Entry(self, textvariable = maLong_Tentry,    width = 4)
        mcST = tk.Entry(self, textvariable = macdShort_Tentry, width = 4)
        mcLT = tk.Entry(self, textvariable = macdLong_Tentry,  width = 4)
        eMAT = tk.Entry(self, textvariable = ema_Tentry,       width = 4)
        rLT  = tk.Entry(self, textvariable = rsiLow_Tentry,    width = 4)
        rHT  = tk.Entry(self, textvariable = rsiHigh_Tentry,   width = 4)


        eT1.grid( row =  4, column = 0, sticky = "e")
        separator_label1 = tk.Label(self, text = ' ').grid(row = 18, column = 0, sticky = 'w')
        separator_label2 = tk.Label(self, text = '--------- Programmable Variables ---------').grid(row = 19, column = 0, sticky = 'w')
        mAST.grid(row = 20, column = 0, sticky = "e")
        mALT.grid(row = 22, column = 0, sticky = "e")
        mcST.grid(row = 24, column = 0, sticky = "e")
        mcLT.grid(row = 26, column = 0, sticky = "e")
        eMAT.grid(row = 28, column = 0, sticky = "e")
        rLT.grid( row = 30, column = 0, sticky = "e")
        rHT.grid( row = 32, column = 0, sticky = "e")


        buttonmAST = ttk.Button(self, text = "Update", command = update_mAST_config).grid(row = 20, column = 1, sticky = 'w')
        buttonmALT = ttk.Button(self, text = "Update", command = update_mALT_config).grid(row = 22, column = 1, sticky = 'w')
        buttonmcST = ttk.Button(self, text = "Update", command = update_mcST_config).grid(row = 24, column = 1, sticky = 'w')
        buttonmcLT = ttk.Button(self, text = "Update", command = update_mcLT_config).grid(row = 26, column = 1, sticky = 'w')
        buttoneMAT = ttk.Button(self, text = "Update", command = update_eMAT_config).grid(row = 28, column = 1, sticky = 'w')
        buttonrLT  = ttk.Button(self, text = "Update", command = update_rLT_config).grid( row = 30, column = 1, sticky = 'w')
        buttonrHT  = ttk.Button(self, text = "Update", command = update_rHT_config).grid( row = 32, column = 1, sticky = 'w')


        eT1.focus_set()
              
        buttonAccept = ttk.Button(self, text = "Accept Choice", command = get_entryText)

        buttonAccept.grid(row = 4, column = 1, sticky = 'w')

        buttonGraph = ttk.Button(self, text = "Generate Graph", command =  lambda: subprocess.call(["python", dir_path + "/" + "stocks_1.py", get_entryText() ]))#lambda: controller.show_frame(PageGenerateGraph))

        buttonGraph.grid(row = 10, column = 1, sticky = 'w')

        e2_label = tk.Label(self, text = "First daily run takes 7 minutes\nto build the 500 stocks datawarehouse.\n New folder \"askew\" holds the build.", font = ("Monospace, 10"))

        e2_label.grid(row = 12, column = 0, sticky = 'nw')




#######################################
class PageGenerateGraph(tk.Frame):
#######################################
#-------------------------------------# 
    def __init__(self, parent, controller):
#-------------------------------------# 
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Graph Page", font = "LARGE_FONT")

        label.grid(row = 5, column = 5)

         

#######################################
# M A I N   L O G I C   S T A R T
#######################################

app = SeaofBTCapp()

app.geometry("360x360")

app.mainloop()





