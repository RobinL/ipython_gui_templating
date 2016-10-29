import pandas as pd
from IPython.display import display, clear_output
import ipywidgets  
from ipywidgets import Layout, HBox, VBox, Box, Label
from collections import defaultdict
import json


class Widget_GUI(object):

    def __init__(self, csv_path=None, settings_path=None, model=None):
        self.model = model
        self.settings = self.get_settings(settings_path)
        self.widgets = {} #Stores a list of all the widgets in the interface
        self.list_of_csv_cols_to_use_as_arguments = ["min", "max", "value", "continuous_update"]
        self.gui_elements = self.csv_to_gui_elements(csv_path)
        self.parameters = {} #Stores all the parameters from the widets
        self.layouts = {}
        self.set_default_layouts()
        self.generate_gui()
        self.update_parameter_values()
        self.show_gui()

    def csv_to_gui_elements(self, csv_path):
        """
        Returns a list of dicts.  Each element specifies an interface component
        """
        df = pd.read_csv(csv_path)
        df = df.sort_values(by = ["col_num", "row_num"])
        elements = df.to_dict(orient="records")

        # Data types need to be quite strict here because 
        # e.g. an IntSlider widget will not accept a  flat
        # So we need to convert datatypes

        def convert_if_int(el):
            """
            If type is float but it's really an integer return interger
            """
            if type(el) == float:
                if el.is_integer():
                     return int(el)
            return el

        for el in elements:
            for field in self.list_of_csv_cols_to_use_as_arguments:
                el[field] = convert_if_int(el[field])

        return elements

    def get_settings(self,settings_path):
        if settings_path:   
            with open(settings_path) as data_file:    
                loaded_settings = json.load(data_file)

        return loaded_settings

    def show_gui(self):
        """
        This enables us to make arbitrary alterations to widgets 
        before they're displayed
        """
        display(self.gui)

    def widget_observer(self, callee):

        if callee["type"] == "change" and callee["name"] == "value":
            self.update_parameter_values()
            self.update_widgets()
            self.run_model_using_parameters()


    def update_widgets(self):
        """
        Placeholder in case we need to update widgets after observing
        """
        pass
        
    def update_parameter_values(self):
        """
        Iterates through the widgets, getting parameter values and saving to self.parameters
        """
        for widget_name, widget in self.widgets.iteritems():
            self.parameters[widget_name] = widget.value

    def generate_gui(self):
        """
        Main function that draws the widget GUI in Jupyter
        """

        def get_widget_constructor_arguments():
            """
            Gets a dict of constructor arguments to pass to constructor
            """
            widget_constructor_arguments = {}
            for arg in self.list_of_csv_cols_to_use_as_arguments:
                if pd.notnull(el[arg]):
                    widget_constructor_arguments[arg] = el[arg]
            widget_constructor_arguments["layout"] = self.layouts["single_widget"]
            return widget_constructor_arguments

        gui_cols = defaultdict(list)

        # Iterate through thie list of gui elements creating them and adding to gui in groups
        for el in self.gui_elements:

            widget_constructor = getattr(ipywidgets, el["control_type"]) 
            args = get_widget_constructor_arguments()
            this_widget = widget_constructor(**args)  

            this_widget.observe(self.widget_observer)  
            
            self.widgets[el["id"]] = this_widget
            label = Label(value=el["desc"], layout=self.layouts["label"])
            this_widget_group = Box([label,this_widget], layout=self.layouts["label_and_widget_pair"])
            
            gui_cols[el["col_num"]-1].append(this_widget_group)

        gui_cols = [c for i,c in gui_cols.items()]

        gui_cols = [VBox(c, layout=self.layouts["layout_each_col"] ) for c in gui_cols]
        
        self.gui = HBox(gui_cols, layout=self.layouts["layout_column_container"])


    def set_default_layouts(self):
        """
        Sets default layouts for widgets 
        """

        for k, v in self.settings.iteritems():
            self.layouts[k] = Layout(**v)


    def run_model_using_parameters(self):
        """
        Dispatch gui event to model
        """
        self.model.run(self.parameters)

