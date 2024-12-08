import os  # by sprawdzić istnienie pliku gotowców
import pickle  # by pobierać z plików gotowców
import random
from pathlib import Path

import numpy as np
import sympy as sp

sciezka = str(Path(__file__).parent)

# from sympy.abc import x, y, z
x = sp.Symbol('x', real=True)
y = sp.Symbol('y', real=True)
from sympy.abc import z
import time

random.seed()


# Todo: Wzajemne położenie prostych itp, objętość równoległościanów, wysokości opuszczone z wierzchołka
# Todo: Iloczyny skalarne i wektorowe.
# Todo: Równania prostych i płaszczyzn przechodzących przez punkty i równoległych/prostopadłych do wektorów.
# Todo: Odległość prostych skośnych liczona gdy wektor między prostymi jest prostopadły do obu prostych.

def dlugosc(wektor: sp.Matrix) -> sp.Float:
    return sp.sqrt(wektor.dot(wektor))


def rownanie_prostej():
    """
    Generuje zadanie (w formacie LaTeX wraz z rozwiązaniem) na wyznaczenie równania prostej przechodzącej
     przez w punkty w R^3 oraz na wyznaczeniu odległości uzyskanej prostej od innego punktu.

    Returns:
        tuple: Zawiera polecenie oraz jego odpowiednie rozwiązanie.
    """
    # from sympy.abc import x, y, z
    liczby = (-3, -2, -1, 1, 2, 3, 4, 5)
    while True:
        P_1 = sp.Matrix([sp.Rational(random.choice(liczby)) for _ in range(3)])
        P_2 = sp.Matrix([sp.Rational(random.choice(liczby)) for _ in range(3)])
        P_3 = sp.Matrix([sp.Rational(random.choice(liczby)) for _ in range(3)])
        wektor_kierunkowy = (P_2 - P_1)
        odleglosc = dlugosc((P_2 - P_1).cross(P_3 - P_1)) / dlugosc(P_2 - P_1)
        if round(10 * odleglosc) == 10 * odleglosc and np.count_nonzero(wektor_kierunkowy) >= 2:
            break
    # return (P_1, P_2, P_3), odleglosc
    return (f'Wyznaczyć równanie prostej przechodzącej przez punkty\n'
            f'\t\\[\n'
            f'\t\tP_1 = ({P_1[0]}, {P_1[1]}, {P_1[2]}), \quad P_2 = ({P_2[0]}, {P_2[1]}, {P_2[2]}).\n'
            f'\t\\]\n'
            f'\tObliczyć odległość wyznaczonej prostej od punktu\n'
            f'\t\\[\n'
            f'\t\tP_3 = ({P_3[0]}, {P_3[1]}, {P_3[2]}).\n'
            f'\t\\]',
            f'$l\\colon '
            f' \\frac{{{sp.latex(x - P_1[0])}}}{{{wektor_kierunkowy[0]}}}='
            f' \\frac{{{sp.latex(y - P_1[1])}}}{{{wektor_kierunkowy[1]}}}='
            f' \\frac{{{sp.latex(z - P_1[2])}}}{{{wektor_kierunkowy[2]}}}; \qquad d(P_3,l) = {sp.latex(odleglosc)}$')


