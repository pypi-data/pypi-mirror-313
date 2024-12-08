import os  # by sprawdzić istnienie pliku gotowców
import pickle
import random
import sys  # do czerwonych komunikatów: print('jakis tekst', file=sys.stderr )
import time  # dla testów wydajności
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from random import choice
from sympy.abc import x

plt.rcParams.update({
    "text.usetex": True,
})

sciezka = str(Path(__file__).parent)


# print(sciezka)

# Todo: dołożyć macierze zespolone jako osobne funkcje?

def rownanie_macierzowe():  # na 2000 losowań żadnego powtórzenia
    random.seed()
    rng = np.random.default_rng()
    # wspolczynniki = [-6,-5,-4,-3,-2,-1,2,3,4,5,6,7,8,9]
    while True:
        A = rng.integers(-1, 3, size=(2, 5))
        B = rng.integers(-2, 2, size=(2, 5))
        C = rng.integers(-1, 3, size=(5, 2))
        D = rng.integers(-2, 2, size=(5, 2))
        strona = random.choice(['l', 'p'])
        stala = random.choice([2, 3, 4])
        Ident = stala * np.identity(2)
        wyznacznik1 = random.choice([-3, -2, 2, 3, 4, 5, 6])
        wyznacznik2 = random.choice([-3, -2, 2, 3, 4, 5])
        if abs(np.linalg.det(A @ B.transpose()) - wyznacznik1) < 0.1 and abs(
                np.linalg.det(C.transpose() @ D - Ident) - wyznacznik2) < 0.1:
            break
    # print('A=',(sp.Array(A)))
    # print('B=',(sp.Array(B)))
    # print('C=',(sp.Array(C)))
    # print('D=',(sp.Array(D)))
    if strona == 'p':
        rownanie = ('\t\\[\n'
                    f'\t\t{sp.latex(sp.Array(A))}\\cdot \n'
                    f'\t\t{sp.latex(sp.Array(B))}^T + \n'
                    f'\t\t{stala}X=\n'
                    f'\t\t{sp.latex(sp.Array(C))}^T \\cdot\n'
                    f'\t\t{sp.latex(sp.Array(D))} \\cdot X\n'
                    f'\t\\]')
        # pomysł ze strony https://stackoverflow.com/questions/43804701/round-floats-within-an-expression
        # do wyeliminowania wyników postaci 3.342432*10^(-16) i 0.999999999999997
        Wynik = sp.Matrix(
            ((np.linalg.inv(C.transpose() @ D - Ident)) @ A @ B.transpose() * np.linalg.det(C.transpose() @ D - Ident)))
        for a in sp.preorder_traversal(Wynik):
            if isinstance(a, sp.Float):
                Wynik = Wynik.subs(a, round(a, 10))
        rozwiazanie = (
            f'$ {sp.latex(sp.Array(A @ B.transpose()))} + \n'
            f'\t{stala}X=\n'
            f'\t{sp.latex(sp.Array(C.transpose() @ D))} \\cdot X, \\quad \n'
            f'\t{sp.latex(sp.Array(A @ B.transpose()))} = \n'
            f'\t{sp.latex(sp.Array((C.transpose() @ D) - Ident))} \\cdot X $ \\\\ \n'
            f'\t$X=\\frac{{1}}{{{int(np.rint(np.linalg.det(C.transpose() @ D - Ident)))}}}'
            # f'{sp.latex(sp.Matrix(((np.linalg.inv(C.transpose() @ D - Ident)) @ A @ B.transpose() * np.linalg.det(C.transpose() @ D - Ident))))}.'
            f'{sp.latex(Wynik)}.$')
        rozwiazanie = rozwiazanie.replace('.0', '')  # liczby w macierzach są całkowite i nie chcę wyświetlać .0
    else:
        rownanie = ('\t\\[\n'
                    f'\t\t{sp.latex(sp.Array(A))}\\cdot \n'
                    f'\t\t{sp.latex(sp.Array(B))}^T + \n'
                    f'\t\t{stala}X=\n'
                    f'\t\tX \\cdot {sp.latex(sp.Array(C))}^T \\cdot\n'
                    f'\t\t{sp.latex(sp.Array(D))} \n'
                    f'\t\\]')
        # rownanie = '        $$' + str(sp.latex(sp.Array(A))) + '\\cdot \n' + \
        #            '        ' + str(sp.latex(sp.Array(B))) + '^T +\n ' + \
        #            '        ' + str(stala) + ' X=X \\cdot' + \
        #            '        ' + str(sp.latex(sp.Array(C))) + '^T \\cdot\n' + \
        #            '        ' + str(sp.latex(sp.Array(D))) + '$$\n'
        Wynik = sp.Matrix(
            ((A @ B.transpose() @ np.linalg.inv(C.transpose() @ D - Ident)) * np.linalg.det(C.transpose() @ D - Ident)))
        for a in sp.preorder_traversal(Wynik):
            if isinstance(a, sp.Float):
                Wynik = Wynik.subs(a, round(a, 10))
        rozwiazanie = (
            f'$ {sp.latex(sp.Array(A @ B.transpose()))} + \n'
            f'\t{stala}X=\n'
            f'\tX \\cdot {sp.latex(sp.Array(C.transpose() @ D))} , \\quad \n'
            f'\t{sp.latex(sp.Array(A @ B.transpose()))} = \n'
            f'\tX \\cdot {sp.latex(sp.Array((C.transpose() @ D) - Ident))} $ \\\\ \n'
            f'\t$X=\\frac{{1}}{{{int(np.rint(np.linalg.det(C.transpose() @ D - Ident)))}}}'
            # f'{sp.latex(sp.Matrix(((A @ B.transpose() @ np.linalg.inv(C.transpose() @ D - Ident)) * np.linalg.det(C.transpose() @ D - Ident))))}.\n'
            f'{sp.latex(Wynik)}.$')
        rozwiazanie = rozwiazanie.replace('.0', '')  # liczby w macierzach są całkowite i nie chcę wyświetlać .0
    return ('Rozwiązać równanie:\n'
            f'{rownanie}',
            f'{rozwiazanie}')


