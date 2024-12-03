import streamlit as st
import yfinance as yf
import os

# Función para descargar datos históricos de los ETFs
def download_etf_data(etf, start_date, end_date):
    symbol = etf['symbol']
    name = etf['name']
    description = etf['description']

    st.write(f"Descargando datos de {name} ({symbol}) - {description}...")
    
    # Descargar datos históricos
    etf_data = yf.download(symbol, start=start_date, end=end_date)
    
    # Crear directorio para guardar los archivos si no existe
    if not os.path.exists("etf_data"):
        os.makedirs("etf_data")
    
    # Guardar los datos en un archivo CSV
    file_name = f"etf_data/{symbol}_historical_data.csv"
    etf_data.to_csv(file_name)
    st.write(f"Datos de {name} guardados en {file_name}")

# Lista completa de ETFs con símbolo, nombre y descripción
etfs = [
    {"symbol": "ASHR", "name": "AZ China", "description": "ETF que sigue el índice CSI 300 que incluye acciones de empresas chinas."},
    {"symbol": "EWT", "name": "AZ MSCI Taiwan Index Fund", "description": "ETF que sigue el índice MSCI Taiwan compuesto por empresas líderes en Taiwán."},
    {"symbol": "IWM", "name": "AZ Russell 2000", "description": "ETF que sigue el índice Russell 2000, que incluye empresas estadounidenses de pequeña capitalización."},
    {"symbol": "EWZ", "name": "AZ Brasil", "description": "ETF que sigue el índice MSCI Brasil compuesto por empresas líderes brasileñas."},
    {"symbol": "EWU", "name": "AZ MSCI United Kingdom", "description": "ETF que sigue el índice MSCI United Kingdom, que incluye empresas líderes del Reino Unido."},
    {"symbol": "IYF", "name": "AZ DJ US Financial Sector", "description": "ETF que sigue el índice del sector financiero de EE.UU."},
    {"symbol": "BKF", "name": "AZ BRIC", "description": "ETF que sigue el índice de mercados emergentes BRIC: Brasil, Rusia, India y China."},
    {"symbol": "EWY", "name": "AZ MSCI South Korea Index", "description": "ETF que sigue el índice MSCI South Korea, que incluye las principales empresas de Corea del Sur."},
    {"symbol": "AGG", "name": "AZ Barclays Aggregate", "description": "ETF que sigue el índice Bloomberg Barclays U.S. Aggregate Bond."},
    {"symbol": "EEM", "name": "AZ Mercados Emergentes", "description": "ETF que sigue el índice MSCI Emerging Markets compuesto por empresas en mercados emergentes."},
    {"symbol": "EZU", "name": "AZ MSCI EMU", "description": "ETF que sigue el índice MSCI EMU, que incluye empresas de la Eurozona."},
    {"symbol": "FXI", "name": "AZ FTSE/Xinhua China 25", "description": "ETF que sigue el índice FTSE China 25 que incluye grandes empresas chinas."},
    {"symbol": "GLD", "name": "AZ Oro", "description": "ETF respaldado por oro físico, diseñado para seguir el precio del oro."},
    {"symbol": "CTT", "name": "AZ LATIXX Mex CETETRAC", "description": "ETF que sigue los CETES a corto plazo en México."},
    {"symbol": "QQQ", "name": "AZ QQQ Nasdaq 100", "description": "ETF que sigue el índice Nasdaq 100 compuesto por 100 de las empresas tecnológicas más grandes."},
    {"symbol": "AAXJ", "name": "AZ MSCI Asia Ex-Japan", "description": "ETF que sigue el índice MSCI Asia Ex-Japan, que incluye empresas de Asia sin Japón."},
    {"symbol": "MTF", "name": "AZ LATIXX Mex M10TRAC", "description": "ETF que sigue los bonos M10 de México, un índice de deuda soberana."},
    {"symbol": "SHY", "name": "AZ Barclays 1-3 Year Treasury", "description": "ETF que sigue el índice de bonos del Tesoro de EE.UU. a 1-3 años."},
    {"symbol": "ACWI", "name": "AZ MSCI ACWI Index Fund", "description": "ETF que sigue el índice MSCI All Country World Index, compuesto por empresas globales."},
    {"symbol": "M5TRAC", "name": "AZ LATIXX Mexico M5TRAC", "description": "ETF que sigue los bonos M5 de México, representando deuda gubernamental."},
    {"symbol": "SLV", "name": "AZ Silver Trust", "description": "ETF respaldado por plata física, diseñado para seguir el precio de la plata."},
    {"symbol": "EWH", "name": "AZ MSCI Hong Kong Index", "description": "ETF que sigue el índice MSCI Hong Kong, compuesto por empresas de Hong Kong."},
    {"symbol": "UDI", "name": "AZ LATIXX Mex UDITRAC", "description": "ETF que sigue bonos del gobierno mexicano ligados a la inflación (UDIS)."},
    {"symbol": "SPY", "name": "AZ SPDR S&P 500 ETF Trust", "description": "ETF que sigue el índice S&P 500, compuesto por las 500 empresas más grandes de EE.UU."},
    {"symbol": "EWJ", "name": "AZ MSCI Japan Index Fund", "description": "ETF que sigue el índice MSCI Japan, compuesto por empresas japonesas."},
    {"symbol": "BGR", "name": "AZ BG EUR Govt Bond 1-3", "description": "ETF que sigue los bonos soberanos europeos de corto plazo (1-3 años)."},
    {"symbol": "DIA", "name": "AZ SPDR DJIA Trust", "description": "ETF que sigue el índice Dow Jones Industrial Average (DJIA), compuesto por 30 grandes empresas de EE.UU."},
    {"symbol": "EWQ", "name": "AZ MSCI France Index Fund", "description": "ETF que sigue el índice MSCI France, compuesto por empresas francesas."},
    {"symbol": "XOP", "name": "AZ DJ US Oil & Gas Exploration", "description": "ETF que sigue el índice del sector de exploración de petróleo y gas en EE.UU."},
    {"symbol": "VWO", "name": "AZ Vanguard Emerging Markets ETF", "description": "ETF que sigue el índice de mercados emergentes, compuesto por empresas en economías emergentes."},
    {"symbol": "EWA", "name": "AZ MSCI Australia Index", "description": "ETF que sigue el índice MSCI Australia, que incluye las principales empresas de Australia."},
    {"symbol": "IPC", "name": "AZ IPC Large Cap T R TR", "description": "ETF que sigue el índice IPC Large Cap, compuesto por empresas mexicanas de gran capitalización."},
    {"symbol": "XLF", "name": "AZ Financial Select Sector SPDR", "description": "ETF que sigue el sector financiero del S&P 500, que incluye bancos y aseguradoras."},
    {"symbol": "EWC", "name": "AZ MSCI Canada", "description": "ETF que sigue el índice MSCI Canada, compuesto por empresas líderes en Canadá."},
    {"symbol": "ILF", "name": "AZ S&P Latin America 40", "description": "ETF que sigue el índice S&P Latin America 40, compuesto por las principales empresas de América Latina."},
    {"symbol": "XLV", "name": "AZ Health Care Select Sector", "description": "ETF que sigue el sector salud del S&P 500, compuesto por empresas de salud y biotecnología."},
    {"symbol": "EWG", "name": "AZ MSCI Germany Index", "description": "ETF que sigue el índice MSCI Germany, compuesto por empresas líderes en Alemania."},
    {"symbol": "ITB", "name": "AZ DJ US Home Construction", "description": "ETF que sigue el índice de construcción de viviendas en EE.UU."}
]

# Título de la aplicación en Streamlit
st.title('Descargador de Datos Históricos de ETFs')

# Definir fechas de inicio y fin para los últimos 10 años
start_date = '2013-10-22'
end_date = '2023-10-22'

# Botón para iniciar la descarga
if st.button('Iniciar Descarga'):
    for etf in etfs:
        download_etf_data(etf, start_date, end_date)

    st.write("¡Descarga completada!")