def rownanie_plaszczyzny():
    """
    Generuje zadanie (w formacie LaTeX wraz z rozwiązaniem) na wyznaczenie równania płaszczyzny przechodzącej
     przez 3 punkty w R^3 oraz na wyznaczeniu odległości uzyskanej płaszczyzny od innego punktu.

    Returns:
        tuple: Zawiera polecenie oraz jego odpowiednie rozwiązanie.
    """
    # from sympy.abc import x, y, z
    liczby = (-3, -2, -1, 0, 1, 2, 3, 4, 5)
    while True:
        P_1 = sp.Matrix([sp.Rational(random.choice(liczby)) for _ in range(3)])
        P_2 = sp.Matrix([sp.Rational(random.choice(liczby)) for _ in range(3)])
        P_3 = sp.Matrix([sp.Rational(random.choice(liczby)) for _ in range(3)])
        P_4 = sp.Matrix([sp.Rational(random.choice(liczby)) for _ in range(3)])
        wektor_normalny = (P_2 - P_1).cross(P_3 - P_1)
        wyraz_wolny_plaszczyzny = - wektor_normalny.dot(P_1)
        odleglosc = abs(wektor_normalny.dot(P_4) + wyraz_wolny_plaszczyzny) / dlugosc(wektor_normalny)
        if round(10 * odleglosc) == 10 * odleglosc and np.count_nonzero(wektor_normalny) >= 2:
            break
    return (f'Wyznaczyć równanie płaszczyzny przechodzącej przez punkty\n'
            f'\t\\[\n'
            f'\t\tP_1 = ({P_1[0]}, {P_1[1]}, {P_1[2]}), \quad P_2 = ({P_2[0]}, {P_2[1]}, {P_2[2]}),'
            f' \quad P_3 = ({P_3[0]}, {P_3[1]}, {P_3[2]}).\n'
            f'\t\\]\n'
            f'\tObliczyć odległość wyznaczonej płaszczyzny od punktu\n'
            f'\t\\[\n'
            f'\t\tP_4 = ({P_4[0]}, {P_4[1]}, {P_4[2]}).\n'
            f'\t\\]',
            f'$\pi\\colon '
            f'{sp.latex(wektor_normalny[0] * x + wektor_normalny[1] * y + wektor_normalny[2] * z + wyraz_wolny_plaszczyzny)}=0;'
            f' \qquad d(P_4,\pi) = {sp.latex(odleglosc)}$')


