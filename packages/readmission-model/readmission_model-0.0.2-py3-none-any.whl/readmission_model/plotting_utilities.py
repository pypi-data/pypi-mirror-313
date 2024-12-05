import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Literal
import pathlib
from fpdf import FPDF
from tabulate import tabulate
from sklearn.metrics import RocCurveDisplay
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dataframe_image as dfi
from readmission_model.utilities import *


HERE = pathlib.Path('..').resolve().parent.parent


"""
Rate plotting
"""

def plot_rates(years : list, real_rates : list, pred_rates : list, O_E_ratio : list, condition : str):
    """
    Plot the real rates, the predicted rates, and the O/E ratio on the same plot

    Args:
        years (list): A list of the years to plot, normally as strings
        real_rates (list): A list of the real readmission rates for each year, contains floats
        pred_rates (list): A list of the predicted readmission rates for each year, contains floats
        O_E_ratio (list): A list of the O/E ratio for each year, contains floats
        condition (str): The condition being investigated

    Returns:
        fig (matplotlib.figure): A figure showing all three variables and a constant line at 1 for the O/E ratio axis
    """

    fig, ax1 = plt.subplots(figsize=(12,8))
    ax2 = ax1.twinx()

    # Plot real rates
    ax1.plot(years, real_rates, label = 'Real Rate', lw = 1)
    ax1.scatter(years, real_rates, s = 15)
    # Plot pred rates
    ax1.plot(years, pred_rates, label = 'Predicted Rate', lw = 1)
    ax1.scatter(years, pred_rates, s = 15)
    ax1.set_ylim(min(real_rates+pred_rates)*0.0, max(real_rates+pred_rates)*1.4)
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Readmission Rate')

    # Plot O/E ratio on seperate axis
    ax2.plot(years, O_E_ratio, label = 'O/E Ratio', color = 'r')
    ax2.plot(years, [1]*len(years), linestyle = 'dashed', color = 'grey')
    ax2.scatter(years, O_E_ratio, color = 'r')
    ax2.set_ylim(0, 2)
    ax2.set_ylabel('O/E Ratio')


    fig.suptitle(f'Real and Predicted Readmission Rates for {condition} by Year', fontsize=15)
    fig.legend(loc='upper right', bbox_to_anchor=(0.87, 0.87))

    return fig


def plot_rates_subplots(years : list, real_rates : list, pred_rates : list, O_E_ratio : list, condition : str):
    """
    Plot the real and predicted rates on the same plot, before plotting the O/E ratio on a plot below

    Args:
        years (list): A list of the years to plot, normally as strings
        real_rates (list): A list of the real readmission rates for each year, contains floats
        pred_rates (list): A list of the predicted readmission rates for each year, contains floats
        O_E_ratio (list): A list of the O/E ratio for each year, contains floats
        condition (str): The condition being investigated

    Returns:
        fig (matplotlib.figure): A figure with two subplots - showing all three variables and a constant line at 1 for the O/E ratio axis
    """
    fig, axs = plt.subplots(2, figsize=(12,8))
    fig.suptitle(f'Real and Predicted Readmission Rates for {condition} by Year', fontsize=15)

    # Plotting the real and predicted rates on the same plot
    ax1 = axs[0]
    ax1.plot(years, real_rates, label = 'Real Rate', lw = 1)
    ax1.scatter(years, real_rates, s = 15)
    ax1.plot(years, pred_rates, label = 'Predicted Rate', lw = 1)
    ax1.scatter(years, pred_rates, s = 15)
    ax1.set_ylim(min(real_rates+pred_rates)*0.0, max(real_rates+pred_rates)*1.4)
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Readmission Rate')
    ax1.legend()

    # Plotting the O/E ratio on a plot below
    ax2 = axs[1]
    ax2.plot(years, O_E_ratio, label = 'O/E Ratio', color = 'r')
    ax2.plot(years, [1]*len(years), linestyle = 'dashed', color = 'grey')
    ax2.scatter(years, O_E_ratio, color = 'r')
    ax2.set_ylim(0, 2)
    ax2.set_xlabel('Year')
    ax2.set_ylabel('O/E Ratio')
    ax2.legend()

    return fig


def plotly_rates(years : list, real_rates : list, pred_rates : list, O_E_ratio : list, condition : str):
    """
    Plot the real rates, the predicted rates, and the O/E ratio on the same plotly plot

    Args:
        years (list): A list of the years to plot, normally as strings
        real_rates (list): A list of the real readmission rates for each year, contains floats
        pred_rates (list): A list of the predicted readmission rates for each year, contains floats
        O_E_ratio (list): A list of the O/E ratio for each year, contains floats
        condition (str): The condition being investigated

    Returns:
        fig (plotly figure): A figure showing all three variables and a constant line at 1 for the O/E ratio axis
    """

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Plot real rates
    fig.add_trace(go.Scatter(x = years, y = real_rates, 
                                mode='lines+markers', 
                                name = 'Real Rate'       
                                #line = dict(color='royalblue')
                            )
        ) 
    
    # Plot pred rates
    fig.add_trace(go.Scatter(x = years, y = pred_rates, 
                                mode='lines+markers', 
                                name = 'Predicted Rate'
                                #line = dict(color='royalblue')
                            )
        )
    
    #Plot O/E ratio
    fig.add_trace(go.Scatter(x = years, y = O_E_ratio, 
                                mode='lines+markers', 
                                name = 'O/E Ratio',
                                yaxis = "y2",
                                legendgroup='O/E'
                                #line = dict(color='royalblue')
                            )
        )
    
    # Add constant line at 1
    fig.add_trace(go.Scatter(x = years, y = [1]*len(years), 
                                mode='lines', 
                                name = 'O/E Ratio',
                                yaxis = "y2",
                                line=dict(color='slategrey', width=2,
                                        dash='dash'),
                                showlegend=False,
                                legendgroup='O/E'
                                #line = dict(color='royalblue')
                            )
        )
    fig.update_layout(
        title = {'text': f'Real and Predicted Readmission Rates for {condition} by Year',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
        },
        autosize=False,
        width=2000,
        height=500,
        xaxis_title="Date of Admission",
        yaxis_title='Readmission Rate',
        legend=dict(
                    x=1.005
                    )
    )
    
    # Set y-axes titles and set limits 
    fig.update_yaxes(title_text="Readmission Rate", secondary_y=False)
    fig.update_yaxes(title_text="O/E Ratio", secondary_y=True)
    fig.update_yaxes(range=[0, 1.2*max(real_rates+pred_rates)], secondary_y=False)
    fig.update_yaxes(range=[0, 2], secondary_y=True)
    fig['layout']['yaxis1']['showgrid'] = False

    return fig


