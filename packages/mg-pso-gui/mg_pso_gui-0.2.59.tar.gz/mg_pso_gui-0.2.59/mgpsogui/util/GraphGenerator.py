import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os
from PIL import Image, ImageTk
import customtkinter
import traceback
import math

baseFigureWidth = 700
baseFigureHeight = 350

theme_background_color = {
    "Dark": 'rgba(42, 42, 42, 0)',
    "Light": 'rgba(255, 255, 255, 0)',
    "Publication": 'rgba(255, 255, 255, 0)'
}

theme_background_color_html = {
    "Dark": '#2a2a2a',
    "Light": '#ffffff',
    "Publication": '#ffffff'
}

theme_plot_color = {
    "Dark": 'rgb(62, 62, 62)',
    "Light": 'rgba(245,245,255,255)',
    "Publication": 'rgba(245,245,255,255)'
}

theme_grid_color = {
    "Dark": 'rgb(72, 72, 72)',
    "Light": 'rgb(255, 255, 255)',
    "Publication": 'rgb(255, 255, 255)'
}

theme_line_color = {
    "Dark": 'rgb(102, 102, 102)',
    "Light": 'rgb(102, 102, 102)',
    "Publication": 'rgb(102, 102, 102)'
}

theme_font_color = {
    "Dark": 'white',
    "Light": 'black',
    "Publication": 'black'
}

theme_plot_color_pallet = [
    "rgba(151, 209, 233, 255)", 
    "rgba(0, 120, 179, 255)", 
    "rgba(179, 223, 146, 255)", 
    "rgba(49, 169, 90, 255)", 
    "rgba(227, 136, 220, 255)", 
    "rgba(127, 0, 255, 255)", 
    "rgba(255, 128, 0, 255)",
    "rgba(255, 99, 71, 255)",   
    "rgba(102, 205, 170, 255)",
    "rgba(255, 215, 0, 255)",
    "rgba(70, 130, 180, 255)"
]

def generate_graphs(HomePage):

    try:
        selected_graph = HomePage.option_manager.get("selected_graph").get()
        folder = HomePage.option_manager.get_project_folder()
        if not os.path.exists(folder):
            os.makedirs(folder)
            
        if (selected_graph == "Best Cost Stacked"):
            HomePage.selected_graph_name = "best_cost_stacked"
            best_cost_stacked(HomePage, HomePage.running_config['steps'], HomePage.progress_data, HomePage.option_manager)
        elif (selected_graph == "Best Cost by Round"):
            HomePage.selected_graph_name = "best_cost_by_round"
            best_cost_by_round(HomePage, HomePage.running_config['steps'], HomePage.progress_data, HomePage.option_manager)
        elif (selected_graph == "Iteration Table"):
            HomePage.selected_graph_name = "table"
            table(HomePage, HomePage.running_config['steps'], HomePage.progress_data, HomePage.option_manager)
        elif (selected_graph == "Calibrated Parameters"):
            HomePage.selected_graph_name = "calibrated_params_by_round"
            calibrated_params_by_round(HomePage, HomePage.running_config['steps'], HomePage.calibration_data, HomePage.option_manager)
        elif (selected_graph == "Custom CSV"):
            HomePage.selected_graph_name = "custom_csv"
            custom_csv(HomePage, HomePage.option_manager)
        elif (selected_graph == "Compare CSV"):
            HomePage.selected_graph_name = "compare_csv"
            compare_csv(HomePage, HomePage.option_manager)
        elif (selected_graph == "Sampling CSV"):
            HomePage.selected_graph_name = "sampling_csv"
            sampling_csv(HomePage, HomePage.option_manager)
        elif (selected_graph == "Matrix Editor"):
            HomePage.selected_graph_name = "matrix_editor"
            matrix_editor(HomePage, HomePage.option_manager)
            pass
            
        image_path = os.path.join(folder, HomePage.selected_graph_name + ".png")
        
        if not os.path.exists(image_path):
            image_path = os.path.join("./images", "up.png")
        
        HomePage.graph_image_obj = Image.open(image_path)
        HomePage.graph_image = customtkinter.CTkImage(HomePage.graph_image_obj, size=(HomePage.image_width * HomePage.image_scale, HomePage.image_height * HomePage.image_scale))
        HomePage.graph_label.configure(image=HomePage.graph_image)
    except Exception as e:
        print(f"An exception occurred in Graph Generator: {str(e)}")
        print(f"Exception type: {type(e).__name__}")
        print("Traceback:")
        traceback.print_exc()

