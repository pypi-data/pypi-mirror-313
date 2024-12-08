import os  # by sprawdzić istnienie pliku gotowców
import pickle  # do ładowania gotowca
import random
import sys  # do czerwonych komunikatów: print('jakis tekst', file=sys.stderr )
import time
from pathlib import Path

import sympy as sp

sciezka = str(Path(__file__).parent)

x = sp.Symbol('x', real=True)


# Todo: Dołożyć rysunki przy polach

def pole_obszaru(typ: int = 1, gotowiec: bool = False):
    if gotowiec is True:
        if typ == 3:  # 2760/10000 różnych gotowych
            if os.path.isfile(sciezka + '//gotowe//pole_obszaru_typ_3.pickle'):
                gotowe = pickle.load(open(sciezka + '//gotowe//pole_obszaru_typ_3.pickle', 'rb'))
                return gotowe[random.randint(0, len(gotowe)) - 1]
            else:
                print('Brak gotowca do tego typu', file=sys.stderr)
        if typ == 4:
            if os.path.isfile(sciezka + '//gotowe//pole_obszaru_typ_4.pickle'):  # 160/1000 różnych gotowych
                gotowe = pickle.load(open(sciezka + '//gotowe//pole_obszaru_typ_4.pickle', 'rb'))
                return gotowe[random.randint(0, len(gotowe)) - 1]
            else:
                print('Brak gotowca do tego typu', file=sys.stderr)
    # to nie musi być w else, bo wcześniejsze warunku w przypadku sukcesu konczą funkcje returnem
    if typ == 1:  # parabola i prosta 706/1000 różnych
        while True:
            a, d = [random.choice((-2, -1, 1, 2)) for _ in range(2)]
            while True:
                b, c, e = [random.choice((-3, -2, -1, 0, 1, 2, 3, 4, 5)) for _ in range(3)]
                przeciecia = sp.solve(a * x ** 2 + b * x + c - d * x - e)
                if len(przeciecia) == 2 and all(punkty.is_integer for punkty in przeciecia):
                    break
            break
        F = a * x ** 2 + b * x + c
        G = d * x + e
        calka = abs(sp.integrate(F - G, (x, min(przeciecia), max(przeciecia))))
        posredni = (min(przeciecia) + max(przeciecia)) / 2
        return (f'Obliczyć pole obszaru ograniczonego wykresami krzywych\n'
                f'\t\\[\n'
                f'\t\t f(x) = {sp.latex(F)} \\quad \\textnormal{{ oraz }} \\quad g(x) = {sp.latex(G)} \n'
                f'\t\\]\n',
                f'Pole obszaru to $\\int\\limits_{{{min(przeciecia)}}}^{{{max(przeciecia)}}}'
                f'\\left({sp.latex(F - G) if F.subs(x, posredni) > G.subs(x, posredni) else sp.latex(G - F)}\\right)\\,dx = '
                f' {sp.latex(calka)}$')
    if typ == 2:  # dwie parabole 890/1000 różnych
        while True:
            while True:
                a, d = [random.choice((-2, -1, 1, 2)) for _ in range(2)]
                if a != d:
                    break
            while True:
                b, c, e, f = [random.choice((-3, -2, -1, 0, 1, 2, 3, 4, 5)) for _ in range(4)]
                F = a * x ** 2 + b * x + c
                G = d * x ** 2 + e * x + f
                przeciecia = sp.solve(F - G, x)
                if len(przeciecia) == 2 and all(punkty.is_integer for punkty in przeciecia):
                    break
            break
        calka = abs(sp.integrate(F - G, (x, min(przeciecia), max(przeciecia))))
        # calka = sp.collect(calka, (sp.sin(d * x), sp.cos(d * x)))  # tu czasem źle grupuje sin(x) - to jest jakiś bug - sympy 1.12
        posredni = (min(przeciecia) + max(przeciecia)) / 2
        return (f'Obliczyć pole obszaru ograniczonego wykresami krzywych\n'
                f'\t\\[\n'
                f'\t\t f(x) = {sp.latex(F)} \\quad \\textnormal{{ oraz }} \\quad g(x) = {sp.latex(G)} \n'
                f'\t\\]\n',
                f'Pole obszaru to $\\int\\limits_{{{min(przeciecia)}}}^{{{max(przeciecia)}}}'
                f'\\left({sp.latex(F - G) if F.subs(x, posredni) > G.subs(x, posredni) else sp.latex(G - F)}\\right)\\,dx = '
                f' {sp.latex(calka)}$')
    if typ == 3:  # prosta i wielomian trzeciego stopnia 837/1000 różnych
        while True:
            a, c = [random.choice((-4, -3, -2, -1, 1, 2, 3, 4)) for _ in range(2)]
            b, c, d, e, f = [random.choice((-3, -2, -1, 0, 1, 2, 3, 4, 5)) for _ in range(5)]
            F = a * x + b
            G = c * x ** 3 + d * x ** 2 + e * x + f
            przeciecia = sp.solve(F - G, x)
            if len(przeciecia) == 3 and all((punkty).is_integer for punkty in przeciecia):
                break
        # print(przeciecia, przeciecia[1])
        calka = abs(sp.integrate(abs(F - G), (x, min(przeciecia), max(przeciecia))))
        # calka = sp.collect(calka, (sp.sin(d * x), sp.cos(d * x)))  # tu czasem źle grupuje sin(x) - to jest jakiś bug - sympy 1.12
        posredni1 = (min(przeciecia) + przeciecia[1]) / 2
        posredni2 = (przeciecia[1] + max(przeciecia)) / 2
        # print(posredni1, posredni2, F.subs(x, posredni1) > F.subs(x, posredni1))
        return (f'Obliczyć pole obszaru ograniczonego wykresami krzywych\n'
                f'\t\\[\n'
                f'\t\t f(x) = {sp.latex(F)} \\quad \\textnormal{{ oraz }} \\quad g(x) = {sp.latex(G)} \n'
                f'\t\\]\n',
                f'Pole obszaru to $\\int\\limits_{{{min(przeciecia)}}}^{{{przeciecia[1]}}}'
                f'\\left({sp.latex(F - G) if F.subs(x, posredni1) > G.subs(x, posredni1) else sp.latex(G - F)}\\right)\\,dx + '
                f'\\int\\limits_{{{przeciecia[1]}}}^{{{max(przeciecia)}}}'
                f'\\left({sp.latex(F - G) if F.subs(x, posredni2) > G.subs(x, posredni2) else sp.latex(G - F)}\\right)\\,dx = '
                f' {sp.latex(calka)}$')
    if typ == 4:  # hiperbola i parabola bez wielokrotnych przecieć w jednej ćwiartce
        # Na 1000 losowań wyszło 160 różnych zadań.
        while True:
            a, b = [random.choice((-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6)) for _ in range(2)]
            c, d = [random.choice((-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6)) for _ in range(2)]
            # a, b, c, d = -1, sp.Rational(3 / 2), 5, sp.Rational(9 / 2)
            # a, b, c, d = 1, -sp.Rational(3 / 2), -5, -sp.Rational(9 / 2)

            F = a / x
            G = b * x ** 2 + c * x + d
            przeciecia = sp.solve(F - G, x)
            # print(przeciecia)
            if len(przeciecia) == 3 and all((6 * punkty).is_integer for punkty in przeciecia):
                break
        # calka = abs(sp.integrate((F - G), (x, min(przeciecia), max(przeciecia))))
        calka1 = abs(sp.integrate(F - G, (x, min(przeciecia), przeciecia[1])))
        calka2 = abs(sp.integrate(F - G, (x, przeciecia[1], max(przeciecia))))
        if calka1.is_finite:
            posredni = (min(przeciecia) + przeciecia[1]) / 2
            return (f'Obliczyć pole obszaru ograniczonego wykresami krzywych\n'
                    f'\t\\[\n'
                    f'\t\t f(x) = {sp.latex(F)} \\quad \\textnormal{{ oraz }} \\quad g(x) = {sp.latex(G)} \n'
                    f'\t\\]\n',
                    f'Pole obszaru to $\\int\\limits_{{{min(przeciecia)}}}^{{{przeciecia[1]}}}'
                    f'\\left({sp.latex(F - G) if F.subs(x, posredni) > G.subs(x, posredni) else sp.latex(G - F)}\\right)\\,dx = '
                    f' {sp.latex(calka1)}$'.replace('log', 'ln'))
        else:
            posredni = (max(przeciecia) + przeciecia[1]) / 2
            return (f'Obliczyć pole obszaru ograniczonego wykresami krzywych\n'
                    f'\t\\[\n'
                    f'\t\t f(x) = {sp.latex(F)} \\quad \\textnormal{{ oraz }} \\quad g(x) = {sp.latex(G)} \n'
                    f'\t\\]\n',
                    f'Pole obszaru to $\\int\\limits_{{{przeciecia[1]}}}^{{{max(przeciecia)}}}'
                    f'\\left({sp.latex(F - G) if F.subs(x, posredni) > G.subs(x, posredni) else sp.latex(G - F)}\\right)\\,dx = '
                    f' {sp.latex(calka2)}$'.replace('log', 'ln'))

    if typ == 5:  # hiperbola i parabola z wielokrotnymi przecięciami w jednej ćwiartce. Tylko 24 różne zadania.
        while True:
            # to poniżej daje mało różnych wyników i strasznie długo trwa. Wybrałem z nich tylko te co działają
            # a, b, c, d = [
            #     random.choice((-6, sp.Rational(-11 / 2), -5, sp.Rational(-9 / 2), -4, sp.Rational(-7 / 2), -3,
            #                    sp.Rational(-5 / 2), -2, sp.Rational(-3 / 2), -1, sp.Rational(-1 / 2), 0,
            #                    sp.Rational(1 / 2), 1,
            #                    sp.Rational(3 / 2), 2, sp.Rational(5 / 2), 3, sp.Rational(7 / 2), 4,
            #                    sp.Rational(9 / 2), 5, sp.Rational(11 / 2), sp.Rational(-11 / 3),
            #                    sp.Rational(-9 / 5), sp.Rational(-7 / 3), sp.Rational(-5 / 3), sp.Rational(-3 / 4),
            #                    -sp.Rational(-1 / 3), sp.Rational(1 / 3), sp.Rational(3 / 4), sp.Rational(5 / 4),
            #                    sp.Rational(7 / 3),
            #                    sp.Rational(9 / 4), sp.Rational(11 / 3))) for _ in range(4)]
            a, b, c, d = random.choice(((-3, sp.Rational(1 / 2), 3, sp.Rational(11 / 2)),
                                        (-3, -sp.Rational(1 / 2), 3, -sp.Rational(11 / 2)),
                                        (-2, -sp.Rational(3 / 2), sp.Rational(11 / 2), -6),
                                        (-sp.Rational(3 / 2), -1, sp.Rational(9 / 2), -5),
                                        (-sp.Rational(3 / 2), 1, sp.Rational(9 / 2), 5),
                                        (-1, -sp.Rational(3 / 2), 5, -sp.Rational(9 / 2)),
                                        (-1, -1, sp.Rational(7 / 2), -sp.Rational(7 / 2)),
                                        (-1, 1, sp.Rational(7 / 2), sp.Rational(7 / 2)),
                                        (-1, sp.Rational(3 / 2), 5, sp.Rational(9 / 2)),
                                        (-sp.Rational(1 / 2), -3, sp.Rational(11 / 2), -3),
                                        (-sp.Rational(1 / 2), 3, sp.Rational(11 / 2), 3),
                                        (-sp.Rational(1 / 2), sp.Rational(3 / 4), sp.Rational(5 / 2),
                                         sp.Rational(9 / 4)),
                                        (sp.Rational(1 / 2), -3, -sp.Rational(11 / 2), -3),
                                        (sp.Rational(1 / 2), 3, -sp.Rational(11 / 2), 3),
                                        (sp.Rational(1 / 2), sp.Rational(3 / 4), -sp.Rational(5 / 2),
                                         sp.Rational(9 / 4)),
                                        (1, -sp.Rational(3 / 2), -5, -sp.Rational(9 / 2)),
                                        (1, -1, -sp.Rational(7 / 2), -sp.Rational(7 / 2)),
                                        (1, 1, -sp.Rational(7 / 2), sp.Rational(7 / 2)),
                                        (1, sp.Rational(3 / 2), -5, sp.Rational(9 / 2)),
                                        (sp.Rational(3 / 2), -2, -6, -sp.Rational(11 / 2)),
                                        (sp.Rational(3 / 2), -1, -sp.Rational(9 / 2), -5),
                                        (sp.Rational(3 / 2), 1, -sp.Rational(9 / 2), 5),
                                        (sp.Rational(3 / 2), 2, -6, sp.Rational(11 / 2)),
                                        (2, -sp.Rational(3 / 2), -sp.Rational(11 / 2), -6),
                                        (3, -sp.Rational(1 / 2), -3, -sp.Rational(11 / 2)),
                                        (3, sp.Rational(1 / 2), -3, sp.Rational(11 / 2)),
                                        (-sp.Rational(3 / 4), -sp.Rational(1 / 2), sp.Rational(9 / 4),
                                         -sp.Rational(5 / 2)),
                                        (-sp.Rational(3 / 4), sp.Rational(1 / 2), sp.Rational(9 / 4),
                                         sp.Rational(5 / 2))))
            F = a / x
            G = b * x ** 2 + c * x + d
            przeciecia = sp.solve(F - G, x)
            # print(przeciecia)
            if len(przeciecia) == 3 and all(sp.im(punkty) < 1e-10 for punkty in przeciecia):
                przeciecia = [sp.re(punkty) for punkty in przeciecia]
                przeciecia = sorted(przeciecia)
                # calka = (abs(sp.integrate(F - G, (x, min(przeciecia), przeciecia[1]))) +
                #          abs(sp.integrate(F - G, (x, przeciecia[1], max(przeciecia)))))
                # print(przeciecia, file=sys.stderr)
                if (all((60 * punkty).is_integer for punkty in przeciecia)
                        and (all(sp.sign(punkty) == 1 for punkty in przeciecia)
                             or all(sp.sign(punkty) == -1 for punkty in przeciecia))):
                    break

        calka = (abs(sp.integrate(F - G, (x, min(przeciecia), przeciecia[1]))) +
                 abs(sp.integrate(F - G, (x, przeciecia[1], max(przeciecia)))))
        if calka.is_finite:
            posredni1 = (min(przeciecia) + przeciecia[1]) / 2
            posredni2 = (przeciecia[1] + max(przeciecia)) / 2
            return (f'Obliczyć pole obszaru ograniczonego wykresami krzywych\n'
                    f'\t\\[\n'
                    f'\t\t f(x) = {sp.latex(F)} \\quad \\textnormal{{ oraz }} \\quad g(x) = {sp.latex(G)} \n'
                    f'\t\\]\n',
                    f'Pole obszaru to $\\int\\limits_{{{min(przeciecia)}}}^{{{przeciecia[1]}}}'
                    f'\\left({sp.latex(F - G) if F.subs(x, posredni1) > G.subs(x, posredni1) else sp.latex(G - F)}\\right)\\,dx + '
                    f'\\int\\limits_{{{przeciecia[1]}}}^{{{max(przeciecia)}}}'
                    f'\\left({sp.latex(F - G) if F.subs(x, posredni2) > G.subs(x, posredni2) else sp.latex(G - F)}\\right)\\,dx = '
                    f' {sp.latex(calka)}$'.replace('log', 'ln'))


if __name__ == "__main__":
    start = time.time()
    gotowce = True
    os.chdir('..')  # by wczytywać z gotowca - inaczej problem ze ścieżkami!
    polecenie, rozwiazanie = pole_obszaru(typ=5, gotowiec=gotowce)
    print(polecenie, '\n', rozwiazanie)
    print(f'czas generowania: {round(time.time() - start, 3)}s')
