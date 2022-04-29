import pandas as pd
from tkinter import *
from tkinter import ttk, filedialog

# wczytanie pliku
def file_open():
    filename = filedialog.askopenfilename(
        initialdir="C:\\Users\\macie\\Desktop\\",
        title="Open a file",
        # filetypes=("Obsługiwane pliki", formaty)
        filetypes=(("obsługiwane pliki", "*.xlsx *.csv *.txt"),
                   ("all files",
                    "*.*"))
    )
    global df
    global err_mess
    if filename:
        try:
            filename = r"{}".format(filename)
            if filename.endswith(".txt"):
                df = pd.read_csv(filename, delimiter="\t")
            elif filename.endswith(".csv"):
                df = pd.read_csv(filename)
            elif filename.endswith(".xlsx"):
                df = pd.read_excel(filename)
        except ValueError:
            err_mess = "Nie można otworzyć pliku!"

    print_data()


# menu
def menu():
    my_menu = Menu(window)
    window.config(menu=my_menu)
    file_menu = Menu(my_menu, tearoff=False)  # tearoff kropki przy menu
    my_menu.add_cascade(label="Wybierz plik", menu=file_menu)
    file_menu.add_command(label="Otwórz", command=file_open)
    global err_mess
    my_label = Label(window, text=err_mess)
    my_label.pack(pady=20)


def clear_tree():
    my_tree.delete(*my_tree.get_children())


# wyświetlanie całej tabeli
def print_data():
    global df
    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    clear_tree()
    restart_button.pack_forget()
    if not isinstance(df, int):
        my_tree["column"] = list(df.columns)
        my_tree["show"] = "headings"
        for column in my_tree["column"]:
            my_tree.heading(column, text=column)

        # dodanie danych do treeview
        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            my_tree.insert("", "end", values=row)
        my_tree.pack()
        text_row.config(text="Ilość rzędów - " + str(df.shape[0]))
        choose_button.pack()


def print_selected_data(columns, top_window):
    top_window.destroy()
    final_columns = []
    for i in range(1, len(columns), 2):
        if columns[i].get() == 1:
            final_columns.append(columns[i-1])
    global df
    clear_tree()

    im = df[final_columns]
    my_tree["column"] = final_columns
    my_tree["show"] = "headings"
    for column in my_tree["column"]:
        my_tree.heading(column, text=column)

    # dodanie danych do treeview
    df_rows = im.to_numpy().tolist()
    for row in df_rows:
        my_tree.insert("", "end", values=row)
    my_tree.pack()
    restart_button.pack(pady=5)


# nowe okno do wyboru danych
def choose_data():
    global df

    top_window = Toplevel(window)
    top_window.title("Zazacz dane")
    # pozycja okna
    app_y_center_poz = window.winfo_screenwidth() // 2 - top_window.winfo_reqwidth() // 2
    app_x_center_poz = window.winfo_screenheight() // 2 - top_window.winfo_reqheight() // 2
    top_window.geometry(f"+{app_y_center_poz}+{app_x_center_poz}")

    columns = list(df.columns)
    for i in range(1, 2 * len(columns), 2):
        columns.insert(i, 0)
    for i in range(0, len(columns), 2):
        columns[i+1] = IntVar()
        l = Checkbutton(top_window, text=columns[i], variable=columns[i+1])
        l.pack()
    przycisk = Button(top_window,text="Zatwierdź",command= lambda: print_selected_data(columns, top_window) )
    przycisk.pack()


window = Tk()
window.title("Analizator")
app_width = 900
app_height = 600

#rozmiar i pozycja okna
app_y_center_poz = window.winfo_screenwidth() // 2 - app_width // 2
app_x_center_poz = window.winfo_screenheight() // 2 - app_height // 2
window.geometry(f"{app_width}x{app_height}+{app_y_center_poz}+{app_x_center_poz}")

# okno dla danych
frame = Frame(window)
frame.pack(pady=20)

#ilosć rzędów
text_row = Label(window, text="",font=("",12))
text_row.pack()

#treeview scrollbar
scrolly = Scrollbar(frame, orient="vertical")
scrollx = Scrollbar(frame, orient="horizontal")

# treeview
my_tree = ttk.Treeview(frame, yscrollcommand=scrolly.set, xscrollcommand=scrollx.set, selectmode="extended")
scrolly.config(command=my_tree.yview)
scrollx.config(command=my_tree.xview)

#globalna Data Frame
df = 0

err_mess = ""

menu()

# przyciski
choose_button = Button(window, text="Zaznacz dane", command=choose_data)

restart_button = Button(window, text="Wyświetl wszystkie dane", command=print_data)

#kolory taeli
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="silver")
style.map("Treeview", background=[("selected", "green")])

window.mainloop()