"""
PDF generation utilities
"""

# roc - TODO - move to Model function?
def plot_roc_curve(y_true, y_predicted_proba, title_subset):
    fig,axs=plt.subplots(figsize=(10,6))
    display = RocCurveDisplay.from_predictions(
        y_true,
        y_predicted_proba,
        #name=f"{class_of_interest} vs the rest",
        color="firebrick",
        plot_chance_level=True,
        ax=axs,
    )
    _ = display.ax_.set(
        xlabel="False Positive Rate",
        ylabel="True Positive Rate",
        title="ROC curve {}".format("for "+title_subset if title_subset!="" else ""),
    )
    #fig.savefig(HERE / "../outputs/Figure ROC {} {}.png".format(subset,date), dpi=500, pad_inches = 0, bbox_inches='tight')
    return fig 

def visualise_coefficients(coefs :dict):
    coef_vis = {
        k: round(v, 3)
        for k, v in sorted(
           coefs.items(), key=lambda item: item[1], reverse=True
        )
        if k != "Intercept"
    }
    intercept_vis = round(coefs["Intercept"], 3)
    features,coefs = ["Intercept"] + list(coef_vis.keys()),[intercept_vis] + list(coef_vis.values())
    return features,coefs # tabulate(table, headers=["Feature", "Coefficient"])

# THIS FUNCTION DOES NOT SHOW THE READMISSION RATES

# def generate_pdf(model_objects : dict, name : str, date : str, version: str, title : str, p_threshold : float, uk : bool = False):
#     """
#     Generate pdf from logistic regression models - for models considering both the conditions and the triggers
#     Args:
#         model_objects (dict) : Dictionary containing model objects.
#         name (str) : Name of pdf
#         date (str) : Date to use in versioning of pdf e.g. 240202
#         version (str) : Version number to use in versioning of pdf e.g. v1p1
#         title (str) : Title in pdf header
#         p_threshold (float) : p-value threshold used in the model training
#         uk (bool) : Save in UK folders if True. Defaults to False.
#     """
#     pdf = FPDF(orientation="portrait", format=(220, 400))
#     ch = 10

#     for chronic_condition in sorted(model_objects):
#         model = model_objects[chronic_condition]
#         pdf.add_page()
#         # versioning
#         pdf.set_font("Helvetica", size=6) 
#         pdf.cell(200,3,
#                     txt= "Version_{}_{}".format(date,version), 
#                     ln=1,align="R")
        
#         # title
#         pdf.set_font("Helvetica", size=20, style="B")
#         pdf.cell(200,15,
#                     txt= str(title),
#                     ln=1,align="L")
        
#         # subtitle
#         pdf.set_font("Helvetica", size=16, style="B")
#         pdf.cell(200,15,
#                     txt= str(chronic_condition),
#                     ln=1,align="L")

#         # coefficients
#         y = pdf.get_y()
#         pdf.set_font("Helvetica", size=12, style="B")
#         pdf.cell(200,10,
#                     txt= "Coefficients",
#                     ln=1,align="L")
#         pdf.set_font("Helvetica", size=10) 
#         """for feature in model.coefs:
#             text = str(feature) + "   " + str(round(model.coefs[feature],4))
#             pdf.cell(200,4,
#                     txt= text, 
#                     ln=1,align="L")"""
#         features,coefs = visualise_coefficients(model.coefs)
#         for i in range(len(features)):
#             text = str(features[i]) + "   " + str(coefs[i])
#             pdf.cell(200,4,
#                     txt= text, 
#                     ln=1,align="L")
#         pdf.cell(200,4,
#                     txt= "", 
#                     ln=1,align="L")
        
#         # confusion matrix
#         model.confusion_matrix["Test"].savefig(HERE/ "outputs{}/Figure confusion matrix {}.png".format((" UK" if uk else ""), chronic_condition),
#             dpi=200,
#             pad_inches=0,
#             bbox_inches="tight",
#             format="png",
#         )
#         #pdf.set_xy(x=60,y=y)
#         pdf.cell(100,8,
#                         txt= "", 
#                         ln=2,align="L")
#         x, y = pdf.get_x(),  pdf.get_y()
#         pdf.image(str(HERE / "outputs{}/Figure confusion matrix {}.png".format((" UK" if uk else ""), chronic_condition)),
#                     h=80,
#                     w=90,
#                     x=x,
#                     y=y,
#                 )
#         '''pdf.cell(5,0,
#                         txt= "", 
#                         ln=0,align="L")'''

        
#         # roc curve
#         fig = plot_roc_curve(model.data[model.target], model.data["Risk"], chronic_condition)
#         fig.savefig(HERE/ "outputs{}/Figure ROC {}.png".format((" UK" if uk else ""), chronic_condition),
#             dpi=200,
#             pad_inches=0,
#             bbox_inches="tight",
#             format="png",
#         )
#         '''pdf.cell(100,8,
#                         txt= "", 
#                         ln=0,align="L")'''
#         pdf.image(str(HERE / "outputs{}/Figure ROC {}.png".format((" UK" if uk else ""), chronic_condition)),
#                     h=70,
#                     w=80,
#                     x=x + 100,
#                     y=y,
#                 )
#         pdf.cell(200,4,
#                         txt= "", 
#                         ln=1,align="L")
        
