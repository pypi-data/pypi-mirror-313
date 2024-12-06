from pollination.honeybee_radiance.matrix import MatrixMultiplication, \
    MatrixMultiplicationThreePhase
from queenbee.plugin.function import Function


def test_matrix_multiplication():
    function = MatrixMultiplication().queenbee
    assert function.name == 'matrix-multiplication'
    assert isinstance(function, Function)


def test_matrix_multiplication_three_phase():
    function = MatrixMultiplicationThreePhase().queenbee
    assert function.name == 'matrix-multiplication-three-phase'
    assert isinstance(function, Function)