def odleglosc_prostych_skosnych(gotowiec: bool = False):
    """
    Generuje zadanie (w formacie LaTeX wraz z rozwiązaniem) na wyznaczenie odległości prostych skośnych w R^3

    Args:
        gotowiec (bool, optional): Czy zadanie ma być pobierane z gotowego zestawu. Defaults to False.
            W gotowcu jest 1000 różnych (na 1000 losowań)
    Returns:
        tuple: Zawiera polecenie oraz jego odpowiednie rozwiązanie.
    """

    if (gotowiec is True
            and os.path.isfile(sciezka + '//gotowe//odleglosc_prostych_skosnych.pickle')):  # 10000 różnych gotowych
        gotowe = pickle.load(open(sciezka + '//gotowe//odleglosc_prostych_skosnych.pickle', 'rb'))
        return gotowe[random.randint(0, len(gotowe)) - 1]
    else:
        while True:
            liczby = (-3, -2, -1, 1, 2, 3, 4, 5)
            k_1 = sp.Matrix([sp.Rational(random.choice(liczby)) for _ in range(3)])
            P_1 = sp.Matrix([sp.Rational(random.choice(liczby)) for _ in range(3)])
            k_2 = sp.Matrix([sp.Rational(random.choice(liczby)) for _ in range(3)])
            P_2 = sp.Matrix([sp.Rational(random.choice(liczby)) for _ in range(3)])
            # k_1 = sp.Matrix([2,1,2])
            # P_1 = sp.Matrix([-2,-3,-1])
            # k_2 = sp.Matrix([4,3,2])
            # P_2 = sp.Matrix([2,-3,-2])
            wektor_normalny = k_1.cross(k_2)
            wyraz_wolny_plaszczyzny = - wektor_normalny.dot(P_2)
            # odleglosc1 = abs(wektor_normalny.dot(P_1) + wyraz_wolny_plaszczyzny) / dlugosc(wektor_normalny)
            if dlugosc(wektor_normalny) > 0.0001:
                odleglosc2 = abs(k_1.dot(k_2.cross(P_1 - P_2))) / dlugosc(wektor_normalny)
                # print(odleglosc2)
                # to można prościej zrobić płaszczyznami
                # równanie płaszczyzny można zrobić tak:
                # n.dot(sp.Matrix((x, y, z)) - sp.Matrix((2, 3, 4)))
                # a jeszcze prościej można zrobić wektorem łączącym proste. On musi być prostopadły do obu
                # https://brilliant.org/wiki/3d-coordinate-geometry-skew-lines/
                parametr_t = ((k_2.dot(k_2)) * k_1 - (k_1.dot(k_2)) * k_2).dot(P_2 - P_1) / (
                    k_1.cross(k_2).dot(k_1.cross(k_2)))
                Punkt_1 = k_1 * parametr_t + P_1
                parametr_u = ((k_1.dot(k_1) * k_2) - (k_1.dot(k_2)) * k_1).dot(P_1 - P_2) / (
                    k_1.cross(k_2).dot(k_1.cross(k_2)))
                Punkt_2 = k_2 * parametr_u + P_2
                if (round(10 * odleglosc2) == 10 * odleglosc2
                        and odleglosc2 > 0.01
                        and round(2 * parametr_t) == 2 * parametr_t
                        and round(2 * parametr_u) == 2 * parametr_u):
                    break
        # return (k_1, P_1, k_2, P_2), odleglosc2, parametr_t, parametr_u, Punkt_1, Punkt_2, dlugosc(
        #     Punkt_1 - Punkt_2), sp.N(odleglosc2 - dlugosc(Punkt_2 - Punkt_1))
        return (f'Obliczyć odległość prostych skośnych\n'
                f'\t\\[\n'
                f'\t\tl_1\\colon \\frac{{{sp.latex(x - P_1[0])}}}{{{k_1[0]}}}='
                f'\\frac{{{sp.latex(y - P_1[1])}}}{{{k_1[1]}}}=\\frac{{{sp.latex(z - P_1[2])}}}{{{k_1[2]}}}, \\quad \n'
                f'\t\tl_2\\colon \\frac{{{sp.latex(x - P_2[0])}}}{{{k_2[0]}}}='
                f'\\frac{{{sp.latex(y - P_2[1])}}}{{{k_2[1]}}}=\\frac{{{sp.latex(z - P_2[2])}}}{{{k_2[2]}}}.\n'
                f'\t\\]'
                f'\tWyznaczyć punkty realizujące minimalną odległość.',
                f'Płaszczyzna zawierająca $l_2$ i równoległa do $l_1$ to $\\pi\\colon '
                f'{sp.latex(wektor_normalny[0] * x + wektor_normalny[1] * y + wektor_normalny[2] * z + wyraz_wolny_plaszczyzny)}=0$;\\\\'
                f'$d(l_1,l_2)={sp.latex(odleglosc2)};$\\quad '
                f'Punkty realizujące minimalną odległość to:\ '
                f'$ P_3=({sp.latex(Punkt_1[0])},{sp.latex(Punkt_1[1])},{sp.latex(Punkt_1[2])}),\ '
                f'P_4=({sp.latex(Punkt_2[0])},{sp.latex(Punkt_2[1])},{sp.latex(Punkt_2[2])})$.\n')


