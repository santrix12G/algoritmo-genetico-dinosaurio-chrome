"""
Funciones de álgebra lineal para operaciones con matrices y vectores.
"""
import numpy as np


def matrix_vector_multiplication(matrix, vector):
    """
    Multiplica una matriz por un vector.
    
    Args:
        matrix: numpy array 2D
        vector: numpy array 1D
    
    Returns:
        numpy array 1D con el resultado
    """
    result = np.zeros(matrix.shape[0])
    for i in range(matrix.shape[0]):
        sum_val = 0
        for j in range(matrix.shape[1]):
            sum_val += matrix[i][j] * vector[j]
        result[i] = sum_val
    return result


def zeroes_matrix(rows, cols):
    """
    Crea una matriz de ceros.
    
    Args:
        rows: número de filas
        cols: número de columnas
    
    Returns:
        numpy array 2D de ceros
    """
    return np.zeros((rows, cols))


def random_vector(size):
    """
    Crea un vector con valores aleatorios entre -1 y 1.
    
    Args:
        size: tamaño del vector
    
    Returns:
        numpy array 1D con valores aleatorios
    """
    return np.random.uniform(-1, 1, size)