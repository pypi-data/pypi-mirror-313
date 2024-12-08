import random

import sympy as sp
from sympy.abc import n, x


def granica_ciagu(typ: int = 0):
    if typ == 0:
        liczby = (-3, -2, -1, 0, 0, 0, 1, 2, 3, 4, 5)
        while True:
            a, b, c, d, e, f, g, h, i, j = [random.choice(liczby) for _ in range(10)]
            if (a != d or b != e or c != f) and (a != 0 or b != 0 or c != 0 or d != 0) and (
                    e != 0 or f != 0 or j != 0):
                break
        granica = sp.limit(
            (a * n ** 3 + b * n ** 2 + c * n + d + i * n ** 5) / (e * n ** 3 + e * n ** 2 + f * n + g + j * n ** 5),
            n, sp.oo)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{n \\rightarrow \\infty}}'
                f' {sp.latex((a * n ** 3 + b * n ** 2 + c * n + d + i * n ** 5) / (e * n ** 3 + e * n ** 2 + f * n + g + j * n ** 5))} \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')

    if typ == 1:
        liczby = (-3, -2, -1, 1, 2, 3, 4, 5)
        gora = random.choice((0, 1))
        while True:
            a, b, c, d, e = [random.choice(liczby) for _ in range(5)]
            if gora == 1:
                granica = sp.limit((sp.sqrt(a * n ** 2 + b * n + c) / (d * n + e)), n, sp.oo)
                if granica.is_real:
                    return (f'Obliczyć granicę\n'
                            f'\t\\[\n'
                            f'\t\t\\lim\\limits_{{n \\rightarrow \\infty}} {sp.latex((sp.sqrt(a * n ** 2 + b * n + c) / (d * n + e)))} \n'
                            f'\t\\]\n',
                            f'${sp.latex(granica)}$')
            else:
                granica = sp.limit((d * n + e) / (sp.sqrt(a * n ** 2 + b * n + c)), n, sp.oo)
                if granica.is_real:
                    return (f'Obliczyć granicę\n'
                            f'\t\\[\n'
                            f'\t\t\\lim\\limits_{{n \\rightarrow \\infty}} {sp.latex((d * n + e) / (sp.sqrt(a * n ** 2 + b * n + c)))} \n'
                            f'\t\\]\n',
                            f'${sp.latex(granica)}$')

    if typ == 2:
        liczby = (-3, -2, -1, 1, 2, 3, 4)
        while True:
            a, b, c, d = [random.choice(liczby) for _ in range(4)]
            e, f, g, h = [random.choice((2, 3, 4, 5)) for _ in range(4)]
            if a != b and c != d and e != f and g != h:
                break
        granica = sp.limit((a * e ** n + b * f ** n) / (d * g ** n + e * h ** n), n, sp.oo)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{n \\rightarrow \\infty}} {sp.latex((a * e ** n + b * f ** n) / (d * g ** n + e * h ** n))} \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')

    if typ == 3:
        liczby = (-3, -2, -1, 0, 1, 2, 3, 4, 5)
        while True:
            a, b, c, d, e, f = [random.choice(liczby) for _ in range(6)]
            if a == b > 0 and (c != d or e != f):
                break
        granica = sp.limit(sp.sqrt(a * n ** 2 + c * n + e) - sp.sqrt(b * n ** 2 + d * n + f), n, sp.oo)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{n \\rightarrow \\infty}} \\left({sp.latex(sp.sqrt(a * n ** 2 + c * n + e) - sp.sqrt(b * n ** 2 + d * n + f))} \\right) \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')
    if typ == 4:
        liczby = (-3, -2, -1, 1, 2, 3, 4, 5)
        while True:
            a, b, d, e, f = [random.choice(liczby) for _ in range(5)]
            c = a
            if b != d and e != 0:
                break
        granica = sp.limit(((a * n + b) / (c * n + d)) ** (e * n + f), n, sp.oo)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{n \\rightarrow \\infty}} {sp.latex(((a * n + b) / (c * n + d)) ** (e * n + f))} \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')
