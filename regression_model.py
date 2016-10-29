from gui_template.model_template import Model
import numpy as np
from IPython.display import display, clear_output
import pandas as pd

from pandas.tools.plotting import scatter_matrix
from IPython.display import HTML

import statsmodels.formula.api as sm

import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="white")
import matplotlib
matplotlib.use('GTKAgg') 


class RegressionModel(Model):

    def __init__(self):
        self.parameters = {}
        self.regression_data = None

    def run(self, parameters):
        
        clear_output()
        display(HTML(open("custom_styles.html").read()))
        self.parameters = parameters

        self.regression_data = self.get_regression_data()
        self.run_regression()

        mapping = {"Snippet of raw data": self.regression_data.head,
                  "Paired scatter plots": self.run_pair_plot_original_data,
                  "Regression results": self.regression_results.summary, 
                  "Residual plot": self.run_pair_plot_residuals}

        # Only compute the pair plots if the options are selected


        for d in self.parameters["display_elements"]:

            if d in ["Snippet of raw data", "Regression results"]:
                display(mapping[d]())
            else:
                mapping[d]()





    def get_regression_data(self):

        def random_cov(num_variables):
            cov = []
            for i in range(num_variables):
                cov.append([None]*num_variables)
            for i in range(num_variables):
                for j in range(num_variables):
                    if i<j:
                        r = np.random.uniform(-1,1)
                        cov[i][j] = r
                        cov[j][i] = r
                    if i == j:
                        cov[i][j] = 1
            return cov


        def is_pos_def(x):
            return np.all(np.linalg.eigvals(x) > 0)

        def get_pos_def_cov(num_variables):
            while True:
                 cov = random_cov(num_variables)
                 if is_pos_def(cov):
                    break
            return cov

        num_points = self.parameters["num_points"]
        num_x_vars = self.parameters["num_x_vars"]
        var_x = self.parameters["var_x"]
        var_e = self.parameters["var_e"]

        cov = get_pos_def_cov(num_x_vars)
        x = np.random.multivariate_normal([var_x]*num_x_vars, cov,num_points) 
        e = np.random.normal(0,var_e,num_points)

        coefficients = np.random.uniform(-2,2,num_x_vars)

        var_names = ["x{}".format(i+1) for i in range(num_x_vars)]

        real_formula = "y = {} + error"
        mid_formula_str = " + ".join(["{}*{}".format(t[0],t[1]) for t in zip(coefficients,var_names)])
        real_formula = real_formula.format(mid_formula_str)
        print real_formula

        df = pd.DataFrame(x, columns=var_names)
        df["e"] = e
        df["y"] = 0
        for i, c in enumerate(coefficients):
            df["y"] += df["x{}".format(i+1)]
        df["y"] += df["e"]

        return df

    def run_pair_plot_original_data(self):

        cols = [c for c in self.regression_data.columns if c != "e" and c !="resid"]

        g = scatter_matrix(self.regression_data[cols], alpha=0.2, figsize=(4, 4), diagonal='kde')
        # g = sns.PairGrid(self.regression_data, diag_sharey=False)
        # g.map_lower(sns.kdeplot, cmap="Blues_d")
        # g.map_upper(plt.scatter)
        # g.map_diag(sns.kdeplot, lw=3)
        plt.show()

    def run_pair_plot_residuals(self):

        cols = [c for c in self.regression_data.columns if c != "e"]

        g = scatter_matrix(self.regression_data[cols], alpha=0.2, figsize=(4, 4), diagonal='kde')
        # g = sns.PairGrid(self.regression_data, diag_sharey=False)
        # g.map_lower(sns.kdeplot, cmap="Blues_d")
        # g.map_upper(plt.scatter)
        # g.map_diag(sns.kdeplot, lw=3)
        plt.show()

    def run_regression(self):

        def create_formula():
            formula_template = "y ~ {}"
            deps = " + ".join(self.parameters["x_vars"])
            formula = formula_template.format(deps)
            return formula

        results = sm.ols(formula=create_formula(), data=self.regression_data).fit()

        self.regression_results = results
        self.regression_data["resid"] = results.resid

        


