import os  # by sprawdzić istnienie pliku gotowców
import pickle  # do ładowania gotowca
import random
import sys  # do czerwonych komunikatów: print('jakis tekst', file=sys.stderr )
import time

from pathlib import Path

sciezka = str(Path(__file__).parent)

import sympy as sp

x = sp.Symbol('x', complex=False)


def calka_nieoznaczona(typ: int = 1, gotowiec: bool = False):
    """
    Generuje zadanie (w formacie LaTeX wraz z rozwiązaniem) na całkę nieoznaczoną z "ładnymi" rozwiązaniami

    Args:
        typ (int, optional): Typ problemu. Wartości:

            1 - (a * x ** 2 + b * x + c) * g dla g=e^(d x) lub sin(d x) lub cos(d x) lub ln(d x) - 961/1000 różnych,
            2 - (d * x + e) / (a * x ** 2 + b * x + c) - 881/1000 różnych,
            3 - (a * x + b) * sp.sqrt(c * x + d) - 707/1000 różnych.
            4 - a / (c*x+d)**n - 882/1000 różnych

    Returns:
        tuple: Zawiera polecenie oraz jego odpowiednie rozwiązanie.
    """
    if gotowiec is True:
        if typ == 3:  # 1462/10000 różnych gotowych
            if os.path.isfile(sciezka + '//gotowe//calka_nieoznaczona_typ_3.pickle'):  # 1000 różnych gotowych
                gotowe = pickle.load(open(sciezka + '//gotowe//calka_nieoznaczona_typ_3.pickle', 'rb'))
                return gotowe[random.randint(0, len(gotowe)) - 1]
            else:
                print('Brak gotowca do tego typu', file=sys.stderr)
    # to nie musi być w else, bo wcześniejsze warunku w przypadku sukcesu konczą funkcje returnem
    if typ == 1:  # 961/1000 różnych
        a, b, c = [random.choice((-3, -2, -1, 0, 1, 2, 3, 4, 5)) for _ in range(3)]
        d = random.choice((1, 2, 3, 4))
        g = random.choice((sp.E ** (d * x), sp.sin(d * x), sp.cos(d * x), sp.ln(d * x)))
        f = (a * x ** 2 + b * x + c) * g
        calka = sp.integrate(f, x)
        # print(calka)
        calka = sp.collect(calka,
                           (sp.sin(d * x),
                            sp.cos(d * x)))  # tu czasem źle grupuje sin(x) - to jest jakiś bug - sympy 1.12

        return (f'Obliczyć całkę\n'
                f'\t\\[\n'
                f'\t\t\\int {sp.latex(f)} \\, dx \n'.replace('log', 'ln') +
                f'\t\\]\n',
                f'$\\int {sp.latex(f)}\\,dx = {sp.latex(calka)} + C$'.replace('log', 'ln'))
    if typ == 2:  # 881/1000 różnych
        tylko_tan = False
        tylko_log = random.choice([True, False, False])
        if not tylko_log:
            tylko_tan = random.choice([True, False, False])
        # if tylko_log: print('tylko log')
        # if tylko_tan: print('tylko tan')
        while True:
            if tylko_log:
                b, c, e = [random.choice((-3, -2, -1, 0, 1, 2, 3, 4, 5)) for _ in range(3)]
                a, d = [random.choice((-2, -1, 1, 2)) for _ in range(2)]
                if (sp.simplify((d * x + e) / (2 * a * x + b))).is_integer and b ** 2 - 4 * a * c < 0:
                    mnoznik = random.choice((-2, -1, 2, 3))
                    d, e = d * mnoznik, e * mnoznik
                    break
            elif tylko_tan:
                b, c = [random.choice((-3, -2, -1, 0, 1, 2, 3, 4, 5)) for _ in range(2)]
                a, e = [random.choice((-2, -1, 1, 2)) for _ in range(2)]
                d = 0
                if b ** 2 - 4 * a * c < 0:
                    break
            else:
                print
                b, c, e = [random.choice((-3, -2, -1, 0, 1, 2, 3, 4, 5)) for _ in range(3)]
                a, d = [random.choice((-2, -1, 1, 2)) for _ in range(2)]
                if b ** 2 - 4 * a * c < 0:
                    break
        f = (d * x + e) / (a * x ** 2 + b * x + c)
        calka = sp.integrate(f, x)

        return (f'Obliczyć całkę\n'
                f'\t\\[\n'
                f'\t\t\\int {sp.latex(f)} \\, dx \n'
                f'\t\\]\n',
                f'$\\int {sp.latex(f)}\\,dx = {sp.latex(calka)} + C$'.replace('log', 'ln'))
    if typ == 3:  # 707/1000 różnych
        while True:
            a, b, c, d = [random.choice((-3, -2, -1, 1, 2, 3, 4, 5)) for _ in range(4)]
            # a, b, c, d, = 2, 2, 5, 5  # to daje wyniki z "Piecewise"
            f = (a * x + b) * sp.sqrt(c * x + d)
            calka = sp.integrate(f, x)
            # print(calka)
            tmp = str(calka)  # tu może jakieś założenie co do zmiennych, by wymusić wyniki rzeczywiste
            if 'I' not in tmp and 'P' not in tmp:  # by wykluczyć zespolone wyniki i cząstkowe z "Piecewise"
                break

        return (f'Obliczyć całkę\n'
                f'\t\\[\n'
                f'\t\t\\int {sp.latex(f)} \\, dx \n'
                f'\t\\]\n',
                f'$\\int {sp.latex(f)}\\,dx = {sp.latex(sp.factor(calka))} + C$')
    if typ == 4:
        a, c, d = [random.choice((-3, -2, -1, 1, 2, 3, 4, 5)) for _ in range(3)]
        n = random.choice((1, 2, 3, 4, 5, 6, 7))
        # a, b, c, d, = 2, 2, 5, 5  # to daje wyniki z "Piecewise"
        f = a / ((c * x + d) ** n)
        calka = sp.integrate(f, x)
        return (f'Obliczyć całkę\n'
                f'\t\\[\n'
                f'\t\t\\int {sp.latex(f)} \\, dx \n'
                f'\t\\]\n',
                f'$\\int {sp.latex(f)}\\,dx = {sp.latex(sp.factor(calka))} + C$')


