import os
import pickle
import random
import time
from pathlib import Path

import sympy as sp

sciezka = str(Path(__file__).parent)


def uklad_Cramera(wymiar: int = 3, gotowiec: bool = False):
    if gotowiec is True:
        if wymiar == 7:
            if os.path.isfile(sciezka + '//gotowe//uklad_Cramera_wymiar_7.pickle'):  # 10000 różnych gotowych
                gotowe = pickle.load(open(sciezka + '//gotowe//uklad_Cramera_wymiar_7.pickle', 'rb'))
                return gotowe[random.randint(0, len(gotowe)) - 1]
            else:
                print('Brak gotowca do tego typu', file=sys.stderr)
        if wymiar == 6:
            if os.path.isfile(sciezka + '//gotowe//uklad_Cramera_wymiar_6.pickle'):  # 10000 różnych gotowych
                gotowe = pickle.load(open(sciezka + '//gotowe//uklad_Cramera_wymiar_6.pickle', 'rb'))
                return gotowe[random.randint(0, len(gotowe)) - 1]
            else:
                print('Brak gotowca do tego typu', file=sys.stderr)
    # to nie musi być w else, bo wcześniejsze warunku w przypadku sukcesu konczą funkcje returnem
    x, y, z, t, u, v, w = sp.symbols('x y z t u v w', real=True)
    X = sp.Matrix([x, y, z, t, u, v, w])
    X = sp.Matrix(X[:wymiar])
    liczby = (-3, -2, -1, 0, 1, 2, 3, 4) if wymiar >= 3 else (-3, -2, -1, 1, 2, 3, 4)
    niewiadoma = random.choice([i for i in range(wymiar)])
    while True:
        A = sp.Matrix(wymiar, wymiar, [sp.Rational(random.choice(liczby)) for _ in range(wymiar ** 2)])
        det_A = sp.det(A)
        # print(det_A)
        if det_A != 0 and det_A != 1 and abs(det_A) < 10:
            break
    while True:
        B = sp.Matrix(1, wymiar, [sp.Rational(random.choice(liczby)) for _ in range(wymiar)])
        A_temp = sp.ImmutableDenseMatrix(A)
        A_temp = A_temp.row_del(niewiadoma)
        A_temp = A_temp.row_insert(niewiadoma, B)
        det_A_temp = sp.det(A_temp)
        if det_A_temp != 0 and det_A_temp != 1 and abs(det_A_temp) < 10:
            break
    # Przestawienie alfabetyczne niewiadomych w tworzeniu zadania powoduje zmiany znaków wyznaczników
    # w przypadku t,x,y,z oraz t,u,v,x,y,z.
    if wymiar == 4 or wymiar == 6:
        det_A = -1 * det_A
        det_A_temp = -1 * det_A_temp
    # print(A,'\n',X,'\n', A_temp,'\n',B,'\n', det_A_temp/det_A,'\n',sp.latex(sp.Matrix.multiply(A.transpose(), X) - B.transpose()))
    lewa_strona = sp.Matrix.multiply(A.transpose(), X)
    uklad = ('\t\[\n'
             '\t\t\left\{\n'
             '\t\t\t\\begin{matrix}\n')
    for i in range(wymiar):
        uklad = uklad.join(['', f'\t\t\t\t{sp.latex(lewa_strona[i])} = {B[i]} \\\\ \n'])
    uklad = uklad.join(['', '\t\t\t\\end{matrix}\n\t\t\\right.\n\t\]'])
    # return uklad + str(X[niewiadoma]) + '=' + str(det_A_temp / det_A)

    return (f'Z układu równań wyznaczyć niewiadomą ${X[niewiadoma]}$\n' + uklad,
            f'$\\det(A) = {det_A},\\ \\det(A_{X[niewiadoma]})={det_A_temp},\\ '
            f'{X[niewiadoma]} = {sp.latex(det_A_temp / det_A)}$')


def uklad_rownan_nieoznaczony():  # na 10000 losowań żaden się nie powtórzył
    # random.seed()
    x, y, z, t = sp.symbols('x y z t', real=True)
    while True:
        stala_niewiadoma = random.choice([0, 1, 2, 3])
        wartosc_stalej_niewiadomej = random.choice([-2, -1, 2])
        while True:
            parametr = random.choice([1, 2, 3, 4])
            if parametr != stala_niewiadoma:
                break
        a = random.choice([-3, -2, -1, 2, 3, 4])
        b = random.choice([-3, -2, -1, 2, 3, 4])
        c = random.choice([-3, -2, -1, 2, 3, 4])
        d = random.choice([-3, -2, -1, 2, 3, 4])
        M = sp.zeros(5, )
        for ind in range(0, 3):
            M[ind, ind] = 1
        M[0, 3] = a
        M[0, 4] = b
        M[1, 3] = c
        M[1, 4] = d
        M[2, 4] = wartosc_stalej_niewiadomej
        for ind1 in range(0, 5):
            for ind2 in range(0, 5):
                if ind1 != ind2:
                    mnoznik = random.choice([-1, -1, 0, 1, 1])
                    for ind in range(0, 5):
                        M[ind2, ind] += M[ind1, ind] * mnoznik
        ile_zer = 0
        for ind1 in range(0, 5):
            for ind2 in range(0, 5):
                if M[ind1, ind2] == 0:
                    ile_zer += 1
        if max(abs(M)) < 10 and ile_zer == 2:
            break
    B = M.col(4)
    M.col_del(4)
    if stala_niewiadoma != 2:
        for ind in range(5):
            M[ind, stala_niewiadoma] += M[ind, 2]
            M[ind, 2] = M[ind, stala_niewiadoma] - M[ind, 2]
            M[ind, stala_niewiadoma] -= M[ind, 2]
    X = sp.Matrix([x, y, z, t])
    lewa_strona = sp.Matrix.multiply(M, X)
    uklad = ('\t\[\n'
             '\t\t\left\{\n'
             '\t\t\t\\begin{matrix}\n')
    for i in range(5):
        uklad = uklad.join(['', f'\t\t\t\t{sp.latex(lewa_strona[i])} = {B[i]} \\\\ \n'])
    uklad = uklad.join(['', '\t\t\t\\end{matrix}\n\t\t\\right.\n\t\]'])
    uklad1 = []
    for i in range(5):
        uklad1.append(str(lewa_strona[i]) + '-(' + str(B[i]) + ')')
    rozwiazanie = sp.latex(sp.solve(sp.sympify(uklad1))).replace(':', ' = ')
    odpowiedz = (f'${rozwiazanie}$')
    return ('Rozwiązać układ równań.\\ Jeśli możliwe podać trzy przykładowe rozwiązania.\\ '
            'Jedno rozwiązanie sprawdzić. \n' + uklad,
            odpowiedz)


if __name__ == "__main__":  # to się uruchamia tylko gdy plik jest uruchamiany jako program a nie ładowany jako moduł
    os.chdir('..')  # by wczytywać z gotowca - inaczej problem ze ścieżkami!
    start_time = time.time()
    # print('!!! uklady_rownan_liniowych.py były planowane jako moduł a uruchomiłeś je jako skrypt !!!')
    # print(rownanie_liniowe())
    # print(rownanie_kwadratowe())
    # polecenie, rozwiazanie = uklad_rownan_nieoznaczony()
    polecenie, rozwiazanie = uklad_Cramera(wymiar=random.choice([6]), gotowiec=True)
    # polecenie, rozwiazanie = uklad_Cramera(wymiar=4)
    print(polecenie, '\n', rozwiazanie)
    print("--- %s seconds ---" % (time.time() - start_time))