def wyznacznik_parametr(wymiar: int = 3, gotowiec: bool = False):  # na 1000 losowań nie było żadnej powtórki

    if gotowiec is True:
        if wymiar == 4:
            if os.path.isfile(sciezka + '//gotowe//wyznacznik_parametr_wymiar_4.pickle'):  # 10000 różnych gotowych
                gotowe = pickle.load(open(sciezka + '//gotowe//wyznacznik_parametr_wymiar_4.pickle', 'rb'))
                return gotowe[random.randint(0, len(gotowe)) - 1]
            else:
                print('Brak gotowca do tego typu', file=sys.stderr)
        if wymiar == 3:
            if os.path.isfile(sciezka + '//gotowe//wyznacznik_parametr_wymiar_3.pickle'):  # 10000 różnych gotowych
                gotowe = pickle.load(open(sciezka + '//gotowe//wyznacznik_parametr_wymiar_3.pickle', 'rb'))
                return gotowe[random.randint(0, len(gotowe)) - 1]
            else:
                print('Brak gotowca do tego typu', file=sys.stderr)
    # to nie musi być w else, bo wcześniejsze warunku w przypadku sukcesu konczą funkcje returnem
    x = sp.symbols('x', real=True)
    while True:
        M = sp.randMatrix(wymiar, wymiar, -4, 4)
        licznik_zer = 0
        for ii in range(wymiar):
            for jj in range(wymiar):
                if M[ii, jj] == 0:
                    licznik_zer += 1
        for k in range(wymiar + 1):
            wiersz = random.randint(0, wymiar - 1)
            kol = random.randint(0, wymiar - 1)
            M[wiersz, kol] += x
        wyznacznik = sp.det(M)
        pierwiastki = sp.solve(wyznacznik)
        if (
                2 <= sp.degree(wyznacznik) <= max(2, min(wymiar - 1, 3))  # nie za duże wielomiany
                and 0 < len(pierwiastki) <= max(2, wymiar - 1)  # czy to gwarantuje różne pierwiastki?
                and wyznacznik.coeff(x, sp.degree(wyznacznik)) in {-3, -2, -1, 2, 3}
                and abs(wyznacznik.coeff(x, 0)) < 50  # by wyznacznik nie miał za dużych współczynników
                and licznik_zer < wymiar - 1
                and all(pierwiastek.is_integer for pierwiastek in pierwiastki)
        ):
            break
    return ('Dla jakich rzeczywistych wartości parametru $x$ wyznacznik macierzy $A$ jest różny od zera?\n'
            f'\t\\[\n'
            f'\t\t\\textnormal{{A=}}\n'
            f'\t\t{sp.latex(M)}\n'
            f'\t\\]',
            f'$\\det A='
            f'{sp.latex(wyznacznik)} \\neq 0, \\quad ' +
            ''.join(f'x\\neq {pierwiastek}, \\ ' for pierwiastek in pierwiastki) +
            f'$')


