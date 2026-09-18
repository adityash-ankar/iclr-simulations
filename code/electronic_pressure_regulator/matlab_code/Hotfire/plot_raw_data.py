import numpy as np
from pathlib import Path
import pandas as pd
from datetime import datetime
import json
import plotly.graph_objects as go


if __name__ == "__main__":

    # List of CSV file paths
    test_data_csv_array = [
        # r"C:\Users\adity\Downloads\logs\logs\20260912_120355.825062Z_emb_stark_telem.csv",
        # r"C:\Users\adity\Downloads\logs\logs\20260912_122116.954455Z_emb_greg1_telem.csv",
        # r"C:\Users\adity\Downloads\logs\logs\20260912_122116.389314Z_emb_greg0_telem.csv",
        r"C:\Users\adity\Downloads\hotfire_logs\hotfire_logs\20260912_154408.680649Z_emb_greg1_telem.csv"

        # r"C:\Users\adity\Downloads\another_file.csv",
    ]

    # Index range for each file: (start_index, end_index)
    # Set end_index to None to slice through to the end of that file
    file_index_ranges = [
        # (19517, 19711),  # Index range for file 1
        # (14450, 14644), 
        (0, 10775)
        # (None, None),  # Use None, None to include all data for a file
    ]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    json_file = (
        Path(__file__).parent
        / "hotfire_data"
        / f"test_data_{timestamp}.json"
    )

    html_file = json_file.with_suffix(".html")

    json_file.parent.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # Combine sliced CSVs into one dict
    # -----------------------------

    json_data = {}

    for test_csv, (start_i, end_i) in zip(test_data_csv_array, file_index_ranges):

        test_data_csv = pd.read_csv(test_csv)

        # Slice dataframe by specified row indexes for this specific file
        sliced_df = test_data_csv.iloc[start_i:end_i]

        for header in sliced_df.columns:
            data = sliced_df[header].tolist()

            if header not in json_data:
                json_data[header] = []

            json_data[header].extend(data)

    # -----------------------------
    # Plot settings
    # -----------------------------

    data_headers = [
        'N2TankP',
        'FuelTankP',
        # 'flowmeter',
        'regAngle',
        # 'CdA',
        # 'OxTankP',
        # 'regAngleOx',
        'Feedforward'
        # 'ch1sens',
        # 'ch2sens',

    ]

    labels = [
        'N2 Tank PT',
        'Fuel Tank PT',
        # 'Mass Flow Rate',
        'Fuel Valve Angle',
        # 'CdA',
        # 'Ox Tank PT',
        # 'Ox Valve Angle',
        'Feed Forward Angle'
        # 'Ox Injector',
        # 'Fuel Injector'
    ]

    # -----------------------------
    # Get CdA
    # # -----------------------------
    # P_N2 = np.asarray(json_data['ch0sens'])
    # P_prop = np.asarray(json_data['ch1sens'])
    # mdot = np.asarray(json_data['flowmeter'])
    # rho_prop = 790
    json_data['regAngle'] = list(np.asarray(json_data['regAngle'])/10)
    json_data['CdA'] = list(np.asarray(json_data['Feedforward']) * 6.885 * 1e-07 -1.343340415148949e-05)

    # -----------------------------
    # Create zeroed time axis
    # -----------------------------

    if "system_time" not in json_data:
        raise KeyError("'system_time' not found in combined JSON")

    system_time = np.array(json_data["system_time"], dtype=float)

    # system_time is in ms; zero relative to the first combined data point
    zerod_time = (system_time - system_time[0]) / 1000.0

    json_data['Zerod_time'] = list(zerod_time)
    x_data = zerod_time

    # -----------------------------
    # Save combined JSON
    # -----------------------------

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)

    # -----------------------------
    # Create Plotly figure
    # -----------------------------

    fig = go.Figure()

    for header, label in zip(data_headers, labels):

        if header not in json_data:
            print(f"Warning: '{header}' not found in combined JSON")
            continue

        y_data = json_data[header]

        fig.add_trace(
            go.Scatter(
                x=x_data,
                y=y_data,
                mode="lines",
                name=label
            )
        )

    # -----------------------------
    # Plot layout
    # -----------------------------

    fig.update_layout(
        title="Hotfire Test Data",
        xaxis_title="Time (s)",
        yaxis_title="Value",
        hovermode="x unified"
    )

    # -----------------------------
    # Save HTML
    # -----------------------------

    fig.write_html(html_file)

    print(f"JSON saved to: {json_file}")
    print(f"Plot saved to: {html_file}")