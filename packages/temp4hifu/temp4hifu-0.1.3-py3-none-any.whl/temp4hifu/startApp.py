# USE DASH TO BUILD GUI
from dash import Dash, html, dcc, callback, Output, Input, ctx
import plotly.graph_objects as go
import plotly.express as px
# STANDARD IMPORTS
import pandas as pd
import numpy as np
import os
# CUSTOM FUNCTIONS
from temp4hifu import setParam, calculateBioheat, calculateRayleighIntegral

##### ---- ##### ---- ##### ---- SET FILE PLACEHOLDERS ---- ##### ---- ##### ---- #####

sampledataDirectory = 'https://raw.githubusercontent.com/C2H5OH-Consumer/temp4hifu/refs/heads/main/Temp4HIFU/sampledata/'
placeholder_df = sampledataDirectory + 'df_pressure2D_placeholder.csv'
placeholder_z = sampledataDirectory + 'z_axis_placeholder.csv'
placeholder_r =  sampledataDirectory + 'r_axis_placeholder.csv'

##### ---- ##### ---- ##### ---- BUILD APP ---- ##### ---- ##### ---- #####

app = Dash('temp4hifu')
app.layout = [
    # Title
    html.H1(children='Temperature Compliance for HIFU Transducers',style={'textAlign':'center'}), 
    # TOP Section - Button and Messages
    html.Div([
        html.Button('LOAD FILES',id='buttonLoad',n_clicks=0),
        html.Button('CALCULATE PRESSURE',id='button2D',n_clicks=0),
        html.Button('CALCULATE TEMPERATURE',id='button1D',n_clicks=0),
    ],style={'width': '50%','float': 'right','display': 'inline-block','padding': '10px 5px'}),
    # RIGHT Section - Display Graphs
    html.Div([
        html.H2('Results', style ={'textAlign':'center'}), 
            dcc.Dropdown(['Pressure','Intensity'],'Intensity',id='DROP_field2D'),
            dcc.Graph(id='GRAPH_field2D',hoverData={'points': [{'customdata': 'Pressure'}]}),
            dcc.Graph(id='GRAPH_time1D'),
    ],style={'width': '50%', 'float': 'right', 'display': 'inline-block'}),
    # SPACE
    html.Div([html.H3(' ',style ={'textAlign':'center'})],style={'width': '3%', 'float': 'right', 'display': 'inline-block'}),
    # MIDDLE Section - Inputs
    html.Div([     
        # Call Data (Top)
        html.H3('Call Data Files', style ={'textAlign':'center'}),
            dcc.Input(id="dataFrame",type='text',value=placeholder_df),
            dcc.Input(id="ZAXE",type='text',value=placeholder_z),
            dcc.Input(id="RAXE",type='text',value=placeholder_r),
        # Find Heat Location (Middle 1)
        html.H3('Calculate Heat at Point (Z,R)', style ={'textAlign':'center'}), 
            html.P('Axial Point Z [m]', style ={'textAlign':'left'}),
                dcc.Input(id="observeZ",type='number',value=0.05,min=0),
            html.P('Radial Point R [m]', style ={'textAlign':'left'}),
                dcc.Input(id="observeR",type='number',value=0),
        # Heating Section (Middle 2)
        html.H3('Heating', style ={'textAlign':'center'}), 
            html.P('Time Heating [s]', style ={'textAlign':'left'}),
                dcc.Input(id="HeatTime", type='number', placeholder='Input Heat Time',value=30,min=0),
            html.P('Time Cooling [s]', style ={'textAlign':'left'}),
                dcc.Input(id="CoolTime", type='number', placeholder='Input Cool Time',value=30,min=0),
            html.P('Duty Cycle [Percentage]', style ={'textAlign':'left'}),
                dcc.Input(id="DutyCycle", type='number', placeholder='Input Duty Cycle',value=100,min=0),
            html.P('Time Step for Temperature Graph [s]', style ={'textAlign':'left'}),
                dcc.Input(id="numTime", type='number', placeholder='Input Time Step',value=0.005,min=0),
        # Plotting Section (Bottom)
        html.H3('Plotting Parameters', style ={'textAlign':'center'}), 
            html.P('Number of Axial Steps', style ={'textAlign':'left'}),
                dcc.Input(id="numZ", type='number', placeholder='Input # Axial Steps',value=100,min=1),
            html.P('Number of Radial Steps', style ={'textAlign':'left'}),
                dcc.Input(id="numR", type='number', placeholder='Input # Radial Steps',value=100,min=1),
    ], style={'width': '15%', 'float': 'right', 'display': 'inline-block'}),
    # SPACE
    html.Div([html.H3(' ',style ={'textAlign':'center'})],style={'width': '3%', 'float': 'right', 'display': 'inline-block'}),
    # LEFT Section - Transducer and Medium 
    html.Div([
        # Trandsucer Section (Top)
        html.H3('Transducer', style ={'textAlign':'center'}), 
            html.P('Frequency [MHz]', style ={'textAlign':'left'}),
                dcc.Input(id="Frequency", type='number', placeholder='Input Frequency',value=1,min=0),
            html.P('Radius [m]', style ={'textAlign':'left'}),
                dcc.Input(id="Radius", type='number', placeholder='Input Radius',value=0.02,min=0),
            html.P('Focus Distance [m]', style ={'textAlign':'left'}),
                dcc.Input(id="Focus", type='number', placeholder='Input Focus Distance',value=0.05,min=0.001),
            html.P('Initial Pressure [MPa]', style ={'textAlign':'left'}),
                dcc.Input(id="InitPress", type='number', placeholder='Input Initial Pressure',value=1,min=0),
        # Medium Section (Bottom)
        html.H3('Medium', style ={'textAlign':'center'}), 
            html.P('Presets', style ={'textAlign':'left'}), 
                dcc.Dropdown(['Custom','Water','Glycerol','Egg White','Castor Oil'],'Water',id='DROP_medium'),
            html.P('Speed of Sound [m/s]', style ={'textAlign':'left'}), 
                dcc.Input(id="Speed", type='number', placeholder='Input Speed of Sound'),
            html.P('Density [kg/m^3]', style ={'textAlign':'left'}),
                dcc.Input(id="Density", type='number', placeholder='Input Density'),
            html.P('Absorption Coeffient [Np/(m*MHz^2)]', style ={'textAlign':'left'}),
                dcc.Input(id="AbsCoeff", type='number', placeholder='Input Absorption Coefficient'),
            html.P('Specific Heat Capacity [J/(kg*K)]', style ={'textAlign':'left'}),
                dcc.Input(id="SpecHeatCap", type='number', placeholder='Input Specific Heat Capacity'),
            html.P('Thermal Diffusivity [(m^2)/s]', style ={'textAlign':'left'}),
                dcc.Input(id="ThermDiff", type='number', placeholder='Input Thermal Diffusivity'),  
    ], style={'width': '15%', 'float': 'right', 'display': 'inline-block'}),
]

