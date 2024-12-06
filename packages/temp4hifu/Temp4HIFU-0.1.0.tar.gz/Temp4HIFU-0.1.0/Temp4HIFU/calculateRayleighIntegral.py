def generateField(trans:dict,medium:dict,field:dict,iscomplete=0):
    """
    INPUT ARG
        trans == [dict] dictionary of transducer properties
            "freq" == [float][Hz] Transmit Frequency of transducer
            "radius" == [float][m] Radius of transducer probe
            "focus" == [float][m] Focal point in space 
            "initPressure" == [float][Pa] Initial Pressure output by transducer

        medium == [dict] dictionary of medium properties
            "speed" == [float][m/s] Speed of Sound
            "density" == [float][kg/m^3] Density 
            "absCoeff" == [float][Np/(m*MHz^2)] Absorption Coefficient

        field == [dict] 2D field parameters
            "numAxialStep" == [int] Number of Axial Steps
            "numRadialStep" == [int] Number of Radial Steps

    OUTPUT ARG
        pressure_field == [2D list][p/p0] Resulting Rayleigh Integral Pressure Field
        z_axis == [1D list][m] Axial axis of Pressure Field
        r_axis == [1D list][m] Radial axis of Pressure Field 

    """
    import numpy as np
    
    # Edit and Transform Transducer Properties
    d = trans["focus"] # Reallocate variable
    k = 2 * np.pi * trans["freq"] / medium["speed"] # Wave Number
    angularF = trans["radius"]/trans["focus"] # Angular Frequency
    abs_Coeff = medium["absCoeff"] * (pow((trans["freq"]/(1e6)),2)) # POWER LAW
    # Set Axes
    axial_min = 0.001
    axial_max = 2*d
    radial_min = -trans["radius"]
    dz = (axial_max - axial_min) / field["numAxialStep"]
    numZ = int(np.round((axial_max - axial_min)/dz)+1)
    dr = -1 * radial_min / (field["numRadialStep"]/2)
    numR = int(np.round((0 - radial_min)/dr)+1)
    # Theta Component
    thetaMax = np.arcsin(angularF)
    numT = 100
    dtheta = thetaMax/numT

    # Preallocation
    z_values = list()
    r_values = list()
    pressure_field = np.empty((numZ,numR), dtype=float)
    # Rayleigh Integral
    z = axial_min
    for zz in range(0,numZ):
        r = radial_min
        for rr in range(0,numR):
            p = 0.5 * np.exp(1j * k * np.sqrt(z*z + r*r)) / np.sqrt(z*z + r*r) * dtheta
            for tt in range(1,numT+1):
                theta = tt * dtheta
                numP = (2*tt+1)
                dphi = (2*np.pi)/numP
                e1 = 0
                for pp in range(0,numP):
                    phi = dphi * pp
                    rf = np.sqrt((pow((d*np.sin(theta)),2))+r*r-2*np.sin(theta)*np.absolute(r)*d*np.cos(phi)+pow((z-d+d*np.cos(theta)),2))
                    e1 = e1 + np.exp(1j*k*rf)/rf
                p = p + e1*np.sin(theta)/(2*tt+1)
            amplitude = abs(p)*k*d*d*dtheta*np.exp(-abs_Coeff*(z-axial_min))
            pressure_field[zz,rr] = amplitude
            if zz == 0: 
                r_values.append(r)
            r = r + dr
        z_values.append(z)
        z = z + dz
        print((np.round(100 * (zz+1)/numZ)),'%')
    
    # Set Bottom Halves
    r_value_bothalf = r_values
    pressure_field_bothalf = pressure_field
    # Radial Symmetry (reflect pressure values across z-axis)
    pressure_field_tophalf = np.fliplr(pressure_field_bothalf)
    pressure_field = np.rot90(np.hstack((pressure_field_bothalf,pressure_field_tophalf[:,1:])),1)
    r_value_tophalf = np.flipud(np.absolute(r_value_bothalf))
    r_values = np.concatenate((r_value_bothalf,r_value_tophalf[1:]))
    # Fix Dividing by 0 at the first center point
    r_CenterIdx = round((-1*radial_min/dr))
    r_values[r_CenterIdx] = 1e-20
    pressure_field[r_CenterIdx,0] = 0

    # Finish
    print('Rayleigh Integral Complete')
    iscomplete = 1
    return pressure_field, z_values, r_values, iscomplete