def granica_funkcji(typ: int = 0):
    from sympy.abc import x
    if typ == 0:
        a, b, c = [random.choice((-2, -1, 1, 2, 3, 4)) for _ in range(3)]
        a = sp.Abs(a)
        granica = sp.limit((a - sp.sqrt(a ** 2 - b * x)) / (c * x), x, 0)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{x \\rightarrow 0}}'
                f' {sp.latex((a - sp.sqrt(a ** 2 - b * x)) / (c * x))} \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')
    if typ == 1:
        funkcja = random.choice([-1, 1]) * (sp.E ** x - sp.E ** (-x)) / random.choice([x, sp.sin(x)])
        granica = sp.limit(funkcja, x, 0)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{x \\rightarrow 0}}'
                f' {sp.latex(funkcja)} \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')
    if typ == 2:
        funkcja = sp.ln(x) / sp.sqrt(x ** 2 - 1)
        granica = sp.limit(funkcja, x, 1)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                '\t\t\\lim\\limits_{{x \\rightarrow 1^{+}}}'
                f' {sp.latex(funkcja).replace("log", "ln")} \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')
    if typ == 3:
        funkcja = random.choice([-1, 1]) * (1 / x - 1 / sp.sin(x))
        granica = sp.limit(funkcja, x, 0)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                '\t\t\\lim\\limits_{{x \\rightarrow 0}}'
                f'\\left( {sp.latex(funkcja)} \\right) \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')
    if typ == 4:
        funkcja = random.choice([-1, 1]) * (1 / x ** 2 - 1 / (x * sp.sin(x)))
        granica = sp.limit(funkcja, x, 0)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                '\t\t\\lim\\limits_{{x \\rightarrow 0}}'
                f'\\left( {sp.latex(funkcja)} \\right) \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')
    if typ == 5:
        funkcja = random.choice([-1, 1]) * (1 / x ** 2 - 1 / (sp.sin(x)) ** 2)
        granica = sp.limit(funkcja, x, 0)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                '\t\t\\lim\\limits_{{x \\rightarrow 0}}'
                f'\\left( {sp.latex(funkcja)} \\right)\n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')
    if typ == 6:
        a, b, c, d = [random.choice([1, 2, 3, -1, -2, -3]) for _ in range(4)]
        funkcja = (((x - c) * (x - b)).expand()) / (((x - c) * (x - d)).expand())
        granica = sp.limit(funkcja, x, c)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{x \\rightarrow {c}}}'
                f' {sp.latex(funkcja)} \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')
    if typ == 7:
        funkcja = (1 - x) * sp.ln(1 - x)
        granica = sp.limit(funkcja, x, 1, '-')
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{x \\rightarrow 1^-}}'
                f'\\left( {sp.latex(funkcja).replace("log", "ln")} \\right) \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')
    if typ == 8:
        funkcja = (x) ** (1 / (1 - x))
        granica = sp.limit(funkcja, x, 1)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{x \\rightarrow 1}}'
                f' {sp.latex(funkcja)} \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')
    if typ == 9:
        funkcja = (x) ** (1 / (x))
        granica = sp.limit(funkcja, x, sp.oo)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{x \\rightarrow \\infty}}'
                f'\\left( {sp.latex(funkcja)} \\right)\n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')
    if typ == 10:
        funkcja = (x + sp.exp(random.choice([-3, -2, -1, 1, 2, 3, 4, 5]) * x)) ** (1 / (x))
        granica = sp.limit(funkcja, x, 0)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{x \\rightarrow 0}}'
                f'\\left( {sp.latex(funkcja)} \\right) \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')
    if typ == 11:
        funkcja = (x * sp.ln(x)) / (x - 1)
        granica = sp.limit(funkcja, x, 1)
        return (f'Obliczyć granicę\n'
                f'\t\\[\n'
                f'\t\t\\lim\\limits_{{x \\rightarrow 1}}'
                f' {sp.latex(funkcja).replace("log", "ln")} \n'
                f'\t\\]\n',
                f'${sp.latex(granica)}$')


