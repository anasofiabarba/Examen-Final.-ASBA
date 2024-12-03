import streamlit as st
import sqlite3
import bcrypt
import json
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(
    page_title="Allianz Patrimonial",
    page_icon=":chart_with_upwards_trend:",
    layout="centered"
)

# CSS personalizado
st.markdown("""
    <style>
    .stApp {
        background-color: white;
        color: #002f6c;
    }
    h1, h2, h3, label {
        color: #002f6c;
    }
    .stButton button {
        background-color: #002f6c;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stButton button:hover {
        background-color: #00448a;
    }
    .stImage img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)

# Conexión a la base de datos SQLite
conn = sqlite3.connect("users.db")
c = conn.cursor()

# Crear tablas si no existen
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT UNIQUE,
        phone TEXT,
        password TEXT
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS cliente_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        edad INTEGER,
        ingreso_mensual REAL,
        ocupacion TEXT,
        objetivo TEXT,
        nivel_riesgo TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')
conn.commit()

# Función para registrar un usuario
def register_user(first_name, last_name, email, phone, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        c.execute('INSERT INTO users (first_name, last_name, email, phone, password) VALUES (?, ?, ?, ?, ?)',
                  (first_name.strip(), last_name.strip(), email.strip(), phone.strip(), hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Función para autenticar usuario
def authenticate_user(email, password):
    c.execute('SELECT * FROM users WHERE email = ?', (email.strip(),))
    user = c.fetchone()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[5].encode('utf-8')):
        return user
    return None

# Inicialización de sesión
if "view" not in st.session_state:
    st.session_state.view = "login"

if "user" not in st.session_state:
    st.session_state.user = None

# Vista de inicio de sesión
if st.session_state.view == "login":
    st.image("allianz-1.svg", use_container_width=True, caption=None)
    st.title("Bienvenido a Allianz Patrimonial")
    st.markdown("### Inicia Sesión")
    email = st.text_input("Correo electrónico", key="login_email", placeholder="ejemplo@correo.com")
    password = st.text_input("Contraseña", type="password", key="login_password", placeholder="••••••••")

    if st.button("Iniciar Sesión"):
        user = authenticate_user(email, password)
        if user:
            st.session_state.user = user
            st.session_state.view = "menu"
            st.success(f"¡Bienvenido, {user[1]}!")
        else:
            st.error("Correo o contraseña incorrectos. Por favor, intenta de nuevo.")
    
    if st.button("¿No tienes cuenta? Regístrate aquí"):
        st.session_state.view = "register"

# Vista de registro
elif st.session_state.view == "register":
    st.image("allianz-1.svg", use_container_width=True, caption=None)
    st.title("Crea tu cuenta en Allianz Patrimonial")
    first_name = st.text_input("Nombre", key="register_first_name")
    last_name = st.text_input("Apellido", key="register_last_name")
    email = st.text_input("Correo electrónico", key="register_email", placeholder="ejemplo@correo.com")
    phone = st.text_input("Teléfono", key="register_phone", placeholder="10 dígitos")
    password = st.text_input("Contraseña", type="password", key="register_password", placeholder="••••••••")

    if st.button("Registrarse"):
        if register_user(first_name, last_name, email, phone, password):
            st.success("Registro exitoso. Ahora puedes iniciar sesión.")
            st.session_state.view = "login"
        else:
            st.error("El correo electrónico ya está registrado. Usa otro correo.")

    if st.button("Volver al Inicio de Sesión"):
        st.session_state.view = "login"

# Menú principal después de iniciar sesión
elif st.session_state.view == "menu":
    user = st.session_state.user
    st.sidebar.title("Menú de Navegación")
    menu_option = st.sidebar.selectbox(
        "Selecciona una opción:",
        ["Inicio", "Datos del Cliente", "Datos de Póliza", "Proyección", "Preguntas Frecuentes", "Salir"],
        index=["Inicio", "Datos del Cliente", "Datos de Póliza", "Proyección", "Preguntas Frecuentes", "Salir"].index(st.session_state.get("menu_option", "Inicio"))
    )

# Guardar la opción seleccionada en la sesión
    st.session_state.menu_option = menu_option

    # Vista Inicio
    if menu_option == "Inicio":
        st.title("Página de Inicio")
        st.markdown("¡Bienvenido a Allianz Patrimonial!")
        st.markdown("Desde aquí puedes gestionar tus datos, crear políticas de inversión y más.")
        
        # Información adicional en la página de inicio
        st.markdown("---")
        st.markdown("## Acerca de Allianz en México")
        st.markdown("""
        Allianz es una aseguradora alemana líder en el mercado con presencia internacional, atendiendo a más de 125 millones de clientes en casi 70 países. Desde 1890, trabajamos para brindar tranquilidad a cada uno de nuestros clientes que confían en nosotros.

        En México, Allianz inició operaciones en 1987 a través de una participación en Aseguradora Cuauhtémoc. En 1995, adquirió la totalidad de las acciones, consolidándose como Allianz México. A lo largo de los años, hemos ampliado nuestras operaciones en diversos sectores:

        - **1995**: Ingreso al mercado de Seguros de Daños Empresariales, consolidándonos como líderes en este ramo.
        - **2000**: Lanzamiento de seguros personales con sistemas tecnológicos innovadores para la emisión y cobranza de pólizas.
        - **2002**: Entrada al mercado de Vida y Gastos Médicos Empresariales, posicionándonos entre las principales compañías del segmento.
        - **2004**: Obtención del segundo mayor negocio en la historia de Pensiones en México, con una prima de 1,050 millones.

        Allianz México sigue comprometida con la innovación y el servicio al cliente, siendo uno de los referentes más importantes en el mercado asegurador.
        """)

        st.markdown("---")
        st.markdown("## ¿Qué puedes hacer en Allianz Patrimonial?")
        st.markdown("""
        - Gestionar tus datos personales y financieros.
        - Crear y personalizar tu portafolio de inversión.
        - Visualizar proyecciones financieras basadas en tus decisiones.
        - Resolver tus dudas a través de nuestra sección de Preguntas Frecuentes.
        """)

    # Siguiente pestaña

    
    elif menu_option == "Datos del Cliente":
        st.title("Gestión de Datos del Cliente")
        user_id = st.session_state.user[0]
        c.execute('SELECT * FROM cliente_data WHERE user_id = ?', (user_id,))
        cliente_data = c.fetchone()

        if cliente_data:
            st.markdown("### Datos actuales:")
            st.write(f"**Edad:** {cliente_data[2]}")
            st.write(f"**Ingreso Mensual:** ${cliente_data[3]:,.2f}")
            st.write(f"**Ocupación:** {cliente_data[4]}")
            st.write(f"**Objetivo Financiero:** {cliente_data[5]}")
            st.write(f"**Nivel de Riesgo:** {cliente_data[6]}")

        edad = st.number_input("Edad:", min_value=18, max_value=100, value=cliente_data[2] if cliente_data else 25)
        ingreso_mensual = st.number_input("Ingreso Mensual (USD):", min_value=0.0, value=cliente_data[3] if cliente_data else 1000.0)
        ocupacion = st.text_input("Ocupación:", value=cliente_data[4] if cliente_data else "")
        objetivo = st.text_area("Objetivo Financiero:", value=cliente_data[5] if cliente_data else "")
        nivel_riesgo = st.selectbox("Nivel de Riesgo:", ["Bajo", "Moderado", "Alto"], index=["Bajo", "Moderado", "Alto"].index(cliente_data[6]) if cliente_data else 0)

        if st.button("Guardar Datos"):
            if cliente_data:
                c.execute('''
                    UPDATE cliente_data SET edad = ?, ingreso_mensual = ?, ocupacion = ?, objetivo = ?, nivel_riesgo = ? WHERE user_id = ?
                ''', (edad, ingreso_mensual, ocupacion, objetivo, nivel_riesgo, user_id))
            else:
                c.execute('''
                    INSERT INTO cliente_data (user_id, edad, ingreso_mensual, ocupacion, objetivo, nivel_riesgo)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, edad, ingreso_mensual, ocupacion, objetivo, nivel_riesgo))
            conn.commit()
            st.success("Datos guardados correctamente.")

#DATOS DE PÓLIZA
    elif menu_option == "Datos de Póliza":
        st.title("Gestión de Datos de Póliza")

    # Monto inicial de inversión
        inversion_inicial = st.number_input(
            "Monto inicial de inversión (en USD):",
            min_value=100000.0,
            step=5000.0
    )

    # Plazo de inversión
        plazo_inversion = st.slider(
            "Plazo de inversión (en años):",
            min_value=5,
            max_value=30,
            value=5
    )

    # Selección de ETFs
        st.markdown("### Selección de ETFs para tu portafolio")
        try:
            with open('valid_etfs.json', 'r') as f:
                valid_etfs = json.load(f)
        except FileNotFoundError:
            st.error("El archivo 'valid_etfs.json' no se encontró.")
            valid_etfs = []
        except json.JSONDecodeError:
            st.error("El archivo 'valid_etfs.json' tiene un formato inválido.")
            valid_etfs = []



    # Si hay ETFs válidos, permitir su selección
        if valid_etfs:
        # Concatenar símbolo y nombre
            etf_options = [{"label": f"{etf['symbol']}: {etf['name']}", "symbol": etf['symbol'], "name": etf['name']} for etf in valid_etfs]
        
        # Multiselección con el formato combinado
            selected_labels = st.multiselect(
                "Selecciona los ETFs para tu portafolio:",
                options=[etf["label"] for etf in etf_options]
        )

        # Filtrar los ETFs seleccionados basados en la etiqueta
            selected_etfs = [etf for etf in etf_options if etf["label"] in selected_labels]

        # Asignación de ponderaciones si se seleccionaron ETFs
            ponderaciones = {}  # Inicializar ponderaciones

            if selected_etfs:
                st.markdown("### Asignación de Ponderaciones (%)")
                cols = st.columns(len(selected_etfs))

    # Crear sliders para cada ETF seleccionado
                for i, etf in enumerate(selected_etfs):
                    etf_symbol = etf["symbol"]  # Extraer el símbolo del ETF
                    etf_name = etf["name"]  # Extraer el nombre del ETF
                    ponderaciones[etf_symbol] = cols[i].number_input(
                        f"{etf_symbol}: {etf_name} (%)",
                        min_value=0,
                        max_value=100,
                        step=5,
                        key=f"peso_{i}_{etf_symbol}"  # Usar símbolo para garantizar unicidad
                    )

    # Calcular el total de ponderaciones
                total_ponderacion = sum(ponderaciones.values())

                # Mostrar el total ponderado
                st.markdown(f"**Total de Ponderaciones: {total_ponderacion}%**")
                if total_ponderacion == 100:
                    st.success("Las ponderaciones son válidas y suman exactamente 100%.")
                    st.session_state.ponderaciones = ponderaciones
                elif total_ponderacion > 100:
                    st.error("La suma de las ponderaciones supera el 100%. Ajusta los valores.")
                else:
                    st.warning("La suma de las ponderaciones es menor al 100%. Ajusta los valores.")
            else:
                st.info("Selecciona al menos un ETF para asignar las ponderaciones.")

# Después de la sección "Asignación de Ponderaciones (%)"
            if selected_etfs:
                # Título para la sección de detalles
                st.markdown("### Conocer más acerca de los ETFs seleccionados")

    # Crear un expander para cada ETF seleccionado
                for etf in selected_etfs:
                    etf_symbol = etf["symbol"]  # Extraer el símbolo
                    etf_name = etf["name"]  # Extraer el nombre
                    etf_data = next((item for item in valid_etfs if item['symbol'] == etf_symbol), None)

                    if etf_data:
                        # Crear un expander para mostrar información adicional
                        with st.expander(f"Más información sobre {etf_symbol}: {etf_name}"):
                            st.write(f"**Símbolo:** {etf_data['symbol']}")
                            st.write(f"**Nombre:** {etf_data['name']}")
                            # Agregar un enlace para consultar detalles en Yahoo Finance
                            st.markdown("Consulta más detalles financieros en Yahoo Finance: "
                                        f"[{etf_data['symbol']}](https://finance.yahoo.com/quote/{etf_data['symbol']})")

        # Selección del período para los ETFs
        st.markdown("### Selección del período de análisis para los ETFs")
        periodo_etfs = st.selectbox(
            "Selecciona el período de análisis:",
            ['1mo', '3mo', '6mo', '1y', '5y']
        )

        # Botón para guardar datos y redirigir
        if st.button("Guardar Datos de Póliza"):
            if valid_etfs and selected_etfs and total_ponderacion == 100:
                # Guardar los datos en el estado de la sesión
                st.session_state.datos_poliza = {
                    "inversion_inicial": inversion_inicial,
                    "plazo_inversion": plazo_inversion,
                    "etfs": selected_etfs,
                    "ponderaciones": st.session_state.ponderaciones,
                    "periodo": periodo_etfs  # Guarda el período seleccionado
                }
                st.success("Datos de póliza guardados correctamente.")
            else:
                st.error("Asegúrate de que las ponderaciones sumen exactamente 100% antes de guardar.")

# Botón para ir a la proyección
        if st.button("Calcular Proyección"):
    # Establece el estado en la pestaña "Proyección"
            st.session_state.view = "menu"
            st.session_state.menu_option = "Proyección"
    
    # Usa parámetros de consulta para refrescar
            st.query_params.update({"menu": "Proyección"})
    

    elif menu_option == "Proyección":
        st.title("Proyección de Inversiones")

    # Verificar si hay datos guardados en la sesión
        if "datos_poliza" in st.session_state:
            datos = st.session_state.datos_poliza

        # Mostrar un resumen de los datos seleccionados
            st.markdown("### Resumen de Datos de Póliza")
            st.write(f"**Monto Inicial de Inversión:** ${datos['inversion_inicial']}")
            st.write(f"**Plazo de Inversión:** {datos['plazo_inversion']} años")
            st.write(f"**Periodo de Análisis:** {datos['periodo']}")
            st.write("**Ponderaciones:**")
            for etf in datos["etfs"]:
                symbol = etf["symbol"]
                nombre = etf["name"]
                ponderacion = datos["ponderaciones"].get(symbol, 0)
                st.write(f"- {symbol} ({nombre}): {ponderacion}%")

       # Cálculo de rentabilidad y gráficos
            st.markdown("### Cálculos de Proyección")


        # Parámetros del cliente
            periodo = datos["periodo"]  # Período seleccionado en Datos de Póliza ('1mo', '3mo', '6mo', etc.)
            
        # Extraer los símbolos de los ETFs seleccionados
            if "etfs" in datos and isinstance(datos["etfs"], list):  # Verifica que 'etfs' sea una lista
                etfs_seleccionados = [etf["symbol"] for etf in datos["etfs"]]  # Extraer símbolos
                ponderaciones = datos["ponderaciones"]  # Ponderaciones de cada ETF
                st.write(f"ETFs seleccionados: {etfs_seleccionados}")
            else:
                st.error("No se encontraron ETFs seleccionados o el formato es incorrecto.")
        
    # Función para calcular rentabilidad, volatilidad y Sharpe Ratio
        def calcular_estadisticas(simbolo, periodo):
            try:
        # Descargar datos del ETF
                data = yf.download(simbolo, period=periodo)
        
        # Calcular retorno diario
                data['daily_return'] = data['Close'].pct_change()
        
        # Calcular métricas
                avg_annual_return = data['daily_return'].mean() * 252  # Rendimiento promedio anual
                annual_volatility = data['daily_return'].std() * (252 ** 0.5)  # Volatilidad anual
                sharpe_ratio = avg_annual_return / annual_volatility if annual_volatility != 0 else 0  # Ratio de Sharpe
        
        # Devolver las estadísticas
                return {
                    "avg_annual_return": avg_annual_return,
                    "annual_volatility": annual_volatility,
                    "sharpe_ratio": sharpe_ratio
        }
            except Exception as e:
                st.error(f"Error al procesar datos de {simbolo}: {e}")
                return {
                    "avg_annual_return": 0,
                    "annual_volatility": 0,
                    "sharpe_ratio": 0
        }
            
            # Calcular estadísticas para cada ETF seleccionado
        estadisticas_etfs = {
            symbol: calcular_estadisticas(symbol, periodo)
            for symbol in etfs_seleccionados
}


# Calcular estadísticas ponderadas del portafolio
        rendimiento_portafolio = sum(
            estadisticas_etfs[symbol]["avg_annual_return"] * ponderaciones[symbol] / 100
            for symbol in estadisticas_etfs
)
        volatilidad_portafolio = sum(
            estadisticas_etfs[symbol]["annual_volatility"] * ponderaciones[symbol] / 100
            for symbol in estadisticas_etfs
)
        sharpe_portafolio = rendimiento_portafolio / volatilidad_portafolio if volatilidad_portafolio != 0 else 0

        # Mostrar estadísticas de cada ETF
        st.markdown("### Estadísticas de los ETFs Seleccionados")
        for symbol, stats in estadisticas_etfs.items():
            st.write(f"**{symbol}:**")
            st.write(f"- Rendimiento Promedio Anual: {stats['avg_annual_return'] * 100:.2f}%")
            st.write(f"- Volatilidad Anual: {stats['annual_volatility'] * 100:.2f}%")
            st.write(f"- Ratio de Sharpe: {stats['sharpe_ratio']:.2f}")

# Mostrar estadísticas del portafolio
        st.markdown("### Estadísticas del Portafolio Total")
        st.write(f"**Rendimiento Promedio Anual:** {rendimiento_portafolio * 100:.2f}%")
        st.write(f"**Volatilidad Anual:** {volatilidad_portafolio * 100:.2f}%")
        st.write(f"**Ratio de Sharpe:** {sharpe_portafolio:.2f}")

# Calcular el valor del portafolio a lo largo del tiempo
        valores_portafolio = datos["inversion_inicial"] * (1 + rendimiento_portafolio) ** np.arange(1, datos["plazo_inversion"] + 1)

# Calcular los picos y drawdowns
        picos = np.maximum.accumulate(valores_portafolio)  # Máximos acumulados
        drawdowns = (valores_portafolio - picos) / picos  # Diferencia entre el valor actual y el pico, normalizada
        drawdown_maximo = drawdowns.min()  # El drawdown máximo

# Mostrar el Drawdown máximo
        st.markdown(f"**Drawdown Máximo:** {drawdown_maximo * 100:.2f}%")


# Obtener los símbolos de los ETFs seleccionados
        if "datos_poliza" in st.session_state:
            datos_poliza = st.session_state["datos_poliza"]
            etfs_seleccionados = [etf["symbol"] for etf in datos_poliza["etfs"]]
        else:
            st.error("No se encontraron datos de póliza. Regresa a la pestaña 'Datos de Póliza' para completarlos.")


# Descargar datos históricos de cierre ajustado
        precios = yf.download(etfs_seleccionados, period="1y")["Adj Close"]

# Calcular rendimientos diarios
        rendimientos_diarios = precios.pct_change()

# Calcular matriz de correlación
        matriz_correlacion = rendimientos_diarios.corr()

# Crear el heatmap
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(matriz_correlacion, annot=True, cmap="coolwarm", ax=ax, fmt=".2f", linewidths=0.5)
        ax.set_title("Matriz de Correlación entre ETFs")
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        st.pyplot(fig)


# Preparar datos para la gráfica
        rendimientos = [estadisticas_etfs[symbol]["avg_annual_return"] * 100 for symbol in estadisticas_etfs]
        volatilidades = [estadisticas_etfs[symbol]["annual_volatility"] * 100 for symbol in estadisticas_etfs]
        etfs = list(estadisticas_etfs.keys())

# Agregar los datos del portafolio total
        rendimientos.append(rendimiento_portafolio * 100)
        volatilidades.append(volatilidad_portafolio * 100)
        etfs.append("Portafolio Total")

# Crear la gráfica de puntos
        plt.figure(figsize=(10, 6))
        plt.scatter(volatilidades, rendimientos, color='blue', s=100)  # Gráfica de puntos
        for i, etf in enumerate(etfs):  # Etiquetas de los puntos
            plt.text(volatilidades[i], rendimientos[i], etf, fontsize=9, ha='right')

# Configurar la gráfica
        plt.title("Gráfica de Riesgo vs Rendimiento")
        plt.xlabel("Volatilidad Anual (%)")
        plt.ylabel("Rendimiento Promedio Anual (%)")
        plt.grid(alpha=0.3)
        st.pyplot(plt)

# Utilizar el periodo seleccionado por el cliente
        periodo_cliente = datos["periodo"]  # Esto debería venir de los datos ingresados por el cliente

# Descargar datos históricos de los ETFs seleccionados
        precios_historicos = yf.download(etfs_seleccionados, period=periodo_cliente)["Adj Close"]

# Calcular rendimientos diarios
        rendimientos_diarios = precios_historicos.pct_change()

# Calcular rendimientos acumulados
        rendimientos_acumulados = (1 + rendimientos_diarios).cumprod()

# Graficar rendimientos acumulados
        plt.figure(figsize=(12, 6))
        for ticker in rendimientos_acumulados.columns:
            plt.plot(rendimientos_acumulados.index, rendimientos_acumulados[ticker], label=ticker)

        plt.title("Rendimientos Acumulados de los ETFs Seleccionados", fontsize=14)
        plt.xlabel("Fecha", fontsize=12)
        plt.ylabel("Rendimiento Acumulado", fontsize=12)
        plt.legend(title="ETFs", fontsize=10)
        plt.grid(alpha=0.3)
        st.pyplot(plt)

# Pestaña de Preguntas Frecuentes
    if menu_option == "Preguntas Frecuentes":
        st.title("Preguntas Frecuentes")

        # Pregunta 1: ¿Qué es el rendimiento promedio anual?
        with st.expander("¿Qué es el rendimiento promedio anual?"):
            st.write("""
            El rendimiento promedio anual mide el porcentaje de crecimiento de una inversión en promedio por año. 
            Se calcula utilizando los rendimientos diarios y ajustándolos al número de días laborales en un año (252 días).
            Este cálculo es útil para entender el desempeño general de un activo o portafolio durante un periodo prolongado.
            """)

        # Pregunta 2: ¿Qué es la volatilidad anual?
        with st.expander("¿Qué es la volatilidad anual?"):
            st.write("""
            La volatilidad anual mide la variabilidad o dispersión de los rendimientos diarios de un activo durante un año. 
            Es una métrica clave para evaluar el riesgo asociado con una inversión. Una alta volatilidad indica mayor riesgo,
            mientras que una baja volatilidad indica estabilidad en los rendimientos.
            """)

        # Pregunta 3: ¿Qué es el ratio de Sharpe?
        with st.expander("¿Qué es el ratio de Sharpe?"):
            st.write("""
            El ratio de Sharpe evalúa la relación entre el rendimiento y el riesgo de una inversión. 
            Se calcula dividiendo el rendimiento promedio anual entre la volatilidad anual. 
            Un ratio de Sharpe alto indica que una inversión ofrece un rendimiento alto en relación con su nivel de riesgo.
            """)

        # Pregunta 4: ¿Qué representa el drawdown máximo?
        with st.expander("¿Qué representa el drawdown máximo?"):
            st.write("""
            El drawdown máximo es la mayor caída porcentual desde un pico histórico hasta un valle durante un periodo específico. 
            Es una métrica utilizada para evaluar el riesgo de pérdida de una inversión.
            """)

        # Pregunta 5: ¿Qué muestra la gráfica de riesgo vs. rendimiento?
        with st.expander("¿Qué muestra la gráfica de riesgo vs. rendimiento?"):
            st.write("""
            La gráfica de riesgo vs. rendimiento compara la relación entre la volatilidad (riesgo) y el rendimiento promedio anual
            de los ETFs seleccionados y del portafolio total. Permite identificar visualmente los activos con mejor rendimiento ajustado al riesgo.
            """)

        # Pregunta 6: ¿Qué muestra la matriz de correlación?
        with st.expander("¿Qué muestra la matriz de correlación?"):
            st.write("""
            La matriz de correlación mide la relación entre los rendimientos de diferentes ETFs. 
            Valores cercanos a 1 indican una alta correlación positiva, mientras que valores cercanos a -1 indican una alta correlación negativa.
            Una matriz de correlación ayuda a identificar activos diversificados.
            """)

        # Pregunta 7: ¿Qué representa la gráfica de rendimientos acumulados?
        with st.expander("¿Qué representa la gráfica de rendimientos acumulados?"):
            st.write("""
            La gráfica de rendimientos acumulados muestra cómo creció cada ETF seleccionado durante el periodo de análisis. 
            Es útil para visualizar el desempeño histórico de los activos y compararlos entre sí.
            """)

        st.write("Si tienes más preguntas, no dudes en contactarnos al 3324567829 o enviando un correo a dudas@allianz.com")


# Pestaña de Salir
    if menu_option == "Salir":
        st.title("Salir")

        # Mensaje de confirmación
        st.write("¿Estás seguro de que deseas salir de tu sesión?")

        # Botón para cerrar sesión
        if st.button("Cerrar Sesión"):
            # Resetear los datos de sesión
            st.session_state.clear()
            
            # Configurar una bandera para redirigir al inicio
            st.session_state.view = "Inicio"
            st.success("Has cerrado sesión exitosamente")
