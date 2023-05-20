import numpy as np
from numpy.typing import NDArray


def lu(A: NDArray, permute: bool) -> tuple[NDArray, NDArray, NDArray]:
    # Получаем размерность матрицы A
    n = A.shape[0]
    # Инициализируем матрицы L, U и P (L, P - еденичные)
    L = np.eye(n)
    U = np.copy(A)
    P = np.eye(n)

    for u_column in range(n):
        if permute:
            # Ищем максимальный элемент в столбце с учетом перестановок
            max_row = u_column + np.argmax(abs(U[u_column:, u_column]))
            # Меняем местами строки в матрицах U и P
            U[[u_column, max_row], u_column:] = U[[max_row, u_column], u_column:]
            P[[u_column, max_row], :] = P[[max_row, u_column], :]
            # Если матрица L больше не единичная то применяем такую же перестановку строк
            if u_column >= 1:
                L[[u_column, max_row], :u_column] = L[[max_row, u_column], :u_column]

        # Применяем элементарное преобразование к столбцу j матрицы U и обновляем матрицу L
        for i in range(u_column + 1, n):
            L[i, u_column] = U[i, u_column] / U[u_column, u_column]
            U[i, u_column:] -= L[i, u_column] * U[u_column, u_column:]

    return L, U, P

def solve(L: NDArray, U: NDArray, P: NDArray, b: NDArray) -> NDArray:
    # Переставляем элементы b точно так же как строки A
    b_permuted = np.dot(P, b)
    # Решаем систему Ly = b
    y = np.linalg.solve(L, b_permuted)
    # Решаем систему Ux = y
    x = np.linalg.solve(U, y)

    return x


def check_validity( L, U ):
    if np.isnan(L).any() or np.isinf(L).any():
        return False

    if np.isnan(U).any() or np.isinf(U).any():
        return False

    return True

def get_A_b(a_11: float, b_1: float) -> tuple[NDArray, NDArray]:
    A = np.array([[a_11, 1.0, -3.0], [6.0, 2.0, 5.0], [1.0, 4.0, -3.0]])
    b = np.array([b_1, 12.0, -39.0])
    return A, b


if __name__ == "__main__":
    # Let's implement the LU decomposition with and without pivoting
    # and check its stability depending on the matrix elements
    p = 16  # modify from 7 to 16 to check instability
    a_11 = 3 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    b_1 = -16 + 10 ** (-p)  # add/remove 10**(-p) to check instability
    A, b = get_A_b(a_11, b_1)


    # With pivoting
    L, U, P = lu(A, permute=True)
    print("Матрица L:")
    print(L)
    print("Матрица U:")
    print(U)
    print("Матрица P:")
    print(P)
    x = solve(L, U, P, b)
    print("Решение x:")
    print(x)
    assert np.all(np.isclose(x, [1, -7, 4])), f"The anwser {x} is not accurate enough"
    print("______________________________________________________________")

    # Without pivoting
    L, U, P = lu(A, permute=False)
    print("Матрица L:")
    print(L)
    print("Матрица U:")
    print(U)
    print("Матрица P:")
    print(P)
    if check_validity(L, U):
        x_ = solve(L, U, P, b)
        print("Решение x:")
        print(x_)
        assert np.all(np.isclose(x_, [1, -7, 4])), f"The anwser {x_} is not accurate enough"
    else:
        print("Some values in L, U matrices are invalid. Pivoting is required.")