def macierz_odwrotna_parametr(wymiar: int = 3, gotowiec: bool = False):
    if gotowiec is True:
        if wymiar == 3:
            if os.path.isfile(
                    sciezka + '//gotowe//macierz_odwrotna_parametr_wymiar_3.pickle'):  # 10000/10000 różnych gotowych
                gotowe = pickle.load(open(sciezka + '//gotowe//macierz_odwrotna_parametr_wymiar_3.pickle', 'rb'))
                return gotowe[random.randint(0, len(gotowe)) - 1]
            else:
                print('Brak gotowca do tego typu', file=sys.stderr)
        if wymiar == 4:
            if os.path.isfile(sciezka + '//gotowe//macierz_odwrotna_parametr_wymiar_4.pickle'):  # 1000 różnych gotowych
                gotowe = pickle.load(open(sciezka + '//gotowe//macierz_odwrotna_parametr_wymiar_4.pickle', 'rb'))
                return gotowe[random.randint(0, len(gotowe)) - 1]
            else:
                print('Brak gotowca do tego typu', file=sys.stderr)
    # to nie musi być w else, bo wcześniejsze warunku w przypadku sukcesu konczą funkcje returnem
    x = sp.symbols('x', real=True)
    while True:
        M = sp.randMatrix(wymiar, wymiar, -4, 4)
        licznik_zer = 0
        for ii in range(wymiar):
            for jj in range(wymiar):
                if M[ii, jj] == 0:
                    licznik_zer += 1
        for k in range(4):
            wiersz = random.randint(0, wymiar - 1)
            kol = random.randint(0, wymiar - 1)
            M[wiersz, kol] += x
        wyznacznik = sp.det(M)
        pierwiastki = sp.solve(wyznacznik)

        if (
                sp.degree(wyznacznik) == 2
                and len(pierwiastki) == 2
                and wyznacznik.coeff(x, 2) in {-3, -2, -1, 2, 3}
                and licznik_zer < wymiar - 1
                and all(pierwiastek.is_integer for pierwiastek in pierwiastki)
        ):
            podstaw = random.choice(list({-2, -1, 2, 3} - set(pierwiastki)))
            wyznacznik_podstaw = wyznacznik.subs(x, podstaw)
            # print(pierwiastki)
            # print(wyznacznik_podstaw, licznik_zer)
            if 1 < abs(wyznacznik_podstaw) < 3 ** wymiar:  # trochę duży.
                break

    # print(podstaw)
    # print(wyznacznik_podstaw)
    N = M.subs(x, podstaw)
    return ('Dla jakich rzeczywistych wartości parametru $x$ macierz $A$ posiada odwrotność?\n'
            f'\t\\[\n'
            f'\t\t\\textnormal{{A=}}{sp.latex(M)}\n'
            f'\t\\]\n'
            f'Wyznaczyć macierz odwrotną dla $x={podstaw}.$ Wykonać sprawdzenie.\\\\',
            f'$\\det A={sp.latex(wyznacznik)}\\neq 0, \\quad \n'
            f'\tx\\neq {pierwiastki[0]}\\ \\textnormal{{oraz}} \\ x\\neq {pierwiastki[1]},$\\\\\n'
            f'\t$A({podstaw})= {sp.latex(M.subs(x, podstaw))},\\ \n'
            f'\t\\det A({podstaw})={wyznacznik_podstaw},\\ \n'
            f'\tA^{{-1}}={sp.latex(sp.sympify(1 / wyznacznik_podstaw))}'
            f'{sp.latex((N.inv()) * wyznacznik_podstaw)}.$')