##### ---- ##### ---- ##### ---- CALLBACKS AND FUNCTIONS  ---- ##### ---- ##### ---- #####

# Set Medium Properties Callback
@callback(
    Output('Speed','value'),            # [m/s]
    Output('Density','value'),          # [kg/m^3]
    Output('AbsCoeff','value'),         # [Np/(m*MHz^2)]
    Output('SpecHeatCap','value'),      # [J/(kg*K)]
    Output('ThermDiff','value'),        # [(m^2)/s]

    Input('DROP_medium','value'),       # [text]
    Input('Speed','value'),             # [m/s]
    Input('Density','value'),           # [kg/m^3]
    Input('AbsCoeff','value'),          # [Np/(m*MHz^2)]
    Input('SpecHeatCap','value'),       # [J/(kg*K)]
    Input('ThermDiff','value'),         # [(m^2)/s]
)
def getMedium(DROP_medium:str, Speed:float, Density:float, AbsCoeff:float, SpecHeatCap:float, ThermDiff:float):
    mediumProp = setParam.setMedium(DROP_medium, Speed, Density, AbsCoeff, SpecHeatCap, ThermDiff)
    return mediumProp['speed'], mediumProp['density'], mediumProp['absCoeff'], mediumProp['specHeatCap'], mediumProp['thermDiff']

