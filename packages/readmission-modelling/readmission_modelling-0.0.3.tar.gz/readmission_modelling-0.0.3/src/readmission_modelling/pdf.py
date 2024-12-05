import pathlib
import os
from fpdf import FPDF
from tqdm import tqdm
import shutil
from datetime import datetime

HERE = pathlib.Path("..").resolve().parent.parent


"""
Functions used for pdf generation

"""


def create_pdf(width: int = 220, height: int = 400):
    pdf = FPDF(orientation="portrait", format=(width, height))
    return pdf


# TODO - move these to FPDF class definition - see camgenium package version of PTL package 
def add_header_title(
    pdf: FPDF, title: str, subtitle: str = "", date: str = "", version: str = "v1p0"
):

    # versioning and datestamp
    if date == "":
        date = datetime.now().strftime("%y%m%d")
    pdf.set_font("Helvetica", size=6)
    pdf.cell(200, 3, txt=f"Version_{date}_{version}", ln=1, align="R")

    # title and subtitle
    pdf.set_font("Helvetica", size=20, style="B")
    pdf.cell(200, 15, txt=str(title), ln=1, align="L")
    if subtitle != "":
        pdf.set_font("Helvetica", size=16, style="B")
        pdf.cell(200, 15, txt=str(subtitle), ln=1, align="L")

    return pdf


def add_subtitle(pdf, title):
    pdf.set_font("Helvetica", size=12, style="B")
    pdf.cell(60, 10, txt=title, ln=2, align="L")

    return pdf


# performance
def print_metrics(pdf, title, metrics, y, x=10):
    pdf.set_xy(x, y)
    pdf.set_font("Helvetica", size=12, style="B")
    pdf.cell(60, 10, txt=title, ln=2, align="L")
    pdf.set_font("Helvetica", size=10)
    # target rate and datatpoints
    if "Datapoints" in metrics.keys():
        pdf.cell(60, 4, txt="Datapoints: " + str(metrics["Datapoints"]), ln=2, align="L")
    if "Proportion" in metrics.keys():
        pdf.cell(60, 4, txt="Proportion: " + str(metrics["Proportion"]) + "%", ln=2, align="L")
    
    pdf.cell(
        60,
        4,
        txt="Target rate: " + str(round(100 * metrics["Target rate"], 2)) + "%",
        ln=2,
        align="L",
    )
    # mortality rate and performance metrics
    for metric in metrics:
        if metric in [
            "Datapoints",
            "Proportion",
            "Target rate",
            "Balanced accuracy",
            "Accuracy",
            "Average precision",
        ]:
            continue
        text = str(metric) + ": " + str(round(metrics[metric], 4))
        if metric in ["Mortality", "Mean of predictions"]:
            text = str(metric) + ": " + str(round(100 * metrics[metric], 2)) + "%"
        pdf.cell(60, 4, txt=text, ln=2, align="L")
    pdf.cell(60, 3, txt="", ln=2, align="L")

    return pdf


def add_image(pdf, image, image_filepath, x: int = -1, y: int = -1, h : int = 70, w : int = 80):
    # save image to location
    image.savefig(
            image_filepath,
            dpi=200,
            pad_inches=0,
            bbox_inches="tight",
            format="png",
        )
    # open image and place in pdf 
    if x == -1:
        x = pdf.get_x()
    if y == -1:
        y = pdf.get_y()
    pdf.cell(100, h, txt="", ln=1, align="L")
    pdf.image(
        str(image_filepath),
        h=h,
        w=w,
        x=x,
        y=y,
    )
    pdf.cell(100, 8, txt="", ln=1, align="L")
    return pdf 
    
    
def add_metrics(pdf, metrics : dict, title : str = "", x : int = 10):
    pdf.set_x(x)
    if title!="":
        pdf.set_font("Helvetica", size=12, style="B")
        pdf.cell(60, 10, txt=title, ln=2, align="L")
    pdf.set_font("Helvetica", size=10)
    
    for metric in metrics:
        #FIXME - generalise this e.g. add to_round parameters list
        if metric == "count":
            text = str(metric) + ": " + str(int(metrics[metric]))
            
        else:
            text = str(metric) + ": " + str(round(100* metrics[metric],2))
        pdf.cell(60, 4, txt=text, ln=2, align="L")
    pdf.cell(60, 3, txt="", ln=2, align="L")

    return pdf


