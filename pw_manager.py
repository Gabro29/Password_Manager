from pandas import read_csv, read_excel, set_option, DataFrame, Series, concat, to_datetime
from numpy import array, vstack, nan
from cryptpandas import to_encrypted, read_encrypted
from tkinter import Label, CENTER, Frame, Entry, TclError, END, Toplevel, Tk, Menu, Button, \
    LabelFrame, Scrollbar, ttk, messagebox, NW, NO, W, E, ttk
from tkinter.ttk import Combobox
from tkinter import font as tkfont
from ttkthemes import ThemedStyle
from PIL import ImageTk, Image
import os
from threading import Thread



all_pass = read_encrypted(path='password.crypt', password='GMZhnaOm1IdUyTvQgR1zmJReT_qmd-HUTavi8LI6u9o=')
all_pass = all_pass[["Username", "Site", "Password"]]
count_color_a = int()
hidden = str()
KEY = 'GMZhnaOm1IdUyTvQgR1zmJReT_qmd-HUTavi8LI6u9o='
main_style = "clearlooks"
my_password = list()
starting = True


class SecondWindow(Toplevel):
    """Class to open different window at the same time"""

    def __init__(self, parent, title, geometry, propagate, b):
        super().__init__(parent)
        self.title(title)
        self.geometry(geometry)
        self.propagate(propagate)
        self.resizable(0, 0)
        self.iconbitmap("icon.ico")



def generate_key():
    from cryptography.fernet import Fernet
    return Fernet.generate_key()


def ask_for_pw(self, controller):
    def check_pw(pw_window, controller):
        all_pass = read_encrypted(path='password.crypt', password=KEY)
        df = all_pass[all_pass["Site"] == "PERSONAL"]
        if df[df["Username"] == user_entry.get()].size > 0:
            if pw_entry.get() == df[df["Username"] == user_entry.get()]["Password"].values[0]:
                my_password.clear()
                pw_window.destroy()
                controller.show_frame("Secret")
            else:
                pw_window.destroy()
                messagebox.showerror("Attenzione", "Password Errata!")
                my_password.clear()
        else:
            pw_window.destroy()
            messagebox.showerror("Attenzione", "Password Errata!")
            my_password.clear()

    global main_style
    pw_window = SecondWindow(self, "Log In", "200x150", False, (0, 0))
    style = ThemedStyle(pw_window)
    style.theme_use(f"{main_style}")

    account_image = Image.open("AccountT.png")
    raff_account_image = ImageTk.PhotoImage(account_image)
    label_raff_account_image = Label(pw_window, image=raff_account_image)
    label_raff_account_image.image = raff_account_image
    label_raff_account_image.place(relx=0.03, rely=0.17, height=40, width=40)

    all_pass = read_encrypted(path='password.crypt', password=KEY)
    combo_values = list()
    for val in all_pass[all_pass["Site"] == "PERSONAL"]["Username"].values:
        combo_values.append(val)
    user_entry = Combobox(pw_window, values=combo_values, font=("Helvetica", 10), foreground="black")
    user_entry.place(relx=0.22, rely=0.22, width=120, height=20)
    user_entry.current(0)

    key_image = Image.open("key.PNG")
    raff_key_image = ImageTk.PhotoImage(key_image)
    label_raff_key_image = Label(pw_window, image=raff_key_image)
    label_raff_key_image.image = raff_key_image
    label_raff_key_image.place(relx=0.03, rely=0.37, height=30, width=30)

    pw_entry = Entry(pw_window, font=("Lucinda Console", 15), show="*")
    pw_entry.place(relx=0.22, rely=0.4, width=120, height=20)
    pw_entry.bind("<Return>", lambda x: check_pw(pw_window, controller))
    pw_entry.focus()

    enter_button = Button(pw_window, text="Entra", command=lambda: check_pw(pw_window, controller),
                          fg="black", bg="Silver", relief="raised",
                          activebackground="sandy brown", font=("Spectral", 15))

    enter_button.place(relx=0.35, rely=0.6, height=30)


