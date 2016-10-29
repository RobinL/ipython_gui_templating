from interface_template import Widget_GUI, Model
from IPython.display import display

class Widget_Gui_Regression(Widget_GUI):
    
    def show_gui(self):
        """
        This enables us to make arbitrary alterations to widgets 
        before they're displayed
        """
        self.widgets["x_vars"].options = list("abc")
        display(self.gui)
