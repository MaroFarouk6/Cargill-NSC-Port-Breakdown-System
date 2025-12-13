from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import sqlite3 as sq
import time
from datetime import datetime
import threading
from tksheet import *
from xlsxwriter.workbook import Workbook
from xlsxwriter.exceptions import FileCreateError
# to do:
# light mode

root = Tk()
root.config(bg='#03050f')
root.title('Breakdown System')
# root.minsize(1100, 700)
root.state('zoomed')
root.iconbitmap('ico.ico')

font = ('Segoe UI', 11)
bg_colour = "#11131c"

top_frame = Frame(root, bg='#03050f')
top_frame.pack(fill='x')


lbl_frame = Frame(top_frame, bg='#03050f')
lbl_frame.grid(row=0, column=0, pady=10, padx=10)

Label(lbl_frame, pady=10, padx=20, text='Available', bg='green', fg='white', font=font).grid(row=0, column=0, sticky='news')
Label(lbl_frame, pady=10, padx=20, text='Breakdown', bg='red', fg='white', font=font).grid(row=0, column=1, sticky='news')
Label(lbl_frame, pady=10, padx=20, text='Planned Maintenance', bg='blue', fg='white', font=font).grid(row=0, column=2, sticky='news')
Label(lbl_frame, pady=10, padx=20, text='Out of Service', bg='orange', fg='white', font=font).grid(row=0, column=3, sticky='news')


refresh_frame = Frame(top_frame, bg='#03050f')
refresh_frame.grid(row=0, column=1, padx=(10, 0))

log_in_ico = PhotoImage(file='assets/icons8-login-30.png')
create_user_ico = PhotoImage(file='assets/icons8-account-30.png')
log_ico = PhotoImage(file='assets/icons8-log-30.png')
logo_ico = PhotoImage(file='assets/cargill-logo.png')

last_refresh = Button(refresh_frame, bg='#03050f', fg='white', relief='flat', text=f'Last refresh: {datetime.now().strftime("%I:%M:%S %p")}', font=font,
                      activebackground='#798185', activeforeground='white')
last_refresh.grid(row=0, column=0, padx=(0, 50))
last_refresh.bind('<Enter>', lambda x: last_refresh.config(bg='#394145'))
last_refresh.bind('<Leave>', lambda x: last_refresh.config(bg='#03050f'))

log_in_btn = Button(refresh_frame, text=' Log in', bg='#03050f', fg='white', relief='flat', font=font, image=log_in_ico, compound='left',
                    activebackground='#798185', activeforeground='white')
log_in_btn.grid(row=0, column=1)
log_in_btn.bind('<Enter>', lambda x: log_in_btn.config(bg='#394145'))
log_in_btn.bind('<Leave>', lambda x: log_in_btn.config(bg='#03050f'))

create_user_btn = Button(refresh_frame, text=' Create User', bg='#03050f', fg='white', relief='flat', font=font, compound='left',
                         activebackground='#798185', activeforeground='white', image=create_user_ico)
create_user_btn.grid(row=0, column=2, padx=(20, 0))
create_user_btn.bind('<Enter>', lambda x: create_user_btn.config(bg='#394145'))
create_user_btn.bind('<Leave>', lambda x: create_user_btn.config(bg='#03050f'))

log_btn = Button(refresh_frame, text=' Log', bg='#03050f', fg='white', relief='flat', font=font, compound='left',
                 activebackground='#798185', activeforeground='white', image=log_ico)
log_btn.grid(row=0, column=3, padx=(20, 0))
log_btn.bind('<Enter>', lambda x: log_btn.config(bg='#394145'))
log_btn.bind('<Leave>', lambda x: log_btn.config(bg='#03050f'))

logo =Label(refresh_frame, bg='#03050f', relief='flat', font=font, compound='left', activebackground='#798185',
      activeforeground='white', image=logo_ico)
logo.grid(row=0, column=4, padx=(20, 0))
logo.bind('<Enter>', lambda x: logo.config(bg='#394145'))
logo.bind('<Leave>', lambda x: logo.config(bg='#03050f'))

notebook = ttk.Notebook()
notebook.pack(fill='both', expand=1)

# Variables
status_colors = ['green', 'orange', 'blue', 'red', 'yellow']
status_words = ['Available', 'Out of Service', 'Planned Maintenance', 'Breakdown', 'Ready']

column_num = 6

cells = []
user_name = ''
user_role = ''