def punkt_symetryczny_do_plaszczyzny():  # na 50000 losowań było 6862 róznych wyników
    """
    Generuje zadanie (w formacie LaTeX wraz z rozwiązaniem) na wyznaczenie punktu symetrycznego względem płaszczyzny.

    Returns:
        tuple: Zawiera polecenie oraz jego odpowiednie rozwiązanie.
    """
    liczby = (-3, -2, -1, 1, 2, 3, 4, 5)
    # from sympy.abc import x, y, z
    while True:
        '''Parametry płaszczyzny Ax+By+Cz+D=0'''
        # plaszczyzna = [sp.Rational(random.choice(liczby)) for _ in range(4)]
        A, B, C, D = [sp.Rational(random.choice(liczby)) for _ in range(4)]
        '''Współrzędne punktu do odbicia P=(P_x, P_y, P_z)'''
        # punkt = list([random.choice(liczby) for _ in range(3)])
        P_x, P_y, P_z = list([random.choice(liczby) for _ in range(3)])
        t_przeciecia = (
                (-D - A * P_x - B * P_y - C * P_z) /
                (A ** 2 + B ** 2 + C ** 2))
        if t_przeciecia.is_integer is True and t_przeciecia != 0 and t_przeciecia != 1 and t_przeciecia != -1:
            # punkt_przeciecia = [0] * 3
            break
    Pp_x = P_x + A * t_przeciecia
    Pp_y = P_y + B * t_przeciecia
    Pp_z = P_z + C * t_przeciecia
    # punkt_symetryczny = [None] * 3
    Ps_x = 2 * Pp_x - P_x
    Ps_y = 2 * Pp_y - P_y
    Ps_z = 2 * Pp_z - P_z
    pi = A * x + B * y + C * z + D
    return (f'Wyznaczyć punkt symetryczny do punktu\n'
            f'\t\\[\n'
            f'\t\tP = ({P_x}, {P_y}, {P_z})\n'
            f'\t\\]\n'
            f'\twzględem płaszczyzny\n'
            f'\t\\[\n'
            f'\t\t\\pi\\colon {sp.latex(pi)}  = 0.\n'
            f'\t\\]',
            f'Prosta prostopadła: $'
            f' \\frac{{{sp.latex(x - P_x)}}}{{{A}}}='
            f' \\frac{{{sp.latex(y - P_y)}}}{{{B}}}='
            f' \\frac{{{sp.latex(z - P_z)}}}{{{C}}}= t,$ \\quad $t_p={t_przeciecia}$ \\\\\n'
            f'Punkt przecięcia to: $P_p ='
            f'({Pp_x},{Pp_y},{Pp_z}),$ \\quad \n'
            f'Punkt symetryczny to: $P_s = '
            f'({Ps_x},{Ps_y},{Ps_z})$')


def punkt_symetryczny_do_prostej():  # na 50000 losowań było 37341 różnych wyników
    """
    Generuje zadanie (w formacie LaTeX wraz z rozwiązaniem) na wyznaczenie punktu symetrycznego względem płaszczyzny.

    Returns:
        tuple: Zawiera polecenie oraz jego odpowiednie rozwiązanie.
    """
    liczby = (-3, -2, -1, 1, 2, 3, 4, 5)
    # from sympy.abc import x, y, z
    while True:
        '''Parametry prostej w postaci kierunkowej (x-x_0)/A = (y-y_0)/B = (z-z_0)/C'''
        A, B, C, x_0, y_0, z_0 = [sp.Rational(random.choice(liczby)) for _ in range(6)]
        # A, B, C, x_0, y_0, z_0 = [sp.Rational(2), 1, 1, 5, 2, 5]
        '''Współrzędne punktu do odbicia P=(P_x, P_y, P_z)'''
        P_x, P_y, P_z = [random.choice(liczby) for _ in range(3)]
        # P_x, P_y, P_z = [2, -2, -3]
        t_przeciecia = (A * (P_x - x_0) + B * (P_y - y_0) + C * (P_z - z_0)) / (A ** 2 + B ** 2 + C ** 2)
        # print(A, B, C, x_0, y_0, z_0, P_x, P_y, P_z, t_przeciecia, type(t_przeciecia), t_przeciecia.is_integer)
        if t_przeciecia.is_integer is True and t_przeciecia != 0 and t_przeciecia != 1 and t_przeciecia != -1:
            break
    # punkt_przeciecia = [0] * 3
    Pp_x = x_0 + A * t_przeciecia
    Pp_y = y_0 + B * t_przeciecia
    Pp_z = z_0 + C * t_przeciecia
    # punkt_symetryczny = [None] * 3
    Ps_x = 2 * Pp_x - P_x
    Ps_y = 2 * Pp_y - P_y
    Ps_z = 2 * Pp_z - P_z
    l = (f'\\frac{{{sp.latex(x - x_0)}}}{{{A}}}='
         f' \\frac{{{sp.latex(y - y_0)}}}{{{B}}}='
         f' \\frac{{{sp.latex(z - z_0)}}}{{{C}}}')
    pi = (A * x + B * y + C * z - A * P_x - B * P_y - C * P_z)

    return (f'Wyznaczyć punkt symetryczny do punktu\n'
            f'\t\\[\n'
            f'\t\tP = ({P_x}, {P_y}, {P_z})\n'
            f'\t\\]\n'
            f'\twzględem prostej\n'
            f'\t\\[\n'
            f'\t\tl\\colon {l}.\n'
            f'\t\\]',
            f'Płaszczyzna prostopadła: $\\pi\\colon '
            f'{sp.latex(pi)} = 0, \\quad t_p={t_przeciecia}$ \\\\\n'
            f'\t\t\t\tPunkt przecięcia to: $P_p ='
            f'({Pp_x},{Pp_y},{Pp_z}),$ \\quad \n'
            f'\t\t\t\tPunkt symetryczny to: $P_s = '
            f'({Ps_x},{Ps_y},{Ps_z})$')