def best_cost_stacked(homepage, config, data, option_manager):
    theme = homepage.option_manager.get("graph_theme").get()

    fig = go.Figure()
        
    total_steps = len(config)
    
    # Get unique values from the round_step column of the dataframe
    pp = 0
    for round_step in data.keys():
        fig.add_trace(go.Scatter(x=data[round_step]["percent"], y=data[round_step]["best_cost"], name=round_step, marker_color=theme_plot_color_pallet[pp]))
        pp += 1

    fig.update_layout(
        title="",
        xaxis_title="Progress (% through Group)",
        yaxis_title="Best Cost",
        font=dict(color=theme_font_color[theme]),
        paper_bgcolor=theme_background_color[theme],
        plot_bgcolor=theme_plot_color[theme],
        xaxis=dict(
            gridcolor=theme_grid_color[theme],
            gridwidth=1
        ),
        yaxis=dict(
            range=[0, 0.6],
            autorange=True,
            gridcolor=theme_grid_color[theme],
            gridwidth=0.1
        )
    )
    if (theme == "Publication"):
        fig.update_layout(
            font=dict(
                size=16
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.47
            ),
            margin=dict(
                t=0,
                b=1,
                l=1,
                r=1,
                autoexpand=True
            )
        )
    
    info = option_manager.get_project_data()
    folder = os.path.join(info['path'], info['name'])
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    fig.write_image(os.path.join(folder, "best_cost_stacked.png"), width=1280, height=720)
    fig.write_html(os.path.join(folder, "best_cost_stacked.html"), include_plotlyjs='cdn', auto_open=False)
    fig.write_json(os.path.join(folder, "best_cost_stacked.json"))
    fig.write_image(os.path.join(folder, "best_cost_stacked.pdf"), engine="kaleido", width=baseFigureWidth, height=baseFigureHeight)
    with open(os.path.join(folder, "best_cost_stacked.html"), "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open(os.path.join(folder, "best_cost_stacked.html"), "w") as f:
        f.write(html)

    
        return fig

def table(homepage, config, dataframe, option_manager):
    theme = homepage.option_manager.get("graph_theme").get()

    # Create a plotly table with the values in the dataframe
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(dataframe.columns),
            font=dict(color='black'),
            align="left"
        ),
        cells=dict(
            values=[dataframe[k].tolist() for k in dataframe.columns],
            font=dict(color='black'),
            align = "left")
    )])
    
    fig.update_layout(
        title="",
        xaxis_title="Iteration",
        yaxis_title="Best Cost",
        font=dict(color=theme_font_color[theme]),
        paper_bgcolor=theme_background_color[theme],
        plot_bgcolor=theme_plot_color[theme],
        xaxis=dict(
            gridcolor=theme_grid_color[theme],
            gridwidth=1
        ),
        yaxis=dict(
            range=[0, 0.6],
            autorange=True,
            gridcolor=theme_grid_color[theme],
            gridwidth=0.1
        )
    )
    if (theme == "Publication"):
        fig.update_layout(
            font=dict(
                size=16
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.47
            ),
            margin=dict(
                t=0,
                b=1,
                l=1,
                r=1,
                autoexpand=True
            )
        )

    info = option_manager.get_project_data()
    folder = os.path.join(info['path'], info['name'])
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    fig.write_image(os.path.join(folder, "table.png"), width=1280, height=720)
    fig.write_html(os.path.join(folder, "table.html"), include_plotlyjs='cdn', auto_open=False)
    fig.write_json(os.path.join(folder, "table.json"))
    fig.write_image(os.path.join(folder, "table.pdf"), engine="kaleido", width=baseFigureWidth, height=baseFigureHeight)
    with open(os.path.join(folder, "table.html"), "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open(os.path.join(folder, "table.html"), "w") as f:
        f.write(html)
    
    return fig

def best_cost_by_round(homepage, config, data, option_manager):
    theme = homepage.option_manager.get("graph_theme").get()

    fig = go.Figure()
        
    total_steps = len(config)
    
    pp = 0
    # Get unique values from the round_step column of the dataframe
    for round_step in data.keys():
    #for iteration in dataframe['round_step'].unique():
        # Get best_cost and completed rounds rows for this iteration

        round_index = int(round_step.split(" -")[0].replace("Round: ", "")) - 1

        #df = dataframe[dataframe['round_step'] == iteration]
        
        #step_index = ((iteration) % total_steps)
        #round_index = ((iteration) // total_steps)

        fig.add_trace(go.Scatter(x=np.array(data[round_step]['percent']) + (100 * round_index), y=data[round_step]['best_cost'], name=round_step, marker_color=theme_plot_color_pallet[pp]))
        pp += 1

        #fig.add_trace(go.Scatter(x=df['completed_rounds'] + (df['total_rounds'] * round_index), y=df['best_cost'], name='Group ' + str(step_index + 1)))
        
        
        xx = np.max(np.array(data[round_step]["percent"]) + (100 * round_index))
        fig.add_shape(
            type='line',
            x0=xx,
            y0=0,
            x1=xx,
            y1=1,
            yref='paper',
            line=dict(
                color=theme_line_color[theme],
                width=2
            )
        )
        
        fig.add_annotation(
            x=xx + 0.5,
            y=1,
            yref='paper',
            text='Round ' + str(round_index + 1),
            showarrow=False,
            yshift=-10
        )

    fig.update_layout(
        title="",
        xaxis_title="Progress (%)",
        yaxis_title="Best Cost",
        font=dict(color=theme_font_color[theme]),
        paper_bgcolor=theme_background_color[theme],
        plot_bgcolor=theme_plot_color[theme],
        xaxis=dict(
            gridcolor=theme_grid_color[theme],
            gridwidth=1
        ),
        yaxis=dict(
            range=[0, 0.6],
            autorange=True,
            gridcolor=theme_grid_color[theme],
            gridwidth=0.1
        )
    )
    if (theme == "Publication"):
        fig.update_layout(
            font=dict(
                size=16
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.47
            ),
            margin=dict(
                t=0,
                b=1,
                l=1,
                r=1,
                autoexpand=True
            )
        )
    
    info = option_manager.get_project_data()
    folder = os.path.join(info['path'], info['name'])
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    fig.write_image(os.path.join(folder, "best_cost_by_round.png"), width=1280, height=720)
    fig.write_html(os.path.join(folder, "best_cost_by_round.html"), include_plotlyjs='cdn', auto_open=False)
    fig.write_json(os.path.join(folder, "best_cost_by_round.json"))
    fig.write_image(os.path.join(folder, "best_cost_by_round.pdf"), engine="kaleido", width=baseFigureWidth, height=baseFigureHeight)
    with open(os.path.join(folder, "best_cost_by_round.html"), "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open(os.path.join(folder, "best_cost_by_round.html"), "w") as f:
        f.write(html)
    
    return fig

def calibrated_params_by_round(homepage, config, list_of_objs, option_manager):
    theme = homepage.option_manager.get("graph_theme").get()

    fig = go.Figure()
        
    total_steps = len(config)
    
    datalines = {"step": [], "round": []}
    step = 1
    round = 1
    for index, obj in enumerate(list_of_objs):
        if (obj == {}):
            continue
        for key in obj.keys():
            if key not in datalines:
                datalines[key] = []
            datalines[key].append(obj[key])
        datalines["step"].append(step)
        datalines['round'].append(round)
        step += 1
        if (step > total_steps):
            step = 1
            round += 1
    
    # Get unique values from the round_step column of the dataframe
    pp = 0
    for key in datalines.keys():
        # Get best_cost and completed rounds rows for this iteration
        if key == 'step' or key == 'round':
            continue
        
        fig.add_trace(go.Scatter(x=datalines['round'], y=datalines[key], name=key, marker_color=theme_plot_color_pallet[pp]))
        pp += 1

    fig.update_layout(
        title="",
        xaxis_title="Round",
        yaxis_title="Particle Parameters",
        font=dict(color=theme_font_color[theme]),
        paper_bgcolor=theme_background_color[theme],
        plot_bgcolor=theme_plot_color[theme],
        xaxis=dict(
            gridcolor=theme_grid_color[theme],
            gridwidth=1
        ),
        yaxis=dict(
            gridcolor=theme_grid_color[theme],
            gridwidth=0.1
        )
    )
    if (theme == "Publication"):
        fig.update_layout(
            font=dict(
                size=16
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.47
            ),
            margin=dict(
                t=0,
                b=1,
                l=1,
                r=1,
                autoexpand=True
            )
        )

    info = option_manager.get_project_data()
    folder = os.path.join(info['path'], info['name'])
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    fig.write_image(os.path.join(folder, "calibrated_params_by_round.png"), width=1280, height=720)
    fig.write_html(os.path.join(folder, "calibrated_params_by_round.html"), include_plotlyjs='cdn', auto_open=False)
    fig.write_json(os.path.join(folder, "calibrated_params_by_round.json"))
    fig.write_image(os.path.join(folder, "calibrated_params_by_round.pdf"), engine="kaleido", width=baseFigureWidth, height=baseFigureHeight)
    with open(os.path.join(folder, "calibrated_params_by_round.html"), "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open(os.path.join(folder, "calibrated_params_by_round.html"), "w") as f:
        f.write(html)

    return fig

def custom_csv(homepage, option_manager):
    theme = homepage.option_manager.get("graph_theme").get()

    fig = go.Figure()

    data = homepage.csv_data["data"]

    x = option_manager.get("selected_x").get()
    val = option_manager.get("selected_y1").get()
    val2 = option_manager.get("selected_y2").get()
    
    xx = None
    if x == "time":
        xx = pd.to_datetime(data["time"], format='%Y-%m-%d', errors='coerce')
    elif x == "date":
        xx = pd.to_datetime(data["date"], format='%d-%m-%Y', errors='coerce')
    else:
        xx = pd.to_numeric(data[x], errors="coerce")
        
    yy = pd.to_numeric(data[val], errors="coerce")
    
    yy_unit = "-"
    if "Unit" in homepage.csv_data["data_attributes"]:
        yy_unit = homepage.csv_data["data_attributes"]["Unit"][val]
    
    yy2 = pd.to_numeric(data[val2], errors="coerce")
    
    yy2_unit = "-"
    if "Unit" in homepage.csv_data["data_attributes"]:
        yy2_unit = homepage.csv_data["data_attributes"]["Unit"][val2]

    fig.add_trace(go.Scatter(x=xx, y=yy, name=val, marker_color=theme_plot_color_pallet[1]))
    fig.add_trace(go.Scatter(x=xx, y=yy2, name=val2, yaxis='y2', marker_color=theme_plot_color_pallet[3]))

    fig.update_layout(
        title="",
        xaxis_title=x,
        yaxis_title=val,
        font=dict(color=theme_font_color[theme]),
        paper_bgcolor=theme_background_color[theme],
        plot_bgcolor=theme_plot_color[theme],
        xaxis=dict(
            gridcolor=theme_grid_color[theme],
            gridwidth=1
        ),
        yaxis=dict(
            title=val + " (" + str(yy_unit) + ")",
            autorange=True,
            gridcolor=theme_grid_color[theme],
            gridwidth=0.1
        ),
        yaxis2=dict(
            title=val2 + " (" + str(yy2_unit) + ")",
            overlaying='y',
            side='right'
        )
    )
    if (theme == "Publication"):
        fig.update_layout(
            font=dict(
                size=16
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.47
            ),
            margin=dict(
                t=0,
                b=1,
                l=1,
                r=1,
                autoexpand=True
            )
        )

    info = option_manager.get_project_data()
    folder = os.path.join(info['path'], info['name'])
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    fig.write_image(os.path.join(folder, "custom_csv.png"), width=1280, height=720)
    fig.write_html(os.path.join(folder, "custom_csv.html"), include_plotlyjs='cdn', auto_open=False)
    fig.write_json(os.path.join(folder, "custom_csv.json"))
    fig.write_image(os.path.join(folder, "custom_csv.pdf"), engine="kaleido", width=baseFigureWidth, height=baseFigureHeight)
    with open(os.path.join(folder, "custom_csv.html"), "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open(os.path.join(folder, "custom_csv.html"), "w") as f:
        f.write(html)

    return fig

def compare_csv(homepage, option_manager):
    theme = homepage.option_manager.get("graph_theme").get()

    fig = go.Figure()

    data = homepage.csv_data["data"]
    data2 = homepage.csv_data2["data"]

    x = option_manager.get("selected_x").get()
    val = option_manager.get("selected_y1").get()
    val2 = option_manager.get("selected_y2").get()
    
    xx = None
    if x == "time":
        xx = pd.to_datetime(data["time"], format='%Y-%m-%d', errors='coerce')
    elif x == "date":
        xx = pd.to_datetime(data["date"], format='%d-%m-%Y', errors='coerce')
    else:
        xx = pd.to_numeric(data[x], errors="coerce")
        
    yy = pd.to_numeric(data[val], errors="coerce")
    
    xx2 = None
    if x == "time":
        xx2 = pd.to_datetime(data2["time"], format='%Y-%m-%d', errors='coerce')
    elif x == "date":
        xx2 = pd.to_datetime(data2["date"], format='%d-%m-%Y', errors='coerce')
    else:
        xx2 = pd.to_numeric(data2[x], errors="coerce")
    
    yy_unit = "-"
    if "Unit" in homepage.csv_data["data_attributes"]:
        yy_unit = homepage.csv_data["data_attributes"]["Unit"][val]
    
    yy2 = pd.to_numeric(data[val2], errors="coerce")
    
    yy2_unit = "-"
    if "Unit" in homepage.csv_data["data_attributes"]:
        yy2_unit = homepage.csv_data["data_attributes"]["Unit"][val2]

    fig.add_trace(go.Scatter(x=xx, y=yy, name=val, marker_color=theme_plot_color_pallet[1]))
    fig.add_trace(go.Scatter(x=xx2, y=yy2, name=val2, yaxis='y2', marker_color=theme_plot_color_pallet[3]))

    fig.update_layout(
        title="",
        xaxis_title=x,
        yaxis_title=val,
        font=dict(color=theme_font_color[theme]),
        paper_bgcolor=theme_background_color[theme],
        plot_bgcolor=theme_plot_color[theme],
        xaxis=dict(
            gridcolor=theme_grid_color[theme],
            gridwidth=1
        ),
        yaxis=dict(
            title=val + " (" + str(yy_unit) + ")",
            autorange=True,
            gridcolor=theme_grid_color[theme],
            gridwidth=0.1
        ),
        yaxis2=dict(
            title=val2 + " (" + str(yy2_unit) + ")",
            overlaying='y',
            side='right'
        )
    )
    if (theme == "Publication"):
        fig.update_layout(
            font=dict(
                size=16
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.47
            ),
            margin=dict(
                t=0,
                b=1,
                l=1,
                r=1,
                autoexpand=True
            )
        )

    info = option_manager.get_project_data()
    folder = os.path.join(info['path'], info['name'])
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    fig.write_image(os.path.join(folder, "compare_csv.png"), width=1280, height=720)
    fig.write_html(os.path.join(folder, "compare_csv.html"), include_plotlyjs='cdn', auto_open=False)
    fig.write_json(os.path.join(folder, "compare_csv.json"))
    fig.write_image(os.path.join(folder, "compare_csv.pdf"), engine="kaleido", width=baseFigureWidth, height=baseFigureHeight)
    with open(os.path.join(folder, "compare_csv.html"), "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open(os.path.join(folder, "compare_csv.html"), "w") as f:
        f.write(html)

    return fig

def sampling_csv(homepage, option_manager):
    theme = homepage.option_manager.get("graph_theme").get()

    fig = go.Figure()

    style = option_manager.get("figure_style").get()

    data = homepage.csv_data

    x = option_manager.get("selected_x").get()
    val = option_manager.get("selected_y1").get()
    val2 = option_manager.get("selected_y2").get()
    
    xx = None
    if x == "time":
        xx = pd.to_datetime(data["time"], format='%Y-%m-%d', errors='coerce')
    elif x == "date":
        xx = pd.to_datetime(data["date"], format='%d-%m-%Y', errors='coerce')
    else:
        xx = pd.to_numeric(data[x], errors="coerce")
        
    yy = pd.to_numeric(data[val], errors="coerce")
    
    yy_unit = ""
    
    yy2 = pd.to_numeric(data[val2], errors="coerce")
    
    yy2_unit = ""

    if (style == "Scatter"):
        fig.add_trace(go.Scatter(x=xx, y=yy, name=val, mode='markers', marker_color=theme_plot_color_pallet[1]))
        fig.add_trace(go.Scatter(x=xx, y=yy2, name=val2, yaxis='y2', mode='markers', marker_color=theme_plot_color_pallet[3]))
    elif (style == "Bars"):
        fig.add_trace(go.Bar(x=xx, y=yy, name=val, marker_color=theme_plot_color_pallet[1]))
        fig.add_trace(go.Bar(x=xx, y=yy2, name=val2, yaxis='y2', marker_color=theme_plot_color_pallet[3]))
    elif (style == "Lines"):
        fig.add_trace(go.Scatter(x=xx, y=yy, name=val, marker_color=theme_plot_color_pallet[1]))
        fig.add_trace(go.Scatter(x=xx, y=yy2, name=val2, yaxis='y2', marker_color=theme_plot_color_pallet[3]))
    elif (style == "Area"):
        fig.add_trace(go.Scatter(x=xx, y=yy, name=val, fill='tozeroy', marker_color=theme_plot_color_pallet[1]))
        fig.add_trace(go.Scatter(x=xx, y=yy2, name=val2, yaxis='y2', fill='tozeroy', marker_color=theme_plot_color_pallet[3]))
    elif (style == "Box"):
        fig.add_trace(go.Box(x=xx, y=yy, name=val, marker_color=theme_plot_color_pallet[1]))
        fig.add_trace(go.Box(x=xx, y=yy2, name=val2, yaxis='y2', marker_color=theme_plot_color_pallet[3]))

    fig.update_layout(
        title="",
        xaxis_title=x,
        yaxis_title=val,
        font=dict(color=theme_font_color[theme]),
        paper_bgcolor=theme_background_color[theme],
        plot_bgcolor=theme_plot_color[theme],
        xaxis=dict(
            gridcolor=theme_grid_color[theme],
            gridwidth=1
        ),
        yaxis=dict(
            title=val,
            autorange=True,
            gridcolor=theme_grid_color[theme],
            gridwidth=0.1
        ),
        yaxis2=dict(
            title=val2,
            overlaying='y',
            side='right'
        )
    )
    if (theme == "Publication"):
        fig.update_layout(
            font=dict(
                size=16
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.47
            ),
            margin=dict(
                t=0,
                b=1,
                l=1,
                r=1,
                autoexpand=True
            )
        )

    info = option_manager.get_project_data()
    folder = os.path.join(info['path'], info['name'])
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    fig.write_image(os.path.join(folder, "sampling_csv.png"), width=1280, height=720)
    fig.write_html(os.path.join(folder, "sampling_csv.html"), include_plotlyjs='cdn', auto_open=False)
    fig.write_json(os.path.join(folder, "sampling_csv.json"))
    fig.write_image(os.path.join(folder, "sampling_csv.pdf"), engine="kaleido", width=baseFigureWidth, height=baseFigureHeight)
    with open(os.path.join(folder, "sampling_csv.html"), "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open(os.path.join(folder, "sampling_csv.html"), "w") as f:
        f.write(html)

    return fig

def matrix_editor(homepage, option_manager):
    theme = homepage.option_manager.get("graph_theme").get()

    style = option_manager.get("figure_style").get()
    data = homepage.csv_data
    x = option_manager.get("selected_x").get()

    all_figures = []
    figure_parameters = option_manager.get('figure_parameters')

    #color_list = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
    color_index = 0
    color_dict = {}

    total_figures = 0
    for parameter in figure_parameters:
        name = parameter['name'].get()
        if ("Fig" not in name):
            continue
        total_figures += 1

    figures_per_row = 1
    if (total_figures == 1):
        figures_per_row = 1
    elif (total_figures == 2):
        figures_per_row = 2
    elif (total_figures == 3 or total_figures == 4):
        figures_per_row = 2
    elif (total_figures == 5 or total_figures == 6):
        figures_per_row = 3
    elif (total_figures == 7 or total_figures == 8):
        figures_per_row = 4
    elif (total_figures == 9):
        figures_per_row = 3
    else:
        figures_per_row = 4

    fig_combined = make_subplots(rows=(math.ceil(total_figures / figures_per_row)), cols=figures_per_row, shared_xaxes=False, shared_yaxes=False)

    pp = 0
    for parameter in figure_parameters:
        name = parameter['name'].get()

        if ("Fig" not in name):
            continue

        fig = go.Figure()
        val = parameter['value'].get()
        
        xx = None
        #if x == "time":
        #    xx = pd.to_datetime(data["time"], format='%Y-%m-%d', errors='coerce')
        #elif x == "date":
        #    xx = pd.to_datetime(data["date"], format='%d-%m-%Y', errors='coerce')
        #else:
        xx = pd.to_numeric(data[x], errors="coerce") 
        yy = pd.to_numeric(data[val], errors="coerce")
        
        yy_unit = ""

        if (style == "Scatter"):
            fig.add_trace(go.Scatter(x=yy, y=xx, name=val, mode='markers', marker_color=theme_plot_color_pallet[pp]))
        elif (style == "Bars"):
            fig.add_trace(go.Bar(x=yy, y=xx, name=val, marker_color=theme_plot_color_pallet[pp]))
        elif (style == "Lines"):
            fig.add_trace(go.Scatter(x=yy, y=xx, name=val, marker_color=theme_plot_color_pallet[pp]))
        elif (style == "Area"):
            fig.add_trace(go.Scatter(x=yy, y=xx, name=val, fill='tozeroy', marker_color=theme_plot_color_pallet[pp]))
        elif (style == "Box"):
            fig.add_trace(go.Box(x=yy, y=xx, name=val, marker_color=theme_plot_color_pallet[pp]))
        
        pp += 1

        fig.update_layout(
            title="",
            xaxis_title=val,
            yaxis_title=x,
            font=dict(color=theme_font_color[theme]),
            paper_bgcolor=theme_background_color[theme],
            plot_bgcolor=theme_plot_color[theme],
            xaxis=dict(
                gridcolor=theme_grid_color[theme],
                gridwidth=1
            ),
            yaxis=dict(
                title=x,
                autorange=True,
                gridcolor=theme_grid_color[theme],
                gridwidth=0.1
            )
        )
        if (theme == "Publication"):
            fig.update_layout(
                font=dict(
                    size=16
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.47
                ),
                margin=dict(
                    t=0,
                    b=1,
                    l=1,
                    r=1,
                    autoexpand=True
                )
            )

        all_figures.append(fig)

    row = 1
    col = 1
    for fig in all_figures:
        for trace in fig.data:

            if trace.name not in color_dict:
                color_dict[trace.name] = theme_plot_color_pallet[color_index % len(theme_plot_color_pallet)]
                color_index += 1

            trace.marker.color = color_dict[trace.name]

            if fig_combined.data:
                trace.showlegend = not any(t.name == trace.name for t in fig_combined.data)
            fig_combined.add_trace(trace, row=row, col=col)
        
        # Get the layout titles from the individual figure
        xaxis_title = fig.layout.xaxis.title.text
        yaxis_title = fig.layout.yaxis.title.text

        # Update the combined figure's subplot with the titles
        fig_combined.update_xaxes(title_text=xaxis_title, row=row, col=col)
        fig_combined.update_yaxes(title_text=yaxis_title, row=row, col=col)

        col += 1
        if col > figures_per_row:
            row += 1
            col = 1

    info = option_manager.get_project_data()
    folder = os.path.join(info['path'], info['name'])
    
    fig = fig_combined
    fig.update_layout(
        title="",
        font=dict(color=theme_font_color[theme]),
        paper_bgcolor=theme_background_color[theme],
        plot_bgcolor=theme_plot_color[theme]
    )
    if (theme == "Publication"):
        fig.update_layout(
            font=dict(
                size=16
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.47
            ),
            margin=dict(
                t=0,
                b=1,
                l=1,
                r=1,
                autoexpand=True
            )
        )

    if not os.path.exists(folder):
        os.makedirs(folder)

    fig.write_image(os.path.join(folder, "matrix_editor.png"), width=1280, height=720)
    fig.write_html(os.path.join(folder, "matrix_editor.html"), include_plotlyjs='cdn', auto_open=False)
    fig.write_json(os.path.join(folder, "matrix_editor.json"))
    fig.write_image(os.path.join(folder, "matrix_editor.pdf"), engine="kaleido", width=baseFigureWidth, height=baseFigureHeight)
    with open(os.path.join(folder, "matrix_editor.html"), "r") as f:
        html = f.read()
        html = html.replace("<body>", "<body bgcolor='#2a2a2a'>")
    with open(os.path.join(folder, "matrix_editor.html"), "w") as f:
        f.write(html)

    return fig