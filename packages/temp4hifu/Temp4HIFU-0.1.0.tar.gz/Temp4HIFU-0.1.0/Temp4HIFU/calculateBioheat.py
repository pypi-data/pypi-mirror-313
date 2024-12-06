def generateVector(axial_loc:float,radial_loc:float,trans:dict,medium:dict,heat:dict,pressure2D:list,z_values:list,r_values:list,iscomplete=0):
    """
    INPUT ARG
        axial_loc == [float][m] Coordinate Z of Interest Location
        radial_loc == [float][m] Coordinate R of Interest Location

        trans == [dict] dictionary of transducer properties
            "freq" == [float][Hz] Transmit Frequency of transducer
            "radius" == [float][m] Radius of transducer probe
            "focus" == [float][m] Focal point in space 
            "initPressure" == [float][Pa] Initial Pressure output by transducer

        medium == [dict] dictionary of medium properties
            "speed" == [float][m/s] Speed of Sound
            "density" == [float][kg/m^3] Density 
            "absCoeff" == [float][Np/(m*MHz^2)] Absorption Coefficient
            "specHeatCap" == [float][J/(kg*K)] Specific Heat Capacity
            "thermDiff" == [float][(m^2)/s] Thermal Diffusivity 

        heat == [dict] dictionary of heating parameters
            "numTime" == [float][s] Time Step aka Delta Time
            "HeatTime" == [int][s] Amount of Time for Heating
            "CoolTime" == [int][s] Amount of Time for Cooling
            "DutyCycle" == [int][%] Ratio of On vs Off Time during Heating

        pressure2D == [2D list][p/p0] Rayleigh Integral Pressure Field
        z_values == [1D list][m] Axial axis of Pressure Field
        r_values == [1D list][m] Radial axis of Pressure Field 
        
    OUTPUT ARG
        time_axis == [1D list][s] Time Axis
        temp_vec == [1D list][Celsius] Temperature Vector over Time
        Q == [2D list][Joules] Heat Map 
    """
    import numpy as np

    # Edit and Transform Transducer Properties
    d = trans["focus"] # Reallocate variable
    abs_Coeff = medium["absCoeff"] * (pow((trans["freq"]/(1e6)),2)) # POWER LAW
    dutyCycleRatio = heat["DutyCycle"]/100 # Duty Cycle Percentage
    # Set Axes and Steps
    axial_min = 0.001
    axial_max = 2*d
    radial_min = -trans["radius"]
    dz = (axial_max - axial_min) / (len(z_values)-1)
    dr = -1 * radial_min / ((len(r_values)-1)/2)
    dt = heat["numTime"]
    time_axis = np.arange(0,(heat["HeatTime"]+heat["CoolTime"]+dt),dt)
    # Conversion of Heat Input due to Intensity
    intensity2D = pow(pressure2D,2) * pow(trans["initPressure"],2) * dutyCycleRatio / (2 * medium["density"] * medium["speed"])
    Q = intensity2D * 2 * abs_Coeff / (medium["density"] * medium["specHeatCap"])

    # Temperature Matrix and Indices
    numR,numZ = np.shape(pressure2D)
    temp_dist = np.zeros((numR,numZ),dtype=np.float64)
    r_center_idx = round(((0-radial_min)/dr)+1)
    radial_temp_idx = round(((radial_loc-radial_min)/dr)+1)
    axial_temp_idx = round(((axial_loc-axial_min)/dz)+1)
    temp_vec = []
    temp_vec.append(temp_dist[axial_temp_idx,radial_temp_idx])

    # FTCS Scheme ADD FUNCTION FOR HEAT
    print('HEATING')
    for time_step in np.arange(dt,heat["HeatTime"]+dt,dt):
        curr_temp_dist = temp_dist
        for ii in range(1,numR-1):
            for jj in range(1, numZ-1):
                currTemp = curr_temp_dist[ii,jj]

                z_component = ((dt * medium["thermDiff"]) / pow(dr,2)) \
                * (curr_temp_dist[ii+1,jj] - (2 * curr_temp_dist[ii,jj]) + curr_temp_dist[ii-1,jj]) 

                r_component = ((dt * medium["thermDiff"]) / pow(dr,2)) \
                * (curr_temp_dist[ii,jj+1] - (2 * curr_temp_dist[ii,jj]) + curr_temp_dist[ii,jj-1]) \
                + (1/r_values[jj]) * (curr_temp_dist[ii,jj+1] - curr_temp_dist[ii,jj-1]) \
                * (dt * medium["thermDiff"] / (2*dr))

                if jj == r_center_idx:
                    r_component = 4*((dt * medium["thermDiff"]) / pow(dr,2)) \
                    * (curr_temp_dist[ii,jj+1] - curr_temp_dist[ii,jj])

                Q_US = dt * Q[ii,jj]
                temp_dist[ii,jj] = currTemp + z_component + r_component + Q_US
        temp_vec.append(temp_dist[axial_temp_idx,radial_temp_idx])

    # FTCS Scheme ADD FUNCTION FOR COOL
    print('COOLING')
    for time_step in np.arange(dt,heat["CoolTime"],dt):
        curr_temp_dist = temp_dist
        for ii in range(1,numR-2):
            for jj in range(1, numZ-2):
                currTemp = curr_temp_dist[ii,jj]

                z_component = ((dt * medium["thermDiff"]) / pow(dr,2)) \
                * (curr_temp_dist[ii+1,jj] - (2 * curr_temp_dist[ii,jj]) + curr_temp_dist[ii-1,jj]) 

                r_component = ((dt * medium["thermDiff"]) / pow(dr,2)) \
                * (curr_temp_dist[ii,jj+1] - (2 * curr_temp_dist[ii,jj]) + curr_temp_dist[ii,jj-1]) \
                + (1/r_values[jj]) * (curr_temp_dist[ii,jj+1] - curr_temp_dist[ii,jj-1]) \
                * (dt * medium["thermDiff"] / (2*dr))

                if jj == r_center_idx:
                    r_component = 4*((dt * medium["thermDiff"]) / pow(dr,2)) \
                    * (curr_temp_dist[ii,jj+1] - curr_temp_dist[ii,jj])

                temp_dist[ii,jj] = currTemp + z_component + r_component
        temp_vec.append(temp_dist[axial_temp_idx,radial_temp_idx])

    # Finish
    print("Bioheat Calculation Complete")
    iscomplete = 1
    return time_axis, temp_vec, Q, iscomplete
