from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.properties import NumericProperty, ListProperty, BooleanProperty
from kivy.metrics import dp
from kivymd.uix.card import MDSeparator
from kivy.uix.scrollview import ScrollView
from kivymd.uix.refreshlayout import MDScrollViewRefreshLayout
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.behaviors import HoverBehavior
from kivymd.theming import ThemableBehavior
from kivy.graphics import *

class Cell(MDLabel, ThemableBehavior, HoverBehavior):
	''' creates a cell for the data table  the contain the data for the table'''
	length = NumericProperty()
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.size_hint = (None,None)
		self.height = dp(24)
		#print('height of cell', self.height)
		self.markup = True
		self.halign = 'center'
		self.theme_cls.theme_style = "Dark" 
		self.theme_cls.primary_palette = "Teal"
		self.opposite_colors = False
		self.md_bg_color = self.theme_cls.bg_normal
	
	def on_enter(self, *args):
		self.md_bg_color = self.theme_cls.bg_light
		


	def on_leave(self, *args): 
		self.md_bg_color = self.theme_cls.bg_normal


class Table(MDScrollViewRefreshLayout):
	data = ListProperty()
	head = ListProperty()
	new = BooleanProperty()
	len_of_data = NumericProperty(0)
	def __init__(self,Data=[], Header=[], **kwargs):
		super().__init__(**kwargs)
		self.orientation = 'vertical'
		self.header_title = MDBoxLayout(orientation='horizontal', 
										size_hint_y=None, 
										height='57dp')

		self.toolbar = MDToolbar(title='Table', pos_hint={'top':1})
		self.row_container = MDBoxLayout(orientation='vertical', adaptive_height=True)
		self.table = MDBoxLayout(orientation='vertical', adaptive_height=True)
		
		self.table.add_widget(self.toolbar)
		#self.padding = dp(12)
		self.head = Header
		self.data = Data
		self.size_hint = (1, None)
		self.size = (1, dp(Window.height))


		# bind activity
		self.bind(on_new=self.on_len_of_data)
	def row(self, data):
		if isinstance(data, (tuple, list)):
			self.data = data
			self.add_cell()
	def add_cell(self):
		''' add a cell in the table'''
		row = None
		for values in self.data:
			row = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(24))
			for value in values:
				row.add_widget(Cell(text=value, md_bg_color=(1, 0.6, 0.3,0)))
				row.add_widget(MDSeparator(orientation='vertical'))
			self.row_container.add_widget(row)
			row = None
			self.row_container.add_widget(MDSeparator())

		self.table.add_widget(self.row_container)
		
		
	def on_head(self, *args):
		''' creates the header of the table'''
		print(' Creating header')
		if self.header_title in self.table.children[:]:
			#check if the header is in the table already
			#if so remove the old header
			self.table.remove_widget(self.header_title)
		self.header()

	def on_data(self, *args):
		''' populate the table with the new data'''
		print('populating data')
		if self.row_container not in self.table.children[:]:
			self.row(self.data)
		else:
			print('new data detected')
			self.len_of_data = len(self.data)
			self.new = True
	def on_len_of_data(self, *args):
		''' add the last data added to the row'''
		new_data = self.data[self.len_of_data-1]
		print(new_data)
		row = MDBoxLayout(orientation='horizontal')
		for value in new_data:
			row.add_widget(Cell(text=value))
			row.add_widget(MDSeparator(orientation='vertical'))
		self.row_container.add_widget(row)
		self.row_container.add_widget(MDSeparator())
		print('added New data')
		self.new = False


	def header(self):
		''' input the header of the table'''
		for value in self.head:
			self.header_title.add_widget(Cell(text=value))

		self.table.add_widget(self.header_title)
		self.table.add_widget(MDSeparator())
	def create(self):
		''' Does the work of building the table based on the data provided'''
		#creates the header of the table first
		if self.table in self.children[:]:
			#do not add in the tree
			pass
		else:
			self.add_widget(self.table)

class Test(MDApp):
	def build(self):
		header = ['Name', 'Age', 'Sex']
		data = [['Bernice', '24','M'],['Bernice', '24','M']]
		table = Table()
		table.head = header
		table.data = data
		table.create()
		return table

if __name__ == '__main__':
	Test().run()