def calka_wymierna(wlasciwy: bool = False):
    """
    Generuje zadanie (w formacie LaTeX wraz z rozwiązaniem) na całkę wymierną z "ładnymi" rozwiązaniami
    Funkcja całkowana to wielomian stopnia co najwyżej dwa plus ułamek prosty pierwszego rodzaju (jeden lub dwa)
    i ułamek prosty drugiego rodzauj (zero lub jeden)

    Returns:
        tuple: Zawiera polecenie oraz jego odpowiednie rozwiązanie.
    """
    while True:
        b, c = [random.randint(-4, 4) for i in range(2)]
        if b ** 2 - 4 * c < 0:
            break
    f = (-(int(wlasciwy) - 1) * (random.randint(-2, 2) * x ** 2 + random.randint(-2, 2) * x + random.randint(-2, 2))
         + (-1) ** random.randint(0, 1) * random.randint(1, 3) / (
                 x + (-1) ** random.randint(0, 1) * random.randint(1, 4)) ** random.randint(1, 2)
         + random.randint(0, 1) * random.randint(-2, 3) / (x + random.randint(-4, 4)) ** random.randint(1, 2)
         + random.randint(0, 1) * (random.randint(-2, 2) * x + random.randint(-2, 2)) / (x ** 2 + b * x + c))
    wynik = sp.latex(sp.integrate(f, x)).replace('log', 'ln').replace('operatorname{atan}', 'arctan')
    return (f'Obliczyć całkę\n'
            f'\t\\[\n'
            f'\t\t\\int {sp.latex(sp.cancel(f))} \\, dx \n'
            f'\t\\]\n',
            f'$\\int \\left({sp.latex(f)}\\right)\\,dx = {wynik} + C$')


if __name__ == "__main__":
    start_time = time.time()
    gotowce = True
    os.chdir('..')  # by wczytywać z gotowca - inaczej problem ze ścieżkami!
    # for _ in range(1):
    #     polecenie, rozwiazanie = calka_wymierna(wlasciwy=True)
    # polecenie, rozwiazanie = calka_(typ=3, gotowiec=gotowce)

    for _ in range(10):
        polecenie, rozwiazanie = calka_nieoznaczona(typ=3, gotowiec=gotowce)
        print(polecenie, '\n', rozwiazanie)
    # for _ in range(3):
    #     polecenie, rozwiazanie = calka_nieoznaczona(typ=3)
    print(polecenie, '\n', rozwiazanie)
    print("--- %s seconds ---" % (time.time() - start_time))
