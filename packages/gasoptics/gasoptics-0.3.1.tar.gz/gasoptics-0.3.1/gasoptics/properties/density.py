import math
from properties.gas_constant import calculate_specific_gas_constant
from properties.cv import calculate_humidity_ratio
from backends.redlich_kwong import calculate_redlich_kwong_Z

def calculate_density(T, P, gas="air", RH=0):
    """
    Calculate the density (rho) for a gas.

    - If gas is "air" and RH > 0, calculate for humid air.
    - If gas is "air" and RH = 0 (default), calculate for dry air.
    - For other gases, calculate real gas density.

    :param T: Temperature in Kelvin.
    :param P: Pressure in Pascals.
    :param gas: Name of the gas (default: "air").
    :param RH: Relative humidity (0 to 1, default: 0 for dry air).
    :return: Density (rho) in kg/m³.
    """
    if gas == "air" and RH > 0:  # Humid air case
        # Convert temperature to Celsius for saturation pressure calculation
        T_celsius = T - 273.15
        P_vs = 611.21 * math.exp((17.502 * T_celsius) / (240.97 + T_celsius))  # Saturation vapor pressure in Pa
        P_v = RH * P_vs  # Partial pressure of water vapor
        P_d = P - P_v  # Partial pressure of dry air

        Z_air = calculate_redlich_kwong_Z(P_d, T, 'air')
        z_water = calculate_redlich_kwong_Z(P_v, T, 'water_vapor')

        # Specific gas constants
        R_air = calculate_specific_gas_constant("air")
        R_water_vapor = calculate_specific_gas_constant("water_vapor")

        # Density calculation for dry air and water vapor
        rho_dry_air = P_d / (Z_air * R_air * T)
        rho_water_vapor = P_v / (z_water * R_water_vapor * T)

        # Total density
        rho_humid_air = rho_dry_air + rho_water_vapor
        return rho_humid_air
    
    else:  # Dry air or other gases
        # Specific gas constant
        R_specific = calculate_specific_gas_constant(gas)

        # Compressibility factor
        Z = calculate_redlich_kwong_Z(P, T, gas)

        # Real gas density
        rho = P / (Z * R_specific * T)
        return rho

def calculate_density_test(T, P, gas="air", RH=0):
    """
    Calculate the density (rho) for a gas.

    - If gas is "air" and RH > 0, calculate for humid air.
    - If gas is "air" and RH = 0 (default), calculate for dry air.
    - For other gases, calculate real gas density.

    :param T: Temperature in Kelvin.
    :param P: Pressure in Pascals.
    :param gas: Name of the gas (default: "air").
    :param RH: Relative humidity (0 to 1, default: 0 for dry air).
    :return: Density (rho) in kg/m³.
    """

    # Specific gas constant
    R_specific = calculate_specific_gas_constant(gas)

    # Compressibility factor
    Z = calculate_redlich_kwong_Z(P, T, gas)

    # Real gas density
    rho = P / (Z * R_specific * T)

    if gas == "air" and RH > 0:  # Humid air case

        # Convert temperature to Celsius for saturation pressure calculation
        T_celsius = T - 273.15
        P_vs = 611.21 * math.exp((17.502 * T_celsius) / (240.97 + T_celsius))  # Saturation vapor pressure in Pa
        P_v = RH * P_vs  # Partial pressure of water vapor
        P_d = P - P_v  # Partial pressure of dry air
        Z_air = calculate_redlich_kwong_Z(P_d, T, gas)
        Z_water = calculate_redlich_kwong_Z(P_v, T, gas)
        
        # Specific gas constants
        R_air = calculate_specific_gas_constant("air")
        R_water_vapor = calculate_specific_gas_constant("water_vapor")

        # Density calculation for dry air and water vapor
        rho_dry_air = P_d / (Z_air * R_air * T)
        rho_water_vapor = P_v / (Z_water * R_water_vapor * T)

        # Total density
        rho_humid_air = rho_dry_air + rho_water_vapor
        return rho_humid_air  
        

    return rho