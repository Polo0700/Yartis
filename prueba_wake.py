from core.wake import wake

w = wake()
w.stream.start()
input("Presiona Enter para detener el stream...")
w.stream.stop()
