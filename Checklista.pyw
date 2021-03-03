import tkinter 
from datetime import date
import datetime
import pandas
import csv
from date_from_text import DateFromText

## TODO Större INFO-ruta
## TODO Fromatering på listan
## TODO Hämta val för Möte
## TODO Knapp/X för att ta bort rad
## TODO En Frame per rad/En textruta per rad?
## TODO Datumkontroller ??

class Schedule():
    def __init__(self):
        self.file_name = 'checklista.csv'

    def insert_new_info(self, info, category, in_date, story):
        if in_date:
            insert_list = [in_date, category, info, story]
            with open(self.file_name, 'a', encoding='utf-8') as file:
                file_writer = csv.writer(file)
                file_writer.writerows([insert_list])

    def meeting_info(self, in_date):
        """
        data = pandas.read_csv(self.file_name)
        data = data[data.Datum == date.today().isoformat()]
        categories = data[['Kategori']].drop_duplicates()
        categories = [row.Kategori for (index, row) in categories.iterrows()]

        category_dict = {}
        for category in categories:
            data = data[data.Kategori == category]
            stories = data[['Story']].drop_duplicates()
            stories = [row.Story for (index, row) in stories.iterrows()]
            story_dict = {}
            category_dict[category] = story_dict
            for story in stories:
                info = data[data.Story == story]
                info = [row.Info for (index, row) in info.iterrows()]
                story_dict[story] = info
        """            
        data = pandas.read_csv(self.file_name)
        data = data[data.Datum == in_date.isoformat()]
        data = data[['Kategori', 'Story', 'Info']].sort_values(by=['Kategori'])
        lista = [f'{row.Kategori:9} : {row.Story:30} : {row.Info} ' for (index, row) in data.iterrows()]
        return lista


class MenuLabelEntry(tkinter.Frame):
    def __init__(self, master, *args, **kwargs):
        self.master = master
        label = kwargs.pop('label', '')
        super().__init__(master)

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


schedule = Schedule()
entry_date = DateFromText()

class GUI:
    def __init__(self, master):
        self.master = master
        self.menu()
        self.text = tkinter.Text(self.master, height=1)
        self.text_info = tkinter.Text(self.master, height=20)
        self.text.pack(side='top')
        self.text_info.pack(side='top')
        self.print_info(date.today())

    def menu(self):
        menu_frame = tkinter.Frame(self.master)
        menu_frame.pack(side='top')

        self.date = MenuLabelEntry(menu_frame, label='Dag')
        self.meeting = MenuLabelEntry(menu_frame, label='Möte')
        self.story = MenuLabelEntry(menu_frame, label='Story')
        self.info = MenuLabelEntry(menu_frame, label='Info')

        self.date.bind("<Return>", self.get_info)
        self.meeting.bind("<Return>", self.save)
        self.story.bind("<Return>", self.save)
        self.info.bind("<Return>", self.save)

        self.date.focus_set()

    def get_info(self, event=None):
        in_date = entry_date.this_week_date(self.date.get())
        self.print_info(in_date)

    def save(self, event=None):
        in_date = entry_date.future_date(self.date.get())
        if in_date:
            info = self.info.get()
            category = self.meeting.get()
            if info and category:
                schedule.insert_new_info(info=info, category=category, in_date=in_date, story=self.story.get())
                self.text.delete(1.0, 2.0)
                self.text.insert(1.0, f'{in_date}: {category:12}: {info}')
            self.print_info(in_date)

    def print_info(self, in_date):
        self.text_info.delete(1.0, 20.0)
        info = schedule.meeting_info(in_date)
        self.text_info.insert(1.0, '\n'.join(info))


if __name__ == '__main__':
    tk = tkinter.Tk()
    GUI(tk)
    tk.mainloop()
