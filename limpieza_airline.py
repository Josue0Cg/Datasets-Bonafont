import pandas as pd
import os

FILE_NAME = 'L_AIRLINE_ID_bruto.csv'
OUTPUT_NAME = 'L_AIRLINE_ID_limpio.csv'

try:
    df = pd.read_csv(FILE_NAME)
    print("Carga inicial exitosa. Filas:", len(df))
    print("\nColumnas antes de la limpieza:")
    print(df.head())
    print("\nInformación del DataFrame:")
    df.info()

except FileNotFoundError:
    print(f"ERROR: Archivo no encontrado en la ruta: {FILE_NAME}")
    exit()

# paso 2, renombrar las columnas
print("\n--- PASO 1: Renombrando Columnas ---")

df.rename(columns={'Code': 'AirlineID', 'Description': 'AirlineName'}, inplace=True)

print("Nuevas columnas:", df.columns.tolist())
print(df.head())

# paso 3, manejo de valores nulos y duplicados
print("\n--- PASO 2: Manejo de Nulos y Duplicados ---")

# nulos
nulos_antes = df.isnull().sum()
print("Nulos en AirlineName antes de limpiar:", nulos_antes['AirlineName'])

df.dropna(subset=['AirlineID', 'AirlineName'], inplace=True)

nulos_despues = df.isnull().sum()
print("Nulos en AirlineName despues de limpiar:", nulos_despues['AirlineName'])
print("Filas restantes después de eliminar nulos:", len(df))

# duplicados
duplicados_antes = df.duplicated().sum()
df.drop_duplicates(inplace=True)
duplicados_despues = df.duplicated().sum()

print(f"Se eliminaron {duplicados_antes - duplicados_despues} filas duplicadas.")

# paso 4 limpiar el campo AirlineName
print("\n--- PASO 3: Limpieza y Estandarización de AirlineName ---")

#separar el nombre del código 
df[['AirlineName_Clean', 'AirlineCode']] = df['AirlineName'].str.rsplit(':', n=1, expand=True)

# eliminar comillas 
df['AirlineName_Clean'] = df['AirlineName_Clean'].str.strip().str.replace('"', '', regex=False)

# eliminar espacios extra
df['AirlineCode'] = df['AirlineCode'].str.strip()

#reemplazar la columna antigua y eliminar columnas intermedias si es necesario
df.drop('AirlineName', axis=1, inplace=True)
df.rename(columns={'AirlineName_Clean': 'AirlineName'}, inplace=True)


print("Muestra después de la separación:")
print(df[['AirlineID', 'AirlineName', 'AirlineCode']].head())

#paso final guardar el archivo limpio
print("\n--- PASO FINAL: Guardando el Archivo Limpio ---")

# Convertir el ID a entero antes de guardar
df['AirlineID'] = df['AirlineID'].astype(int)

df.to_csv(OUTPUT_NAME, index=False, encoding='utf-8')

print(f"Archivo limpio guardado exitosamente como: {OUTPUT_NAME}")
print("\n¡Limpieza completada!")