def wartosci_wlasne(wymiar: int = 3, zespolone: bool = False):  # na 10000 losowań 50 powtórzeń
    liczby = (-2, -1, 0, 1, 2, 3)
    while True:
        # wymiar = 4
        # zespolone = True

        M = sp.Matrix(wymiar, wymiar, [random.choice(liczby) for _ in range(wymiar ** 2)])
        N = sp.matrix2numpy(M, dtype=float)
        w, v = np.linalg.eig(N)

        if (wymiar == 2):
            if zespolone is False:
                rzeczywiste_ww = True
                for i in w:
                    if abs(np.imag(i)) > 0.01:
                        rzeczywiste_ww = False
                if rzeczywiste_ww is True:
                    break
            else:
                zespolone_ww = True
                for i in w:
                    if abs(np.imag(i)) < 0.01:
                        zespolone_ww = False
                if zespolone_ww is True:
                    break
        if wymiar == 3:
            if zespolone is False:
                rzeczywiste_ww = True
                for i in w:
                    if abs(np.imag(i)) > 0.01:
                        rzeczywiste_ww = False
                    if np.around(np.real(i), 0) != np.around(np.real(i), 2):
                        rzeczywiste_ww = False
                if rzeczywiste_ww is True:
                    break
            else:
                zespolone_ww = False
                for i in w:
                    if abs(np.imag(i)) > 0.01:
                        zespolone_ww = True
                calkowite = False
                if zespolone_ww is True:
                    calkowite = True
                    for i in w:
                        if (np.around(np.real(i), 0) != np.around(np.real(i), 2)
                                or np.around(np.imag(i), 0) != np.around(np.imag(i), 2)):
                            calkowite = False
                if zespolone_ww is True and calkowite is True:
                    break
        if wymiar >= 4:
            ladne_ww = True
            for i in w:
                if not (np.around(np.real(i), 0) == np.around(np.real(i), 2)
                        and np.around(np.imag(i), 0) == np.around(np.imag(i), 2)
                        and abs(np.imag(i)) < 0.01):
                    ladne_ww = False
            if ladne_ww is True:
                break

    return (f'Wyznaczyć wartości własne i wektory własne macierzy \n'
            f'\t\\[\n'
            f'\t\t\\textnormal{{A=}} {sp.latex(M)}\n'
            f'\t\\]',
            f'$\\det\\left(\\lambda \mathbb{{I}} - A \\right) = {sp.latex(M.charpoly().as_expr())}$, \\quad \n'  # znak: (A-lambda*I)
            f'Wartości własne:$ {sp.latex(M.eigenvals())}, $\\\\\n'
            f'\t\\parbox{{4em}}{{Wektory\\\\własne:}} ${sp.latex(M.eigenvects())}$')


