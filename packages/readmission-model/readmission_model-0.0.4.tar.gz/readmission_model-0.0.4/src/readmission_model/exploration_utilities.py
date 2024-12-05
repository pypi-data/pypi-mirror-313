import pandas as pd
import pathlib
import seaborn as sns
import pickle
import matplotlib.pyplot as plt
import math


HERE = pathlib.Path('..').resolve().parent


# ## DATA IMPORT

# # US
DATA = pd.read_csv(HERE / "Data/Processed Data.csv", low_memory=False)
DATAORIGINAL = pd.read_csv(HERE / "Data/Processed Data_original_method.csv", low_memory=False)


## EXCLUSIONS

# triggers no longer being used
triggers_exclude = [
    "Trigger_Readmission to intensive care",
    "Trigger_Transfer to higher level of care",
    "Trigger_Unplanned admission to intensive care",
    "Trigger_Removal/Injury or repair of organ",
    "Trigger_Complication of procedure or treatment",
    "Trigger_Wound infection",
    "Trigger_Return to Theatre or Operating room",
    "Trigger_Change in planned procedure",
    "Trigger_Readmission to hospital within 30 days",
    "Trigger_Staph aureus septicaemia",
]

# drop these features due to high correlations with other triggers
to_drop_corr_chosen = [
    "Trigger_Administration of glucagon or 50% glucose",
    "Trigger_Conditions associated with a raised troponin",
    "Trigger_Transfusion",
    "Trigger_DVT/PE following admission",
    "Trigger_High INR causing haemorrhage",
    # "Trigger_Hospital acquired chest infection",
]



## NAMES

# Triggers and Conditions
trigger_to_name = {
    "Clinical sepsis": "Clinical sepsis",
    "Acute kidney injury": "AKI",
    "Hospital acquired chest infection": "HAP",
    "Shock or cardiac arrest": "Shock",
    "Lack of early warning score or early warning score requiring response": "EWS",
}
top_triggers = list(trigger_to_name.keys())
top_conditions = [
    "Chronic pulmonary disease",
    "Dementia",
    "Diabetes",
    "Ischaemic heart disease",
    "Myocardial infarction",
    "Named infectious disease",
    "Pneumonia",
    "Stroke",
    "Heart failure",  # added 22/04/24
]


# for UK data, Y95 present indicates condition was POAN - update: requirement removed
df_poan_pneumonia_opids = pd.DataFrame()



def get_trigger_data(trigger: str, uk: bool = False):
    """
    Return subset of data where patients have the trigger, for the trigger models (mortality predictor)
    Args:
        trigger (str) : trigger for which to get data
        uk (bool) : whether to use UK (True) or US (False) data. Defaults to False.
    """
    data = DATA_UK if uk else DATA

    trigger_col = "Trigger_" + str(trigger)
    mask = data[trigger_col] == 1

    # if HAP, take POA=N only
    if trigger == "Hospital acquired chest infection":
        # update - remove HA requirement for UK data - take HAP column only (see 'POAN Analysis' for justification)
        """
        if uk:
            mask = data["AdmissionRef"].isin(df_poan_pneumonia_opids["AdmissionRef"])
        else:
            mask = (data[trigger_col] == 1) & (data[str(trigger_col) + "_POAN"] == 0)
        """
        if uk == False:
            mask = (data[trigger_col] == 1) & (data[str(trigger_col) + "_POAN"] == 0)
    df_trigger = data[mask]
    return df_trigger


def get_chronic_data(chronic_condition: str, uk: bool = False):
    """
    Return subset of data where patients have the chronic condition, for the chronic condition models (mortality predictor)
    Args:
        chronic_condition (str) : chronic condition for which to get data
        uk (bool) : whether to use UK (True) or US (False) data. Defaults to False.

    """
    data = DATA_UK if uk else DATA

    condition_col = "Condition_" + str(chronic_condition)
    mask = data[condition_col] == 1
    df_condition = data[mask]
    return df_condition

def get_chronic_data_original_method(chronic_condition: str, uk: bool = False):
    """
    Return subset of data where patients have the chronic condition, for the chronic condition models (mortality predictor)
    Args:
        chronic_condition (str) : chronic condition for which to get data
        uk (bool) : whether to use UK (True) or US (False) data. Defaults to False.

    """
    data = DATA_UK if uk else DATAORIGINAL

    condition_col = "Condition_" + str(chronic_condition)
    mask = data[condition_col] == 1
    df_condition = data[mask]
    return df_condition


def plot_percentage_trigger(trigger: str, uk: bool = False):
    """
    Plot trigger incidence with age
    Args:
        trigger (str) : trigger for which to plot incidence
        uk (bool) : whether to use UK (True) or US (False) data. Defaults to False.

    """
    data = DATA_UK if uk else DATA

    name = trigger_to_name[trigger]
    trigger_col = "Trigger_" + str(trigger)
    perc, perc_non, ages = [], [], []
    # subset dataframe
    df_plot = data.copy()

    for age in sorted(df_plot["Age"].unique()):
        if math.isnan(age) == False:
            ages.append(age)
            perc.append(
                df_plot.loc[
                    ((df_plot["Age"] == age) & (df_plot[trigger_col] == 1))
                ].shape[0]
                / df_plot.loc[df_plot.Age == age].shape[0]
            )
            perc_non.append(
                df_plot.loc[
                    ((df_plot["Age"] == age) & (df_plot[trigger_col] == 0))
                ].shape[0]
                / df_plot.loc[df_plot.Age == age].shape[0]
            )

    mean_trigger = df_plot[trigger_col].mean()
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.bar(ages, perc, label=name)
    ax.bar(ages, perc_non, bottom=perc, label="No {}".format(name))
    plt.hlines(mean_trigger, -2, 139, linestyle="--", linewidth=2)
    plt.vlines(60, 0, 0.4, linestyle="--", color="red", linewidth=3)
    plt.hlines(2 * mean_trigger, -2, 139, linestyle="--", linewidth=2)
    plt.vlines(77, 0, 0.4, linestyle="--", color="purple", linewidth=3)
    plt.ylim(0, 3 * mean_trigger)
    plt.legend(loc="upper right")
    plt.ylabel("Percentage")
    plt.xlabel("Age")
    plt.title("Percentage of {} with age equal to x value".format(name))
    fig.show()


# SAVING MODELS
# functions for cleaning model names in generation of .onnx


def get_model_name_from_model_target(model_target):
    model_type, condition_trigger, target_name = model_target

    model_name = (
        model_type
        + "_"
        + (
            trigger_to_name[condition_trigger]
            if condition_trigger in list(trigger_to_name.keys())
            else condition_trigger
        )
        + "_"
        + (
            trigger_to_name[target_name]
            if target_name in list(trigger_to_name.keys())
            else target_name
        )
    )
    return model_name


# TODO - adjust to specify filepath in inputs instead of hardcoded in function
def get_model_from_model_target(model_target, date_input, ordered : bool =False):
    """
    Read model object if exists.
    Args:
        model_target (str) : Describing model, part of model object file name
        date_input (str) : Describing date of model generation, part of model object file name
        ordered (bool) : whether to read 'Ordered' or normal model. Defaults to False for normal.
    """
    model_name = get_model_name_from_model_target(model_target)
    if ordered:
        path = HERE / "outputs UK/Ordered_Model_{}_{}.obj".format(model_name, date_input)
    else:
        path = HERE / "outputs UK/Model_{}_{}.obj".format(model_name, date_input)
        

    if os.path.exists(path):
        # get object
        with open(path, "rb") as f:
            model = pickle.load(f)
            print("\n", model_name)

            return model
