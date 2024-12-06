def setMedium(index:str, speed_in:float, dens_in:float, absCoeff_in:float, specHeatCap_in:float, thermDiff_in:float):
    """
    INPUT ARG
        index == [str] text to call specific preset dictionary
        speed_in == [float][m/s] Speed of Sound
        density_in == [float][kg/m^3] Density 
        absCoeff_in == [float][Np/(m*MHz^2)] Absorption Coefficient
        specHeatCap_in == [float][J/(kg*K)] Specific Heat Capacity
        thermDiff_in == [float][(m^2)/s] Thermal Diffusivity 

    OUTPUT ARG
        medium == [dict] dictionary of medium properties
            "name" == [str] Identifying Name for Preset Dictionaries 
            "speed" == [float][m/s] Speed of Sound
            "density" == [float][kg/m^3] Density 
            "absCoeff" == [float][Np/(m*MHz^2)] Absorption Coefficient
            "specHeatCap" == [float][J/(kg*K)] Specific Heat Capacity
            "thermDiff" == [float][(m^2)/s] Thermal Diffusivity 
    """
    # If Input is None, Set to Zero
    if speed_in == None: 
        speed_in = 0
    if dens_in == None: 
        dens_in = 0
    if absCoeff_in == None: 
        absCoeff_in = 0
    if specHeatCap_in == None: 
        specHeatCap_in = 0
    if thermDiff_in == None: 
        thermDiff_in = 0
    # Get Preset based on Index
    match index:
        case 'Water':
            medium = dict(
                name = 'Water',
                speed = 1500,
                density = 1000,
                absCoeff = 0.025,
                specHeatCap = 4180,
                thermDiff = 1.46 * 1e-7,
            )
        case 'Glycerol':
            medium = dict(
                name = 'Glycerol',
                speed = 1920,
                density = 1264,
                absCoeff = 3.6,
                specHeatCap = 2407,
                thermDiff = 0.95 * 1e-7,
            )
        case 'Egg White':
            medium = dict(
                name = 'Egg White',
                speed = 1546,
                density = 1045,
                absCoeff = 3.5,
                specHeatCap = 4270,
                thermDiff = 1.32 * 1e-7,
            )
        case 'Castor Oil':
            medium = dict(
                name = 'Castor Oil',
                speed = 1500,
                density = 960,
                absCoeff = 6,
                specHeatCap = 1800,
                thermDiff = 1.05 * 1e-7,
            )
        case 'Custom':
            medium = dict(
                name = 'Custom',
                speed = speed_in,
                density = dens_in,
                absCoeff = absCoeff_in,
                specHeatCap = specHeatCap_in,
                thermDiff = thermDiff_in,
            )
    return medium