#         # performance
#         def print_metrics(title, metrics, y, x=10):
#             pdf.set_xy(x,y)
#             pdf.set_font("Helvetica", size=12, style="B")
#             pdf.cell(60,10,
#                         txt= title,
#                         ln=2,align="L")
#             pdf.set_font("Helvetica", size=10) 
#             # target rate and datatpoints
#             pdf.cell(60,4,
#                     txt= "p-threshold: " + str(p_threshold) ,
#                     ln=2,align="L")
#             pdf.cell(60,4,
#                     txt= "Datapoints: " + str(metrics["Datapoints"]) ,
#                     ln=2,align="L")
#             pdf.cell(60,4,
#                     txt= "Target rate: " + str(round(100*metrics["Target rate"],2)) + "%", 
#                     ln=2,align="L")
#             # mortality rate and performance metrics
#             for metric in metrics:
#                 if metric in ["Datapoints","Target rate", "Balanced accuracy", "Accuracy", "Average precision", "Trigger_Readmission to hospital within 30 days"]:
#                     continue
#                 text = str(metric) +": " + str(round(metrics[metric],4))
#                 # if metric == "Mortality":
#                 #     text = str(metric) +": " + str(round(100*metrics[metric],2)) + "%"
#                 pdf.cell(60,4,
#                         txt= text, 
#                         ln=2,align="L")
#             pdf.cell(60,3,
#                         txt= "", 
#                         ln=2,align="L")
        
#         #y = pdf.get_y()
#         # add datapoints and target rate to metrics
#         y=y+90
#         for set in ["Train","Test"]:
#             x =10 if set=="Train" else 70
#             metrics = model.metrics[set]
#             subset = model.data[model.data["Set"]==set]
#             metrics["Datapoints"] = subset.shape[0]
#             metrics["Target rate"] = subset[model.target].mean()
#             print_metrics(set, metrics, x=x, y=y)
        
        

#     pdf.output(HERE / "pdfs{}/{}/LogisticRegression_{}_{}_{}.pdf".format((" UK" if uk else ""), name, name, date, version))


# THIS FUNCTION DOES NOT SHOW THE READMISSION RATES

# def generate_pdf_no_triggers(model_objects : dict, name : str, date : str, version: str, title : str, p_threshold : float, uk : bool = False):
#     """
#     Generate pdf from logistic regression models - for models only considering the conditions and not the triggers
#     Args:
#         model_objects (dict) : Dictionary containing model objects.
#         name (str) : Name of pdf
#         date (str) : Date to use in versioning of pdf e.g. 240202
#         version (str) : Version number to use in versioning of pdf e.g. v1p1
#         title (str) : Title in pdf header
#         p_threshold (float) : p-value threshold used in the model training
#         uk (bool) : Save in UK folders if True. Defaults to False.

#     """
#     pdf = FPDF(orientation="portrait", format=(220, 400))
#     ch = 10

#     for chronic_condition in sorted(model_objects):
#         model = model_objects[chronic_condition]
#         pdf.add_page()
#         # versioning
#         pdf.set_font("Helvetica", size=6) 
#         pdf.cell(200,3,
#                     txt= "Version_{}_{}".format(date,version), 
#                     ln=1,align="R")
        
#         # title
#         pdf.set_font("Helvetica", size=20, style="B")
#         pdf.cell(200,15,
#                     txt= str(title),
#                     ln=1,align="L")
        
#         # subtitle
#         pdf.set_font("Helvetica", size=16, style="B")
#         pdf.cell(200,15,
#                     txt= str(chronic_condition),
#                     ln=1,align="L")

#         # coefficients
#         y = pdf.get_y()
#         pdf.set_font("Helvetica", size=12, style="B")
#         pdf.cell(200,10,
#                     txt= "Coefficients",
#                     ln=1,align="L")
#         pdf.set_font("Helvetica", size=10) 
#         """for feature in model.coefs:
#             text = str(feature) + "   " + str(round(model.coefs[feature],4))
#             pdf.cell(200,4,
#                     txt= text, 
#                     ln=1,align="L")"""
#         features,coefs = visualise_coefficients(model.coefs)
#         for i in range(len(features)):
#             text = str(features[i]) + "   " + str(coefs[i])
#             pdf.cell(200,4,
#                     txt= text, 
#                     ln=1,align="L")
#         pdf.cell(200,4,
#                     txt= "", 
#                     ln=1,align="L")
        
