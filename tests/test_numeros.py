from brain.numeros import calculadorNumtoString


def test_string_valido():
    assert calculadorNumtoString("7", 10) == "7"


def test_int_valido():
    assert calculadorNumtoString(7, 10) == "7"


def test_basura():
    assert calculadorNumtoString("x", 10) is None


def test_fuera_de_rango():
    assert calculadorNumtoString("99", 10) is None


def test_mezclado():
    assert calculadorNumtoString("3x", 10) is None


def test_vacio():
    assert calculadorNumtoString("", 10) is None


def test_negativo():
    assert calculadorNumtoString("-1", 10) is None


def test_cero():
    assert calculadorNumtoString("0", 10) == "0"