def katy_w_trojkacie(prosty: bool = True, calkowite: bool = True):
    """
    Generuje zadanie (w formacie LaTeX wraz z rozwiązaniem) na wyznaczenie kątów wewnętrznych trójkąta w R^3.

    Args:
        prosty (bool, optional): Czy trójkąt ma mieć kąt prosty. Defaults to True.
        calkowite (bool, optional): Czy kąty mają być całkowite. Defaults to True.

    Returns:
        tuple: Zawiera polecenie oraz jego odpowiednie rozwiązanie.
    """
    liczby = (-3, -2, -1, 0, 1, 2, 3, 4, 5)
    while True:
        while True:
            A_x, A_y, A_z = [sp.Rational(random.choice(liczby)) for _ in range(3)]
            B_x, B_y, B_z = [sp.Rational(random.choice(liczby)) for _ in range(3)]
            C_x, C_y, C_z = [sp.Rational(random.choice(liczby)) for _ in range(3)]

            alpha = sp.acos(((B_x - A_x) * (C_x - A_x) + (B_y - A_y) * (C_y - A_y) + (B_z - A_z) * (C_z - A_z))
                            / (sp.sqrt((B_x - A_x) ** 2 + (B_y - A_y) ** 2 + (B_z - A_z) ** 2)
                               * sp.sqrt((C_x - A_x) ** 2 + (C_y - A_y) ** 2 + (C_z - A_z) ** 2))).evalf()
            beta = sp.acos(((C_x - B_x) * (A_x - B_x) + (C_y - B_y) * (A_y - B_y) + (C_z - B_z) * (A_z - B_z))
                           / (sp.sqrt((C_x - B_x) ** 2 + (C_y - B_y) ** 2 + (C_z - B_z) ** 2)
                              * sp.sqrt((A_x - B_x) ** 2 + (A_y - B_y) ** 2 + (A_z - B_z) ** 2))).evalf()
            gamma = sp.acos(((A_x - C_x) * (B_x - C_x) + (A_y - C_y) * (B_y - C_y) + (A_z - C_z) * (B_z - C_z))
                            / (sp.sqrt((A_x - C_x) ** 2 + (A_y - C_y) ** 2 + (A_z - C_z) ** 2)
                               * sp.sqrt((B_x - C_x) ** 2 + (B_y - C_y) ** 2 + (B_z - C_z) ** 2))).evalf()
            # print(alpha, beta, gamma)
            if alpha != sp.nan and beta != sp.nan and gamma != sp.nan:
                break
        # print(prosty)
        if calkowite is not True:
            if ((prosty is not True)
                    or abs(alpha - sp.pi / 2) < 10 ** (-10)
                    or abs(beta - sp.pi / 2) < 10 ** (-10)
                    or abs(gamma - sp.pi / 2) < 10 ** (-10)):
                break
        else:
            if (((abs(alpha - sp.pi / 2) < 10 ** (-10)
                  or abs(alpha - sp.pi / 3) < 10 ** (-10)
                  or abs(alpha - sp.pi / 4) < 10 ** (-10)
                  or abs(alpha - sp.pi / 6) < 10 ** (-10))
                 and (abs(beta - sp.pi / 2) < 10 ** (-10)
                      or abs(beta - sp.pi / 3) < 10 ** (-10)
                      or abs(beta - sp.pi / 4) < 10 ** (-10)
                      or abs(beta - sp.pi / 6) < 10 ** (-10))
                 and (abs(gamma - sp.pi / 2) < 10 ** (-10)
                      or abs(gamma - sp.pi / 3) < 10 ** (-10)
                      or abs(gamma - sp.pi / 4) < 10 ** (-10)
                      or abs(gamma - sp.pi / 6) < 10 ** (-10)))):
                break

    # print(A_x, A_y, A_z, B_x, B_y, B_z, C_x, C_y, C_z)
    alpha = sp.re((alpha * 180 / sp.pi).evalf(10))
    beta = sp.re((beta * 180 / sp.pi).evalf(10))
    gamma = sp.re((gamma * 180 / sp.pi).evalf(10))
    return (f'Wyznaczyć miary kątów wewnętrznych trójkąta $ABC,$ gdzie\n'
            f'\t\\[\n'
            f'\t\tA = ({A_x}, {A_y}, {A_z}),\\ B = ({B_x}, {B_y}, {B_z}),\\ C = ({C_x}, {C_y}, {C_z})\n'
            f'\t\\]\n'
            f'\tSprawdzić, czy sumują się do $180^{{\\circ}}.$\\\\',
            f'$\\alpha ' +
            str('= ' if round(alpha, 1) == round(alpha, 5) else '\\approx ') +
            f'{alpha:.2f}^{{\\circ}},\\  '
            f'\\beta ' +
            str('= ' if round(beta, 1) == round(beta, 5) else '\\approx ') +
            f'{beta:.2f}^{{\\circ}},\\  '
            f'\\gamma ' +
            str('= ' if round(gamma, 1) == round(gamma, 5) else '\\approx ') +
            f'{gamma:.2f}^{{\\circ}}.$')


