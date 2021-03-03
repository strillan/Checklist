from datetime import date
from datetime import timedelta

class DateFromText:
    def __init__(self):
        self.today = date.today()
        self.output_date = False
        self.type = ''
        self.weekdays= {
            'mån': 1,
            'tis': 2,
            'ons': 3,
            'tors': 4,
            'tor': 4,
            'fre': 5,
            'lör': 6,
            'sön': 7
        }
    
    def this_week_date(self, input_date):
        self.construe(input_date=input_date)
        """
        if self.output_date and self.output_date < self.today and self.type:
            if self.type == 'day':
                print('smaller day')
            if self.type == 'date':
                print('smaller date')
            if self.type == 'month':
                print('smaller month')
        """
        return self.output_date

    # Used in Checklista   
    def future_date(self, input_date):
        self.construe(input_date=input_date)
        if self.output_date and self.output_date < self.today and self.type:
            if self.type == 'day':
                self.output_date += timedelta(weeks=1)
            elif self.type == 'date':
                d = self.output_date
                self.output_date = date(d.year, d.month+1, d.day)
            elif self.type == 'month':
                d = self.output_date
                self.output_date = date(d.year+1, d.month, d.day)
        return self.output_date

    def make_date(self, year=0, month=0, day=0, weekday=0, error=False, today=False):
        if today:
            self.output_date = self.today
            return
        if error:
            self.output_date = False
            return
        if not year:
            year = self.today.year
        elif len(year) == 2:
            year = '20' + year
        if weekday:
            week = self.today.isocalendar().week
            new_date = date.fromisocalendar(year, week, weekday)
        else:
            if not month:
                month = self.today.month
            try:
                new_date = date(int(year), int(month), int(day))
            except ValueError:
                new_date = False
        self.output_date = new_date
        
    def construe(self, input_date):
        if not input_date:  # today
            self.make_date(today=True)
        elif len(input_date) < 3:  # 21
            self.make_date(day=input_date)
            self.type = 'date'
        elif '-' in input_date and '/' in input_date:  # 21/1-[20]21
            temp1 = input_date.split('/')
            temp2 = temp1[1].split('-')
            self.make_date(year=temp2[1], month=temp2[0], day=temp1[0])
        elif '/' in input_date:  # 21/1
            temp = input_date.split('/')            
            self.make_date(month=temp[1], day=temp[0])
            self.type = 'month'
        elif '-' in input_date:  # [20]21-01-21
            temp = input_date.split('-')
            self.make_date(year=temp[0], month=temp[1], day=temp[2])
        elif ':' in input_date:  # 21:a
            temp = input_date.split(':')[0]
            self.make_date(day=temp)
            self.type = 'date'
        else:  # Tor, Tors, tor, tors, torsdag
            day = input_date.lower()
            if len(day) > 4:
                day = day[:-3]
            if day in self.weekdays:
                self.make_date(weekday=self.weekdays[day])
                self.type = 'day'
            else:
                self.make_date(error=True)

"""
d = DateFromText()
print(d.future_date(''))
print(d.future_date('tis'))
print(d.future_date('Lördag'))
print(d.future_date('ti'))
print(d.future_date('16'))
print(d.future_date('17/1'))
print(d.future_date('18/1-20'))
print(d.future_date('30/1-2020'))
print(d.future_date('21-01-19'))
print(d.future_date('21-1-20'))
print(d.future_date('2121-1-21'))
print(d.future_date('2121-1-22'))
print(d.future_date('1:a'))
print(d.future_date('15'))
"""