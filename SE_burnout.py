# Sistema Experto: Evaluación de Síndrome de Burnout
# Incluye: Manejo de Incertidumbre (Factores de Certeza), Hechos, Reglas y Motor de Inferencia.

# REGLAS: (condiciones_requeridas, conclusion, peso_de_la_regla, explicacion)
# El peso de la regla (0.0 a 1.0) representa la confianza del experto en esa deducción.
RULES = [
    (["agotamiento", "insomnio"], "fatiga_fisica_alta", 0.8,
     "El agotamiento constante sumado al insomnio es un fuerte indicador de fatiga física."),

    (["desmotivacion", "baja_eficacia"], "desgaste_mental", 0.9,
     "La desmotivación y la sensación de baja eficacia son signos clave de desgaste mental (cinismo)."),

    (["fatiga_fisica_alta", "desgaste_mental"], "riesgo_burnout", 0.95,
     "La combinación clínica de fatiga física y desgaste mental indica un riesgo inminente de Síndrome de Burnout."),

    (["tension"], "estres_somatizado", 0.7,
     "Los dolores físicos frecuentes (cabeza, cuello) indican que el cuerpo está somatizando el estrés.")
]

# PREGUNTAS: (id_hecho, pregunta_texto)
QUESTIONS = [
    ("agotamiento", "¿Con qué frecuencia te sientes exhausto/a al final del día?"),
    ("desmotivacion", "¿Sientes desmotivación por tus tareas escolares o laborales?"),
    ("insomnio", "¿Te cuesta trabajo dormir o descansar adecuadamente?"),
    ("baja_eficacia", "¿Sientes que tu rendimiento académico o laboral ha disminuido?"),
    ("tension", "¿Tienes dolores de cabeza o tensión muscular frecuente?"),
]


def ask_certainty(q):
    """Manejo de Incertidumbre: Pide un valor del 1 al 5 y lo convierte en un Factor de Certeza (0.0 a 1.0)"""
    print(f"\n{q}")
    print("1: Nunca | 2: Rara vez | 3: A veces | 4: Casi siempre | 5: Siempre")
    while True:
        try:
            ans = int(input("Tu respuesta (1-5): ").strip())
            if 1 <= ans <= 5:
                # Convertimos la escala 1-5 a un factor de 0.0 a 1.0
                return (ans - 1) / 4.0
            else:
                print("Por favor, ingresa un número entre 1 y 5.")
        except ValueError:
            print("Entrada inválida. Ingresa un número del 1 al 5.")


def infer(facts):
    """
    Motor de Inferencia con Encadenamiento hacia Adelante (Forward Chaining)
    y manejo de Factores de Certeza (FC).
    """
    conclusions = {}
    proof = []
    changed = True

    # El ciclo sigue evaluando reglas hasta que ya no se descubran nuevos hechos
    while changed:
        changed = False
        for conds, concl, rule_weight, expl in RULES:
            # Si aún no hemos deducido esta conclusión
            if concl not in facts:
                # Verificamos si TODAS las condiciones previas existen en nuestros hechos con un FC mayor a 0.2
                if all(c in facts and facts[c] > 0.2 for c in conds):
                    # Lógica clásica de Sistemas Expertos (MYCIN):
                    # El FC de múltiples condiciones (AND) es el valor MÍNIMO de ellas.
                    cf_premise = min(facts[c] for c in conds)

                    # El FC final es la certeza de la premisa multiplicada por el peso de la regla
                    cf_conclusion = cf_premise * rule_weight

                    # Agregamos la nueva conclusión a los hechos para que otras reglas puedan usarla
                    facts[concl] = cf_conclusion
                    conclusions[concl] = cf_conclusion
                    changed = True

                    proof.append(f"• Se deduce '{concl}' con una certeza del {cf_conclusion * 100:.1f}%. ({expl})")

    return conclusions, proof


# -------------------- Ejecutar Sistema --------------------

print("=== SISTEMA EXPERTO: EVALUACIÓN DE BURNOUT ===")
print("Responde las siguientes preguntas para evaluar tu nivel de desgaste.\n")

# 1. Recolección de Hechos iniciales
facts = {}
for key, q in QUESTIONS:
    certainty = ask_certainty(q)
    if certainty > 0:  # Solo guardamos el hecho si hay algo de certeza
        facts[key] = certainty

print("\n--- Analizando respuestas... ---")

# 2. Ejecutar Motor de Inferencia
conclusions, proof = infer(facts)

print("\n--- Trazabilidad del Motor de Inferencia (Pasos) ---")
if proof:
    for p in proof:
        print(p)
else:
    print("• No se detectaron niveles de riesgo significativos con las reglas actuales.")

print("\n--- Diagnóstico Final ---")
if "riesgo_burnout" in conclusions:
    riesgo = conclusions["riesgo_burnout"]
    if riesgo > 0.7:
        print(f"⚠️ ALERTA: Riesgo ALTO de Burnout (Certeza: {riesgo * 100:.1f}%).")
        print(
            "Recomendación: Es crucial que busques apoyo psicológico, hables con tus coordinadores para ajustar tu carga y priorices el descanso urgente.")
    elif riesgo > 0.4:
        print(f"⚠️ PRECAUCIÓN: Riesgo MODERADO de Burnout (Certeza: {riesgo * 100:.1f}%).")
        print(
            "Recomendación: Estás en una fase de advertencia. Implementa técnicas de gestión de tiempo y asegúrate de desconectarte del trabajo/escuela los fines de semana.")
else:
    if "fatiga_fisica_alta" in conclusions or "estres_somatizado" in conclusions:
        print("🔔 RESULTADO: Tienes estrés o fatiga, pero aún no cumples los criterios completos para Burnout.")
        print("Recomendación: Cuida tus horas de sueño y vigila tu postura al trabajar/estudiar.")
    else:
        print("✅ RESULTADO: Riesgo bajo. Mantén tus buenos hábitos de salud mental.")