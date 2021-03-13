from pickle import Unpickler
from pickle import Pickler
from itertools import groupby
from operator import itemgetter

import tkinter 
from date_from_text import DateFromText
from tkinter import ttk


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
            # { kategori : [info, info, info] }
            return [{key: [item[1] for item in data]} for (key, data) in groups]
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
        label = kwargs.pop('label', '')
        start_focus = kwargs.pop('start_focus', False)
        side = kwargs.pop('side', 'left')
        return_command = kwargs.pop('hit_return', '')
        super().__init__(master, *args, **kwargs)

        self.master = master
        l = tkinter.Label(self, text=label)
        self.e = tkinter.Entry(self, *args, **kwargs)

        l.pack(side='left')
        self.e.pack(side='left')
        self.pack(side=side)

        if start_focus:
            self.focus_set()

        if return_command:
            self.bind("<Return>", return_command)

    def get(self):
        return self.e.get()

    def bind(self, *args, **kwargs):
        self.e.bind(*args, **kwargs)

    def focus_set(self, *args, **kwargs):
        self.e.focus_set(*args, **kwargs)


class Checklist(ttk.Treeview):
    def __init__(self, master, *args, **kwargs):
        side = kwargs.pop('side', 'top')
        super().__init__(master, columns='info', *args, **kwargs)
        self.column('#0', width=100)
        self.column('info', width=500)
        self.pack(side=side)
        self.bind('<Return>', self.delete)
        self.bind('<Double 1>', self.delete)
        self.bind('<Control-z>', self.undo)
        self.bind('<Control-s>', self.save)
        self.removed_item = ''
        self.removed_parent = ''

    def save(self, event=None):
        for node in self.get_children():
            print(node)

    def undo(self, event=None):
        if self.removed_parent:
            self.reattach(self.removed_parent[0], self.removed_parent[1], self.removed_parent[2])
            self.removed_parent = ''
        if self.removed_item:
            self.reattach(self.removed_item[0], self.removed_item[1], self.removed_item[2])
            self.removed_item = ''

    def delete(self, event):
        item = self.focus()
        if(self.parent(item)):
            parent = self.parent(item)
            self.removed_item = (item, parent, self.index(item))
            self.detach(item)
            kids = self.get_children(parent)
            if not kids:
                self.removed_parent = (parent, '', self.index(parent))
                self.detach(parent)
                parent = self.get_children()[0]
                kids = self.get_children(parent)
            self.focus(kids[0])

    def set(self, info):
        for child in self.get_children():
            print(child)
            self.detach(child)
            
        for line in info:
            for key in line:
                a = self.insert('', 'end', text=key, values=(''))
                for value in line[key]:
                    b = self.insert(a, 'end', text='', values=(value, ''))
                    self.see(b)

class GUI():
    def __init__(self, master):
        self.master = master
        menu_frame = tkinter.Frame(self.master)
        menu_frame.pack(side='top')
        self.tree1 = Checklist(self.master)
        self.date = MenuLabelEntry(menu_frame, label='Dag', width='7', hit_return=self.get_info, start_focus=True)
        self.meeting = MenuLabelEntry(menu_frame, label='Möte', width='15', hit_return=self.save)
        self.info = MenuLabelEntry(menu_frame, label='Info', width='60', hit_return=self.save)
        self.schedule = Schedule()
        self.format_date = DateFromText()
        self.master.bind('<Control-s>', self.tree1.save)
        self.master.bind('<Control-z>', self.tree1.undo)
        self.get_info()

    def save(self, event=None):
        in_date = self.format_date.future_date(self.date.get())
        self.master.title(str(in_date))
        info = self.info.get()
        category = self.meeting.get()
        if info and category:
            self.schedule.insert(info=info, category=category, in_date=in_date)
        info = self.schedule.get(in_date)
        self.tree1.set(info)

    def get_info(self, event=None):
        in_date = self.format_date.this_week_date(self.date.get())
        self.master.title(str(in_date))
        info = self.schedule.get(in_date)
        self.tree1.set(info)


if __name__ == '__main__':
    tk = tkinter.Tk()
    GUI(tk)
    tk.mainloop()