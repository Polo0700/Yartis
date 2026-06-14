from brain.opencode import peticion
import pyttsx3

asistente = peticion()
tts = pyttsx3.init()
tts.setProperty("rate", 150)

def hablar(texto):
    print(f"🤖 Yartis dice: {texto}")
    tts.say(texto)
    tts.runAndWait()

print("=== YARTIS — Modo escritura ===")
print("Escribe 'salir' para terminar\n")

while True:
    entrada = input("👉 Tú: ")
    if entrada.lower() in ("salir", "exit", "q"):
        print("👋 Adiós")
        break

    respuesta = asistente.ejecutar(entrada)
    hablar(respuesta)
    print()
