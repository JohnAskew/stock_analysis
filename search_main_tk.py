import os, sys

import tkinter as tk

from tkinter import *

from tkinter import ttk

from tkinter.filedialog import asksaveasfile 

try:
    import pandas as pd

except:
    os.system('pip install pandas')
    import pandas as pd

pER_Stock_List = []
ePS_Stock_List = []
div_Stock_List = []
rSI_Stock_List = []
aCl_Stock_List = []
# FUNCTIONS
###############################
# #-----------------------------#
def Process_List():
 #-----------------------------#
    master_Stock_List = []
    if len(pER_Stock_List) > 0:
        master_Stock_List.append(pER_Stock_List)
    if len(ePS_Stock_List) > 0:
        master_Stock_List.append(ePS_Stock_List)

    if len(master_Stock_List)  == 0:
        print("Process_List Stubbed..No matches on any selection.")
        return []

    if len(master_Stock_List) == 1:
        print("Process_List Stubbed. Need way to display singleton search results")
        return master_Stock_List[0]

    for master_Stock in master_Stock_List:
        for stock in master_Stock:
            if stock in master_Stock_List[1]:
                print("Process_list HIT match on stock:", stock)


#     #if (operator == "<" & float(col_value) < float(value)) or (operator == "<=" & float(col_value) <= float(value)) or (operator == "=" & float(col_value) == float(value)) or (operator == ">=" & float(col_value) >= float(value)) or (operator == ">" & float(col_value) > float(value)):
#     if ((operator == ">=" ) & (float(col_value) >= float(value))): 
#         print("pER_Process_Set HIT")
#         pER_Stock_List.append(stock)
#     print(pER_Stock_List)
#-----------------------------#
def pER_Parse_Set():
#-----------------------------#

    pER_List = pER_Cbox_set()
    column   = pER_List[0]
    operator = pER_List[1]
    value    = pER_List[2]
    for stockz in os.listdir('askew/'):
        try:
            stock = pd.read_csv('askew/' + stockz)
            myPER = stock['PE_RATIO'].dropna(inplace = False)
            myPER = float(myPER)
            print('pER_Parse_Set: stockz:', stockz, 'has myPER:', str(myPER))

            if ((operator == ">=" ) & ((float(myPER) >= float(value)))): 
                stockz = stockz.replace('.csv', '')
                pER_Stock_List.append(stockz)
                print('pER_Parse_Set: stockz:', stockz)

        except Exception as e:
            print("Unable to recognize", stockz, ". Skipping...")
    print(pER_Stock_List)
#-----------------------------#
def ePS_Parse_Set():
#-----------------------------#

    ePS_List = ePS_Cbox_set()
    column   = ePS_List[0]
    oePSator = ePS_List[1]
    value    = ePS_List[2]
    for stockz in os.listdir('askew/'):
        try:
            stock = pd.read_csv('askew/' + stockz)
            myePS = stock['EPS_RATIO'].dropna(inplace = False)
            myePS = float(myePS)
            if ((oePSator == ">=" ) & (float(myePS) >= float(value))): 
                stockz = stockz.replace('.csv', '')
                ePS_Stock_List.append(stockz)
        except Exception as e:
            print("Unable to recognize", stockz, ". Skipping...")
    print(ePS_Stock_List)
    Process_List()
# #-----------------------------#
# def ePS_process_set():
# #-----------------------------#

#     ePS_List = ePS_Cbox_set()
#     print(ePS_List)

#-----------------------------#
def div_process_set():
#-----------------------------#

    div_List = div_Cbox_set()
    print(div_List)

#-----------------------------#
def rSI_process_set():
#-----------------------------#

    rSI_List = rSI_Cbox_set()
    print(rSI_List)

#-----------------------------#
def aCl_process_set():
#-----------------------------#

    aCl_List = aCl_Cbox_set()
    print(aCl_List)

#-----------------------------#
def pER_Cbox_set():
#-----------------------------#
    pER_List = []
    

    x = app.pER_Cbox.get()
    

    if x == 1:

        x = app.pER_Cbox.set(0)
        return ['']
    else:

        x = app.pER_Cbox.set(1)
        pER_List.append('PE_RATIO')
        pER_List.append(app.pER_Cobox.get())
        pER_List.append(app.pER_Tentry.get())

        return pER_List
#-----------------------------#
def ePS_Cbox_set():
#-----------------------------#
    ePS_List = []
   

    x = app.ePS_Cbox.get()
    
    if x == 1:

        x = app.ePS_Cbox.set(0)
        return ['']

    else:
        x = app.ePS_Cbox.set(1)
        ePS_List.append('EPS_RATIO')
        ePS_List.append(app.ePS_Cobox.get())
        ePS_List.append(app.ePS_Tentry.get())
        return ePS_List