def create_tab_dict():  # Makes a dict of tab names and tab objects
    db = sq.connect('equipment.db')
    cr = db.cursor()

    cr.execute("SELECT name FROM sqlite_master WHERE type='table'")
    all_tables = list(map(lambda x: x[0], cr.fetchall()[:-2]))
    # all_tables.remove("Accounts")  <<<-------------------------------------------------------------------
    db.close()

    t_dict = {}

    for table in all_tables:
        t_dict[table] = Tab(table)

    return t_dict


class Cell:
    breakdown_cells = []

    def __init__(self, name, status, row, column, type, tab_frame, parent_cell=None):
        self.name = name
        self.status = status
        self.type = type
        # self.tab_frame = tab_frame
        self.parent_cell = parent_cell

        self.frame = Frame(tab_frame, bg='#03050f')
        if self.parent_cell is None:  # Determining whether the cell is a normal cell or a breakdown cell
            self.breakdown_cell = Cell(self.name, 3, None, None, self.type, breakdown_tab.equipment_frame, self)
            self.frame.grid(row=row, column=column, sticky='news', padx=5, pady=5)
        self.frame.columnconfigure([0], weight=1)
        self.frame.rowconfigure([0, 1, 2], weight=1)

        self.title_lbl = Label(self.frame, text=name, fg='white')
        self.title_lbl.grid(row=0, column=0, sticky='news')

        self.status_lbl = Label(self.frame, fg='white')
        self.status_lbl.grid(row=1, column=0, sticky='new')

        self.inner_frame = Frame(self.frame, bg='#03050f')
        self.inner_frame.columnconfigure([0, 1], weight=1)
        self.inner_frame.rowconfigure([0, 1], weight=1, minsize=45)
        self.inner_frame.grid(row=3, column=0, sticky='news', padx=3, pady=3)

        def on_enter(e):
            e.widget['bg'] = '#394145'

        def on_leave(e):
            e.widget['bg'] = '#091115'

        self.available_btn = Button(self.inner_frame, bg='#091115', fg='white', bd=0, text='Available',
                                    command=lambda: self.change_status(0), activebackground='#798185', activeforeground='white')

        self.available_btn.grid(row=0, column=0, sticky='news', padx=3, pady=3)

        self.not_available_btn = Button(self.inner_frame, bg='#091115', fg='white', bd=0, text='Out of Service',
                                        command=lambda: self.change_status(1), activebackground='#798185', activeforeground='white')
        self.not_available_btn.grid(row=1, column=1, sticky='news', padx=3, pady=3)

        self.maintenance_btn = Button(self.inner_frame, bg='#091115', fg='white', bd=0, text='Planned\nMaintenance',
                                      command=lambda: self.change_status(2), activebackground='#798185', activeforeground='white')
        self.maintenance_btn.grid(row=1, column=0, sticky='news', padx=3, pady=3)

        self.break_down_btn = Button(self.inner_frame, bg='#091115', fg='white', bd=0, text='Breakdown',
                                     command=lambda: self.change_status(3), activebackground='#798185', activeforeground='white')
        self.break_down_btn.grid(row=0, column=1, sticky='news', padx=3, pady=3)

        self.buttons = [self.available_btn, self.not_available_btn, self.maintenance_btn, self.break_down_btn]

        for btn in self.buttons:
            btn.bind('<Enter>', on_enter)
            btn.bind('<Leave>', on_leave)

        self.redraw(self.status)

        # cells.append(Cell(name, status, row, column))

    def change_status(self, new_status, is_refresh=False):  # Changes status on button press or when retrieving data from DB
        db = sq.connect('equipment.db')
        db.execute(f'UPDATE "{self.type}" SET Status = {new_status} WHERE Tool = "{self.name}"')
        if not is_refresh:
            db.execute(f'INSERT INTO Log (Username, Role, Equipment, "Equipment type", "Old status", "New status", Date, Time) VALUES ("{user_name}",'
                       f' "{user_role}", "{self.name}", "{self.type}", "{self.status}", "{new_status}", "{datetime.now().strftime("%a, %d-%m-%Y")}",'
                       f' "{datetime.now().strftime("%I:%M:%S %p")}")')
        db.commit()
        db.close()

        if self.parent_cell is None:  # if parent cell is clicked
            if self.status == 3 and new_status != 3:
                self.redraw(new_status, True)
            else:
                self.redraw(new_status)

            self.status = new_status
        else:  # if breakdown_cell is clicked
            self.parent_cell.status = new_status
            self.parent_cell.redraw(new_status, True)

    def draw_breakdown_cell(self, i):
        column = i % column_num
        row = int(i / column_num)
        self.breakdown_cell.frame.grid(row=row, column=column, sticky='news', padx=5, pady=5)
        breakdown_tab.canvas.configure(scrollregion=breakdown_tab.canvas.bbox("all"))

    def redraw(self, new_status, from_breakdown=False):  # Updates cell based on status (does not determine status)
        self.title_lbl['bg'] = status_colors[new_status]
        self.status_lbl['bg'] = status_colors[new_status]
        self.status_lbl['text'] = status_words[new_status]

        if new_status == 4:
            self.title_lbl['fg'] = 'black'
            self.status_lbl['fg'] = 'black'
        else:
            self.title_lbl['fg'] = 'white'
            self.status_lbl['fg'] = 'white'

        if user_role == 'ENG':

            for btn in self.buttons:
                btn['state'] = 'normal'
            if self.parent_cell is None:
                for btn in self.breakdown_cell.buttons[:3]:
                    btn['state'] = 'normal'

            if new_status == 4:
                self.available_btn['state'] = 'disabled'
                self.title_lbl['fg'] = 'black'
                self.status_lbl['fg'] = 'black'

            self.available_btn['text'] = 'Ready'
            self.available_btn['command'] = lambda: self.change_status(4)
            self.breakdown_cell.available_btn['text'] = 'Ready'
            self.breakdown_cell.available_btn['command'] = lambda: self.change_status(4)

        elif user_role == 'OPS':
            self.available_btn['text'] = 'Available'
            self.available_btn['command'] = lambda: self.change_status(0)

            for btn in self.buttons:
                btn['state'] = 'disabled'

            if self.parent_cell is None:
                for btn in self.breakdown_cell.buttons:
                    btn['state'] = 'disabled'

            if new_status == 4:
                self.available_btn['state'] = 'normal'

        else:
            for btn in self.buttons:
                btn['state'] = 'disabled'

            if self.parent_cell is None:
                for btn in self.breakdown_cell.buttons:
                    btn['state'] = 'disabled'
        if new_status != 4:
            self.buttons[new_status]['state'] = 'disabled'

        if from_breakdown:  # Removing the cell from BDN tab and realigning every cell after it
            if self.parent_cell is None:
                # Determining if the cell is the breakdown cell itself or its parent
                removed_cell = self.breakdown_cell
            else:
                removed_cell = self

            removed_index = Cell.breakdown_cells.index(removed_cell)
            temp = Cell.breakdown_cells[removed_index:].copy()  # A list from starting from the cell to remove

            for cell in temp:  # Removing the cell and every cell after it
                cell.frame.grid_forget()
                Cell.breakdown_cells.remove(cell)

            temp.pop(0)  # Removing the cell from the list
            for cell in temp:  # Redrawing every cell except the one that has been removed
                cell.parent_cell.draw_breakdown_cell(len(Cell.breakdown_cells))
                Cell.breakdown_cells.append(cell)

            breakdown_tab.canvas.configure(scrollregion=breakdown_tab.canvas.bbox("all"))

        elif new_status == 3 and self.parent_cell is None and self.breakdown_cell not in Cell.breakdown_cells:
            # Adding a cell to BDN tab and ordering every cell
            temp = Cell.breakdown_cells.copy()
            temp.append(self.breakdown_cell)

            while Cell.breakdown_cells:  # Removing every cell and emptying the list
                Cell.breakdown_cells[0].frame.grid_forget()
                Cell.breakdown_cells.pop(0)

            Cell.breakdown_cells = sorted(temp, key=lambda x: x.name)

            for i, cell in enumerate(Cell.breakdown_cells):  # Redrawing every cell in order
                Cell.draw_breakdown_cell(cell.parent_cell, i)