# Tdoo: odpowiedź wektory włąsne w dwóch linijkach bo 4x4 jest za szerokie czasami.
def diagonalizacja_macierzy(wymiar: int = 3):  # na 10000 losowań 50 powtórzeń
    liczby = (-2, -1, 0, 1, 2, 3)
    while True:
        M = sp.Matrix(wymiar, wymiar, [random.choice(liczby) for _ in range(wymiar ** 2)])
        N = sp.matrix2numpy(M, dtype=float)
        w, v = np.linalg.eig(N)
        rzeczywiste_ww = True
        for i in w:
            if abs(np.imag(i)) > 0.01:
                rzeczywiste_ww = False
            if np.around(np.real(i), 0) != np.around(np.real(i), 2):
                rzeczywiste_ww = False
        # print(n, end = ',')
        if rzeczywiste_ww is True:
            break
    if M.is_diagonalizable():
        P, D = M.diagonalize()
        return (f'Przeprowadzić diagonalizację macierzy (jeśli możliwa) \n'
                f'\t\\[\n'
                f'\t\t\\textnormal{{A=}} {sp.latex(M)}\n'
                f'\t\\]',
                f'$\\det\\left(\\lambda \mathbb{{I}} - A \\right) = {sp.latex(M.charpoly().as_expr())}$, \\quad \n'
                f'Wartości własne:$ {sp.latex(M.eigenvals())}, $\\\\\n'
                f'\\parbox{{4em}}{{Wektory\\\\własne:}} ${sp.latex(M.eigenvects())}$,\\\\\n'
                f'$A = P\\,D\\,P^{{-1}}: \\quad P={sp.latex(P)},$ \\quad \n'
                f'$D={sp.latex(D)}$')
    else:
        return (f'Przeprowadzić diagonalizację macierzy (jeśli możliwa) \n'
                f'\t\\[\n'
                f'\t\t\\textnormal{{A=}} {sp.latex(M)}\n'
                f'\t\\]',
                f'$\\det\\left(\\lambda \mathbb{{I}} - A \\right) = {sp.latex(M.charpoly().as_expr())}$, \\quad \n'
                f'Wartości własne:$ {sp.latex(M.eigenvals())}, $\\\\\n'
                f'\\parbox{{4em}}{{Wektory\\\\własne:}} ${sp.latex(M.eigenvects())}$,\\\\\n'
                f'Macierz nie jest diagonalizowalna.')


def diagonalizacja_macierzy_z_wielokrotnym_wartosciami_wlasnymi(wymiar: int = 3):
    liczby = (-2, -1, 0, 1, 2, 3)

    while True:
        M = sp.Matrix(wymiar, wymiar, [random.choice(liczby) for _ in range(wymiar ** 2)])
        values = [*M.eigenvals().values()]
        if max(values) > 1:
            try:
                P, D = M.diagonalize()
            except Exception:
                pass
            else:
                break
    return (f'Przeprowadzić diagonalizację macierzy\n'
            f'\t\\[\n'
            f'\t\t\\textnormal{{A=}} {sp.latex(M)}\n'
            f'\t\\]',
            f'$\\det\\left(\\lambda \mathbb{{I}} - A \\right) = {sp.latex(M.charpoly().as_expr())}$, \\quad \n'
            f'Wartości własne:$ {sp.latex(M.eigenvals())}, $\\\\\n'
            f'\\parbox{{4em}}{{Wektory\\\\własne:}} ${sp.latex(M.eigenvects())}$,\\\\\n'
            f'$A = P\\,D\\,P^{{-1}}: \\quad P={sp.latex(P)},$ \\quad \n'
            f'$D={sp.latex(D)}$')


def rzad_macierzy():
    liczby = (-2, -1, 0, 1, 2, 3)
    wymiar = random.choice((4, 5, 6))
    licznik = 0
    los = np.random.choice(([0] * 4 + [1] * 1))  # pozwól na rząd równy wymiarowi macierzy — ale nie za często
    while True:
        licznik += 1
        M = sp.Matrix(wymiar, 10 - wymiar, [random.choice(liczby) for _ in range(wymiar * (10 - wymiar))])
        N = N = sp.matrix2numpy(M, dtype=np.int32)  # bez astype nie będzie sprawdzał poprawnie logiki macierzy!!!
        za_duzo_zer = (~np.any(N, axis=0)).any() or (~np.any(N, axis=1)).any()
        """ Następne robi to samo co ostatnie dwie linijki ale jakoś strasznie długo? 
        # m, n = np.shape(M)
        # za_duzo_zer = False # unikamy wierszy lub kolumn pełnych zer
        # for i in range(n):
        #     if np.count_nonzero(M[:, i]) <= 1:
        #         za_duzo_zer = True
        # for i in range(m):
        #     if np.count_nonzero(M[i, :]) <= 1:
        #         za_duzo_zer = True
        """
        if M.rank() < min(wymiar, 10 - wymiar) + los and not za_duzo_zer:
            break
    # print(licznik)
    # print(len(M) - np.count_nonzero(M))

    return ('Wyznaczyć rząd macierzy A\n'
            f'\t\\[\n'
            f'\t\t\\textnormal{{A=}} {sp.latex(M)}\n'
            f'\t\\]',
            f'$R(A)= {M.rank()}$')