def pole_trojkata(calkowite: bool = False):
    """
    Generuje zadanie (w formacie LaTeX wraz z rozwiązaniem) na wyznaczenie pola trójkąta w R^3 oraz jednej z wysokości.

    Args:
        calkowite (bool, optional): Czy pole i wysokości mają być całkowite lub podzielne przez dwa. Defaults to True.

    Returns:
        tuple: Zawiera polecenie oraz jego odpowiednie rozwiązanie.
    """
    liczby = (-3, -2, -1, 1, 2, 3, 4, 5)
    wierzcholek = random.choice(('A', 'B', 'C'))
    while True:
        A = sp.Matrix([sp.Rational(random.choice(liczby)) for _ in range(3)])
        B = sp.Matrix([sp.Rational(random.choice(liczby)) for _ in range(3)])
        C = sp.Matrix([sp.Rational(random.choice(liczby)) for _ in range(3)])
        AB = A - B
        AC = A - C
        BC = B - C
        # BA = B - A
        CA = C - A
        # CB = C - B
        pole = sp.sqrt((AB.cross(AC)).dot(AB.cross(AC))) / 2
        wysokosc = 0  # niepotrzebne w zasadzie, ale bez tego pycharm zgłasza potencjalny błąd nieprzypisania wartości
        match wierzcholek:
            case 'A':
                wysokosc = 2 * pole / sp.sqrt(BC.dot(BC))
            case 'B':
                wysokosc = 2 * pole / sp.sqrt(CA.dot(CA))
            case 'C':
                wysokosc = 2 * pole / sp.sqrt(AB.dot(AB))
        if (pole != 0
                and pole < 10
                and wysokosc < 10
                and ((round(wysokosc) == wysokosc and round(2 * pole) == 2 * pole) or not calkowite)):
            break

    return (
        f'Wyznaczyć pole trójkąta $ABC$ oraz długość wysokości opuszczonej z wierzchołka {wierzcholek} dla\n'
        f'\t\\[\n'
        f'\t\tA = ({A[0]}, {A[1]}, {A[2]}),\\ B = ({B[0]}, {B[1]}, {B[2]}),\\ C = ({C[0]}, {C[1]}, {C[2]})\n'
        f'\t\\]',
        f'$P={sp.latex(pole)},\\ \\ h_{wierzcholek}={sp.latex(wysokosc)}$')
    # A.T, B.T, C.T, calkowite, pole, wysokosc, wierzcholek