# Update 2D Figure (Pressure or Intensity)
@callback(
    Output('GRAPH_field2D', 'figure'),  # [fig]
    
    Input('buttonLoad','n_clicks'),     # [num]
    Input('DROP_field2D','value'),      # [text]
    Input('dataFrame','value'),         # [p/p0]
    Input('ZAXE','value'),              # [m]
    Input('RAXE','value'),              # [m]
    Input('InitPress','value'),         # [MPa]
    Input('DutyCycle','value'),         # [%]
    Input('Speed','value'),             # [m/s]
    Input('Density','value'),           # [kg/m^3]
)
def update2Dfigure(btnClicks:int,DROP_field2D:str,filename1:str,filename2:str,filename3:str,
                InitPress:float,DutyCycle:int,Speed:float,Density:float):
    if btnClicks > 0:
        # Load in Files
        df_pressure2D = np.array(pd.read_csv(filename1))[:,1:]
        z_axis = np.array(pd.read_csv(filename2))[:,1]
        r_axis = np.array(pd.read_csv(filename3))[:,1]
        # Identify what to Graph
        match DROP_field2D:
            case 'Intensity':
                display_array = pow(df_pressure2D,2) * pow(InitPress,2) * DutyCycle / (2 * Density * Speed)
                colorbarLabel = "[MPa^2]"
                titleLabel = "Intensity Map"
            case 'Pressure':
                display_array = df_pressure2D * InitPress
                colorbarLabel = "[MPa]"
                titleLabel = "Pressure Map"
        # Plotly Express Figure Structure
        fig2D = px.imshow(
            display_array, 
            x = z_axis, 
            y = r_axis,
            labels={"x":"Z-Axis [m]", "y":"R-Axis [m]", "color":colorbarLabel},
            title=titleLabel,
            aspect='auto', 
            origin='lower',
            color_continuous_scale='jet', 
        )
        return fig2D
    else:
        fig2D = go.Figure()
        fig2D.update_layout(
            title=dict(text='Load Data Required'),
            xaxis=dict(title=dict(text='Z-Axis [m]')),
            yaxis=dict(title=dict(text='R-Axis [m]')),
        )
        return fig2D

# Calculate Pressure Field (When Button is Pressed)
@callback(
    Output('dataFrame','value'),        # [text] links to 2D List [p/p0] 
    Output('ZAXE','value'),             # [text] links to 1D List [m]
    Output('RAXE','value'),             # [text] links to 1D List [m]

    Input('button2D','n_clicks'),       # [n_clicks]
    Input('Frequency','value'),         # [MHz] will get converted to [Hz]
    Input('Radius','value'),            # [m]
    Input('Focus','value'),             # [m]
    Input('InitPress','value'),         # [MPa] will get converted to [Pa]
    Input('DROP_medium','value'),       # [text]
    Input('Speed','value'),             # [m/s]
    Input('Density','value'),           # [kg/m^3]
    Input('AbsCoeff','value'),          # [Np/(m*MHz^2)]
    Input('SpecHeatCap','value'),       # [J/(kg*K)]
    Input('ThermDiff','value'),         # [(m^2)/s]
    Input('numZ','value'),              # [num]
    Input('numR','value'),              # [num]
    Input('dataFrame','value'),         # [text] links to 2D List [p/p0]
    Input('ZAXE','value'),              # [text] links to 1D List [m]
    Input('RAXE','value'),              # [text] links to 1D List [m]
)
def calculate2DField(button2DClicks:int,
                    Frequency:float, Radius:float, Focus:float, InitPress:float, 
                    DROP_medium:str, Speed:float, Density:float, AbsCoeff:float, SpecHeatCap:float, ThermDiff:float,
                    numZ:int, numR:int, 
                    filename1:str, filename2:str, filename3:str):
    # When the Button is Pressed
    if 'button2D' == ctx.triggered_id:
        # Set Input Parameters
        trans = dict(freq = Frequency*1e6,radius = Radius, focus = Focus, initPressure = InitPress*1e6)
        medium = setParam.setMedium(DROP_medium, Speed, Density, AbsCoeff, SpecHeatCap, ThermDiff)
        field = dict(numAxialStep = numZ, numRadialStep = numR)
        # Rayleigh Integral
        df_pressure2D, z_axis, r_axis, iscomplete = calculateRayleighIntegral.generateField(trans,medium,field)
        # Check and Return Filenames
        if iscomplete == 0:
            # Error
            filename1="ERROR_df"
            filename2="ERROR_z"
            filename3="ERROR_r"
            return filename1, filename2, filename3
        else:
            # Convert Data to Pandas Data Frame
            df_pressure2D = pd.DataFrame(df_pressure2D)
            z_axis = pd.DataFrame(z_axis)
            r_axis = pd.DataFrame(r_axis)
            # File Names and Save to CSV
            filename1="df_pressure2D_" + str(button2DClicks) + ".csv"
            df_pressure2D.to_csv(filename1)
            filename2="z_axis_" + str(button2DClicks) + ".csv"
            z_axis.to_csv(filename2)
            filename3="r_axis_" + str(button2DClicks) + ".csv"
            r_axis.to_csv(filename3)
            # Return Links
            directory = os.getcwd()  
            filename1_path = directory + "\\" +  filename1
            filename2_path = directory + "\\" +  filename2
            filename3_path = directory + "\\" +  filename3

            return filename1_path, filename2_path, filename3_path
    # When Button is Not Pressed
    else:
        return filename1, filename2, filename3

