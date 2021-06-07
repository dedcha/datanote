from Imports import *


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.refresh_from_data()
        
        #self.mymsg = [{'text': str(i)} for i in range(20)]
        #Clock.schedule_interval(self.updateRecycleView, 10)
        
        #self.bind(data=self.dbList)
        #self.data = self.dbList()
        #self.refresh_from_data()
        
    
# List menu
class BoxL(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(BoxL, self).__init__(*args, **kwargs)
        Window.clearcolor = (1, 0.5, 1, 0.1)
        myname = ObjectProperty(None)
        mytitle = ObjectProperty(None)
        myage = ObjectProperty(None)
        myincome = ObjectProperty(None)
        myexp = ObjectProperty(None)
    
    def insertIntoDatabase(self):
        if self.myincome.text.isnumeric() and self.myexp.text.isnumeric() and self.myage.text.isnumeric():
            self.person = Details(self.myname.text, self.mytitle.text, self.myage.text, self.myincome.text, self.myexp.text)
            
            print(self.person)
            print(self.person.balance)

            details = self.person.details
            self.ids.Label1.text = "Data Entry Success"
            con = sql.connect('mydatabase.db')
            cur = con.cursor()
            cur.execute(""" INSERT INTO details (name, title, age, income, expenditure, balance) VALUES (?,?,?,?,?,?)
            """,(str(details[0]), str(details[1]), int(details[2]), int(details[3]), int(details[4]), int(self.person.balance)))
            con.commit()
            con.close()

        else:
            print("Input Error")
            self.ids.Label1.text = "Input Error"

class BoxM(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(BoxM, self).__init__(*args, **kwargs)
        # window color
        Window.clearcolor = (0, 0, 0.2, 0.1)

        #for id obj
        rowID = ObjectProperty(None)

        con = sql.connect('mydatabase.db')
        cur = con.cursor()
        self.detail_list = cur.execute(""" SELECT * FROM details;
        """)
        con.commit()

        self.ids.rv1.data = [{'text':str(rows[0]) + " Name: " + rows[1] + " Title: " + str(rows[2]) + " Age: " + str(rows[3]) + " Income: " + str(rows[4]) + " Expenditure: " + str(rows[5])
        + " Balance: " + str(rows[6])} for rows in self.detail_list]
        self.recycle = self.ids.rv1

    def refresh(self):
        con = sql.connect('mydatabase.db')
        cur = con.cursor()
        detail = cur.execute(""" SELECT * FROM details;
        """)
        con.commit()

        self.recycle.data = [{'text':str(rows[0]) + " Name: " + rows[1] + " Title: " + str(rows[2]) + " Age: " + str(rows[3]) + " Income: " + str(rows[4]) + " Expenditure: " + str(rows[5])
        + " Balance: " + str(rows[6])} for rows in detail]
        self.recycle.refresh_from_data()
    
    def deleteRow(self):
        if self.rowID.text.isnumeric():
            con = sql.connect('mydatabase.db')
            cur = con.cursor()
            detail = cur.execute(""" DELETE FROM details WHERE id=(?);
            """, (self.rowID.text,))
            con.commit()

            self.recycle.refresh_from_data()
        else:
            self.ids.rowID.text = "Input Error"

        
    def remove(self):
        for item in self.detail_list:
            self.remove_widget(self.item)
        pass

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
                                 pass

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))

class homescrn(Screen):
    pass

class datascrn(Screen):
    pass

class Details():
    def __init__(self, name, title, age, income, expenditure):
        self.name = name
        self.title = title
        self.age = age
        self.income = income
        self.expenditure = expenditure
    
    @property
    def details(self):
        return [
            self.name,
            self.title,
            self.age,
            self.income,
            self.expenditure
        ]
    @property
    def balance(self):
        return int(self.income) - int(self.expenditure)

    def __repr__(self):
        return f'{self.name} {self.title} {self.age} {self.income} {self.expenditure}'