#         # confusion matrix
#         model.confusion_matrix["Test"].savefig(HERE/ "outputs{}/Figure confusion matrix {}.png".format((" UK" if uk else ""), chronic_condition),
#             dpi=200,
#             pad_inches=0,
#             bbox_inches="tight",
#             format="png",
#         )
#         #pdf.set_xy(x=60,y=y)
#         pdf.cell(100,8,
#                         txt= "", 
#                         ln=2,align="L")
#         x, y = pdf.get_x(),  pdf.get_y()
#         pdf.image(str(HERE / "outputs{}/Figure confusion matrix {}.png".format((" UK" if uk else ""), chronic_condition)),
#                     h=80,
#                     w=90,
#                     x=x,
#                     y=y,
#                 )
#         '''pdf.cell(5,0,
#                         txt= "", 
#                         ln=0,align="L")'''

        
#         # roc curve
#         fig = plot_roc_curve(model.data[model.target], model.data["Risk"], chronic_condition)
#         fig.savefig(HERE/ "outputs{}/Figure ROC {}.png".format((" UK" if uk else ""), chronic_condition),
#             dpi=200,
#             pad_inches=0,
#             bbox_inches="tight",
#             format="png",
#         )
#         '''pdf.cell(100,8,
#                         txt= "", 
#                         ln=0,align="L")'''
#         pdf.image(str(HERE / "outputs{}/Figure ROC {}.png".format((" UK" if uk else ""), chronic_condition)),
#                     h=70,
#                     w=80,
#                     x=x + 100,
#                     y=y,
#                 )
#         pdf.cell(200,4,
#                         txt= "", 
#                         ln=1,align="L")
        
#         # performance
#         def print_metrics(title, metrics, y, x=10):
#             pdf.set_xy(x,y)
#             pdf.set_font("Helvetica", size=12, style="B")
#             pdf.cell(60,10,
#                         txt= title,
#                         ln=2,align="L")
#             pdf.set_font("Helvetica", size=10) 
#             # target rate and datatpoints
#             pdf.cell(60,4,
#                     txt= "p-threshold: " + str(p_threshold) ,
#                     ln=2,align="L")
#             pdf.cell(60,4,
#                     txt= "Datapoints: " + str(metrics["Datapoints"]) ,
#                     ln=2,align="L")
#             pdf.cell(60,4,
#                     txt= "Target rate: " + str(round(100*metrics["Target rate"],2)) + "%", 
#                     ln=2,align="L")
#             # mortality rate and performance metrics
#             for metric in metrics:
#                 if metric in ["Datapoints","Target rate", "Balanced accuracy", "Accuracy", "Average precision", "Trigger_Readmission to hospital within 30 days"]:
#                     continue
#                 text = str(metric) +": " + str(round(metrics[metric],4))
#                 # if metric == "Mortality":
#                 #     text = str(metric) +": " + str(round(100*metrics[metric],2)) + "%"
#                 pdf.cell(60,4,
#                         txt= text, 
#                         ln=2,align="L")
#             pdf.cell(60,3,
#                         txt= "", 
#                         ln=2,align="L")
        
#         #y = pdf.get_y()
#         # add datapoints and target rate to metrics
#         y=y+90
#         for set in ["Train","Test"]:
#             x =10 if set=="Train" else 70
#             metrics = model.metrics[set]
#             subset = model.data[model.data["Set"]==set]
#             metrics["Datapoints"] = subset.shape[0]
#             metrics["Target rate"] = subset[model.target].mean()
#             print_metrics(set, metrics, x=x, y=y)
        
        
#     pdf.output(HERE / "pdfs{}/No covid/{}/LogisticRegression_{}_{}_{}.pdf".format((" UK" if uk else ""), name, name, date, version))