class Tab:
    def __init__(self, name):
        self.name = name
        self.main_frame = Frame(master=None, bg=bg_colour)

        self.canvas = Canvas(self.main_frame, bg=bg_colour)
        self.canvas.pack(side='left', fill='both', expand=1)

        self.scroll_bar = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.canvas.yview)
        self.scroll_bar.pack(side='right', fill='y')

        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.equipment_frame = Frame(master=self.main_frame, bg=bg_colour)
        self.canvas.create_window((0, 0), window=self.equipment_frame, anchor='nw',
                                  width=self.canvas.winfo_screenwidth() - 23)

        self.equipment_frame.columnconfigure(list(range(column_num)), weight=1, uniform=1)

        if self.name != 'Currently in BDN':
            self.equipment_dict = self.get_equipment()
            self.cell_dict = self.create_cells()

    def get_equipment(self):  # Makes a dict of each tab's equipment and their statuses
        db = sq.connect('equipment.db')
        cr = db.cursor()

        cr.execute(f'SELECT Tool, Status FROM "{self.name}"')
        equipment_data = cr.fetchall()
        equipment_dict = {}
        for item in equipment_data:
            equipment_dict[item[0]] = item[1]

        db.close()
        return equipment_dict

    def create_cells(self):
        cell_dict = {}
        for i in range(len(self.equipment_dict)):
            column = i % column_num
            row = int(i / column_num)

            cell_dict[list(self.equipment_dict.keys())[i]] = Cell(list(self.equipment_dict.keys())[i],
                                                                  list(self.equipment_dict.values())[i],
                                                                  row, column,
                                                                  self.name, self.equipment_frame)

        return cell_dict


