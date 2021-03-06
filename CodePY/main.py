import pandas
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import logging
from kivy.uix.label import Label
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.button import Button
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.core.window import Window
from kivy.properties import StringProperty


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(True)
    selectable = BooleanProperty(False)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected


class QuestionDb(BoxLayout):
    items_list = ObjectProperty(None)
    column_headings = ObjectProperty(None)
    rv_data = ListProperty([])

    random_number = StringProperty()

    def __init__(self, **kwargs):
        super(QuestionDb, self).__init__(**kwargs)
        self.get_dataframe()
        self.random_number = 'SeLect a Student from the list below'

    def change_text(self,instance ):
        print(self.rv_data[instance.index]['selectable'])
        if self.rv_data[instance.index]['selectable'] == True:
            self.random_number = (str(
                "The student selected is: {1}, number {0}".format((self.rv_data[instance.index]['Index']),
                                                                  self.rv_data[instance.index]['text'])))
        else:self.random_number = "Select student name "




    def get_dataframe(self):
        df = pandas.read_excel("items.xlsx")
        # Extract and create column headings
        for heading in df.columns:
            self.column_headings.add_widget(Label(text=heading))

        # Extract and create rows
        data = []
        for row in df.itertuples():
            for i in range(1, len(row)):
                data.append([row[i], row[0]])
        print (data)
        self.rv_data = [{'text': str(x[0]), 'Index': str(x[1] + 1), 'selectable': True} for x in data]

        for enum, item in enumerate(self.rv_data):
            if (enum % 3) == 0:
                item['selectable'] = 'False'
        print(self.rv_data)

    def PrintRowContenent(self, instance):
        # TODO
        self.change_text(instance)

class QuestionApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)    # white background
        return QuestionDb()


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    QuestionApp().run()