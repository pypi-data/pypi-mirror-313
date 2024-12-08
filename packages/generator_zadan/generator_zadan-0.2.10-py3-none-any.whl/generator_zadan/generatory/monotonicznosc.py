import os  # by sprawdzić istnienie pliku gotowców
import pickle  # do ładowania gotowca
import random
import sys  # do czerwonych komunikatów: print('jakis tekst', file=sys.stderr )
import time
from pathlib import Path

import sympy as sp

sciezka = str(Path(__file__).parent)


# Todo: Maksymalne przedziały monotoniczności domknięte
# Todo: W monotonicznościach nie używać sum

def styczna_normalna(typ: int = 1):
    if typ == 1:  # parabola przez prostą
        while True:
            x = sp.Symbol('x', real=True)
            x_0 = random.choice((-2, -1, 2, 3))
            a, c, d, e = [random.choice((-2, -1, 1, 2, 3, 4)) for _ in range(4)]
            b = random.choice((-2, -1, 0, 1, 2, 3, 4))
            f = ((a * x ** 2 + b * x + c) / (d * x + e)) ** (random.choice((-1, 1)))
            # print(a,b,c,d)
            f_prim = f.diff(x)
            try:
                f_x_0 = f.subs(x, x_0)
                f_prim_x_0 = f_prim.subs(x, x_0)
                if (f_prim_x_0 != 0
                        and f_x_0 != 0
                        and (2 * f_prim_x_0).is_integer
                        and (2 * f_x_0).is_integer
                        and sp.Abs(f_prim_x_0) < 10
                        and sp.Abs(f_x_0) < 10):
                    break
            except ValueError:
                pass
        # print(f_x_0, f_prim_x_0)
        return (f'Wyznaczyć równanie stycznej i normalnej do wykresu funkcji\n'
                f'\t\\[\n'
                f'\t\tf(x) = {sp.latex(f)}\n'
                f'\t\\]\n'
                f' w punkcie $x_0 = {sp.latex(x_0)}.$',
                f'Styczna: $y = {sp.latex(f_prim_x_0 * (x - x_0) + f_x_0)},$ \\quad\n'
                f'Normalna: $y = {sp.latex(-1 / f_prim_x_0 * (x - x_0) + f_x_0)}$')
    if typ == 2:  # pierwiastek z paraboli przez prostą
        potega = random.choice((0, 1))  # by w do drugim był mianownik
        x_0 = random.choice((-2, -1, 2, 3))  # by nie wychodziło za często sqrt(1)
        wykladnicza = random.choice((0, 1))
        iloraz = random.choice((True,False))
        while True:
            x = sp.Symbol('x', real=True)
            a, c, d, e = [random.choice((-2, -1, 1, 2, 3, 4)) for _ in range(4)]
            b = random.choice((-2, -1, 0, 1, 2, 3, 4))
            if iloraz is True:
                f = (sp.sqrt(a * x ** 2 + b * x + c) if wykladnicza == 0 else sp.E ** (a * x ** 2 + b * x + c)) / (
                            d * x + e) ** (potega)
            else:
                f = (sp.sqrt(a * x ** 2 + b * x + c) if wykladnicza == 0 else sp.E ** (a * x ** 2 + b * x + c)) * (
                        d * x + e) ** (potega)
            # print(a,b,c,d)
            f_prim = f.diff(x)
            try:
                f_x_0 = f.subs(x, x_0)
                f_prim_x_0 = f_prim.subs(x, x_0)
                if (f_prim_x_0 != 0
                        and f_x_0 != 0
                        and (2 * f_prim_x_0).is_integer
                        and (2 * f_x_0).is_integer
                        and sp.Abs(f_prim_x_0) < 10
                        and sp.Abs(f_x_0) < 10):
                    break
            except ValueError:
                pass
        # print(f_x_0, f_prim_x_0)
        return (f'Wyznaczyć równanie stycznej i normalnej do wykresu funkcji\n'
                f'\t\\[\n'
                f'\t\tf(x) = {sp.latex(f)}\n'
                f'\t\\]\n'
                f' w punkcie $x_0 = {sp.latex(x_0)}.$',
                f'Styczna: $y = {sp.latex(f_prim_x_0 * (x - x_0) + f_x_0)},$ \\quad\n'
                f'Normalna: $y = {sp.latex(-1 / f_prim_x_0 * (x - x_0) + f_x_0)}$')