def wyznacznik(wymiar: int = 5):
    zerowy = random.choice([False, False, True])
    if wymiar not in {2, 3, 4, 5, 6}:
        return 'Tylko stopień 2, 3, 4, 5 lub 6', ''
    liczby = (-2, -1, 0, 1, 2, 3)
    while True:
        M = sp.Matrix(wymiar, wymiar, [random.choice(liczby) for _ in range(wymiar ** 2)])
        wyznacznik = M.det()
        if zerowy is True:
            if abs(wyznacznik) == 0:
                break
        else:
            if abs(wyznacznik) <= 20 and wyznacznik != 0:
                break

    return ('Obliczyć wyznacznik macierzy A\n'
            f'\t\\[\n'
            f'\t\t\\textnormal{{A=}} {sp.latex(M)}\n'
            f'\t\\]',
            f'$\\det(A)= {M.det()}$')


def regresja(stopien: int = 1, nr_zadania: int = 1):
    if stopien not in {1, 2}:
        return 'Tylko stopień 1 lub 2', ''
    if not os.path.exists('pics'):
        os.makedirs('pics')
        print(" ! Tworzę katalog pics ", file=sys.stderr)
    if stopien == 2:
        kwadratowa = random.choice([True, False])
    if stopien == 1:
        kwadratowa = False
    while True:
        args = random.sample(range(-5, 6), 5)
        vals = random.sample(range(-5, 6), 5)
        if stopien == 1:
            A = sp.Matrix([args, [1 for i in range(5)]]).transpose()
        if stopien == 2:
            A = sp.Matrix([[i ** 2 for i in args], args, [1 for _ in range(5)]]).transpose()
        B = sp.Matrix(vals)
        # A, B
        reg = (A.transpose() @ A).inv() @ A.transpose() @ B
        odchylenia = A @ reg - B
        err = odchylenia.transpose() @ odchylenia
        if kwadratowa is True:
            if reg[0] != 0 and all([(i * 6).is_integer for i in reg]) and err[0] < 10:
                break
        if kwadratowa is False:
            if all([(i * 6).is_integer for i in reg]) and err[0] < 10:
                break
    x_s = np.linspace(min(args) - 1 / 2, max(args) + 1 / 2, 100)
    if stopien == 1:
        y_s = x_s * reg[0] + reg[1]
        rownanie = reg[0] * x + reg[1]
    if stopien == 2:
        y_s = x_s ** 2 * reg[0] + x_s * reg[1] + reg[2]
        rownanie = reg[0] * x ** 2 + reg[1] * x + reg[2]
    plt.figure(figsize=(4.5, 4.5))
    plt.xticks([i for i in range(min(args) - 1, max(args) + 2)])
    plt.yticks([i for i in range(min(vals) - 4, max(vals) + 5)])
    if stopien == 1:
        wartosci = [i * reg[0] + reg[1] for i in args]
    if stopien == 2:
        wartosci = [i ** 2 * reg[0] + i * reg[1] + reg[2] for i in args]
    plt.scatter(args, wartosci)
    for i in range(len(args)):
        plt.plot([args[i], args[i]], [wartosci[i], vals[i]], 'g:', linewidth=2)
    plt.scatter(args, vals, c='red')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(
        f'$\\textnormal{{{"Prosta" if stopien == 1 else "Trójmian kwadratowy"}: }} y={sp.latex(rownanie)}$' +
        '\n' +
        f"$\\textnormal{{Suma kwadratów reszt: }} {sp.latex(err[0])} $ ",
        multialignment='center')

    plt.grid(which='both', linestyle=':')
    plt.plot(x_s, y_s)
    plt.savefig(f'./pics/regresja{nr_zadania}.png')
    plt.savefig(f'./pics/regresja{nr_zadania}.pdf')
    plt.close()
    if stopien == 1:
        tmp1 = 'a \\\\ b'
        tmp2 = f'{sp.latex(reg[0])} \\\\ {sp.latex(reg[1])}'
        przesuniecie = -4.9
    if stopien == 2:
        tmp1 = 'a \\\\ b \\\\ c'
        tmp2 = f'{sp.latex(reg[0])} \\\\ {sp.latex(reg[1])} \\\\ {sp.latex(reg[2])}'
        przesuniecie = -5.2
    return (f'Wyznaczyć {"prostą" if stopien == 1 else "trójmian kwadratowy"} regresji dla punktów \n'
            f'\t\[\n'
            f'\t\t({args[0]},{vals[0]}),\  ({args[1]},{vals[1]}),\  ({args[2]},{vals[2]}),\ '
            f' ({args[3]},{vals[3]}),\  ({args[4]},{vals[4]}).\n'
            f'\t\]',
            f'\t\\begin{{tabular}}{{p{{0.5\\textwidth}}p{{0.3\\textwidth}}}}\n'
            f'\t\\vspace{"{-5pt}" if stopien == 2 else "{0pt}"}\n'
            f'\t\\[\n'
            f'\t\t{sp.latex(A)}\n'
            f'\t\t\\cdot \\left[\\begin{{matrix}} {tmp1} \\end{{matrix}}\\right]\n'
            f'\t\t\\simeq {sp.latex(B)}\n'
            f'\t\t\\quad \\Biggm/ \\cdot \\left(\\left(A^T A \\right)^{{-1}} A^T \\right)_L\n'
            f'\t\\]\n'
            f'\t\\[\n'
            f'\t\t \\left[\\begin{{matrix}} {tmp1} \\end{{matrix}}\\right] = \n'
            f'\t\t \\left[\\begin{{matrix}} {tmp2} \\end{{matrix}}\\right]\n'
            f'\t\\]\n'
            f'\t&\n'
            f'\t\t\\raisebox{{{przesuniecie}cm}}{{\\resizebox{{5.2cm}}{{!}}{{\\includegraphics{{../pics/regresja{nr_zadania}}}}}}}\n'
            f'\t\\end{{tabular}}\n')


