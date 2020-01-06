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

programming_variable_start_row = 20

value = 0

#######################################
# F U N C T I O N S 
#######################################

#-------------------------------------#
def radio_chosen(value):
#-------------------------------------#
    radioLabel = tk.Label(app, text = value).grid(row = 6, column = 0, sticky = 'nw')

    return value
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
class SeaofSTOXapp(tk.Tk):
#######################################
#-------------------------------------#
    def __init__(self, *args, **kwargs): #args = any num variables; same kwargs
#-------------------------------------#    
        tk.Tk.__init__(self, *args, **kwargs)

        if os.name== 'nt':

            tk.Tk.iconbitmap(self, default = "py.ico")
    
        tk.Tk.wm_title(self, "Stock Tracker client")

        container = tk.Frame(self)

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
        frame.config(bg = frame_bg) ##FFFFFA')


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


        RADIO_DAYS = [

         (365, "365")

        ,(270, "270")

        ,(180, "180")
        
        ,]
        


        label = tk.Label(self, text = "Stock Tracker Tool", fg = label_big_fg, bg = label_big_bg, font = ("Times", "24", "bold italic underline"))
        
        label.grid(row = 1, column = 0, sticky = 'w')

        eT1_label = tk.Label(self,text="Enter Stock Symbol here ==>  ", fg = label_fg_red, bg = label_bg, font = ("Courier New", "10", "bold"), width = 35)
        
        eT1_label.grid(row = 4, column = 0, sticky = "w")

        radio_days       = tk.StringVar()
        
        entryText        = tk.StringVar()
        
        maShort_Tentry   = tk.StringVar()
        
        maLong_Tentry    = tk.StringVar()
        
        macdShort_Tentry = tk.StringVar()
        
        macdLong_Tentry  = tk.StringVar()
        
        ema_Tentry       = tk.StringVar()
        
        rsiLow_Tentry    = tk.StringVar()
        
        rsiHigh_Tentry   = tk.StringVar()

        
        radio_days.set("365")

         
        x = tk.Radiobutton(self, text = RADIO_DAYS[0][0], bg = color_white,  fg = button_fg, variable = radio_days, value = RADIO_DAYS[0][1]).grid(row = programming_variable_start_row + 2, column = 0, padx = 0, sticky = 'W', )
        
        y = tk.Radiobutton(self, text = RADIO_DAYS[1][0], bg = color_white,  fg = button_fg, variable = radio_days, value = RADIO_DAYS[1][1]).grid(row = programming_variable_start_row + 2, column = 0, padx = 0)
        
        z = tk.Radiobutton(self, text = RADIO_DAYS[2][0], bg = color_white,  fg = button_fg, variable = radio_days, value = RADIO_DAYS[2][1]).grid(row = programming_variable_start_row + 2, column = 0, padx = 0, stick = 'E')


        maShort_label   = tk.Label(self,text="    Moving Average days (short):", fg = label_fg, bg = label_bg, font = ("Courier New", "8", "bold")).grid(row = programming_variable_start_row + 13, column = 0, sticky = 'nw')
        
        maLong_label    = tk.Label(self,text="     Moving Average days (long):", fg = label_fg, bg = label_bg, font = ("Courier New", "8", "bold")).grid(row = programming_variable_start_row + 14, column = 0, sticky = 'nw')
        
        macdShort_label = tk.Label(self,text="Mov Avg Cnvg/DeCnvg short cycle:", fg = label_fg, bg = label_bg, font = ("Courier New", "8", "bold")).grid(row = programming_variable_start_row + 15, column = 0, sticky = 'nw')
        
        macdLong_label  = tk.Label(self,text="Mov Avg Cnvg/DeCnvg long cycle:",  fg = label_fg, bg = label_bg, font = ("Courier New", "8", "bold")).grid(row = programming_variable_start_row + 16, column = 0, sticky = 'nw')
        
        ema_label       = tk.Label(self,text="Exponential Moving Avg Periods:",  fg = label_fg, bg = label_bg, font = ("Courier New", "8", "bold")).grid(row = programming_variable_start_row + 17, column = 0, sticky = 'nw')
        
        rsiLow_label    = tk.Label(self,text=" Relative Strength Index % low:",  fg = label_fg, bg = label_bg, font = ("Courier New", "8", "bold")).grid(row = programming_variable_start_row + 18, column = 0, sticky = 'nw')
        
        rsiHigh_label   = tk.Label(self,text="Relative Strength Index % high:",  fg = label_fg, bg = label_bg, font = ("Courier New", "8", "bold")).grid(row = programming_variable_start_row + 19, column = 0, sticky = 'nw')
        
 
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
        

        
        rBC  = tk.Entry(self, textvariable = radio_days,       width = 8, fg = entry_fg, bg = entry_bg)
        
        eT1  = tk.Entry(self, textvariable = entryText,        width = 8, fg = entry_fg, bg = entry_bg)
        
        mAST = tk.Entry(self, textvariable = maShort_Tentry,   width = 3, font = ("Courier New", "9", "bold"), fg = entry_fg, bg = entry2_bg)
        
        mALT = tk.Entry(self, textvariable = maLong_Tentry,    width = 3, font = ("Courier New", "9", "bold"), fg = entry_fg, bg = entry2_bg)
        
        mcST = tk.Entry(self, textvariable = macdShort_Tentry, width = 3, font = ("Courier New", "9", "bold"), fg = entry_fg, bg = entry2_bg)
        
        mcLT = tk.Entry(self, textvariable = macdLong_Tentry,  width = 3, font = ("Courier New", "9", "bold"), fg = entry_fg, bg = entry2_bg)
        
        eMAT = tk.Entry(self, textvariable = ema_Tentry,       width = 3, font = ("Courier New", "9", "bold"), fg = entry_fg, bg = entry2_bg)
        
        rLT  = tk.Entry(self, textvariable = rsiLow_Tentry,    width = 3, font = ("Courier New", "9", "bold"), fg = entry_fg, bg = entry2_bg)
        
        rHT  = tk.Entry(self, textvariable = rsiHigh_Tentry,   width = 3, font = ("Courier New", "9", "bold"), fg = entry_fg, bg = entry2_bg)


        eT1.grid( row =  4, column = 0, sticky = "e")
        
        separator_label1 = tk.Label(self, text = '___________________________________________________________',bg = label_separator_bg, fg = label_separator_fg,).grid(row = 17, column = 0, sticky = 'w')
        
        separator_label2 = tk.Label(self, text = '--------- Programmable Variables ---------', bg = label_separator_bg, fg = label_separator_fg, font = ("Courier New", "9", "bold"), height = 1).grid(row = programming_variable_start_row + 12, column = 0, sticky = 'w')
        
        mAST.grid(row = programming_variable_start_row + 13, column = 0, sticky = "e")
        
        mALT.grid(row = programming_variable_start_row + 14, column = 0, sticky = "e")
        
        mcST.grid(row = programming_variable_start_row + 15, column = 0, sticky = "e")
        
        mcLT.grid(row = programming_variable_start_row + 16, column = 0, sticky = "e")
    
        eMAT.grid(row = programming_variable_start_row + 17, column = 0, sticky = "e")
        
        rLT.grid( row = programming_variable_start_row + 18, column = 0, sticky = "e")
        
        rHT.grid( row = programming_variable_start_row + 19, column = 0, sticky = "e")


        
        buttonRadio = tk.Button(self, text = "Accept choice of historical days to track", fg = button_fg, height = 2, command = lambda: radio_chosen(radio_days.get())).grid(  row = programming_variable_start_row - 2,  column = 0, sticky = 'sew')
        
        buttonmAST  = tk.Button(self, text = "Update", fg = button_fg, bg = button_bg, command = update_mAST_config).grid(row = programming_variable_start_row + 13,  column = 1, sticky = 'e')
        
        buttonmALT  = tk.Button(self, text = "Update", fg = button_fg, bg = button_bg, command = update_mALT_config).grid(row = programming_variable_start_row + 14, column = 1, sticky = 'e')
        
        buttonmcST  = tk.Button(self, text = "Update", fg = button_fg, bg = button_bg, command = update_mcST_config).grid(row = programming_variable_start_row + 15, column = 1, sticky = 'e')
        
        buttonmcLT  = tk.Button(self, text = "Update", fg = button_fg, bg = button_bg, command = update_mcLT_config).grid(row = programming_variable_start_row + 16, column = 1, sticky = 'e')
        
        buttoneMAT  = tk.Button(self, text = "Update", fg = button_fg, bg = button_bg, command = update_eMAT_config).grid(row = programming_variable_start_row + 17, column = 1, sticky = 'e')
        
        buttonrLT   = tk.Button(self, text = "Update", fg = button_fg, bg = button_bg, command = update_rLT_config).grid(row  = programming_variable_start_row + 18, column = 1, sticky = 'e')
        
        buttonrHT   = tk.Button(self, text = "Update", fg = button_fg, bg = button_bg, command = update_rHT_config).grid(row  = programming_variable_start_row + 19, column = 1, sticky = 'e')


        eT1.focus_set()
              
        buttonAccept = tk.Button(self, text = "Accept Choice", fg = 'red', bg = button_bg, command = get_entryText)
        
        buttonAccept.grid(row = 4, column = 1, sticky = 'e')

        buttonGraph = tk.Button(self, text = " Create Graph ", fg = button_fg, bg = button_bg, command =  lambda: subprocess.call(["python", dir_path + "/" + "stocks_1.py", get_entryText(), radio_days.get() ]))#lambda: controller.show_frame(PageGenerateGraph))

        buttonGraph.grid(row = 10, column = 1, sticky = 'e')

        e2_label = tk.Label(self, fg = color_verbose, bg = label_bg, text = "First daily run takes up to 30 minutes to build the stocks\ndatawarehouse. Scraping 500+ stocks gets throttled by Yahoo!\nNew folder \"askew\" holds the build.", font = ("Monospace, 8"))

        e2_label.grid(row = 10, column = 0, sticky = 'nw', rowspan = 3)




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

color_melon  = '#F53335'

color_purple = '#890b86'

color_black  = '#0F0F0A'

color_red    = 'red'

color_white  = '#FFFFFA'

color_blue   = 'blue'

color_gray   = 'lavender'#'floralwhite'

color_verbose = 'lemonchiffon' #antiquewhite'

color_firebrick = 'turquoise2' #steelblue2'


frame_fg = color_black

frame_bg = color_purple

label_fg = color_white

label_bg = color_purple

label_big_fg = color_black

label_big_bg = color_purple

label_fg_red = color_verbose

label_separator_fg = color_firebrick

label_separator_bg = color_purple

entry_fg     = color_red

entry_bg     = color_white

entry2_fg    = color_blue

entry2_bg    = color_gray

button_fg    = color_blue

button_bg    = color_gray

# style = ttk.Style()

# style.configure("But.ton", foreground = button_fg, background = button_bg)

app = SeaofSTOXapp()

app.geometry("405x410")

app.mainloop()





