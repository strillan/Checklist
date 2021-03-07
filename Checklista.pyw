from pickle import Unpickler
from pickle import Pickler
from itertools import groupby
from operator import itemgetter

import tkinter 
from date_from_text import DateFromText
from tkinter import ttk


## TODO Större INFO-ruta
## TODO Fromatering på listan
## TODO Hämta val för Möte
## TODO Knapp/X för att ta bort rad
## TODO En Frame per rad/En textruta per rad?
## TODO Datumkontroller ??
## TODO Bocka i färdiga task:s och flytta fram ofärdiga till nästa dag

class Schedule():
    def __init__(self):
        self.file_name = 'checklista.p'

    def insert(self, info, category, in_date):
        if in_date:
            insert_list = (in_date, category, info)
            with open(self.file_name, 'ab') as file:
                Pickler(file).dump(insert_list)

    def get(self, in_date):
        with open(self.file_name, 'rb') as file:
            data = []
            try:
                while True:
                    list = Unpickler(file).load()
                    if list[0] == in_date:
                        data.append([list[1], list[2]])
            except EOFError:
                pass

            key=itemgetter(0)
            data.sort(key=key)
            groups = groupby(data, key)
            g = [{key: [item[1] for item in data]} for (key, data) in groups]
            return g
        return []

    """
    def export_from_csv(self):
        import pandas
        data = pandas.read_csv('checklista.csv')
        #self.file_name = 'test.p'
        data = data[['Datum', 'Kategori', 'Info']]
        [self.insert(in_date=row.Datum, category=row.Kategori, info=row.Info) for (index, row) in data.iterrows()]
    """


class MenuLabelEntry(tkinter.Frame):
    def __init__(self, master, *args, **kwargs):
        self.master = master
        super().__init__(master)

        label = kwargs.pop('label')
        l = tkinter.Label(self, text=label)
        self.e = tkinter.Entry(self, *args, **kwargs)

        l.pack(side='left')
        self.e.pack(side='left')
        self.pack(side='left')

    def get(self):
        return self.e.get()

    def bind(self, *args, **kwargs):
        self.e.bind(*args, **kwargs)

    def focus_set(self, *args, **kwargs):
        self.e.focus_set(*args, **kwargs)


class GUI:
    def __init__(self, master):
        self.master = master
        self.menu()
        self.schedule = Schedule()
        self.format_date = DateFromText()
        self.text = tkinter.Text(self.master, height=1)
        self.text_info = tkinter.Text(self.master, height=20)
        self.text.pack(side='top')
        self.text_info.pack(side='top')
        self.print_info(self.format_date.this_week_date(''))
        
    def menu(self):
        menu_frame = tkinter.Frame(self.master)
        menu_frame.pack(side='top')

        self.date = MenuLabelEntry(menu_frame, label='Dag')
        self.meeting = MenuLabelEntry(menu_frame, label='Möte')
        self.info = MenuLabelEntry(menu_frame, label='Info')

        self.date.bind("<Return>", self.get_info)
        self.meeting.bind("<Return>", self.save)
        self.info.bind("<Return>", self.save)

        self.date.focus_set()

    def get_info(self, event=None):
        in_date = self.format_date.this_week_date(self.date.get())
        self.print_info(in_date)

    def save(self, event=None):
        in_date = self.format_date.future_date(self.date.get())
        if in_date:
            info = self.info.get()
            category = self.meeting.get()
            if info and category:
                self.schedule.insert(info=info, category=category, in_date=in_date)
                self.text.delete(1.0, 2.0)
                self.text.insert(1.0, f'{in_date}: {category}: {info}')
            self.print_info(in_date)

    def print_info(self, in_date):
        self.text_info.delete(1.0, 20.0)
        info = self.schedule.get(in_date)
        for dictionary in info:
            for key in dictionary:
                self.text_info.insert(tkinter.END, '\n' + key + '\n')
                for list in dictionary[key]:
                    self.text_info.insert(tkinter.END, '  - ' + list + '\n')


if __name__ == '__main__':
    tk = tkinter.Tk()
    GUI(tk)
    tk.mainloop()
