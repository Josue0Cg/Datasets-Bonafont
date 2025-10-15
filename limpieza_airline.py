import pandas as pd
import numpy as np

INPUT = "L_AIRLINE_ID_dirty.csv"
OUTPUT = "L_AIRLINE_ID_clean.csv"

df = pd.read_csv(INPUT, dtype=str)
print("Primeras filas del dataset:")
print(df.head(), "\n")

print("Dimensiones:", df.shape)
print("\nValores nulos por columna:")
print(df.isnull().sum())

df = df.dropna(how="all")

df = df.drop_duplicates()

for col in df.columns:
    df[col] = df[col].astype(str).str.strip().replace({'nan': np.nan})

if 'Airline' in df.columns:
    df['Airline'] = df['Airline'].str.title()
if 'Origin' in df.columns:
    df['Origin'] = df['Origin'].str.upper()
if 'Destination' in df.columns:
    df['Destination'] = df['Destination'].str.upper()

if 'Delay' in df.columns:
    df['Delay'] = pd.to_numeric(df['Delay'], errors='coerce')
    df = df[df['Delay'] >= 0]  # eliminar retrasos negativos

df = df.fillna({
    'Airline': 'Desconocido',
    'Origin': 'SIN_DATO',
    'Destination': 'SIN_DATO'
})

df.to_csv(OUTPUT, index=False)
print(f"\nArchivo limpio guardado como {OUTPUT}")