def asymptoty(typ: int = 1):
    x = sp.Symbol('x', real=True)
    if typ == 1:
        while True:
            a, b, c, d, e = [random.choice([-2, -1, 0, 1, 2, 3]) for _ in range(5)]
            if (a ** 2 + b ** 2 != 0
                    and d ** 2 != 0
                    and sp.solve(d * x + e, x)[0] not in sp.solve(a * x ** 2 + b * x + c, x)):
                break
        funkcja = (a * x ** 2 + b * x + c) / (d * x + e)
        a_2 = sp.limit(funkcja / x, x, sp.oo)
        b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo)
        x_0 = sp.solve(d * x + e, x)[0]
        return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
                f'\t\\[\n'
                f'\t\tf(x)= {sp.latex(funkcja)}.\n'
                f'\t\\]\n',
                f'$D_f\\colon \\mathbb{{R}}\\setminus \\left\\{{{sp.latex(x_0)}\\right\\}}.$' + '\\\\' +
                f'{"Asymptota pionowa dwustronna w $x_0=" + str(sp.latex(x_0)) + ".$ "}' + '\\\\' +
                f'{("Asymptota ukośna w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
                f'{("Asymptota pozioma w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}')
    if typ == 2:
        while True:
            a, b, c, d, e = [random.choice([-2, -1, 0, 1, 2, 3]) for _ in range(5)]
            if (a != 0
                    and d ** 2 != 0
                    and sp.solve(d * x + e, x)[0] in sp.solve(a * x ** 2 + b * x + c, x)):
                break
        funkcja = (a * x ** 2 + b * x + c) / (d * x + e)
        a_2 = sp.limit(funkcja / x, x, sp.oo)
        b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo)
        x_0 = sp.solve(d * x + e, x)[0]
        return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
                f'\t\\[\n'
                f'\t\tf(x)= {sp.latex(funkcja)}.\n'
                f'\t\\]\n',
                f'$D_f\\colon \\mathbb{{R}}\\setminus \\left\\{{{sp.latex(x_0)}\\right\\}}.$' + '\\\\' +
                f'{("Asymptota ukośna w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
                f'{("Asymptota pozioma w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}')
    if typ == 3:
        while True:
            a, b, c, d, e, f = [random.choice([-2, -1, 0, 1, 2, 3]) for _ in range(6)]
            x_licznik = sp.solve(a * x ** 2 + b * x + c)
            x_mianownik = sp.solve(d * x ** 2 + e * x + f)
            # print(x_licznik, x_mianownik)
            # print(type(x_mianownik[0]), type(x_mianownik[1]))
            if (a != 0 and d ** 2 != 0
                    and all(int(i * 6) == i * 6 for i in x_mianownik)
                    and set(x_mianownik).isdisjoint(set(x_licznik))):
                break
        funkcja = (a * x ** 2 + b * x + c) / (d * x ** 2 + e * x + f)
        a_2 = sp.limit(funkcja / x, x, sp.oo)
        b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo)
        if len(x_mianownik) == 0:
            return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
                    f'\t\\[\n'
                    f'\t\tf(x)= {sp.latex(funkcja)}.\n'
                    f'\t\\]\n',
                    f'$D_f\\colon \\mathbb{{R}}.$' + '\\\\' +
                    f'{("Asymptota ukośna w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
                    f'{("Asymptota pozioma w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}')
        if len(x_mianownik) == 1:
            return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
                    f'\t\\[\n'
                    f'\t\tf(x)= {sp.latex(funkcja)}.\n'
                    f'\t\\]\n',
                    f'$D_f\\colon \\mathbb{{R}}\\setminus \\left\\{{{sp.latex(x_mianownik[0])}\\right\\}}.$' + '\\\\' +
                    f'{"Asymptota pionowa dwustronna w $x_0=" + str(sp.latex(x_mianownik[0])) + ".$ "}' + '\\\\' +
                    f'{("Asymptota ukośna w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
                    f'{("Asymptota pozioma w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}')
        if len(x_mianownik) == 2:
            return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
                    f'\t\\[\n'
                    f'\t\tf(x)= {sp.latex(funkcja)}.\n'
                    f'\t\\]\n',
                    f'$D_f\\colon \\mathbb{{R}}\\setminus {sp.latex(set(x_mianownik))}.$' + '\\\\' +
                    f'{"Asymptota pionowa dwustronna w $x_1=" + str(sp.latex(x_mianownik[0])) + ".$ "}' + '\\\\' +
                    f'{"Asymptota pionowa dwustronna w $x_2=" + str(sp.latex(x_mianownik[1])) + ".$ "}' + '\\\\' +
                    f'{("Asymptota ukośna w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
                    f'{("Asymptota pozioma w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}')
    if typ == 4:
        while True:
            a, b, c, d, e, f = [random.choice([-2, -1, 0, 1, 2, 3]) for _ in range(6)]
            x_mianownik = sp.solve(d * x ** 2 + e * x + f)
            x_licznik = sp.solve(a * x ** 2 + b * x + c)

            if (a != 0 and d ** 2 != 0
                    and all(int(i * 6) == i * 6 for i in x_mianownik)
                    and len(x_mianownik) == 2
                    and len(x_licznik) == 2
                    and e != 0
                    and f != 0
                    and len(set(x_mianownik).union(set(x_licznik))) == len(x_mianownik) + len(x_licznik) - 1):
                break
        funkcja = (a * x ** 2 + b * x + c) / (d * x ** 2 + e * x + f)
        a_2 = sp.limit(funkcja / x, x, sp.oo)
        b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo)
        return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
                f'\t\\[\n'
                f'\t\tf(x)= {sp.latex(funkcja)}.\n'
                f'\t\\]\n',
                f'$D_f\\colon \\mathbb{{R}}\\setminus {sp.latex(set(x_mianownik))}.$' + '\\\\' +
                f'{("Asymptota pionowa dwustronna w $x_1=" + str(sp.latex(x_mianownik[0])) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, x_mianownik[0]).is_real else ""}' +
                f'{("Asymptota pionowa dwustronna w $x_2=" + str(sp.latex(x_mianownik[1])) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, x_mianownik[1]).is_real else ""}' +
                f'{("Asymptota ukośna w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
                f'{("Asymptota pozioma w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}')
    if typ == 5:
        a, b = [random.choice([-2, -1, 1, 2, 3]) for _ in range(2)]
        c = random.choice([-2, -1, 0, 1, 2, 3])
        funkcja = a * sp.exp(random.choice([-1, 1]) * x) + b * x + c
        a_1 = sp.limit(funkcja / x, x, -sp.oo)
        b_1 = sp.limit(sp.factor(funkcja - a_1 * x), x, -sp.oo) if a_1.is_real else None
        a_2 = sp.limit(funkcja / x, x, sp.oo)
        b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo) if a_2.is_real else None
        return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
                f'\t\\[\n'
                f'\t\tf(x)= {sp.latex(funkcja)}.\n'
                f'\t\\]\n',
                f'$D_f\\colon \\mathbb{{R}}.$' + '\\\\' +
                f'{("Asymptota ukośna w minus nieskończoności o równaniu $y=" + str(sp.latex(a_1 * x + b_1)) + ".$ ") if a_1.is_real and b_1.is_real and a_1 != 0 else ""}' +
                f'{("Asymptota pozioma w minus nieskończoności o równaniu $y=" + str(sp.latex(a_1 * x + b_1)) + ".$ ") if a_1.is_real and b_1.is_real and a_1 == 0 else ""}' +
                f'{("Asymptota ukośna w plus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
                f'{("Asymptota pozioma w plus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}'
                )
    if typ == 6:
        a, e = [random.choice([-1, 1, 2]) for _ in range(2)]
        b, c, d, f = [random.choice([-1, 0, 0, 0, 1, 2]) for _ in range(4)]
        funkcja = (a * sp.exp(random.choice([-1, 1]) * x) + b * x ** 2 + c * x + d) / (e * x + f)
        a_1 = sp.limit(funkcja / x, x, -sp.oo)
        b_1 = sp.limit(sp.factor(funkcja - a_1 * x), x, -sp.oo) if a_1.is_real else None
        a_2 = sp.limit(funkcja / x, x, sp.oo)
        b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo) if a_2.is_real else None
        x_0 = sp.solve(e * x + f)[0]
        # print(a_1, b_1, a_2, b_2)
        return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
                f'\t\\[\n'
                f'\t\tf(x)= {sp.latex(funkcja)}.\n'
                f'\t\\]\n',
                f'$D_f\\colon \\mathbb{{R}}\\setminus {sp.latex(set(sp.solve(e * x + f)))}.$' + '\\\\' +
                f'{("Asymptota pionowa dwustronna w $x_0=" + str(sp.latex(x_0)) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, x_0).is_real else ""}' +
                f'{("Asymptota ukośna w minus nieskończoności o równaniu $y=" + str(sp.latex(a_1 * x + b_1)) + ".$ ") if a_1.is_real and b_1.is_real and a_1 != 0 else ""}' +
                f'{("Asymptota pozioma w minus nieskończoności o równaniu $y=" + str(sp.latex(a_1 * x + b_1)) + ".$ ") if a_1.is_real and b_1.is_real and a_1 == 0 else ""}' +
                f'{("Asymptota ukośna w plus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
                f'{("Asymptota pozioma w plus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}'
                )
    if typ == 7:
        a, c, d = [random.choice([-1, 1, 2]) for _ in range(3)]
        b = random.choice([0, 1, -1])
        funkcja = a * x + b + c * sp.atan(d * x)
        a_1 = sp.limit(funkcja / x, x, -sp.oo)
        b_1 = sp.limit(sp.factor(funkcja - a_1 * x), x, -sp.oo) if a_1.is_real else None
        a_2 = sp.limit(funkcja / x, x, sp.oo)
        b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo) if a_2.is_real else None
        return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
                f'\t\\[\n'
                f'\t\tf(x)= {sp.latex(funkcja)}.\n'
                f'\t\\]\n',
                f'$D_f\\colon \\mathbb{{R}}.$' + '\\\\' +
                f'{("Asymptota ukośna w minus nieskończoności o równaniu $y=" + str(sp.latex(a_1 * x + b_1)) + ".$ " + chr(92) + chr(92)) if a_1.is_real and b_1.is_real and a_1 != 0 else ""}' +
                f'{("Asymptota pozioma w minus nieskończoności o równaniu $y=" + str(sp.latex(a_1 * x + b_1)) + ".$ " + chr(92) + chr(92)) if a_1.is_real and b_1.is_real and a_1 == 0 else ""}' +
                f'{("Asymptota ukośna w plus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
                f'{("Asymptota pozioma w plus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}'
                )
    if typ == 8:
        a = random.choice([-1, 1, 2])
        b = random.choice([0, 1, -1])
        funkcja = (a * x + b)*sp.exp(random.choice([-1,1])*1/x)
        a_1 = sp.limit(funkcja / x, x, -sp.oo)
        b_1 = sp.limit(sp.factor(funkcja - a_1 * x), x, -sp.oo) if a_1.is_real else None
        a_2 = sp.limit(funkcja / x, x, sp.oo)
        b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo) if a_2.is_real else None
        return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
                f'\t\\[\n'
                f'\t\tf(x)= {sp.latex(funkcja)}.\n'
                f'\t\\]\n',
                f'$D_f\\colon \\mathbb{{R}} \\setminus {sp.latex({0})}.$' + '\\\\' +
                f'{("Asymptota pionowa lewostronna w $x_0=" + str(sp.latex(0)) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, 0,"-").is_real else ""}' +
                f'{("Asymptota pionowa prawostronna w $x_0=" + str(sp.latex(0)) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, 0).is_real else ""}' +
                f'{("Asymptota ukośna w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
                f'{("Asymptota pozioma w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}'
                )
    if typ == 9:
        a = random.choice([-1, 1, 2])
        b = random.choice([0, 1, -1])
        funkcja = (a * x + b) + random.choice([-1,1]) * sp.exp(random.choice([-1,1])*1/x)
        a_1 = sp.limit(funkcja / x, x, -sp.oo)
        b_1 = sp.limit(sp.factor(funkcja - a_1 * x), x, -sp.oo) if a_1.is_real else None
        a_2 = sp.limit(funkcja / x, x, sp.oo)
        b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo) if a_2.is_real else None
        return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
                f'\t\\[\n'
                f'\t\tf(x)= {sp.latex(funkcja)}.\n'
                f'\t\\]\n',
                f'$D_f\\colon \\mathbb{{R}} \\setminus {sp.latex({0})}.$' + '\\\\' +
                f'{("Asymptota pionowa lewostronna w $x_0=" + str(sp.latex(0)) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, 0,"-").is_real else ""}' +
                f'{("Asymptota pionowa prawostronna w $x_0=" + str(sp.latex(0)) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, 0).is_real else ""}' +
                f'{("Asymptota ukośna w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
                f'{("Asymptota pozioma w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}'
                )
    if typ == 10:
        a = random.choice([-1, 1, 2])
        b = random.choice([0, 1, -1])
        funkcja = (a * x + b) + random.choice([-1,1]) * sp.ln(x)/x
        a_2 = sp.limit(funkcja / x, x, sp.oo)
        b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo) if a_2.is_real else None
        return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
                f'\t\\[\n'
                f'\t\tf(x)= {sp.latex(funkcja)}.\n'.replace('log','ln') +
                f'\t\\]\n',
                f'$D_f\\colon \\left(0, \\infty\\right).$' + '\\\\' +
                f'{("Asymptota pionowa prawostronna w $x_0=" + str(sp.latex(0)) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, 0).is_real else ""}' +
                f'{("Asymptota ukośna w plus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
                f'{("Asymptota pozioma w plus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}'
                )


if __name__ == "__main__":
    polecenie, rozwiazanie = granica_funkcji(typ=0)
    print(polecenie, '\n', rozwiazanie)

    res2 = sp.limit(1 / x ** 2 - 1 / (x * sp.sin(x)), x, 0)

    print(res2)

    for i in range(1):
        granica = sp.limit(((sp.E ** (-2 / x ** 2)) ** (sp.sin(x ** 2))), x, 0)
        print(sp.latex(granica))