def pdf_rates_included(model_objects : dict, name : str, date : str, version: str, title : str, p_threshold : float, uk : bool = False):
    """
    Generate pdf from logistic regression models - for models only considering the conditions and not the triggers
    Calculates the risk and plots the predicted readmission rates against actual readmission rate.
    Calculates the O/E ratio and plots over time.
    Creates a dataframe with predicted rates, real rates, and O/E ratios over the years and overall
    Args:
        model_objects (dict) : Dictionary containing model objects.
        name (str) : Name of pdf
        date (str) : Date to use in versioning of pdf e.g. 240202
        version (str) : Version number to use in versioning of pdf e.g. v1p1
        title (str) : Title in pdf header
        p_threshold (float) : p-value threshold used in the model training
        uk (bool) : Save in UK folders if True. Defaults to False.
    """
    pdf = FPDF(orientation="portrait", format=(220, 400))
    ch = 10

    for chronic_condition in sorted(model_objects):
        model = model_objects[chronic_condition]
        pdf.add_page()
        # versioning
        pdf.set_font("Helvetica", size=6) 
        pdf.cell(200,3,
                    txt= "Version_{}_{}".format(date,version), 
                    ln=1,align="R")
        
        # title
        pdf.set_font("Helvetica", size=20, style="B")
        pdf.cell(200,15,
                    txt= str(title),
                    ln=1,align="L")
        
        # subtitle
        pdf.set_font("Helvetica", size=16, style="B")
        pdf.cell(200,15,
                    txt= str(chronic_condition),
                    ln=1,align="L")

        # coefficients
        y = pdf.get_y()
        pdf.set_font("Helvetica", size=12, style="B")
        pdf.cell(200,10,
                    txt= "Coefficients",
                    ln=1,align="L")
        pdf.set_font("Helvetica", size=10) 
        """for feature in model.coefs:
            text = str(feature) + "   " + str(round(model.coefs[feature],4))
            pdf.cell(200,4,
                    txt= text, 
                    ln=1,align="L")"""
        features,coefs = visualise_coefficients(model.coefs)
        for i in range(len(features)):
            text = str(features[i]) + "   " + str(coefs[i])
            pdf.cell(200,4,
                    txt= text, 
                    ln=1,align="L")
        pdf.cell(200,4,
                    txt= "", 
                    ln=1,align="L")
        
        # confusion matrix
        model.confusion_matrix["Test"].savefig(HERE/ "outputs{}/Figure confusion matrix {}.png".format((" UK" if uk else ""), chronic_condition),
            dpi=200,
            pad_inches=0,
            bbox_inches="tight",
            format="png",
        )
        #pdf.set_xy(x=60,y=y)
        pdf.cell(100,8,
                        txt= "", 
                        ln=2,align="L")
        x, y = pdf.get_x(),  pdf.get_y()
        pdf.image(str(HERE / "outputs{}/Figure confusion matrix {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=80,
                    w=90,
                    x=x,
                    y=y,
                )
        '''pdf.cell(5,0,
                        txt= "", 
                        ln=0,align="L")'''

        
        # roc curve
        fig = plot_roc_curve(model.data[model.target], model.data["Risk"], chronic_condition)
        fig.savefig(HERE/ "outputs{}/Figure ROC {}.png".format((" UK" if uk else ""), chronic_condition),
            dpi=200,
            pad_inches=0,
            bbox_inches="tight",
            format="png",
        )
        '''pdf.cell(100,8,
                        txt= "", 
                        ln=0,align="L")'''
        pdf.image(str(HERE / "outputs{}/Figure ROC {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=70,
                    w=80,
                    x=x + 100,
                    y=y,
                )
        pdf.cell(200,4,
                        txt= "", 
                        ln=1,align="L")
        
        # performance
        def print_metrics(title, metrics, y, x=10):
            pdf.set_xy(x,y)
            pdf.set_font("Helvetica", size=12, style="B")
            pdf.cell(60,10,
                        txt= title,
                        ln=2,align="L")
            pdf.set_font("Helvetica", size=10) 
            # target rate and datatpoints
            pdf.cell(60,4,
                    txt= "p-threshold: " + str(p_threshold) ,
                    ln=2,align="L")
            pdf.cell(60,4,
                    txt= "Datapoints: " + str(metrics["Datapoints"]) ,
                    ln=2,align="L")
            pdf.cell(60,4,
                    txt= "Target rate: " + str(round(100*metrics["Target rate"],2)) + "%", 
                    ln=2,align="L")
            # mortality rate and performance metrics
            for metric in metrics:
                if metric in ["Datapoints","Target rate", "Balanced accuracy", "Accuracy", "Average precision", "Trigger_Readmission to hospital within 30 days"]:
                    continue
                text = str(metric) +": " + str(round(metrics[metric],4))
                # if metric == "Mortality":
                #     text = str(metric) +": " + str(round(100*metrics[metric],2)) + "%"
                pdf.cell(60,4,
                        txt= text, 
                        ln=2,align="L")
            pdf.cell(60,3,
                        txt= "", 
                        ln=2,align="L")
        
        #y = pdf.get_y()
        # add datapoints and target rate to metrics
        y=y+90
        for set in ["Train","Test"]:
            x =10 if set=="Train" else 70
            metrics = model.metrics[set]
            subset = model.data[model.data["Set"]==set]
            metrics["Datapoints"] = subset.shape[0]
            metrics["Target rate"] = subset[model.target].mean()
            print_metrics(set, metrics, x=x, y=y)

        pdf.add_page()
        pdf.set_font("Helvetica", size=16, style="B")
        pdf.cell(200,15,
                    txt= str('Risk Adjusted Readmission Rates - Summing Risk Method'),
                    ln=1,align="L")
        
        y = pdf.get_y()
        
        years = [2019, 2020, 2021, 2022, 2023]
        real_rates_overall, pred_rates_risk_overall, overall_o_e_risk = overall_readmission_rates_risk(model.data, years) 
        years, real_rates, pred_rates, O_E_ratio = find_readmission_rates_and_OE_risk(model.data, years)
        df_risk = readmission_dataframe(years, real_rates, pred_rates, O_E_ratio, real_rates_overall, pred_rates_risk_overall, overall_o_e_risk)

        dfi.export(df_risk, HERE/ "outputs{}/Figure df_risk {}.png".format((" UK" if uk else ""), chronic_condition))
        pdf.image(str(HERE/ "outputs{}/Figure df_risk {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=40,
                    w=110,
                    x=x-45,
                    y=y+5,
                )
        pdf.cell(200,4,
                        txt= "", 
                        ln=1,align="L")
        
        fig = plot_rates_subplots(years, real_rates, pred_rates, O_E_ratio, title)
        plt.savefig(HERE/ "outputs{}/Figure plot_risk {}.png".format((" UK" if uk else ""), chronic_condition))
        pdf.image(str(HERE/ "outputs{}/Figure plot_risk {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=120,
                    w=200,
                    x=x-65,
                    y=y+50,
                )
        pdf.cell(200,4,
                        txt= "", 
                        ln=1,align="L")
        
        y=y+167
        x=x-60
        pdf.set_xy(x,y)
        pdf.set_font("Helvetica", size=16, style="B")
        pdf.cell(200,15,
                    txt= str('Risk Adjusted Readmission Rates - Setting Threshold Method'),
                    ln=1,align="L")
        

        years = [2019, 2020, 2021, 2022, 2023]
        real_rates_overall, pred_rates_risk_overall, overall_o_e_risk = overall_readmission_rates_threshold(model.data, years) 
        years, real_rates, pred_rates, O_E_ratio = find_readmission_rates_and_OE_threshold(model.data, years)
        df_risk = readmission_dataframe(years, real_rates, pred_rates, O_E_ratio, real_rates_overall, pred_rates_risk_overall, overall_o_e_risk)

        dfi.export(df_risk, HERE/ "outputs{}/Figure df_th {}.png".format((" UK" if uk else ""), chronic_condition))
        pdf.image(str(HERE/ "outputs{}/Figure df_th {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=40,
                    w=110,
                    x=x+15,
                    y=y+23,
                )
        pdf.cell(200,4,
                        txt= "", 
                        ln=1,align="L")
        
        fig = plot_rates_subplots(years, real_rates, pred_rates, O_E_ratio, title)
        plt.savefig(HERE/ "outputs{}/Figure plot_th {}.png".format((" UK" if uk else ""), chronic_condition))
        pdf.image(str(HERE/ "outputs{}/Figure plot_th {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=120,
                    w=200,
                    x=x-5,
                    y=y+73,
                )
        pdf.cell(200,4,
                        txt= "", 
                        ln=1,align="L")
        
    pdf.output(HERE / "pdfs{}/Test/{}/LogisticRegression_{}_{}_{}.pdf".format((" UK" if uk else ""), name, name, date, version))
    

def pdf_rates_included_const_th(model_objects : dict, name : str, date : str, version: str, title : str, p_threshold : float, uk : bool = False):
    """
    Generate pdf from logistic regression models - for models only considering the conditions and not the triggers
    Calculates the risk and plots the predicted readmission rates against actual readmission rate.
    Calculates the O/E ratio and plots over time.
    Creates a dataframe with predicted rates, real rates, and O/E ratios over the years and overall.

    Args:
        model_objects (dict) : Dictionary containing model objects.
        name (str) : Name of pdf
        date (str) : Date to use in versioning of pdf e.g. 240202
        version (str) : Version number to use in versioning of pdf e.g. v1p1
        title (str) : Title in pdf header
        p_threshold (float) : p-value threshold used in the model training
        uk (bool) : Save in UK folders if True. Defaults to False.
    """
    pdf = FPDF(orientation="portrait", format=(220, 400))
    ch = 10

    for chronic_condition in sorted(model_objects):
        model = model_objects[chronic_condition]
        pdf.add_page()
        # versioning
        pdf.set_font("Helvetica", size=6) 
        pdf.cell(200,3,
                    txt= "Version_{}_{}".format(date,version), 
                    ln=1,align="R")
        
        # title
        pdf.set_font("Helvetica", size=20, style="B")
        pdf.cell(200,15,
                    txt= str(title),
                    ln=1,align="L")
        
        # subtitle
        pdf.set_font("Helvetica", size=16, style="B")
        pdf.cell(200,15,
                    txt= str(chronic_condition),
                    ln=1,align="L")

        # coefficients
        y = pdf.get_y()
        pdf.set_font("Helvetica", size=12, style="B")
        pdf.cell(200,10,
                    txt= "Coefficients",
                    ln=1,align="L")
        pdf.set_font("Helvetica", size=10) 
        """for feature in model.coefs:
            text = str(feature) + "   " + str(round(model.coefs[feature],4))
            pdf.cell(200,4,
                    txt= text, 
                    ln=1,align="L")"""
        features,coefs = visualise_coefficients(model.coefs)
        for i in range(len(features)):
            text = str(features[i]) + "   " + str(coefs[i])
            pdf.cell(200,4,
                    txt= text, 
                    ln=1,align="L")
        pdf.cell(200,4,
                    txt= "", 
                    ln=1,align="L")
        
        # confusion matrix
        model.confusion_matrix["Test"].savefig(HERE/ "outputs{}/Figure confusion matrix {}.png".format((" UK" if uk else ""), chronic_condition),
            dpi=200,
            pad_inches=0,
            bbox_inches="tight",
            format="png",
        )
        #pdf.set_xy(x=60,y=y)
        pdf.cell(100,8,
                        txt= "", 
                        ln=2,align="L")
        x, y = pdf.get_x(),  pdf.get_y()
        pdf.image(str(HERE / "outputs{}/Figure confusion matrix {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=80,
                    w=90,
                    x=x,
                    y=y,
                )
        '''pdf.cell(5,0,
                        txt= "", 
                        ln=0,align="L")'''

        
        # roc curve
        fig = plot_roc_curve(model.data[model.target], model.data["Risk"], chronic_condition)
        fig.savefig(HERE/ "outputs{}/Figure ROC {}.png".format((" UK" if uk else ""), chronic_condition),
            dpi=200,
            pad_inches=0,
            bbox_inches="tight",
            format="png",
        )
        '''pdf.cell(100,8,
                        txt= "", 
                        ln=0,align="L")'''
        pdf.image(str(HERE / "outputs{}/Figure ROC {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=70,
                    w=80,
                    x=x + 100,
                    y=y,
                )
        pdf.cell(200,4,
                        txt= "", 
                        ln=1,align="L")
        
        # performance
        def print_metrics(title, metrics, y, x=10):
            pdf.set_xy(x,y)
            pdf.set_font("Helvetica", size=12, style="B")
            pdf.cell(60,10,
                        txt= title,
                        ln=2,align="L")
            pdf.set_font("Helvetica", size=10) 
            # target rate and datatpoints
            pdf.cell(60,4,
                    txt= "p-threshold: " + str(p_threshold) ,
                    ln=2,align="L")
            pdf.cell(60,4,
                    txt= "Datapoints: " + str(metrics["Datapoints"]) ,
                    ln=2,align="L")
            pdf.cell(60,4,
                    txt= "Target rate: " + str(round(100*metrics["Target rate"],2)) + "%", 
                    ln=2,align="L")
            # mortality rate and performance metrics
            for metric in metrics:
                if metric in ["Datapoints","Target rate", "Balanced accuracy", "Accuracy", "Average precision", "Trigger_Readmission to hospital within 30 days"]:
                    continue
                text = str(metric) +": " + str(round(metrics[metric],4))
                # if metric == "Mortality":
                #     text = str(metric) +": " + str(round(100*metrics[metric],2)) + "%"
                pdf.cell(60,4,
                        txt= text, 
                        ln=2,align="L")
            pdf.cell(60,3,
                        txt= "", 
                        ln=2,align="L")
        
        #y = pdf.get_y()
        # add datapoints and target rate to metrics
        y=y+90
        for set in ["Train","Test"]:
            x =10 if set=="Train" else 70
            metrics = model.metrics[set]
            subset = model.data[model.data["Set"]==set]
            metrics["Datapoints"] = subset.shape[0]
            metrics["Target rate"] = subset[model.target].mean()
            print_metrics(set, metrics, x=x, y=y)

        pdf.add_page()
        pdf.set_font("Helvetica", size=16, style="B")
        pdf.cell(200,15,
                    txt= str('Risk Adjusted Readmission Rates - Summing Risk Method'),
                    ln=1,align="L")
        
        y = pdf.get_y()
        
        years = [2019, 2020, 2021, 2022, 2023]
        real_rates_overall, pred_rates_risk_overall, overall_o_e_risk = overall_readmission_rates_risk(model.data, years) 
        years, real_rates, pred_rates, O_E_ratio = find_readmission_rates_and_OE_risk(model.data, years)
        df_risk = readmission_dataframe(years, real_rates, pred_rates, O_E_ratio, real_rates_overall, pred_rates_risk_overall, overall_o_e_risk)

        dfi.export(df_risk, HERE/ "outputs{}/Figure df_risk {}.png".format((" UK" if uk else ""), chronic_condition))
        pdf.image(str(HERE/ "outputs{}/Figure df_risk {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=40,
                    w=110,
                    x=x-45,
                    y=y+5,
                )
        pdf.cell(200,4,
                        txt= "", 
                        ln=1,align="L")
        
        fig = plot_rates_subplots(years, real_rates, pred_rates, O_E_ratio, title)
        plt.savefig(HERE/ "outputs{}/Figure plot_risk {}.png".format((" UK" if uk else ""), chronic_condition))
        pdf.image(str(HERE/ "outputs{}/Figure plot_risk {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=120,
                    w=200,
                    x=x-65,
                    y=y+50,
                )
        pdf.cell(200,4,
                        txt= "", 
                        ln=1,align="L")
        
        y=y+167
        x=x-60
        pdf.set_xy(x,y)
        pdf.set_font("Helvetica", size=16, style="B")
        pdf.cell(200,15,
                    txt= str('Risk Adjusted Readmission Rates - Setting Threshold Method'),
                    ln=1,align="L")
        

        years = [2019, 2020, 2021, 2022, 2023] 
        real_rates_overall, pred_rates_risk_overall, overall_o_e_risk = overall_readmission_rates_threshold(model.data, years) 
        years, real_rates, pred_rates, O_E_ratio = find_readmission_rates_and_OE_constant_threshold(model.data, years)
        df_risk = readmission_dataframe(years, real_rates, pred_rates, O_E_ratio, real_rates_overall, pred_rates_risk_overall, overall_o_e_risk)

        dfi.export(df_risk, HERE/ "outputs{}/Figure df_th {}.png".format((" UK" if uk else ""), chronic_condition))
        pdf.image(str(HERE/ "outputs{}/Figure df_th {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=40,
                    w=110,
                    x=x+15,
                    y=y+23,
                )
        pdf.cell(200,4,
                        txt= "", 
                        ln=1,align="L")
        
        fig = plot_rates_subplots(years, real_rates, pred_rates, O_E_ratio, title)
        plt.savefig(HERE/ "outputs{}/Figure plot_th {}.png".format((" UK" if uk else ""), chronic_condition))
        pdf.image(str(HERE/ "outputs{}/Figure plot_th {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=120,
                    w=200,
                    x=x-5,
                    y=y+73,
                )
        pdf.cell(200,4,
                        txt= "", 
                        ln=1,align="L")
        
    pdf.output(HERE / "pdfs{}/Test/Date_Ranges/LogisticRegression_{}_{}_{}.pdf".format((" UK" if uk else ""), name, date, version))


# This is the function to use going forward

def generate_pdf(model_objects : dict, name : str, date : str, version: str, title : str, p_threshold : float, uk : bool = False):
    """
    Generate pdf from logistic regression models - for models only considering the conditions and not the triggers
    Calculates the risk and plots the predicted readmission rates against actual readmission rate.
    Calculates the O/E ratio and plots over time.
    Only shows plots using the summing risk method.
    Creates a dataframe with predicted rates, real rates, and O/E ratios over the years and overall.
    
    Args:
        model_objects (dict) : Dictionary containing model objects.
        name (str) : Name of pdf
        date (str) : Date to use in versioning of pdf e.g. 240202
        version (str) : Version number to use in versioning of pdf e.g. v1p1
        title (str) : Title in pdf header
        p_threshold (float) : p-value threshold used in the model training
        uk (bool) : Save in UK folders if True. Defaults to False.
    """
    pdf = FPDF(orientation="portrait", format=(220, 400))
    ch = 10

    for chronic_condition in sorted(model_objects):
        model = model_objects[chronic_condition]
        pdf.add_page()
        # versioning
        pdf.set_font("Helvetica", size=6) 
        pdf.cell(200,3,
                    txt= "Version_{}_{}".format(date,version), 
                    ln=1,align="R")
        
        # title
        pdf.set_font("Helvetica", size=20, style="B")
        pdf.cell(200,15,
                    txt= str(title),
                    ln=1,align="L")
        
        # subtitle
        pdf.set_font("Helvetica", size=16, style="B")
        pdf.cell(200,15,
                    txt= str(chronic_condition),
                    ln=1,align="L")

        # coefficients
        y = pdf.get_y()
        pdf.set_font("Helvetica", size=12, style="B")
        pdf.cell(200,10,
                    txt= "Coefficients",
                    ln=1,align="L")
        pdf.set_font("Helvetica", size=10) 
        """for feature in model.coefs:
            text = str(feature) + "   " + str(round(model.coefs[feature],4))
            pdf.cell(200,4,
                    txt= text, 
                    ln=1,align="L")"""
        features,coefs = visualise_coefficients(model.coefs)
        for i in range(len(features)):
            text = str(features[i]) + "   " + str(coefs[i])
            pdf.cell(200,4,
                    txt= text, 
                    ln=1,align="L")
        pdf.cell(200,4,
                    txt= "", 
                    ln=1,align="L")
        
        # confusion matrix
        model.confusion_matrix["Test"].savefig(HERE/ "outputs{}/Figure confusion matrix {}.png".format((" UK" if uk else ""), chronic_condition),
            dpi=200,
            pad_inches=0,
            bbox_inches="tight",
            format="png",
        )
        #pdf.set_xy(x=60,y=y)
        pdf.cell(100,8,
                        txt= "", 
                        ln=2,align="L")
        x, y = pdf.get_x(),  pdf.get_y()
        pdf.image(str(HERE / "outputs{}/Figure confusion matrix {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=80,
                    w=90,
                    x=x,
                    y=y,
                )
        '''pdf.cell(5,0,
                        txt= "", 
                        ln=0,align="L")'''

        
        # roc curve
        fig = plot_roc_curve(model.data[model.target], model.data["Risk"], chronic_condition)
        fig.savefig(HERE/ "outputs{}/Figure ROC {}.png".format((" UK" if uk else ""), chronic_condition),
            dpi=200,
            pad_inches=0,
            bbox_inches="tight",
            format="png",
        )
        '''pdf.cell(100,8,
                        txt= "", 
                        ln=0,align="L")'''
        pdf.image(str(HERE / "outputs{}/Figure ROC {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=70,
                    w=80,
                    x=x + 100,
                    y=y,
                )
        pdf.cell(200,4,
                        txt= "", 
                        ln=1,align="L")
        
        # performance
        def print_metrics(title, metrics, y, x=10):
            pdf.set_xy(x,y)
            pdf.set_font("Helvetica", size=12, style="B")
            pdf.cell(60,10,
                        txt= title,
                        ln=2,align="L")
            pdf.set_font("Helvetica", size=10) 
            # target rate and datatpoints
            pdf.cell(60,4,
                    txt= "p-threshold: " + str(p_threshold) ,
                    ln=2,align="L")
            pdf.cell(60,4,
                    txt= "Datapoints: " + str(metrics["Datapoints"]) ,
                    ln=2,align="L")
            pdf.cell(60,4,
                    txt= "Target rate: " + str(round(100*metrics["Target rate"],2)) + "%", 
                    ln=2,align="L")
            # mortality rate and performance metrics
            for metric in metrics:
                if metric in ["Datapoints","Target rate", "Balanced accuracy", "Accuracy", "Average precision", "Trigger_Readmission to hospital within 30 days"]:
                    continue
                text = str(metric) +": " + str(round(metrics[metric],4))
                # if metric == "Mortality":
                #     text = str(metric) +": " + str(round(100*metrics[metric],2)) + "%"
                pdf.cell(60,4,
                        txt= text, 
                        ln=2,align="L")
            pdf.cell(60,3,
                        txt= "", 
                        ln=2,align="L")
        
        #y = pdf.get_y()
        # add datapoints and target rate to metrics
        y=y+90
        for set in ["Train","Test"]:
            x =10 if set=="Train" else 70
            metrics = model.metrics[set]
            subset = model.data[model.data["Set"]==set]
            metrics["Datapoints"] = subset.shape[0]
            metrics["Target rate"] = subset[model.target].mean()
            print_metrics(set, metrics, x=x, y=y)

        pdf.add_page()
        pdf.set_font("Helvetica", size=16, style="B")
        pdf.cell(200,15,
                    txt= str('Risk Adjusted Readmission Rates - Summing Risk Method'),
                    ln=1,align="L")
        
        y = pdf.get_y()
        
        years = [2019, 2020, 2021, 2022, 2023]
        real_rates_overall, pred_rates_risk_overall, overall_o_e_risk = overall_readmission_rates_risk(model.data, years) 
        years, real_rates, pred_rates, O_E_ratio = find_readmission_rates_and_OE_risk(model.data, years)
        df_risk = readmission_dataframe(years, real_rates, pred_rates, O_E_ratio, real_rates_overall, pred_rates_risk_overall, overall_o_e_risk)

        dfi.export(df_risk, HERE/ "outputs{}/Figure df_risk {}.png".format((" UK" if uk else ""), chronic_condition))
        pdf.image(str(HERE/ "outputs{}/Figure df_risk {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=40,
                    w=110,
                    x=x-45,
                    y=y+5,
                )
        pdf.cell(200,4,
                        txt= "", 
                        ln=1,align="L")
        
        fig = plot_rates_subplots(years, real_rates, pred_rates, O_E_ratio, title)
        plt.savefig(HERE/ "outputs{}/Figure plot_risk {}.png".format((" UK" if uk else ""), chronic_condition))
        pdf.image(str(HERE/ "outputs{}/Figure plot_risk {}.png".format((" UK" if uk else ""), chronic_condition)),
                    h=120,
                    w=200,
                    x=x-65,
                    y=y+50,
                )
        pdf.cell(200,4,
                        txt= "", 
                        ln=1,align="L")    
        
    pdf.output(HERE / "pdfs{}/LogisticRegression_{}_{}_{}.pdf".format((" UK" if uk else ""), name, date, version))