if __name__ == "__main__":  # to się uruchamia tylko, gdy plik jest uruchamiany jako program, a nie ładowany jako moduł
    gotowce = True
    os.chdir('..')  # by wczytywać z gotowca - inaczej problem ze ścieżkami!
    start_time = time.time()
    polecenie, rozwiazanie = regresja(stopien=2, nr_zadania=1)
    # polecenie, rozwiazanie = wyznacznik_parametr(wymiar=3, gotowiec=gotowce)
    # polecenie, rozwiazanie = wyznacznik_parametr(wymiar=random.choice(([2] * 1) + ([3] * 7) + ([4] * 0)))
    # polecenie, rozwiazanie = rownanie_macierzowe()
    # polecenie, rozwiazanie = wyznacznik_parametr(wymiar=random.choice(([2] * 0) + ([3] * 0) + ([4] * 1)),
    #                                                    gotowiec=True)
    # polecenie, rozwiazanie = wartosci_wlasne(wymiar=random.choice(([2] * 1) + ([3] * 7) + ([4] * 1)),
    #                                          zespolone=random.choice((True, False)))
    # polecenie, rozwiazanie = diagonalizacja_macierzy(wymiar=random.choice(([2]*4) + ([3]*6) + ([4]*1)))
    # polecenie, rozwiazanie = diagonalizacja_macierzy_z_wielokrotnym_wartosciami_wlasnymi(wymiar=3)
    # polecenie, rozwiazanie = rzad_macierzy()

    print(polecenie, '\n', rozwiazanie)
    print("Czas generowania zestawów --- %s seconds ---" % (time.time() - start_time))
