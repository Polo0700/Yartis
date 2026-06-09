from core.wake import wake

w = wake()


def test_wake():
    try:
        w.stream.start()
        w.stream.stop()
        print("Stream iniciado y detenido correctamente.")
    except Exception as e:
        assert False, f"Error al iniciar el stream: {e}"