breakdown_tab = Tab('Currently in BDN')
tab_dict = create_tab_dict()

for tab in tab_dict:
    notebook.add(tab_dict[tab].main_frame, text=tab)
notebook.add(breakdown_tab.main_frame, text=breakdown_tab.name)


def log_in_gui():
    log_in_btn['command'] = ''
    login_top = Toplevel(bg='#03050f')
    login_top.geometry('350x300')
    login_top.title('Login')
    login_top['bg'] = '#03050f'

    Label(login_top, text='Login', font=('Segoe UI', 30, 'bold'), bg='#03050f', fg='white').pack(pady=25)

    login_frm = Frame(login_top, bg='#03050f')
    login_frm.pack(pady=20)

    Label(login_frm, text='Username:', bg='#03050f', fg='white').grid(row=0, column=0)
    username_ent = Entry(login_frm, bg='#33353f', fg='white', relief='flat')
    username_ent.grid(row=0, column=1)

    Label(login_frm, text='Password:', bg='#03050f', fg='white').grid(row=1, column=0)
    password_ent = Entry(login_frm, width=20, show='•', bg='#33353f', fg='white', relief='flat')
    password_ent.grid(row=1, column=1)

    wrong_lbl = Label(login_top, fg='red', bg='#03050f')
    wrong_lbl.pack(pady=20)

    login_btn = Button(login_top, bg='#03050f', fg='white', text='Login', relief='flat',
                       activebackground='#798185', activeforeground='white')
    login_btn.pack()
    login_btn.bind('<Enter>', lambda x: login_btn.config(bg='#394145'))
    login_btn.bind('<Leave>', lambda x: login_btn.config(bg='#03050f'))

    def log_in():
        db = sq.connect('equipment.db')
        cr = db.cursor()
        username = username_ent.get()
        global user_role
        global user_name

        cr.execute(f"SELECT Username, Role, Password FROM Accounts WHERE Username LIKE'{username}' ")
        account = cr.fetchone()
        if account is None:
            wrong_lbl['text'] = 'Incorrect username'
            db.close()
            return

        if password_ent.get() == account[2]:
            user_role = account[1]
            user_name = account[0]
            refresh_func()
            login_top.destroy()
        else:
            wrong_lbl['text'] = 'Incorrect password'

        db.commit()
        log_in_btn['command'] = log_in_gui

    login_btn['command'] = log_in
    login_top.bind('<Escape>', lambda x: login_top.destroy())
    login_top.bind('<Return>', lambda x: log_in())
    login_top.bind('<Destroy>', lambda x: log_in_btn.configure(command=log_in_gui))


