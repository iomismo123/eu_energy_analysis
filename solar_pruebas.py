import matplotlib.pyplot as plt
import utils # uses pysdmx to download data

# Countries of interest
geo_list = ["ES", "FR", "IT", "DE", "PL"]

# Query definition
solar_constraints  = {
    'freq': 'A',
    # 'plants': 'Total',
    # 'operator': 'Total',
    'nrg_bal': 'GEP',
    'siec': ['RA100', 'RA130', 'RA300', 'RA410', 'RA420', 'G3000', 'C0000X0350-0370', 'N900H', 'TOTAL'],  # RA100: Hydro, RA130: Pumped Hydro, RA300: Eólica, RA400: Solar Thermal, RA400: Solar Photo, G3000: Gas, C0000X0350-0370: Carbón
    'unit': 'GWH',
    'geo': geo_list,
}

# 1.- Data download
# with this query, defined in "solar_constraints", we download all the needed data
datos = utils.get_dataset_with_selection('nrg_bal_peh', solar_constraints)
renewables_production = datos.data # type: ignore

# data pivot for convenience
pivot_data = renewables_production.pivot_table(
    index=['TIME_PERIOD', 'geo'],
    columns='siec',
    values='OBS_VALUE',
    aggfunc='sum'
).reset_index().rename(columns={
    'RA100':'hydro_GWh', 
    'RA130':'pumped_hydro_GWh', 
    'RA300':'wind_GWh', 
    'RA410':'solar_therm_GWh', 
    'RA420':'solar_photo_GWh', 
    'G3000':'gas_GWh',
    'C0000X0350-0370':'coal_GWh',
    'N900H': 'nuclear_GWh',
    'TOTAL':'total_GWh'})

# Calcular porcentajes
pivot_data['Total_no_hydro_nuc'] = pivot_data['total_GWh'] - (pivot_data['hydro_GWh'] + pivot_data['pumped_hydro_GWh'] + pivot_data['nuclear_GWh'])
pivot_data['solar_GWh'] = pivot_data['solar_therm_GWh'] + pivot_data['solar_photo_GWh']
pivot_data['renewables_%'] = 100 * (pivot_data['wind_GWh'] + pivot_data['solar_therm_GWh'] + pivot_data['solar_photo_GWh']) / pivot_data['Total_no_hydro_nuc']
pivot_data['gas_%'] = 100 * pivot_data['gas_GWh'] / pivot_data['Total_no_hydro_nuc']
pivot_data['coal_%'] = 100 * pivot_data['coal_GWh'] / pivot_data['Total_no_hydro_nuc']

# 1.- Renewable in electricity generation evolution
# We can see how 
fig, axes = plt.subplots(len(geo_list), 1, figsize=(12, 25), sharex=True)

for idx, country in enumerate(geo_list):
    country_data = pivot_data[pivot_data['geo'] == country]
    ax1 = axes[idx]

    ax1.plot(country_data['TIME_PERIOD'], country_data['solar_GWh'], label='Solar', color='tab:red')
    ax1.plot(country_data['TIME_PERIOD'], country_data['wind_GWh'], label='Wind', color='tab:gray')
    ax1.set_ylabel('Generación (GWh)', color='tab:red')

    ax2 = ax1.twinx()
    ax2.plot(country_data['TIME_PERIOD'], country_data['renewables_%'], label='% Renewables', linestyle='--', color='tab:purple')
    ax2.set_ylabel('Porcentaje (%)', color='tab:purple')

    ax1.set_title(f'{country}')
    ax1.grid()

fig.suptitle('Evolution of Solar and Wind energy in electricity generation')
fig.tight_layout(rect=(0, 0.03, 1, 0.97))
plt.xlabel('Year')
plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
plt.show()

# 2.- Gas and Coal consumption in electricity generation
fig, axes = plt.subplots(len(geo_list), 1, figsize=(12, 25), sharex=True)

for idx, country in enumerate(geo_list):
    country_data = pivot_data[pivot_data['geo'] == country]
    ax1 = axes[idx]

    ax1.plot(country_data['TIME_PERIOD'], country_data['gas_GWh'], label='Natural Gas', color='tab:red')
    ax1.plot(country_data['TIME_PERIOD'], country_data['coal_GWh'], label='Coal', color='tab:gray')
    ax1.set_ylabel('Generación (GWh)', color='tab:red')

    ax2 = ax1.twinx()
    ax2.plot(country_data['TIME_PERIOD'], country_data['gas_%'], label='% ', linestyle='--', color='tab:purple')
    ax2.plot(country_data['TIME_PERIOD'], country_data['coal_%'], label='% Coal', linestyle='--', color='tab:brown')
    ax2.set_ylabel('Porcentaje (%)', color='tab:purple')

    ax1.set_title(f'{country}')
    ax1.grid()

fig.suptitle('Evolution of Natural Gas y Coal in electricity generation')
fig.tight_layout(rect=(0, 0.03, 1, 0.97))
plt.xlabel('Year')
plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
plt.show()

# 3.- Focus on one country, Spain
# 3.1.- Now we re goin to see if rise in renewables and decrease in coal and gas is correlated


# 3.2.- Now we are going to see if there is correlation between the rise in renewables and lower CO2 emissions

input("Presiona Enter para continuar...")



