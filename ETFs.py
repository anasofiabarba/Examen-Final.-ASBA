# Paso 1: Instalar yfinance y pandas
# Primero abre la terminal y ejecuta los siguientes comandos para instalar las librerías necesarias:
# pip install yfinance pandas

import yfinance as yf
import json
import pandas as pd

# Lista inicial de ETFs en JSON
etfs_json = '''
[
    {"symbol": "CNYA", "name": "AZ China"},
    {"symbol": "EWT", "name": "AZ MSCI Taiwan"},
    {"symbol": "IWM", "name": "AZ Russell 2000"},
    {"symbol": "EWZ", "name": "AZ Brasil"},
    {"symbol": "EWU", "name": "AZ MSCI United Kingdom"},
    {"symbol": "XLF", "name": "AZ DJ US Financial Sect"},
    {"symbol": "BKF", "name": "AZ BRIC"},
    {"symbol": "EWY", "name": "AZ MSCI South Korea"},
    {"symbol": "AGG", "name": "AZ Barclays Aggregate"},
    {"symbol": "EEM", "name": "AZ Mercados Emergentes"},
    {"symbol": "EZU", "name": "AZ MSCI EMU"},
    {"symbol": "FXI", "name": "AZ FTSE/Xinhua China 25"},
    {"symbol": "GLD", "name": "AZ Oro"},
    {"symbol": "QQQ", "name": "AZ QQQ NASDAQ 100"},
    {"symbol": "AAXJ","name": "AZ MSCI Asia ex-Japan"},
    {"symbol": "SHY", "name": "AZ Barclays 1-3 Year Tr"},
    {"symbol": "ACWI", "name": "AZ MSCI ACWI Index Fund"},
    {"symbol": "SLV", "name": "AZ Silver Trust"},
    {"symbol": "EWH", "name": "AZ MSCI Hong Kong Index"},
    {"symbol": "SPY", "name": "AZ SPDR S&P 500 ETF Trust"},
    {"symbol": "EWJ", "name": "AZ MSCI Japan Index Fund"},
    {"symbol": "IEI", "name": "AZ BG EUR Govt Bond 1-3"},
    {"symbol": "DIA", "name": "AZ SPDR DJIA Trust"},
    {"symbol": "EWQ", "name": "AZ MSCI France Index Fund"},
    {"symbol": "VWO", "name": "AZ Vanguard Emerging Market ETF"},
    {"symbol": "EWA", "name": "AZ MSCI Australia Index"},
    {"symbol": "EWC", "name": "AZ MSCI Canada"},
    {"symbol": "ILF", "name": "AZ S&P Latin America 40"},
    {"symbol": "XLV", "name": "AZ Health Care Select Sector"},
    {"symbol": "EWG", "name": "AZ MSCI Germany Index"},
    {"symbol": "ITB", "name": "AZ DJ US Home Construct"}
]
'''



# Cargar JSON
etfs = json.loads(etfs_json)

# Función para verificar si el símbolo es válido en Yahoo Finance
def verify_etf_symbols(etfs):
    valid_etfs = []
    for etf in etfs:
        symbol = etf["symbol"]
        ticker = yf.Ticker(symbol)
        try:
            # Intentamos descargar un rango pequeño de datos para verificar si el símbolo es válido
            data = ticker.history(period="1d")
            if not data.empty:
                valid_etfs.append(etf)
                print(f"Valid symbol: {symbol} ({etf['name']})")
            else:
                print(f"Invalid symbol: {symbol} ({etf['name']})")
        except Exception as e:
            print(f"Error with symbol: {symbol} ({etf['name']}), Error: {str(e)}")
    
    return valid_etfs

# Verificar símbolos
valid_etfs = verify_etf_symbols(etfs)

# Guardar en un nuevo archivo JSON solo los símbolos válidos
with open('valid_etfs.json', 'w') as f:
    json.dump(valid_etfs, f, indent=4)

print("\nValid symbols saved to 'valid_etfs.json'")

# Paso 4: Ejecutar el script
# Una vez que hayas instalado las librerías necesarias, guarda este código en un archivo llamado 'verificar_etfs.py'.
# Luego, abre la terminal, navega hasta la carpeta donde guardaste el archivo y ejecuta:
# python verificar_etfs.py