def create_user():
    create_user_btn['command'] = ''
    user_top = Toplevel(bg='#03050f')
    user_top.geometry('350x300')
    user_top.title('Login')

    Label(user_top, text='Create User', font=('Segoe UI', 30, 'bold'), bg='#03050f', fg='white').pack(pady=15)

    user_frame = Frame(user_top, bg='#03050f')
    user_frame.pack()

    Label(user_frame, bg='#03050f', fg='white', text='Username:').grid(row=0, column=0)

    username_ent = Entry(user_frame, bg='#33353f', fg='white', relief='flat')
    username_ent.grid(row=0, column=1, padx=3, pady=(5, 0))

    Label(user_frame, bg='#03050f', fg='white', text='Password:').grid(row=1, column=0, padx=3, pady=(5, 0))

    password_ent = Entry(user_frame, bg='#33353f', fg='white', relief='flat', show='•')
    password_ent.grid(row=1, column=1, padx=3, pady=(5, 0))

    Label(user_frame, bg='#03050f', fg='white', text='Confirm password:').grid(row=2, column=0, padx=3, pady=(5, 0))

    password_check_ent = Entry(user_frame, bg='#33353f', fg='white', relief='flat', show='•')
    password_check_ent.grid(row=2, column=1, padx=3, pady=(5, 0))

    Label(user_frame, bg='#03050f', fg='white', text='Role:').grid(row=3, column=0, padx=3, pady=(7, 0))

    role_menu_var = StringVar()
    role_menu = ttk.OptionMenu(user_frame, role_menu_var, 'Select a Role', 'OPS', 'ENG')
    role_menu.grid(row=3, column=1, pady=(7, 0),)

    create_btn = Button(user_top, text='Create', bg='#03050f', fg='white', activebackground='#798185', activeforeground='white',
                        relief='flat')
    create_btn.pack(pady=(20, 0))
    create_btn.bind('<Enter>', lambda x: create_btn.config(bg='#394145'))
    create_btn.bind('<Leave>', lambda x: create_btn.config(bg='#03050f'))

    wrong_lbl = Label(user_top, bg='#03050f', fg='red')
    wrong_lbl.pack(pady=10)

    def create_func(_=None):
        global user_role
        global user_name

        db = sq.connect('equipment.db')
        cr = db.cursor()

        role = role_menu_var.get()
        username = username_ent.get()
        password = password_ent.get()
        password_check = password_check_ent.get()

        if username == '':
            wrong_lbl['text'] = 'Enter a username'

        else:

            cr.execute('SELECT Username FROM Accounts')
            accounts = cr.fetchall()
            usernames = list(map(lambda x: x[0], accounts))

            if username in usernames:
                wrong_lbl['text'] = 'User already exists'

            else:

                if password == '':
                    wrong_lbl['text'] = 'Enter a password'

                else:
                    if password == password_check:

                        if role == 'Select a Role':
                            wrong_lbl['text'] = 'Select a Role'
                        elif role == 'OPS':
                            db.execute(f'INSERT INTO Accounts (Username, Role, Password) VALUES ("{username}", "{role}", "{password}")')
                            wrong_lbl['text'] = ''
                            user_top.destroy()
                        else:
                            db.execute(f'INSERT INTO Accounts (Username, Role, Password) VALUES ("{username}", "{role}", "{password}")')
                            wrong_lbl['text'] = ''
                            user_top.destroy()
                    else:
                        wrong_lbl['text'] = 'Passwords don\'t match'
        db.commit()
        create_user_btn['command'] = create_user
        user_role = role
        user_name = username
        refresh_func()

    create_btn['command'] = create_func
    user_top.bind('<Escape>', user_top.destroy)
    user_top.bind('<Return>', create_func)
    user_top.bind('<Destroy>', lambda x: create_user_btn.configure(command=create_user))