#-----------------------------#
def div_Cbox_set():
#-----------------------------#
    div_List = []

    x = app.div_Cbox.get()
    

    if x == 1:

        x = app.div_Cbox.set(0)
        return ['']

    else:

        x = app.div_Cbox.set(1)
        div_List.append('DIVIDEND_AND_YIELD') 
        div_List.append(app.div_Cobox.get())
        div_List.append(app.div_Tentry.get())

        return div_List
#-----------------------------#
def rSI_Cbox_set():
#-----------------------------#
    rSI_List = []
    x = app.rSI_Cbox.get()

    if x == 1:

        x = app.rSI_Cbox.set(0)
        return ['']

    else:

        x = app.rSI_Cbox.set(1)
        rSI_List.append('RSI')
        rSI_List.append(app.rSI_Cobox.get())
        rSI_List.append(app.rSI_Tentry.get())
        return rSI_List

#-----------------------------#
def aCl_Cbox_set():
#-----------------------------#
    aCl_List = []
    x = app.aCl_Cbox.get()


    if x == 1:

        x = app.aCl_Cbox.set(0)
        return ['']
    else:

        x = app.aCl_Cbox.set(1)
        aCl_List.append('Adj_Close')
        aCl_List.append(app.aCl_Cobox.get())
        aCl_List.append(app.aCl_Tentry.get())
        return aCl_List

        
