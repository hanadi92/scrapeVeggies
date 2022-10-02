"""Stuff"""
import glob
import os
import random
import sys

import dotenv  # pylint: disable=import-error
import pandas as pd  # pylint: disable=import-error
import plotly.graph_objects as go

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from utils.utils import \
    read_from_file  # pylint: disable=no-name-in-module,wrong-import-position


def _get_config():
    config = dotenv.dotenv_values(".env")
    _csv_directory = config["CSV_DIR"]

    return _csv_directory


def _get_veggies_only(_df):
    return _df.loc[_df["category"] == "خضار"]


def _sort_by_date(_df):
    _df["date"] = pd.to_datetime(_df["date"], format="%d/%m/%Y")
    return _df.sort_values(by="date", ascending=False)


def veggie_price_all(_df):
    """Vegetables price throughout the period of time"""
    _veggies = _get_veggies_only(_df)
    _veggies = _sort_by_date(_veggies)

    fig = go.Figure()

    for _unique_col in _veggies["name"].unique():
        color = random.choices(range(256), k=3)
        fig.add_trace(go.Scatter(
            x=_veggies[_veggies["name"] == _unique_col]["date"],
            y=_veggies[_veggies["name"] == _unique_col]["most"],
            name=_unique_col,
            marker=dict(color=color),
        ))

    fig.update_layout(hovermode='closest')
    fig.show()


def visiualize_outliers(_df):
    """Use Box ploting to visiualize outliers"""
    _veggies = _get_veggies_only(_df)
    _veggies = _sort_by_date(_veggies)

    fig = go.Figure()
    for _unique_col in _veggies["name"].unique():
        fig.add_trace(go.Box(
            y=_veggies[_veggies["name"] == _unique_col]["highest"],
            quartilemethod="exclusive",
            name=f'{_unique_col} highest',
            boxpoints='all',
        ))
        fig.add_trace(go.Box(
            y=_veggies[_veggies["name"] == _unique_col]["most"],
            quartilemethod="exclusive",
            name=f'{_unique_col} most',
            boxpoints='all',
        ))
        fig.add_trace(go.Box(
            y=_veggies[_veggies["name"] == _unique_col]["lowest"],
            quartilemethod="exclusive",
            name=f'{_unique_col} lowest',
            boxpoints='all',
        ))
    fig.update_layout(hovermode='closest')
    fig.update_yaxes(rangemode="tozero")
    fig.show()


def main():
    """
    Process CSV data
    Plot differnt ideas
    """

    _colummns = read_from_file("columns.json")
    _csv_dir = _get_config()

    _files = os.path.join(_csv_dir, "*.csv")
    _files = glob.glob(_files)

    if len(_files) == 0:
        print("There are no files to process.")
        return

    _df = pd.concat([pd.read_csv(f, names=_colummns.values()) for f in _files])

    #_combined_filename = os.path.join(_csv_dir, "combined_csv.csv")
    #_df.to_csv(_combined_filename, index=False)

    veggie_price_all(_df)
    visiualize_outliers(_df)

    print("processed")


if __name__ == "__main__":
    main()