def plaszczyzna_styczna():
    typ = random.choice([i for i in range(6)])
    while True:
        a, b, c, d, e, f, g, h, i, j, k, l = [random.choice([n - 4 for n in range(10)]) for _ in range(12)]
        if typ == 0:
            z = a * (x - b) ** 2 * (y - c) ** 2 + d * (x - e) * (y - f)
        elif typ == 1:
            z = a * (x) ** 2 + b * (y) ** 2 + d * x ** 3 * y + e * x * y ** 3 + f * x ** 2 * y
        elif typ == 2:
            z = a * x / y + b * y / x + c * x + d * y + e / x + f / y
        elif typ == 3:
            z = (f * x + g * y) * sp.exp(a * x ** 2 + b * x + c * y ** 2 + d * y + e)
        elif typ == 4:
            z = sp.sqrt(c ** 2 - a * x ** 2 - b * y ** 2)
        elif typ == 5:
            z = sp.sqrt(c ** 2 - a * x ** 2 - b * y ** 2) / (d * x + e * y)
        P = [random.choice([n - 4 for n in range(10)]) for _ in range(2)]
        try:
            z_x = sp.diff(z, x).subs({x: P[0], y: P[1]})
            z_y = sp.diff(z, y).subs({x: P[0], y: P[1]})
            # print(z.is_real, z, z_x, z_y)
            if ((z.subs({x: P[0], y: P[1]})).is_real and z.subs({x: P[0], y: P[1]}) < 10
                    and 0 < abs(z_x) < 10 and 0 < abs(z_y) < 10 and z_x.is_Rational and z_y.is_Rational):
                break
        except:
            pass
    return (
        f'Wyznaczyć płaszczyznę styczną do powierzchni $$f(x,y)={sp.latex(z)}$$ w punkcie $P=({P[0]},{P[1]},f({P[0]},{P[1]})).$',
        f'$z = {sp.latex(z_x * (x - P[0]) + z_y * (y - P[1]) + z.subs({x: P[0], y: P[1]}))}$')


if __name__ == "__main__":  # to się uruchamia tylko, gdy plik jest uruchamiany jako program, a nie ładowany jako moduł
    os.chdir('..')  # by wczytywać z gotowca - inaczej problem ze ścieżkami!
    start_time = time.time()
    # polecenie, rozwiazanie = rownanie_prostej()
    # polecenie, rozwiazanie = rownanie_plaszczyzny()
    # polecenie, rozwiazanie = odleglosc_prostych_skosnych(gotowiec=True)
    # polecenie, rozwiazanie = punkt_symetryczny_do_plaszczyzny()
    # polecenie, rozwiazanie = punkt_symetryczny_do_prostej()
    # polecenie, rozwiazanie = katy_w_trojkacie(prosty=random.choice((False, True)),
    #                                           calkowite=random.choice((False, True)))
    # polecenie, rozwiazanie = pole_trojkata(calkowite=random.choice((True, False)))
    polecenie, rozwiazanie = plaszczyzna_styczna()
    print(polecenie, '\n', rozwiazanie)
    print("--- %s seconds ---" % (time.time() - start_time))
    # pass