def excel():
    workbook = Workbook(filedialog.asksaveasfilename(filetypes=[('Excel Workbook', '*.xlsx')],
                                                     defaultextension='.xlsx',
                                                     initialfile='Breakdown Log.xlsx',
                                                     title='Export'))

    worksheet = workbook.add_worksheet()

    red_format = workbook.add_format({'bg_color': 'red', 'font_color': 'white'})
    yellow_format = workbook.add_format({'bg_color': '#ffff00', 'font_color': 'black'})
    orange_format = workbook.add_format({'bg_color': '#ff8c00', 'font_color': 'white'})
    green_format = workbook.add_format({'bg_color': 'green', 'font_color': 'white'})
    blue_format = workbook.add_format({'bg_color': 'blue', 'font_color': 'white'})
    title_format = workbook.add_format({'bg_color': '#000066', 'font_color': 'white', 'bold': 1})

    db = sq.connect('equipment.db')
    cr = db.cursor()
    select = cr.execute("SELECT * FROM Log")
    row_num = 1

    for i, type in enumerate(
            ['Username', 'Role', 'Equipment Name', 'Equipment Type', 'Previous Status', 'Current Status', 'Date', 'Time']):
        worksheet.conditional_format('A1:H1', {'type': 'cell',
                                               'criteria': 'equal to',
                                               'value': f'"{type}"',
                                               'format': title_format})
        worksheet.write(0, i, type)

    select = list(select)
    select.reverse()

    select = list(map(lambda x: list(x), select))
    for i in range(len(select)):
        select[i][4] = status_words[select[i][4]]
        select[i][5] = status_words[select[i][5]]

    for i, row in enumerate(select):
        row_num += 1
        for j, value in enumerate(row):
            worksheet.write(i + 1, j, value)

    worksheet.conditional_format(f'E1:F{row_num}', {'type': 'cell',
                                                    'criteria': 'equal to',
                                                    'value': '"Breakdown"',
                                                    'format': red_format})
    worksheet.conditional_format(f'E1:F{row_num}', {'type': 'cell',
                                                    'criteria': 'equal to',
                                                    'value': '"Available"',
                                                    'format': green_format})
    worksheet.conditional_format(f'E1:F{row_num}', {'type': 'cell',
                                                    'criteria': 'equal to',
                                                    'value': '"Planned Maintenance"',
                                                    'format': blue_format})

    worksheet.conditional_format(f'E1:F{row_num}', {'type': 'cell',
                                                    'criteria': 'equal to',
                                                    'value': '"Out of Service"',

                                                    'format': orange_format})
    worksheet.conditional_format(f'E1:F{row_num}', {'type': 'cell',
                                                    'criteria': 'equal to',
                                                    'value': '"Ready"',
                                                    'format': yellow_format})
    worksheet.set_column(0, 7, 20)

    db.close()
    try:
        workbook.close()
    except FileCreateError:
        pass


def log():
    log_btn['command'] = ''
    log_top = Toplevel()
    log_top['bg'] = '#03050f'
    log_top.title('Breakdown System Log')
    log_top.state('zoomed')
    win_width = root.winfo_width()

    excel_icon = PhotoImage(file='assets/excel.png')
    excel_btn = Button(log_top, font=font, padx=10, text='Export to Excel file', relief='flat', image=excel_icon,
                       bg='#03050f', fg='white', activebackground='#798185', activeforeground='white', compound='left', command=excel)
    excel_btn.image = excel_icon
    excel_btn.pack(anchor='e', padx=60, pady=(15, 15))
    excel_btn.bind('<Enter>', lambda x: excel_btn.config(bg='#394145'))
    excel_btn.bind('<Leave>', lambda x: excel_btn.config(bg='#03050f'))

    sheet = Sheet(log_top, column_width=win_width / 8.5,
                  headers=['Username', 'Role', 'Equipment', "Equipment type", "Old status", "New status", 'Date', 'Time'], theme='dark green')
    sheet.pack(fill='both', expand=1)
    sheet.enable_bindings(("single_select", "row_select", "column_select", "column_width_resize", "arrowkeys", "right_click_popup_menu",
                           "rc_select", "copy"))

    db = sq.connect('equipment.db')
    cr = db.cursor()
    cr.execute('SELECT * FROM Log')
    data = cr.fetchall()
    data.reverse()

    data = list(map(lambda x: list(x), data))
    for i in range(len(data)):
        data[i][4] = status_words[data[i][4]]
        data[i][5] = status_words[data[i][5]]

    sheet.set_sheet_data(data)
    db.close()

    log_top.bind('<Destroy>', lambda x: log_btn.configure(command=log))


def refresh_func():
    db = sq.connect('equipment.db')
    cr = db.cursor()
    for t in tab_dict:
        cr.execute(f'SELECT Tool, Status FROM "{t}"')
        data = cr.fetchall()
        data_dict = {}
        for i in data:
            data_dict[i[0]] = i[1]

        for cell in tab_dict[t].cell_dict.values():
            new_status = data_dict[cell.name]
            cell.change_status(new_status, True)

    last_refresh['text'] = f'Last refresh: {datetime.now().strftime("%I:%M:%S %p")}'
    db.close()


def refresh():
    while True:
        time.sleep(10)
        refresh_func()


last_refresh['command'] = refresh_func
log_in_btn['command'] = log_in_gui
create_user_btn['command'] = create_user
log_btn['command'] = log
th = threading.Thread(target=refresh, daemon=True)
th.start()

root.mainloop()