# Calculate Bioheat and Output Time Graph for Specific Location
@callback(
    Output('GRAPH_time1D', 'figure'),   # [fig]
    Input('button1D','n_clicks'),       # [n_clicks]

    Input('Frequency','value'),         # [MHz] will get converted to [Hz]
    Input('Radius','value'),            # [m]
    Input('Focus','value'),             # [m]
    Input('InitPress','value'),         # [MPa] will get converted to [Pa]
    Input('DROP_medium','value'),       # [text]
    Input('Speed','value'),             # [m/s]
    Input('Density','value'),           # [kg/m^3]
    Input('AbsCoeff','value'),          # [Np/(m*MHz^2)]
    Input('SpecHeatCap','value'),       # [J/(kg*K)]
    Input('ThermDiff','value'),         # [(m^2)/s]
    Input('numTime','value'),           # [s]
    Input('HeatTime','value'),          # [s]
    Input('CoolTime','value'),          # [s]
    Input('DutyCycle','value'),         # [%]
    Input('observeZ','value'),          # [m]
    Input('observeR','value'),          # [m]
    Input('dataFrame','value'),         # [text] links to 2D List [p/p0]
    Input('ZAXE','value'),              # [text] links to 1D List [m]
    Input('RAXE','value'),              # [text] links to 1D List [m]
)
def calculate1DField(button1DClicks:int,
                    Frequency:float, Radius:float, Focus:float, InitPress:float, 
                    DROP_medium:str, Speed:float, Density:float, AbsCoeff:float, SpecHeatCap:float, ThermDiff:float,
                    numTime:float, HeatTime:int, CoolTime:int, DutyCycle:int,
                    observeZ:float, observeR:float,
                    filename1:str, filename2:str, filename3:str):
    # When the Button is Pressed
    if 'button1D' == ctx.triggered_id:
        # Get Files   
        df_pressure2D = np.array(pd.read_csv(filename1))[:,1:]
        z_axis = np.array(pd.read_csv(filename2))[:,1]
        r_axis = np.array(pd.read_csv(filename3))[:,1]
        # Set Input Parameters
        trans = dict(freq = Frequency*1e6,radius = Radius, focus = Focus, initPressure = InitPress*1e6)
        medium = setParam.setMedium(DROP_medium, Speed, Density, AbsCoeff, SpecHeatCap, ThermDiff)
        heat = dict(HeatTime = HeatTime, CoolTime = CoolTime, DutyCycle = DutyCycle, numTime = numTime)
        # Bioheat Equation for Location in Space
        time_axis, temp_vec, Q, iscomplete = calculateBioheat.generateVector(observeZ,observeR,trans,medium,heat,df_pressure2D,z_axis,r_axis,iscomplete=0)
        # Check and Plot
        if iscomplete == 0:
            fig1D = go.Figure()
            fig1D.update_layout(
                title=dict(text='Error'),
                xaxis=dict(title=dict(text='Time [s]')),
                yaxis=dict(title=dict(text='Temperature [Degrees Celsius]')),
            )
            return fig1D
        else:
            fig1D = go.Figure(data=go.Scatter(x=time_axis, y=temp_vec))
            fig1D.update_layout(
                    title=dict(text='Temperature Increase at LOC (' + str(observeZ) + ',' + str(observeR) + ') [m]'),
                    xaxis=dict(title=dict(text='Time [s]')),
                    yaxis=dict(title=dict(text='Temperature [Degrees Celsius]')),
            )
            return fig1D
    # When Button is Not Pressed
    else:
        fig1D = go.Figure()
        return fig1D

# Execute App
if __name__ == '__main__':
    app.run(debug=True)