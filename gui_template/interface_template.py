import pandas as pd
from IPython.display import display, clear_output
import ipywidgets  
from ipywidgets import Layout, HBox, VBox, Box, Label
from collections import defaultdict
import json


class Widget_GUI:

    def __init__(self, csv_path=None, settings_path=None, model=None):
        self.settings = self.get_settings(settings_path)
        self.widgets = {} #Stores a list of all the widgets in the interface
        self.list_of_csv_cols_to_use_as_arguments = ["min", "max", "value"]
        self.gui_elements = self.csv_to_gui_elements(csv_path)
        self.parameters = {} #Stores all the parameters from the widets
        self.layouts = {}
        self.set_default_layouts()
        self.generate_gui()
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
        settings = defaultdict(object)
        if settings_path:   
            with open(settings_path) as data_file:    
                loaded_settings = json.load(data_file)

        return defaultdict(lambda: None, loaded_settings)

    def show_gui(self):
        """
        This enables us to make arbitrary alterations to widgets 
        before they're displayed
        """
        # self.widgets["x_vars"].options = list("abc")
        display(self.gui)

    def widget_observer(self, callee):
        self.update_parameter_values()
        self.run_model_using_parameters()

    def update_parameter_values(self):
        """
        Iterates through the widgets, getting parameter values and saving to self.parameters
        """
        pass

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
            
            self.widgets[el["id"]] = this_widget
            label = Label(value=el["desc"], layout=self.layouts["label_layout"])
            this_widget_group = Box([label,this_widget], layout=self.layouts["label_and_widget_pair_layout"])
            
            gui_cols[el["col_num"]-1].append(this_widget_group)

        gui_cols = [c for i,c in gui_cols.items()]

        gui_cols = [VBox(c, layout=self.layouts["layout_for_each_col"] ) for c in gui_cols]
        
        self.gui = HBox(gui_cols, layout=self.layouts["layout_column_container"])


    def set_default_layouts(self):
        """
        Sets default layouts for widgets 
        """

        self.layouts["single_widget"] = Layout( 
                        flex='1 1 auto', 
                        width='50%', 
                        border = 'solid 1px blue')
        
        print "single_widget layout has blue border"

        self.layouts["label_layout"] = Layout(
                        flex='1 1 auto', 
                        width=self.settings["label_width"], 
                        border = 'solid 1px red')
        print "label_layout has red border"

        self.layouts["label_and_widget_pair_layout"] = Layout(
                        display='flex',
                        flex_flow='row',
                        justify_content='space-between',
                        border = 'solid 5px green'
                    )
        print "label_and_widget_pair_layout has green border"

        self.layouts["layout_for_each_col"] = Layout(
                        border='solid 5px yellow', 
                        flex="1 1 auto", 
                        width=self.settings["layout_for_each_col_width"],
                        )
        print "layout_for_each_col has yellow border"

        self.layouts["layout_column_container"] = Layout(
                        border='solid 10px purple')
        print "layout_column_container has purple border"
    

    def run_model_using_parameters():
        """
        Dispatch gui event to model
        """
        self.model.run(self.parameters)