def save_pdf(pdf, filepath, name : str = "", date : str = "", version : str = "v1p0"):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    if date=="":
        date = datetime.now().strftime("%y%m%d")
    filename = f"{name}_{date}_{version}.pdf"
    pdf.output(filepath / filename)


def generate_pdf(
    model_objects: dict,
    name: str,
    date: str,
    version: str,
    title: str,
    save_filepath=HERE / "XGBoost_outputs",
    pdf_save_filepath=HERE / "XGBoost_pdfs",
    plot_importance=False,
):
    """
    Generate pdf from dictionary of trained models with stored outputs.
    Args:
        model_objects (dict) : Dictionary containing model objects. Expected kets are 'LogisticRegression' and 'XGBoost'.
        name (str) : Name prefix of pdf
        date (str) : Date to use in versioning of pdf e.g. 240202
        version (str) : Version number to use in versioning of pdf e.g. v1p1
        title (str) : Title in pdf header
        save_filepath : filepath in which to save figures temporarily
        pdf_save_filepath : filepath in which to save pdfs
    """
    
    # create temp directory to store figures in - make sure it doesn't already exist, else will be deleted
    temp_image_filepath = save_filepath / "temporary"
    if os.path.exists(temp_image_filepath):
        delete = input("Temporary directory already exists and will be deleted. Continue? (Y/N) : ")
        if delete == "Y":
            shutil.rmtree(temp_image_filepath)
        else:
            raise Warning("Temporary directory already exists and would have been deleted. Rename directory.") 
            
    os.makedirs(temp_image_filepath)
    
    # create pdf 
    pdf = create_pdf()

    # iterate though each model
    for model_i in model_objects.keys():
        model = model_objects[model_i]
        pdf.add_page()
        pdf = add_header_title(pdf, title=title, subtitle=model_i, date=date, version=version)
        y = pdf.get_y()

        # add prportion of datapoints train vs test
        proportion = {}
        tot = 0
        for set_data in ["Train","Test"]:
            metrics = model.metrics[set_data]
            proportion[set_data] = metrics["Datapoints"]
            tot+= metrics["Datapoints"]
        for set_data in ["Train","Test"]:
            metrics = model.metrics[set_data]
            metrics["Proportion"] = round(100 * proportion[set_data] / tot, 2) 
        # print metrics 
        for set_name in ["Train","Test"]:
            x = 10 if set_name == "Train" else 70
            metrics = model.metrics[set_name]
            print_metrics(pdf, title= set_name, metrics=metrics, x=x, y=y)

        # confusion matrix
        model.confusion_matrix["Test"].savefig(HERE/ f"outputs/Figure confusion matrix {model_i}.png",
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
        pdf.image(str(HERE / f"outputs/Figure confusion matrix {model_i}.png"),
                    h=80,
                    w=90,
                    x=x-60,
                    y=y,
                )
        
        # roc curve
        model.roc_curve["Test"].savefig(HERE/ f"outputs/Figure ROC {model_i}.png",
            dpi=200,
            pad_inches=0,
            bbox_inches="tight",
            format="png",
        )

        pdf.image(str(HERE / f"outputs/Figure ROC {model_i}.png"),
                    h=70,
                    w=80,
                    x=x + 60,
                    y=y,
                )
           
        # feature importance chart
        pdf.add_page()

        model.feature_importance.savefig(HERE/ f"outputs/Figure feature importance {model_i}.png",
            dpi=200,
            pad_inches=0,
            bbox_inches="tight",
            format="png",
        )

        image_filepath = temp_image_filepath / f"Figure feature importance {model_i}.png"
        image = model.feature_importance
        add_image(pdf, image, image_filepath, h=120, w=200)
    
        
    # delete temp folder
    shutil.rmtree(temp_image_filepath)
    
    save_pdf(pdf, pdf_save_filepath, name, date, version)