#######################################
class stockSearch:
#######################################

    def __init__(self):
 
        x = []
        #-----------------------------#
        # HOUSEKEEPING
        #-----------------------------#
        color_default = '#F0F0F0'

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

        math_values = ["<", "<=", "=", ">=", ">"]

        #######################################
        # DEFINE OUT TextBoxes for Input/Output
        #######################################

        self.pER_Cbox = tk.IntVar()
        self.ePS_Cbox = tk.IntVar()
        self.div_Cbox = tk.IntVar()
        self.rSI_Cbox = tk.IntVar()
        self.aCl_Cbox = tk.IntVar()

        self.pER_Cobox= tk.StringVar()
        self.ePS_Cobox= tk.StringVar()
        self.div_Cobox= tk.StringVar()
        self.rSI_Cobox= tk.StringVar()
        self.aCl_Cobox= tk.StringVar()

        self.pER_Tentry = tk.StringVar()
        self.ePS_Tentry = tk.StringVar()
        self.div_Tentry = tk.StringVar()
        self.rSI_Tentry = tk.StringVar()
        self.aCl_Tentry = tk.StringVar()


        #######################################
        # START PAINTING THE FRAME
        #######################################
        #-------------------------------------#
        # Add Check boxs - code flows up down, left to right
        #-------------------------------------#
        self.pER_Cbox.set(0)
        self.ePS_Cbox.set(0)
        self.div_Cbox.set(0)
        self.rSI_Cbox.set(0)
        self.aCl_Cbox.set(0)


        self.pER_Checkbox = ttk.Checkbutton(root, text = '', variable = self.pER_Cbox).grid(row = 5,  column = 0, sticky = 'w')
        self.ePS_Checkbox = ttk.Checkbutton(root, text = '', variable = self.ePS_Cbox).grid(row = 7,  column = 0, sticky = 'w')
        self.div_Checkbox = ttk.Checkbutton(root, text = '', variable = self.div_Cbox).grid(row = 9,  column = 0, sticky = 'w')
        self.rSI_Checkbox = ttk.Checkbutton(root, text = '', variable = self.rSI_Cbox).grid(row = 11, column = 0, sticky = 'w')
        self.aCl_Checkbox = ttk.Checkbutton(root, text = '', variable = self.aCl_Cbox).grid(row = 13, column = 0, sticky = 'w')

        #-------------------------------------#
        # Add the label for each line
        #-------------------------------------#

        label_header_1 = Label(root, text = 'Stock Search Tool', font = ("Times", "24", "bold italic underline")).grid(row = 0, column =0, )
        label_header_2 = Label(root, text = 'Tool searching datawarehouse which match your criteria.').grid(row = 1, column = 0)
        sep_label1     = Label(root, text = '___________________________________________________________________________________',bg = label_separator_bg, fg = label_separator_fg,).grid(row = 2, column = 0, sticky = 'w')
        label_pER      = Label(root, text = 'Price to Earnings Ratio:', fg = label_fg, bg = label_bg, font = ("Courier New", "8", "bold")). grid(row = 5, column = 0)
        sep_label1     = Label(root, text = ' ',bg = color_default, fg = color_default).grid(row = 6, column = 0, sticky = 'w')
        label_ePS      = Label(root, text = 'Earnings Per Share Ratio:', fg = label_fg, bg = label_bg, font = ("Courier New", "8", "bold")). grid(row = 7, column = 0)
        sep_label2     = Label(root, text = ' ',bg = color_default, fg = color_default).grid(row = 8, column = 0, sticky = 'w')
        label_div      = Label(root, text = '      Dividend Per Share:', fg = label_fg, bg = label_bg, font = ("Courier New", "8", "bold")). grid(row = 9, column = 0)
        sep_label3     = Label(root, text = ' ',bg = color_default, fg = color_default).grid(row = 10, column = 0, sticky = 'w')
        label_rSI      = Label(root, text = 'Relative Strength Percent:', fg = label_fg, bg = label_bg, font = ("Courier New", "8", "bold")). grid(row = 11, column = 0)
        sep_label4     = Label(root, text = ' ',bg = color_default, fg = color_default).grid(row = 12, column = 0, sticky = 'w')
        label_aCl      = Label(root, text = '     Adjusted Close Price:', fg = label_fg, bg = label_bg, font = ("Courier New", "8", "bold")). grid(row = 13, column = 0)
        sep_label5     = Label(root, text = ' ',bg = color_default, fg = color_default).grid(row = 14, column = 0, sticky = 'w')

        self.combo_pER = ttk.Combobox(root, width = 2, textvariable = self.pER_Cobox)
        self.combo_pER['values'] = math_values
        self.combo_pER.grid(row = 5, column = 0, sticky = 'ne')

        self.combo_ePS = ttk.Combobox(root, width = 2, textvariable = self.ePS_Cobox)
        self.combo_ePS['values'] = math_values
        self.combo_ePS.grid(row = 7, column = 0, sticky = 'ne')

        self.combo_div = ttk.Combobox(root, width = 2, textvariable = self.div_Cobox)
        self.combo_div['values'] = math_values
        self.combo_div.grid(row = 9, column = 0, sticky = 'ne')


        self.combo_rSI = ttk.Combobox(root, width = 2, textvariable = self.rSI_Cobox)
        self.combo_rSI['values'] = math_values
        self.combo_rSI.grid(row = 11, column = 0, sticky = 'ne')


        self.combo_aCl = ttk.Combobox(root, width = 2, textvariable = self.aCl_Cobox)
        self.combo_aCl['values'] = math_values
        self.combo_aCl.grid(row = 13, column = 0, sticky = 'ne')


        self.pER  = tk.Entry(root, textvariable = self.pER_Tentry,   width = 5, font = ("Courier New", "9", "bold"), fg = entry_fg, bg = entry2_bg).grid(row = 5,  column =1, padx = 5, sticky = 'w')
        self.ePS  = tk.Entry(root, textvariable = self.ePS_Tentry,   width = 5, font = ("Courier New", "9", "bold"), fg = entry_fg, bg = entry2_bg).grid(row = 7,  column =1, padx = 5, sticky = 'w')
        self.div  = tk.Entry(root, textvariable = self.div_Tentry,   width = 5, font = ("Courier New", "9", "bold"), fg = entry_fg, bg = entry2_bg).grid(row = 9,  column =1, padx = 5, sticky = 'w')
        self.rSI  = tk.Entry(root, textvariable = self.rSI_Tentry,   width = 5, font = ("Courier New", "9", "bold"), fg = entry_fg, bg = entry2_bg).grid(row = 11, column =1, padx = 5, sticky = 'w')
        self.aCl  = tk.Entry(root, textvariable = self.aCl_Tentry,   width = 5, font = ("Courier New", "9", "bold"), fg = entry_fg, bg = entry2_bg).grid(row = 13, column =1, padx = 5, sticky = 'w')


        self.buttonpER  = tk.Button(root, text = "Accept", fg = 'blue', bg = 'lavender', height = 0, width = 5, command = pER_Parse_Set).grid(row = 5,  column = 1 , padx=50, sticky = 'e')
        self.buttonePS  = tk.Button(root, text = "Accept", fg = 'blue', bg = 'lavender', height = 0, width = 5, command = ePS_Parse_Set).grid(row = 7,  column = 1 , padx=50, sticky = 'e')
        self.buttondiv  = tk.Button(root, text = "Accept", fg = 'blue', bg = 'lavender', height = 0, width = 5, command = div_process_set).grid(row = 9,  column = 1 , padx=50, sticky = 'e')
        self.buttonrSI  = tk.Button(root, text = "Accept", fg = 'blue', bg = 'lavender', height = 0, width = 5, command = rSI_process_set).grid(row = 11, column = 1 , padx=50, sticky = 'e')
        self.buttonaCl  = tk.Button(root, text = "Accept", fg = 'blue', bg = 'lavender', height = 0, width = 5, command = aCl_process_set).grid(row = 13, column = 1 , padx=50, sticky = 'e')


        self.pER_Choice = self.pER_Cbox.get()
        self.ePS_Choice = self.ePS_Cbox.get()
        self.div_Choice = self.div_Cbox.get()
        self.rSI_Choice = self.rSI_Cbox.get()
        self.aCl_Choice = self.aCl_Cbox.get()

        
root = tk.Tk()

app = stockSearch()

root.mainloop()
