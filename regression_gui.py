from gui_template.interface_template import Widget_GUI
from IPython.display import display

class Widget_Gui_Regression(Widget_GUI):
    
    def show_gui(self):
        """
        This enables us to make arbitrary alterations to widgets 
        before they're displayed
        """
        # How many 
        print self.parameters
        self.widgets["x_vars"].options = ["x{}".format(i+1) for i in range(self.parameters["num_x_vars"])]
        self.widgets["x_vars"].value = self.widgets["x_vars"].options

        self.widgets["display_elements"].options = ["Snippet of raw data", "Regression results","Paired scatter plots",  "Residual plot"]
        self.widgets["display_elements"].value = ["Regression results"]
        display(self.gui)


    def update_widgets(self):

    	self.widgets["x_vars"].options = ["x{}".format(i+1) for i in range(self.parameters["num_x_vars"])]