def monotonicznosc(typ: int = 1, gotowiec: bool = False):
    """
    Generuje zadanie (w formacie LaTeX wraz z rozwiązaniem) na badanie monotoniczności i ekstremów dla różnych funkcji.

    Args:
        typ (int, optional, defaults to 1):
            1 - parabola przez prostą
            2 - prosta przez parabolę, w gotowcu są 365 różne (na 1000 losowań)
            3 - wielomian 3-go stopnia przez prostą
        gotowiec (bool, optional, defaults to False): Czy zadanie ma być pobierane z gotowego zestawu.

    Returns:
        tuple: Zawiera polecenie oraz jego odpowiednie rozwiązanie.ion of the results.
    """
    if gotowiec is True:
        if typ == 2:
            if os.path.isfile(sciezka + '//gotowe//monotonicznosc_typ_2.pickle'):  # 1000 różnych gotowych
                gotowe = pickle.load(open(sciezka + '//gotowe//monotonicznosc_typ_2.pickle', 'rb'))
                return gotowe[random.randint(0, len(gotowe)) - 1]
            else:
                print('Brak gotowca do tego typu', file=sys.stderr)
        if typ == 3:
            if os.path.isfile(sciezka + '//gotowe//monotonicznosc_typ_3.pickle'):  # 356/1000 różnych gotowych
                gotowe = pickle.load(open(sciezka + '//gotowe//monotonicznosc_typ_3.pickle', 'rb'))
                return gotowe[random.randint(0, len(gotowe)) - 1]
            else:
                print('Brak gotowca do tego typu', file=sys.stderr)
    # to nie musi być w else, bo wcześniejsze warunku w przypadku sukcesu konczą funkcje returnem
    if typ == 1:  # parabola przez prostą
        while True:
            x = sp.Symbol('x', real=True)
            a, c, d, e = [random.choice((-2, -1, 1, 2, 3, 4)) for _ in range(4)]
            b = random.choice((-2, -1, 0, 1, 2, 3, 4))
            f = (a * x ** 2 + b * x + c) / (d * x + e)
            # print(a,b,c,d)
            f_prim = f.diff(x)
            f_bis = f_prim.diff(x)
            krytyczne = sp.solve(f_prim, x)

            if (all([el.is_real for el in krytyczne])
                    and all([10 * el == int(10 * el) for el in krytyczne])
                    and len(krytyczne) > 0):
                break
                # print(f'rozwiazania {krytyczne}')
                # print(sp.latex(f))
        rosnaca = sp.solve(f_prim > 0, x)
        malejaca = sp.solve(f_prim < 0, x)
        if a / d < 0:
            return (f'Zbadać monotoniczność i ekstrema funkcji\n'
                    f'\t\\[\n'
                    f'\t\tf(x)={sp.latex(f)} \n'
                    f'\t\\]\n',
                    f'$f\'(x)={sp.latex(sp.factor(f_prim))}$\\newline\n'
                    # f'$f\'\'(x)={sp.latex(sp.factor(f_bis))}$\\newline\n'
                    f'$f\'(x) > 0 \\textnormal{{ dla: }}'
                    f'{sp.latex(rosnaca)} \\implies f(x) \\textnormal{{ rośnie dla }} '
                    f'x \\in \\left({sp.latex(rosnaca.args[0].args[1])},{sp.latex(rosnaca.args[2].args[1])}  \\right)'
                    f'\\textnormal{{ oraz }} x \\in \\left({sp.latex(rosnaca.args[2].args[1])},{sp.latex(rosnaca.args[1].args[1])}  \\right) $\\newline\n'
                    f'$f\'(x) < 0 \\textnormal{{ dla: }}'
                    f'{sp.latex(malejaca)} \\implies f(x) \\textnormal{{ maleje dla }} '
                    f'x \\in \\left( -\\infty, {sp.latex(malejaca.args[1].args[1])}  \\right)'
                    f'\\textnormal{{ oraz }} x \\in \\left({sp.latex(malejaca.args[0].args[0])}, \\infty  \\right) $\\newline\n'
                    f'$f\'(x) = 0 \\textnormal{{ dla }} x \\in'
                    f' {sp.latex(krytyczne)}'.replace('[', '\\{').replace(']', '\\}') +
                    f' \\implies ' +
                    ('f_{\\min}' if f_bis.subs(x, krytyczne[0]) > 0 else 'f_{\\max}') +
                    f'\\left({sp.latex(krytyczne[0])}\\right) = {sp.latex(f.subs(x, krytyczne[0]))} \\textnormal{{ oraz }} ' +
                    ('f_{\\min}' if f_bis.subs(x, krytyczne[1]) > 0 else 'f_{\\max}') +
                    f'\\left({sp.latex(krytyczne[1])}\\right) = {sp.latex(f.subs(x, krytyczne[1]))}$')
        else:
            return (f'Zbadać monotoniczność i ekstrema funkcji\n'
                    f'\t\\[\n'
                    f'\t\tf(x)={sp.latex(f)} \n'
                    f'\t\\]\n',
                    f'$f\'(x)={sp.latex(sp.factor(f_prim))}$\\newline\n'
                    # f'$f\'\'(x)={sp.latex(sp.factor(f_bis))}$\\newline\n'
                    f'$f\'(x) > 0 \\textnormal{{ dla: }}'
                    f'{sp.latex(rosnaca)}\\implies f(x) \\textnormal{{ rośnie dla }} '
                    f'x \\in \\left( -\\infty, {sp.latex(rosnaca.args[1].args[1])}  \\right)'
                    f'\\textnormal{{ oraz }} x \\in \\left({sp.latex(rosnaca.args[0].args[0])}, \\infty  \\right)$\\newline\n'
                    f'$f\'(x) < 0 \\textnormal{{ dla: }}'
                    f'{sp.latex(malejaca)} \\implies f(x) \\textnormal{{ rośnie dla }} '
                    f'x \\in \\left({sp.latex(malejaca.args[0].args[1])},{sp.latex(malejaca.args[2].args[1])}  \\right)'
                    f'\\textnormal{{ oraz }} x \\in \\left({sp.latex(malejaca.args[2].args[1])},{sp.latex(malejaca.args[1].args[1])}  \\right)$\\newline\n'
                    f'$f\'(x) = 0 \\textnormal{{ dla }} x \\in'
                    f' {sp.latex(krytyczne)}'.replace('[', '\\{').replace(']', '\\}') +
                    f' \\implies ' +
                    ('f_{\\min}' if f_bis.subs(x, krytyczne[0]) > 0 else 'f_{\\max}') +
                    f'\\left({sp.latex(krytyczne[0])}\\right) = {sp.latex(f.subs(x, krytyczne[0]))} \\textnormal{{ oraz }} ' +
                    ('f_{\\min}' if f_bis.subs(x, krytyczne[1]) > 0 else 'f_{\\max}') +
                    f'\\left({sp.latex(krytyczne[1])}\\right) = {sp.latex(f.subs(x, krytyczne[1]))}$')
    if typ == 2:  # prosta przez parabolę - trochę trwa więce jest gotowiec z '' zadaniami.
        ciekawe = random.choice((0, 1))  # co drugie powinno być ciekawe tzn. rozbijane na kilka przedziałów
        while True:
            x = sp.Symbol('x', real=True)
            a, c, d, e = [random.choice((-2, -1, 1, 2, 3, 4)) for _ in range(4)]
            b = random.choice((-2, -1, 0, 1, 2, 3, 4))
            # print(a,b,c,d,e,sep=',')
            # a, b, c, d, e =-2,-2,4,1,-2
            f = (d * x + e) / (a * x ** 2 + b * x + c)
            f_prim = f.diff(x)
            f_bis = f_prim.diff(x)
            krytyczne = sp.solve(f_prim, x)
            asymptoty = sp.solve(a * x ** 2 + b * x + c, x)
            if ciekawe:
                if (all([el.is_real for el in krytyczne])
                        and all([10 * el == int(10 * el) for el in krytyczne])
                        and len(krytyczne) == 2  # trzech być nie może
                        and all([el.is_integer for el in asymptoty])
                        and len(asymptoty) == 2):
                    break
            else:
                if (all([el.is_real for el in krytyczne])
                        and all([10 * el == int(10 * el) for el in krytyczne])
                        and len(krytyczne) > 0  # trzech być nie może
                        and all([el.is_integer for el in asymptoty])
                        and len(asymptoty) >= 0):
                    break
                # print(f'rozwiazania {krytyczne}')
                # print(sp.latex(f))
        rosnaca = sp.solve(f_prim > 0, x)
        malejaca = sp.solve(f_prim < 0, x)
        # print(f, asymptoty, krytyczne, rosnaca, malejaca, sep='\n')
        if len(krytyczne) == 1:  # nie może być len(krytyczne) == 1 oraz len(asymptoty) == 0 lub len(asymptoty) == 2
            if a / d > 0:
                return (f'Zbadać monotoniczność i ekstrema funkcji\n'
                        f'\t\\[\n'
                        f'\t\tf(x)={sp.latex(f)} \n'
                        f'\t\\]\n',
                        f'$f\'(x)={sp.latex(sp.factor(f_prim))}$\\newline\n'
                        # f'$f\'\'(x)={sp.latex(sp.factor(f_bis))}$\\newline\n'
                        f'$f\'(x) > 0 \\textnormal{{ dla: }}'
                        f'{sp.latex(rosnaca)} \\implies f(x) \\textnormal{{ rośnie dla }} '
                        f'x \\in \\left( {sp.latex(rosnaca.args[0].args[0])}, {sp.latex(rosnaca.args[1].args[1])}  \\right)'
                        '$\\newline\n'
                        f'$f\'(x) < 0 \\textnormal{{ dla: }}'
                        f'{sp.latex(malejaca)} \\implies f(x) \\textnormal{{ maleje dla }} '
                        f'x \\in \\left( -\\infty, {sp.latex(malejaca.args[1].args[1])}  \\right)'
                        f'\\textnormal{{ oraz }} x \\in \\left({sp.latex(malejaca.args[0].args[0])}, \\infty  \\right) $\\newline\n'
                        f'$f\'(x) = 0 \\textnormal{{ dla }} x \\in'
                        f' {sp.latex(krytyczne)}'.replace('[', '\\{').replace(']', '\\}') +
                        f' \\implies ' +
                        ('f_{\\min}' if f_bis.subs(x, krytyczne[0]) > 0 else 'f_{\\max}') +
                        f'\\left({sp.latex(krytyczne[0])}\\right) = {sp.latex(f.subs(x, krytyczne[0]))}$')
            else:
                return (f'Zbadać monotoniczność i ekstrema funkcji\n'
                        f'\t\\[\n'
                        f'\t\tf(x)={sp.latex(f)} \n'
                        f'\t\\]\n',
                        f'$f\'(x)={sp.latex(sp.factor(f_prim))}$\\newline\n'
                        # f'$f\'\'(x)={sp.latex(sp.factor(f_bis))}$\\newline\n'
                        f'$f\'(x) > 0 \\textnormal{{ dla: }}'
                        f'{sp.latex(rosnaca)} \\implies f(x) \\textnormal{{ rośnie dla }} '
                        f'x \\in \\left( -\\infty, {sp.latex(rosnaca.args[1].args[1])}  \\right)'
                        f'\\textnormal{{ oraz }} x \\in \\left({sp.latex(rosnaca.args[0].args[0])}, \\infty    \\right)'
                        '$\\newline\n'
                        f'$f\'(x) < 0 \\textnormal{{ dla: }}'
                        f'{sp.latex(malejaca)} \\implies f(x) \\textnormal{{ maleje dla }} '
                        f'x \\in \\left( {sp.latex(malejaca.args[0].args[0])}, {sp.latex(malejaca.args[1].args[1])}  \\right) $\\newline\n'
                        f'$f\'(x) = 0 \\textnormal{{ dla }} x \\in'
                        f' {sp.latex(krytyczne)}'.replace('[', '\\{').replace(']', '\\}') +
                        f' \\implies ' +
                        ('f_{\\min}' if f_bis.subs(x, krytyczne[0]) > 0 else 'f_{\\max}') +
                        f'\\left({sp.latex(krytyczne[0])}\\right) = {sp.latex(f.subs(x, krytyczne[0]))}$')
        else:  # punktów stacjonarnych może być maksymalnie dwa
            # Todo: wyszły 4 przypadki - możliwe, że wyjdzie więcej - może się pojawić błąd
            if len(asymptoty) == 0:
                if a / d > 0:
                    return (f'Zbadać monotoniczność i ekstrema funkcji\n'
                            f'\t\\[\n'
                            f'\t\tf(x)={sp.latex(f)} \n'
                            f'\t\\]\n',
                            f'$f\'(x)={sp.latex(sp.factor(f_prim))}$\\newline\n'
                            # f'$f\'\'(x)={sp.latex(sp.factor(f_bis))}$\\newline\n'
                            f'$f\'(x) > 0 \\textnormal{{ dla: }}'
                            f'{sp.latex(rosnaca)} \\implies f(x) \\textnormal{{ rośnie dla }} '
                            f'x \\in \\left( {sp.latex(rosnaca.args[0].args[0])}, {sp.latex(rosnaca.args[1].args[1])}  \\right) $\\newline\n'
                            f'$f\'(x) < 0 \\textnormal{{ dla: }}'
                            f'{sp.latex(malejaca)} \\implies f(x) \\textnormal{{ maleje dla }} '
                            f'x \\in \\left( -\\infty, {sp.latex(malejaca.args[1].args[1])}  \\right)'
                            f'\\textnormal{{ oraz }} x \\in \\left({sp.latex(malejaca.args[0].args[0])}, \\infty  \\right) $\\newline\n'
                            f'$f\'(x) = 0 \\textnormal{{ dla }} x \\in'
                            f' {sp.latex(krytyczne)}'.replace('[', '\\{').replace(']', '\\}') +
                            f' \\implies ' +
                            ('f_{\\min}' if f_bis.subs(x, krytyczne[0]) > 0 else 'f_{\\max}') +
                            f'\\left({sp.latex(krytyczne[0])}\\right) = {sp.latex(f.subs(x, krytyczne[0]))} \\textnormal{{ oraz }} ' +
                            ('f_{\\min}' if f_bis.subs(x, krytyczne[1]) > 0 else 'f_{\\max}') +
                            f'\\left({sp.latex(krytyczne[1])}\\right) = {sp.latex(f.subs(x, krytyczne[1]))}$')
                else:
                    return (f'Zbadać monotoniczność i ekstrema funkcji\n'
                            f'\t\\[\n'
                            f'\t\tf(x)={sp.latex(f)} \n'
                            f'\t\\]\n',
                            f'$f\'(x)={sp.latex(sp.factor(f_prim))}$\\newline\n'
                            # f'$f\'\'(x)={sp.latex(sp.factor(f_bis))}$\\newline\n'
                            f'$f\'(x) > 0 \\textnormal{{ dla: }}'
                            f'{sp.latex(rosnaca)} \\implies f(x) \\textnormal{{ rośnie dla }} '
                            f'x \\in \\left( -\\infty, {sp.latex(rosnaca.args[1].args[1])}  \\right)'
                            f'\\textnormal{{ oraz }} x \\in \\left({sp.latex(rosnaca.args[0].args[0])}, \\infty    \\right)'
                            '$\\newline\n'
                            f'$f\'(x) < 0 \\textnormal{{ dla: }}'
                            f'{sp.latex(malejaca)} \\implies f(x) \\textnormal{{ maleje dla }} '
                            f'x \\in \\left( {sp.latex(malejaca.args[0].args[0])}, {sp.latex(malejaca.args[1].args[1])}  \\right) $\\newline\n'
                            f'$f\'(x) = 0 \\textnormal{{ dla }} x \\in'
                            f' {sp.latex(krytyczne)}'.replace('[', '\\{').replace(']', '\\}') +
                            f' \\implies ' +
                            ('f_{\\min}' if f_bis.subs(x, krytyczne[0]) > 0 else 'f_{\\max}') +
                            f'\\left({sp.latex(krytyczne[0])}\\right) = {sp.latex(f.subs(x, krytyczne[0]))} \\textnormal{{ oraz }} ' +
                            ('f_{\\min}' if f_bis.subs(x, krytyczne[1]) > 0 else 'f_{\\max}') +
                            f'\\left({sp.latex(krytyczne[1])}\\right) = {sp.latex(f.subs(x, krytyczne[1]))}$')
            if len(asymptoty) == 2:
                if a / d > 0:
                    return (f'Zbadać monotoniczność i ekstrema funkcji\n'
                            f'\t\\[\n'
                            f'\t\tf(x)={sp.latex(f)} \n'
                            f'\t\\]\n',
                            f'$f\'(x)={sp.latex(sp.factor(f_prim))}$\\newline\n'
                            # f'$f\'\'(x)={sp.latex(sp.factor(f_bis))}$\\newline\n'
                            f'$f\'(x) > 0 \\textnormal{{ dla: }}'
                            f'{sp.latex(rosnaca)} \\implies f(x) \\textnormal{{ rośnie dla }} '
                            f'x \\in \\left({sp.latex(rosnaca.args[0].args[1])},{sp.latex(rosnaca.args[2].args[1])}  \\right)'
                            f'\\textnormal{{ oraz }} x \\in \\left({sp.latex(rosnaca.args[2].args[1])},{sp.latex(rosnaca.args[1].args[1])}  \\right) $\\newline\n'
                            f'$f\'(x) < 0 \\textnormal{{ dla: }}'
                            f'{sp.latex(malejaca)} \\implies f(x) \\textnormal{{ maleje dla }} '
                            f'x \\in \\left( -\\infty, {sp.latex(malejaca.args[1].args[1])}  \\right)'
                            f'\\textnormal{{ oraz }} x \\in \\left({sp.latex(malejaca.args[2].args[0].args[0])}, {sp.latex(malejaca.args[2].args[1].args[1])}  \\right) '
                            f'\\textnormal{{ oraz }} x \\in \\left({sp.latex(malejaca.args[0].args[0])}, \\infty  \\right) $\\newline\n'
                            f'$f\'(x) = 0 \\textnormal{{ dla }} x \\in'
                            f' {sp.latex(krytyczne)}'.replace('[', '\\{').replace(']', '\\}') +
                            f' \\implies ' +
                            ('f_{\\min}' if f_bis.subs(x, krytyczne[0]) > 0 else 'f_{\\max}') +
                            f'\\left({sp.latex(krytyczne[0])}\\right) = {sp.latex(f.subs(x, krytyczne[0]))} \\textnormal{{ oraz }} ' +
                            ('f_{\\min}' if f_bis.subs(x, krytyczne[1]) > 0 else 'f_{\\max}') +
                            f'\\left({sp.latex(krytyczne[1])}\\right) = {sp.latex(f.subs(x, krytyczne[1]))}$')
                else:
                    # print(a,b,c,d,e,sep=',')
                    return (f'Zbadać monotoniczność i ekstrema funkcji\n'
                            f'\t\\[\n'
                            f'\t\tf(x)={sp.latex(f)} \n'
                            f'\t\\]\n',
                            f'$f\'(x)={sp.latex(sp.factor(f_prim))}$\\newline\n'
                            # f'$f\'\'(x)={sp.latex(sp.factor(f_bis))}$\\newline\n'
                            f'$f\'(x) > 0 \\textnormal{{ dla: }}'
                            f'{sp.latex(rosnaca)} \\implies f(x) \\textnormal{{ rośnie dla }} '
                            f'x \\in \\left( -\\infty, {sp.latex(rosnaca.args[1].args[1])}  \\right)'
                            f'\\textnormal{{ oraz }} x \\in \\left({sp.latex(rosnaca.args[2].args[0].args[0])}, {sp.latex(rosnaca.args[2].args[1].args[1])}  \\right) '
                            f'\\textnormal{{ oraz }} x \\in \\left({sp.latex(rosnaca.args[0].args[0])}, \\infty  \\right) $\\newline\n'
                            f'$f\'(x) < 0 \\textnormal{{ dla: }}'
                            f'{sp.latex(malejaca)} \\implies f(x) \\textnormal{{ maleje dla }} '
                            f'x \\in \\left({sp.latex(malejaca.args[0].args[1])},{sp.latex(malejaca.args[2].args[1])}  \\right)'
                            f'\\textnormal{{ oraz }} x \\in \\left({sp.latex(malejaca.args[2].args[1])},{sp.latex(malejaca.args[1].args[1])}  \\right)  $\\newline\n'
                            f'$f\'(x) = 0 \\textnormal{{ dla }} x \\in'
                            f' {sp.latex(krytyczne)}'.replace('[', '\\{').replace(']', '\\}') +
                            f' \\implies ' +
                            ('f_{\\min}' if f_bis.subs(x, krytyczne[0]) > 0 else 'f_{\\max}') +
                            f'\\left({sp.latex(krytyczne[0])}\\right) = {sp.latex(f.subs(x, krytyczne[0]))} \\textnormal{{ oraz }} ' +
                            ('f_{\\min}' if f_bis.subs(x, krytyczne[1]) > 0 else 'f_{\\max}') +
                            f'\\left({sp.latex(krytyczne[1])}\\right) = {sp.latex(f.subs(x, krytyczne[1]))}$')
    if typ == 3:  # wielomian 3-go stopnia przez prostą
        def przedzialy(expr):  # nie podoba mi się to!!!
            nonlocal punkty
            if expr.func == sp.core.relational.StrictLessThan:
                if str(expr.args[0]) == 'x':
                    if -sp.oo not in punkty:
                        punkty.append(-sp.oo)
                    if expr.args[1] not in punkty:
                        punkty.append(expr.args[1])
                else:
                    punkty.append(sp.oo)
                    punkty.append(expr.args[0])
            if expr.func == sp.And:
                if expr.args[0].args[0] not in punkty:
                    punkty.append(expr.args[0].args[0])
                if expr.args[1].args[1] not in punkty:
                    punkty.append(expr.args[1].args[1])
            else:
                for arg in expr.args:
                    przedzialy(arg)
            return 0

        x = sp.Symbol('x', real=True)
        while True:
            b, c, d = [random.choice([-3, -2, -1, 1, 0, 0, 2, 3]) for _ in range(3)]
            a, e, g = [random.choice([-2, -1, 1, 2, 3]) for _ in range(3)]
            '''dla następnych danych są 3 ekstrema - wykluczamy to na razie'''
            # a, b, c, d, e, g = 2,2,-3,0,1,-2
            '''dla powyższych danych są 3 ekstrema - wykluczamy to na razie'''
            # a, b, c, d, e, g = -2, 0, 0, 0, 1, 2
            # a, b, c, d, e, g = -2, 0, 0, 0, -1, 1
            # a, b, c, d, e, g = 1, 0, 0, 0, -1, 2
            f = (a * x ** 3 + b * x ** 2 + c * x + d) / (e * x + g)
            f_prim = f.diff(x)
            krytyczne = sp.solve(f_prim, x)
            if (len(krytyczne) == 2
                    and all([el.is_real for el in krytyczne])
                    and all([(2 * el).is_integer for el in krytyczne])):
                # print([el.is_real for el in krytyczne])
                # print([2 * el.is_integer for el in krytyczne])
                break
        f_bis = f_prim.diff(x)
        rosnaca = sp.solve(f_prim > 0, x)
        malejaca = sp.solve(f_prim < 0, x)
        # print(f, krytyczne)
        # for st in krytyczne:
        #     print(f_bis.subs(x, st))

        if a / e > 0:
            # print(a, b, c, d, e, g, sep=',')
            ''' to mi sie strasznie nie podoba '''
            punkty = list()
            przedzialy(rosnaca)
            punkty_rosnaca = sorted(punkty)
            punkty = list()
            przedzialy(malejaca)
            punkty_malejaca = sorted(punkty)
            # print(punkty_rosnaca)
            # print(punkty_malejaca)
            if len(punkty_rosnaca) == 2:
                przedzial_rosnacy = f'\\left({sp.latex(punkty_rosnaca[0])},{sp.latex(sp.oo)}\\right)'
                przedzial_malejacy = (f'\\left({sp.latex(-sp.oo)},{sp.latex(punkty_malejaca[2])}\\right)'
                                      f' \\textnormal{{ oraz }} x \\in'
                                      f'  \\left({sp.latex(punkty_malejaca[2])},{sp.latex(punkty_malejaca[3])}\\right)')
            else:
                przedzial_rosnacy = (f'\\left({sp.latex(punkty_rosnaca[0])},{sp.latex(punkty_rosnaca[1])}\\right)'
                                     f' \\textnormal{{ oraz }} x \\in'
                                     f'  \\left({sp.latex(punkty_rosnaca[1])},{sp.latex(punkty_rosnaca[3])}\\right)')
                przedzial_malejacy = f'\\left({sp.latex(-sp.oo)},{sp.latex(punkty_malejaca[1])}\\right)'
            # print(przedzial_rosnacy)
            # print(przedzial_malejacy)
            return (f'Zbadać monotoniczność i ekstrema funkcji\n'
                    f'\t\\[\n'
                    f'\t\tf(x)={sp.latex(f)} \n'
                    f'\t\\]\n',
                    f'$f\'(x)={sp.latex(sp.factor(f_prim))}$\\newline\n'
                    # f'$f\'\'(x)={sp.latex(sp.factor(f_bis))}$\\newline\n'
                    f'$f\'(x) > 0 \\textnormal{{ dla: }}'
                    f'{sp.latex(rosnaca)} \\implies f(x) \\textnormal{{ rośnie dla }} '
                    f'x \\in {przedzial_rosnacy} $\\newline\n'
                    f'$f\'(x) < 0 \\textnormal{{ dla: }}'
                    f'{sp.latex(malejaca)} \\implies f(x) \\textnormal{{ maleje dla }} '
                    f'x \\in {przedzial_malejacy} $\\newline\n'
                    f'$f\'(x) = 0 \\textnormal{{ dla }} x \\in'
                    f' {sp.latex(krytyczne)}'.replace('[', '\\{').replace(']', '\\}') +
                    f' \\implies ' +
                    (
                        'f_{\\min}' + f'\\left({sp.latex(krytyczne[0])}\\right) = {sp.latex(f.subs(x, krytyczne[0]))}$' if f_bis.subs(
                            x,
                            krytyczne[
                                0]) > 0 else '') +
                    (
                        'f_{\\max}' + f'\\left({sp.latex(krytyczne[0])}\\right) = {sp.latex(f.subs(x, krytyczne[0]))}$' if f_bis.subs(
                            x,
                            krytyczne[
                                0]) < 0 else '') +
                    (
                        'f_{\\min}' + f'\\left({sp.latex(krytyczne[1])}\\right) = {sp.latex(f.subs(x, krytyczne[1]))}$' if f_bis.subs(
                            x,
                            krytyczne[
                                1]) > 0 else '') +
                    (
                        'f_{\\max}' + f'\\left({sp.latex(krytyczne[1])}\\right) = {sp.latex(f.subs(x, krytyczne[1]))}$' if f_bis.subs(
                            x,
                            krytyczne[
                                1]) < 0 else ''))
        else:
            # print(a, b, c, d, e, g, sep=',')
            ''' to mi sie strasznie nie podoba '''
            punkty = list()
            przedzialy(rosnaca)
            punkty_rosnaca = sorted(punkty)
            punkty = list()
            przedzialy(malejaca)
            punkty_malejaca = sorted(punkty)
            # print(punkty_rosnaca)
            # print(punkty_malejaca)
            if len(punkty_rosnaca) == 2:
                przedzial_rosnacy = f'\\left({sp.latex(-sp.oo)},{sp.latex(punkty_rosnaca[1])}\\right)'
                przedzial_malejacy = (f'\\left({sp.latex(punkty_malejaca[0])},{sp.latex(punkty_malejaca[1])}\\right)'
                                      f' \\textnormal{{ oraz }} x \\in'
                                      f'  \\left({sp.latex(punkty_malejaca[1])},{sp.latex(sp.oo)}\\right)')
            else:
                przedzial_rosnacy = (f'\\left({sp.latex(punkty_rosnaca[0])},{sp.latex(punkty_rosnaca[2])}\\right)'
                                     f' \\textnormal{{ oraz }} x \\in'
                                     f'  \\left({sp.latex(punkty_rosnaca[2])},{sp.latex(punkty_rosnaca[3])}\\right)')
                przedzial_malejacy = f'\\left({sp.latex(punkty_malejaca[0])},{sp.latex(sp.oo)}\\right)'
            # print(przedzial_rosnacy)
            # print(przedzial_malejacy)
            return (f'Zbadać monotoniczność i ekstrema funkcji\n'
                    f'\t\\[\n'
                    f'\t\tf(x)={sp.latex(f)} \n'
                    f'\t\\]\n',
                    f'$f\'(x)={sp.latex(sp.factor(f_prim))}$\\newline\n'
                    # f'$f\'\'(x)={sp.latex(sp.factor(f_bis))}$\\newline\n'
                    f'$f\'(x) > 0 \\textnormal{{ dla: }}'
                    f'{sp.latex(rosnaca)} \\implies f(x) \\textnormal{{ rośnie dla }} '
                    f'x \\in {przedzial_rosnacy}  $\\newline\n'
                    f'$f\'(x) < 0 \\textnormal{{ dla: }}'
                    f'{sp.latex(malejaca)} \\implies f(x) \\textnormal{{ maleje dla }} '
                    f'x \\in {przedzial_malejacy} $\\newline\n'
                    f'$f\'(x) = 0 \\textnormal{{ dla }} x \\in'
                    f' {sp.latex(krytyczne)}'.replace('[', '\\{').replace(']', '\\}') +
                    f' \\implies ' +
                    (
                        'f_{\\min}' + f'\\left({sp.latex(krytyczne[0])}\\right) = {sp.latex(f.subs(x, krytyczne[0]))}$' if f_bis.subs(
                            x,
                            krytyczne[
                                0]) > 0 else '') +
                    (
                        'f_{\\max}' + f'\\left({sp.latex(krytyczne[0])}\\right) = {sp.latex(f.subs(x, krytyczne[0]))}$' if f_bis.subs(
                            x,
                            krytyczne[
                                0]) < 0 else '') +
                    (
                        'f_{\\min}' + f'\\left({sp.latex(krytyczne[1])}\\right) = {sp.latex(f.subs(x, krytyczne[1]))}$' if f_bis.subs(
                            x,
                            krytyczne[
                                1]) > 0 else '') +
                    (
                        'f_{\\max}' + f'\\left({sp.latex(krytyczne[1])}\\right) = {sp.latex(f.subs(x, krytyczne[1]))}$' if f_bis.subs(
                            x,
                            krytyczne[
                                1]) < 0 else ''))


if __name__ == "__main__":
    start = time.time()
    gotowce = True
    os.chdir('..')  # by wczytywać z gotowca - inaczej problem ze ścieżkami!
    # polecenie, rozwiazanie = monotonicznosc(typ=3)
    polecenie, rozwiazanie = monotonicznosc(typ=3, gotowiec=gotowce)
    print(polecenie, '\n', rozwiazanie)
    print(f'czas generowania: {round(time.time() - start, 3)}s')
