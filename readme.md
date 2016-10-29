##Declarative ipython GUI example

Some experimentation with ipython widgets - specifically how lay out and format relatively complex interfaces.  

The idea is that you define your interface in columns and rows in a csv file, with an associated json settings file, and then forget about it.  It then lays everything out using flexboxes which keeps everything aligned.

````
from gui_template.interface_template import Widget_GUI
from gui_template.model_template import Model
model = Model()
gui = Widget_GUI("gui_template/examples/interface_definition.csv", "gui_template/examples/gui_settings.json", model)
````

And an interface will be built from the [csv](https://github.com/RobinL/ipython_gui_templating/blob/master/gui_template/examples/interface_definition.csv) and [json](https://github.com/RobinL/ipython_gui_templating/blob/master/gui_template/examples/gui_settings.json) files you provide.

You need to give the interface a [model](https://github.com/RobinL/ipython_gui_templating/blob/master/gui_template/model_template.py) object, which has a [model.run](https://github.com/RobinL/ipython_gui_templating/blob/master/gui_template/model_template.py#L6) method, and which procudes some output (using [ipython rich display](http://jeffskinnerbox.me/notebooks/ipython's-rich-display-system.html).

I haven't managed to control the layout output effectively yet.  At the moment it's all in a vertical column. But a new more flexible approach to this seems to be coming in [JupyterLab](http://blog.jupyter.org/2016/07/14/jupyter-lab-alpha/)  - see particularly the [video at 22mins in](https://youtu.be/Ejh0ftSjk6g?t=22m10s).


###Examples

There are two examples, a very simple proof of concept [here](https://github.com/RobinL/ipython_gui_templating/blob/master/Simplest%20example.ipynb), and a working example with more complex regression simulations [here](https://github.com/RobinL/ipython_gui_templating/blob/master/Regression%20example.ipynb).

The horrid colours are there to help the user understand the relationship between settings and how they affect they layout.  They can be turned off by turning borders off in the settings.json file.





