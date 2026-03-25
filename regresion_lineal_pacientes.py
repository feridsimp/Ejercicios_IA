import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics  import mean_squared_error, r2_score

# Configuración de los gráficos
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

print("Iniciando análisis clínico")

# PASO 1: DATOS (Ingresamos los datos de nuestros 10 pacientes)
edades = np.array([25, 32, 38, 45, 50, 55, 62, 68, 72, 80])
presiones = np.array([110, 118, 115, 126, 132, 135, 142, 148, 145, 154])

n_pacientes = len(edades)

# Preparar los datos para Scikit-Learn
X = edades.reshape(-1, 1)
y = presiones

print(f"   Datos ingresados: {n_pacientes} pacientes.")

# PASO 2: ENTRENAR EL MODELO
modelo = LinearRegression()
modelo.fit(X, y)

beta_0 = modelo.intercept_  # El Intercepto
beta_1 = modelo.coef_[0]  # La Pendiente

print("\n El modelo ha calculado la fórmula basándose 10 pacientes:")
print(f"   Ecuación: Presión = {beta_0:.2f} + {beta_1:.2f} * (Edad)")
print("-" * 50)
print("INTERPRETACIÓN CLÍNICA:")
print(f"   Por cada AÑO extra, la presión sube {beta_1:.2f} mmHg.")

# PASO 3: EVALUAR EL MODELO
y_predicho = modelo.predict(X)
mse = mean_squared_error(y, y_predicho)
rmse = np.sqrt(mse)
r2 = r2_score(y, y_predicho)

print("\n  MÉTRICAS DE RENDIMIENTO:")
print(f"   RMSE (Error Promedio): {rmse:.2f} mmHg.")
print(f"   R^2 (Coeficiente de Determinación): {r2:.3f}")
print("   (Un R^2 de 0.969 sigue siendo excelentísimo y altamente confiable).")

# PASO 4: VISUALIZACIÓN
plt.figure()

# Puntos de los 10 pacientes
plt.scatter(X, y, color='blue', s=100, alpha=0.7, label='Pacientes (10 Datos reales)', edgecolors='black')

# Línea de tendencia
x_linea = np.linspace(20, 85, 100).reshape(-1, 1)
y_linea = modelo.predict(x_linea)
plt.plot(x_linea, y_linea, color='red', linewidth=2.5, label='Línea de Tendencia (Predicción)')

# Residuos (Las líneas verdes que muestran cuánto se aleja la realidad de la teoría)
for i in range(len(X)):
    plt.plot([X[i][0], X[i][0]], [y_predicho[i], y[i]], 'g--', linewidth=1.5, alpha=0.5)

plt.title('Relación entre Edad y Presión Arterial Sistólica (10 Pacientes)', fontsize=14, fontweight='bold')
plt.xlabel('Edad del Paciente (años)', fontsize=12)
plt.ylabel('Presión Arterial Sistólica (mmHg)', fontsize=12)
plt.legend(loc='upper left')
plt.grid(True, alpha=0.3)

texto_explicativo = (
    f"Ecuación: Y = {beta_0:.1f} + {beta_1:.2f}X\n"
    f"Cada año extra = +{beta_1:.2f} mmHg"
)
plt.text(0.05, 0.95, texto_explicativo, transform=plt.gca().transAxes,
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'),
         verticalalignment='top', fontsize=11)

plt.show()

# PASO 5: SIMULADOR DE PACIENTES
print("\n SIMULADOR CLÍNICO:")

try:
    # Usamos nuestro paciente del ejemplo: 55 años
    edad_usuario = 55

    # Predicción con la nueva fórmula
    presion_esperada = modelo.predict([[edad_usuario]])[0]

    estado = "NORMAL SEGÚN TENDENCIA" if presion_esperada < 140 else "ELEVADA SEGÚN TENDENCIA"

    print(f"\n   Si llega un paciente de {edad_usuario} años:")
    print(f"   -> Presión sistólica esperada: {presion_esperada:.2f} mmHg")
    print(f"   -> Alerta preliminar: {estado}")

except Exception as e:
    print(f"Error en la simulación: {e}")