class PW(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Password Manager")
        self.geometry(f"{700}x{670}+{100}+{70}")
        self.propagate(True)
        self.resizable(1, 1)
        self.iconbitmap("icon.ico")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.task(container)

    def task(self, container):
        global starting

        for Finestra in (Secret, MenuP):
            page_name = Finestra.__name__
            frame = Finestra(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("MenuP")
        starting = False

    def show_frame(self, page_name):
        if page_name == "MenuP":
            self.geometry("700x200")
        else:
            self.geometry("800x670")

        frame = self.frames[page_name]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")



class MenuP(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.style = ThemedStyle(self)
        self.style.theme_use(f"{main_style}")
        self.controller = controller
        self.menu_selection = LabelFrame(self, text="Encrypted Area", font=("Times", 15), foreground="black")
        self.menu_selection.place(height=180, width=650, relx=0.03, rely=0.03)

        pw_button = Button(self.menu_selection, text="LOG IN", bg="silver",
                           relief="raised",
                           font=("Spectral", 15), command=lambda: ask_for_pw(self, controller),
                           activebackground="sandy brown")
        pw_button.place(height=30, width=500, relx=0.1, rely=0.3)



class Secret(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.style = ThemedStyle(self)
        self.style.theme_use(f'{main_style}')
        self.removed_index = list()
        self.controller = controller
        label = Label(self, text="Password Manager", font=("Spectral", 15), foreground="black", relief="ridge")
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Back to Main Menu", command=lambda: self.back_to_menu(controller),
                        fg="black", bg="sandy brown", relief="raised",
                        activebackground="light gray", font=("Lucinda Console", 10))
        button.pack()
        self.container = LabelFrame(self)
        self.container.place(height=308, width=720, relx=0.05, rely=0.13)
        self.pw_tabs = ttk.Notebook(self.container)
        self.add_account = Frame(self.pw_tabs, width=740, height=308)  # , bg="#d9ead3")
        self.manage_account = Frame(self.pw_tabs, width=740, height=308)  # , bg="#d9ead3")
        self.pw_tabs.add(self.add_account, text="ADD")
        self.pw_tabs.add(self.manage_account, text="MANAGE")
        self.pw_tabs.place(relx=0, rely=0)
        self.pw_tabs.bind("<<NotebookTabChanged>>", lambda x: self.change_tab_option(x))

        self.tree_add()
        self.tree_manage()
        self.user_entry = Entry(self, font=("Lucinda Console", 15))
        self.user_entry.place(relx=0.05, rely=0.6, width=160, height=30)

        self.site_entry = Entry(self, font=("Lucinda Console", 15))
        self.site_entry.place(relx=0.28, rely=0.6, width=250, height=30)

        self.password_entry = Entry(self, font=("Lucinda Console", 15))
        self.password_entry.place(relx=0.62, rely=0.6, width=180, height=30)
        self.password_entry.bind("<Return>", self.add_the_account)

        self.add_button = Button(self, text="Add", command=lambda: Thread(target=self.add_the_account).start(),
                                 fg="black", bg="Silver", relief="raised",
                                 activebackground="light gray", font=("Times", 15))
        self.add_button.place(relx=0.85, rely=0.6, width=110, height=30)

        self.clear_button = Button(self, text="Clear", command=self.clear_boxes,
                                   fg="black", bg="light gray", relief="raised",
                                   activebackground="#d9ead3", font=("Times", 15))
        self.clear_button.place(relx=0.5, rely=0.7, width=110, height=30)

        self.remove_button = Button(self, text="Remove", command=self.remove_person,
                                    fg="black", bg="sandy brown", relief="raised",
                                    activebackground="light gray", font=("Times", 15))
        self.remove_button.place(relx=0.68, rely=0.7, width=110, height=30)

        self.edit_button = Button(self, text="Edit", command=self.edit_person,
                                  fg="black", bg="wheat1", relief="raised",
                                  activebackground="light gray", font=("Times", 15))
        self.edit_button.place(relx=0.85, rely=0.7, width=110, height=30)

        self.save_button = Button(self, text="Save", command=self.save_to_csv, fg="black", bg="#8fce00",
                                  relief="raised", activebackground="light gray", font=("Times", 15))
        self.save_button.place(relx=0.3, rely=0.7, width=110, height=30)

        self.bind("<<ShowFrame>>", self.on_show_frame)

    def on_show_frame(self, parametro_fittizio):
        if not starting:
            self.change_tab_option(parametro_fittizio)

    def change_tab_option(self, color):
        self.delete_entries()
        if self.pw_tabs.index("current") == 0:
            self.user_entry.focus()
            self.style_tab = ttk.Style()
            self.style_tab.map('TNotebook.Tab', background=[('selected', 'light blue'), ('active', 'gray')])
            try:
                self.hide_button.destroy()
            except AttributeError:
                pass
            self.add_button = Button(self, text="Add", command=lambda: Thread(target=self.add_the_account).start(),
                                     fg="black", bg="Silver", relief="raised",
                                     activebackground="light gray", font=("Times", 15))
            self.add_button.place(relx=0.85, rely=0.6, width=110, height=30)
            self.hide_button = Frame(self, width=160, height=30)  # , bg="#d9ead3")
            self.hide_button.place(relx=0.05, rely=0.08)
        elif self.pw_tabs.index("current") == 1:
            self.style_tab = ttk.Style()
            self.style_tab.map('TNotebook.Tab', background=[('selected', 'orange'), ('active', 'gray')])
            self.hide_button = Frame(self, width=200, height=30)  # , bg="#d9ead3")
            self.hide_button.place(relx=0.85, rely=0.6)
            self.search_entry = Entry(self, font=("Lucinda Console", 15))
            self.search_entry.place(relx=0.05, rely=0.08, width=160, height=30)
            self.search_entry.bind("<KeyRelease>", self.look_for)
            self.search_entry.focus()
            self.show_all_accounts()

    def back_to_menu(self, controller):
        global count_color_a
        count_color_a = 0
        self.delete_entries()
        controller.show_frame("MenuP")

    def delete_entries(self):
        try:
            for row in self.add_tree.get_children():
                self.add_tree.delete(row)
        except TclError:
            pass
        try:
            for row in self.manage_tree.get_children():
                self.manage_tree.delete(row)
        except TclError:
            pass

    def add_the_account(self, parametro_fittizio=0):
        """Add Account"""
        global all_pass
        global count_color_a

        if parametro_fittizio == "MANAGE":
            for contatore, row in enumerate(all_pass.iterrows()):
                if self.search_entry.get().lower() in str(row[1].Site).lower():
                    self.manage_tree.insert(parent="", index="end", iid=contatore, text="",
                                                values=(row[1].Username, row[1].Site, row[1].Password),
                                                tags=("evenrow",))
        else:
            # ADD Tab
            if self.user_entry.get() != "" and self.password_entry.get() != "":
                if self.pw_tabs.index("current") == 0:
                    if count_color_a % 2 == 0:
                        self.add_tree.insert(parent="", index="end", iid=count_color_a, text="",
                                             values=(self.user_entry.get(), self.site_entry.get(), self.password_entry.get()),
                                             tags=("evenrow",))
                    else:
                        self.add_tree.insert(parent="", index="end", iid=count_color_a, text="",
                                             values=(self.user_entry.get(), self.site_entry.get(), self.password_entry.get()),
                                             tags=("oddrow",))
                count_color_a += 1
                self.clear_boxes()
                self.user_entry.focus()
            elif self.user_entry.get() == "":
                messagebox.showerror("Attention", "Do not leave blank the Username's field!")
            elif self.password_entry.get() == "":
                messagebox.showerror("Attention", "Do not leave blank the Password's field!")

    def clear_boxes(self):
        self.user_entry.delete(0, END)
        self.site_entry.delete(0, END)
        self.password_entry.delete(0, END)

    def remove_person(self):
        global count_color_a
        if self.pw_tabs.index("current") == 0:
            try:
                selected_tme = self.add_tree.selection()
                if int(str(selected_tme).split("(")[1][1]) < count_color_a:
                    pass
                else:
                    count_color_a -= 1
                self.add_tree.delete(selected_tme)
            except (TclError, IndexError):
                pass
        elif self.pw_tabs.index("current") == 1:
            selected_tme = self.manage_tree.selection()
            self.manage_tree.delete(selected_tme)
            self.removed_index.append(selected_tme[0])

    def edit_person(self):
        if self.pw_tabs.index("current") == 0:
            if self.user_entry.get() != "" and self.password_entry.get() != "":
                selected = self.add_tree.focus()
                self.add_tree.item(selected, text="", values=(
                    self.user_entry.get(), self.site_entry.get(), self.password_entry.get()))
                self.clear_boxes()
            elif self.user_entry.get() == "":
                messagebox.showerror("Attention", "Do not leave blank the Username's field!")
            elif self.password_entry.get() == "":
                messagebox.showerror("Attention", "Do not leave blank the Password's field!")
        elif self.pw_tabs.index("current") == 1:
            if self.user_entry.get() != "" and self.password_entry.get() != "":
                selected = self.manage_tree.focus()
                self.manage_tree.item(selected, text="", values=(
                    self.user_entry.get(), self.site_entry.get(), self.password_entry.get()))
                self.clear_boxes()
            elif self.user_entry.get() == "":
                messagebox.showerror("Attention", "Do not leave blank the Username's field!")
            elif self.password_entry.get() == "":
                messagebox.showerror("Attention", "Do not leave blank the Password's field!")

    def tree_add(self):
        tree_style = ttk.Style()
        tree_style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Lucinda Console', 16))
        tree_style.configure("mystyle.Treeview.Heading", font=('Spectral', 18, 'italic'), width=1, pady=20)
        tree_style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
        tree_style.configure('Treeview', rowheight=40)
        self.add_tree = ttk.Treeview(self.add_account, style="mystyle.Treeview", selectmode="extended")
        self.add_tree["columns"] = ("Username", "Site", "Password")
        self.add_tree.column("#0", width=0, stretch=NO)
        self.add_tree.column("Username", anchor=W, width=210, stretch=NO)
        self.add_tree.column("Site", anchor=CENTER, width=265, stretch=NO)
        self.add_tree.column("Password", anchor=E, width=200, stretch=NO)
        self.add_tree.heading("#0", text="", anchor=CENTER)
        self.add_tree.heading("Username", text="Username", anchor=W)
        self.add_tree.heading("Site", text="Site", anchor=CENTER)
        self.add_tree.heading("Password", text="Password", anchor=E)
        self.add_tree.tag_configure("oddrow", background="white")
        self.add_tree.tag_configure("evenrow", background="gray")
        # Scrollbar
        add_tree_scrolly = Scrollbar(self.container, orient="vertical", command=self.add_tree.yview)
        self.add_tree.configure(yscrollcommand=add_tree_scrolly.set)
        add_tree_scrolly.pack(side="right", fill="y")
        self.add_tree.bind("<<TreeviewSelect>>", self.display_edit_person)
        self.add_tree.place(width=690, height=300, relx=0, rely=0)

    def tree_manage(self):
        tree_style = ttk.Style()
        tree_style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Lucinda Console', 16))
        tree_style.configure("mystyle.Treeview.Heading", font=('Spectral', 18, 'italic'), width=1, pady=20)
        tree_style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
        tree_style.configure('Treeview', rowheight=40)
        self.manage_tree = ttk.Treeview(self.manage_account, style="mystyle.Treeview", selectmode="extended")
        self.manage_tree["columns"] = ("Username", "Site", "Password")
        self.manage_tree.column("#0", width=0, stretch=NO)
        self.manage_tree.column("Username", anchor=W, width=210, stretch=NO)
        self.manage_tree.column("Site", anchor=CENTER, width=265, stretch=NO)
        self.manage_tree.column("Password", anchor=E, width=200, stretch=NO)
        self.manage_tree.heading("#0", text="", anchor=CENTER)
        self.manage_tree.heading("Username", text="Username", anchor=W)
        self.manage_tree.heading("Site", text="Site", anchor=CENTER)
        self.manage_tree.heading("Password", text="Password", anchor=E)
        self.manage_tree.tag_configure("oddrow", background="white")
        self.manage_tree.tag_configure("evenrow", background="gray")
        # Scrollbar
        manage_tree_scrolly = Scrollbar(self.container, orient="vertical", command=self.manage_tree.yview)
        self.manage_tree.configure(yscrollcommand=manage_tree_scrolly.set)
        manage_tree_scrolly.pack(side="right", fill="y")
        self.manage_tree.bind("<<TreeviewSelect>>", self.display_edit_person)
        self.manage_tree.place(width=690, height=300, relx=0, rely=0)

    def display_edit_person(self, parametro_fittizio):
        self.clear_boxes()
        if self.pw_tabs.index("current") == 0:
            selected = self.add_tree.focus()
            selected_row = self.add_tree.item(selected, "values")
            self.user_entry.insert(0, selected_row[0])
            self.site_entry.insert(0, selected_row[1])
            self.password_entry.insert(0, selected_row[2])
        elif self.pw_tabs.index("current") == 1:
            selected = self.manage_tree.focus()
            selected_row = self.manage_tree.item(selected, "values")
            self.user_entry.insert(0, selected_row[0])
            self.site_entry.insert(0, selected_row[1])
            self.password_entry.insert(0, selected_row[2])

    def show_all_accounts(self):
        global all_pass
        all_pass = read_encrypted(path='password.crypt', password=KEY)
        all_pass = all_pass[["Username", "Site", "Password"]]
        self.add_the_account(parametro_fittizio="MANAGE")

    def look_for(self, parametro_fittizio):
        global all_pass
        self.delete_entries()
        if self.search_entry.get() == '':
            self.show_all_accounts()
        else:
            # Aggiorno i suggerimenti
            self.add_the_account(parametro_fittizio="MANAGE")

    def save_to_csv(self):
        global all_pass
        data_on_the_tree = array([nan, nan, nan])
        all_pass = read_encrypted(path='password.crypt', password=KEY)
        all_pass = all_pass[["Username", "Site", "Password"]]
        if self.pw_tabs.index("current") == 0:
            for index, item in enumerate(self.add_tree.get_children()):
                data_on_the_tree = vstack([data_on_the_tree, [self.add_tree.item(item)["values"][0],
                                                              self.add_tree.item(item)["values"][1],
                                                              self.add_tree.item(item)["values"][2]]])
            tree_data_frame_0 = DataFrame(data_on_the_tree)
            tree_data_frame_0.columns = ["Username", "Site", "Password"]
            tree_data_frame_0.drop(index=0, inplace=True)
            tree_data_frame_0.reset_index(inplace=True, drop=True)
            all_pass = concat([all_pass, tree_data_frame_0])
            to_encrypted(all_pass.reset_index(), password=KEY, path="password.crypt")
            self.delete_entries()
            messagebox.showinfo("Saving Adds", "Saving Process Done!")

        elif self.pw_tabs.index("current") == 1:
            data_on_the_tree = array([nan, nan, nan])
            edit_tree_counter = 0
            for index, item in enumerate(self.manage_tree.get_children()):
                data_on_the_tree = vstack([data_on_the_tree, [self.manage_tree.item(item)["values"][0],
                                                              self.manage_tree.item(item)["values"][1],
                                                              self.manage_tree.item(item)["values"][2]]])
            tree_data_frame = DataFrame(data_on_the_tree)
            tree_data_frame.columns = ["Username", "Site", "Password"]
            tree_data_frame.drop(index=0, inplace=True)
            tree_data_frame.reset_index(inplace=True, drop=True)

            for the_index, row in enumerate(all_pass.iterrows()):
                # Remove rows
                if f"{the_index}" in self.removed_index:
                    all_pass.drop(the_index, inplace=True)
                # Edit rows
                elif self.search_entry.get().lower() in str(row[1].Site).lower():
                    all_pass.loc[the_index, "Username"] = tree_data_frame["Username"][edit_tree_counter]
                    descrizione = tree_data_frame["Site"][edit_tree_counter]
                    if descrizione is None:
                        descrizione = ""
                    all_pass.loc[the_index, "Site"] = descrizione
                    all_pass.loc[the_index, "Password"] = tree_data_frame["Password"][edit_tree_counter]
                    edit_tree_counter += 1

            all_pass.reset_index().to_csv("PasswordEdit.csv", index=False)
            all_pass = read_csv("PasswordEdit.csv", engine="c")
            os.remove("PasswordEdit.csv")
            to_encrypted(all_pass, password=KEY, path="password.crypt")
            self.delete_entries()
            self.removed_index.clear()
            self.search_entry.delete(0, END)
            messagebox.showinfo("Saving Edits", "Saving Process Done!")
            self.show_all_accounts()



if __name__ == "__main__":
    PW().mainloop()
