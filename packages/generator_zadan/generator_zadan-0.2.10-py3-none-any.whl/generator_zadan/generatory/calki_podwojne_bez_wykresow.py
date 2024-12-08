import random
import time

import sympy as sp
from sympy.abc import x, y


# from sympy.integrals.intpoly import polytope_integrate, Polygon # do testów - coś źle liczy dla
# A = [-3, -1]
# B = [-1, 0]
# C = [-1, 3]
# z = 3*x-3 * y

def calka_podwojna_po_trojkacie():
    a, b = [random.choice(
        [-3, -2, -1, 0, sp.Rational(1, 2), 1, sp.Rational(3, 2), 2, 3]) for _ in
        range(2)]
    c = random.choice([-1, 0, 1, 2])
    while True:
        A = [random.choice([-3, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4]) for _ in range(2)]
        B = [random.choice([-3, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4]) for _ in range(2)]
        C = [random.choice([-3, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4]) for _ in range(2)]
        A, B, C = sorted([A, B, C])
        if (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0]):  # pole trójkąta != 0
            break
    A = [0, -3]
    B = [0, 1]
    C = [-1, -2]
    A, B, C = sorted([A, B, C])
    # a, b, c = sp.Rational(1,2), -2, 1
    # A[0], A[1] = A[1], A[0]
    # B[0], B[1] = B[1], B[0]
    # C[0], C[1] = C[1], C[0]
    # a,b = b,a
    z = a * x + b * y + c
    # print(A, B, C, a, b, c)
    # pol_int = polytope_integrate(Polygon(A, B, C), z)
    # print(pol_int)
    zadanie = f"\\iint\\limits_D\\left({sp.latex(z)}\\right)dx\\,dy"
    if A[0] == B[0]:
        print("pierwszy")
        f = sp.Rational(C[1] - A[1]) / (C[0] - A[0]) * (x - A[0]) + A[1]
        g = sp.Rational(C[1] - B[1]) / (C[0] - B[0]) * (x - B[0]) + B[1]
        if A[1] > B[1]:
            # print("f jest wyżej")
            wynik_x = sp.integrate(z, (y, g, f), (x, A[0], C[0]))
            calka_x = f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(g)}}}^{{{sp.latex(f)}}}\\left({sp.latex(z)}\\right)dy\\right)dx"
        else:
            # print("g jest wyżej")
            wynik_x = sp.integrate(z, (y, f, g), (x, A[0], C[0]))
            calka_x = f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(f)}}}^{{{sp.latex(g)}}}\\left({sp.latex(z)}\\right)dy\\right)dx"
        # if wynik_x == pol_int:
        #     print("SUKCES")
        # return (
        #     f'Obliczyć ${zadanie}$ gdzie $D$ - trójkąt $ABC$  dla $A=({A[0]},{A[1]}), B=({B[0]},{B[1]}), C=({C[0]},{C[1]})$',
        #     '$' + calka_x + ' = ' + sp.latex(wynik_x) + '$')
    elif B[0] == C[0]:
        print("drugi")
        f = sp.Rational(C[1] - A[1]) / (C[0] - A[0]) * (x - A[0]) + A[1]
        g = sp.Rational(A[1] - B[1]) / (A[0] - B[0]) * (x - B[0]) + B[1]
        if B[1] > C[1]:
            print("B jest wyżej")
            wynik_x = sp.integrate(z, (y, f, g), (x, A[0], C[0]))
            calka_x = (f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(f)}}}^{{{sp.latex(g)}}}\\left({sp.latex(z)}\\right)dy\\right)dx"+
                       f"=\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left( {sp.latex(sp.integrate(z,(y,f,g)))} \\right)dx")
        else:
            print("C jest wyżej")
            wynik_x = sp.integrate(z, (y, g, f), (x, A[0], C[0]))
            calka_x = (f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(g)}}}^{{{sp.latex(f)}}}\\left({sp.latex(z)}\\right)dy\\right)dx"+
                       f"=\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left( {sp.latex(sp.integrate(z,(y,g,f)).expand())} \\right)dx")
        # if wynik_x == pol_int:
        #     print("SUKCES")
        # return (
        #     f'Obliczyć ${zadanie}$ gdzie $D$ - trójkąt $ABC$ dla $A=({A[0]},{A[1]}), B=({B[0]},{B[1]}), C=({C[0]},{C[1]})$',
        #     '$' + calka_x + ' = ' + sp.latex(wynik_x) + '$')
    else:
        print("trzeci")
        f = sp.Rational(C[1] - A[1]) / (C[0] - A[0]) * (x - A[0]) + A[1]
        g = sp.Rational(C[1] - B[1]) / (C[0] - B[0]) * (x - B[0]) + B[1]
        h = sp.Rational(A[1] - B[1]) / (A[0] - B[0]) * (x - B[0]) + B[1]
        # print("f = ", f)
        # print("g = ", g)
        # print("h = ", h)
        if A[1] + (B[0] - A[0]) / (C[0] - A[0]) * (C[1] - A[1]) > B[1]:
            # print("środkowy poniżej")
            wynik_x = sp.integrate(z, (y, h, f), (x, A[0], B[0])) + sp.integrate(z, (y, g, f), (x, B[0], C[0]))
            calka_x = (
                    f"\\int\\limits_{{{A[0]}}}^{{{B[0]}}}\\left(\\int\\limits_{{{sp.latex(h)}}}^{{{sp.latex(f)}}}\\left({sp.latex(z)}\\right)dy\\right)dx + " +
                    f"\\int\\limits_{{{B[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(g)}}}^{{{sp.latex(f)}}}\\left({sp.latex(z)}\\right)dy\\right)dx")
        else:
            # print("środkowy powyżej")
            wynik_x = sp.integrate(z, (y, f, h), (x, A[0], B[0])) + sp.integrate(z, (y, f, g), (x, B[0], C[0]))
            calka_x = (
                    f"\\int\\limits_{{{A[0]}}}^{{{B[0]}}}\\left(\\int\\limits_{{{sp.latex(f)}}}^{{{sp.latex(h)}}}\\left({sp.latex(z)}\\right)dy\\right)dx + " +
                    f"\\int\\limits_{{{B[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(f)}}}^{{{sp.latex(g)}}}\\left({sp.latex(z)}\\right)dy\\right)dx")
        # if wynik_x == pol_int:
        #     print("SUKCES")
    ''' zamieniam x i y miejscami - raczej można to zrobić lepiej '''
    A[0], A[1] = A[1], A[0]
    B[0], B[1] = B[1], B[0]
    C[0], C[1] = C[1], C[0]
    A, B, C = sorted([A, B, C])
    z_y = b * x + a * y + c
    # print(A, B, C)
    # pol_int = polytope_integrate(Polygon(A, B, C), z)
    # print(pol_int)
    # zadanie = f"\\iint\\limits_D\\left({sp.latex(z)}\\right)dx\\,dy"
    if A[0] == B[0]:
        # print("czwarty")
        f = sp.Rational(C[1] - A[1]) / (C[0] - A[0]) * (x - A[0]) + A[1]
        g = sp.Rational(C[1] - B[1]) / (C[0] - B[0]) * (x - B[0]) + B[1]
        if A[1] > B[1]:
            # print("f jest wyżej")
            wynik_y = sp.integrate(z_y, (y, g, f), (x, A[0], C[0]))
            calka_y = f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(g).replace('x','y')}}}^{{{sp.latex(f).replace('x','y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy"
        else:
            # print("g jest wyżej")
            wynik_y = sp.integrate(z_y, (y, f, g), (x, A[0], C[0]))
            calka_y = f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(f).replace('x','y')}}}^{{{sp.latex(g).replace('x','y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy"
        # if wynik_y == pol_int:
        #     print("SUKCES")
        # return (
        #     f'Obliczyć ${zadanie}$ gdzie $D$ - trójkąt $ABC$  dla $A=({A[0]},{A[1]}), B=({B[0]},{B[1]}), C=({C[0]},{C[1]})$',
        #     '$' + calka_y + ' = ' + sp.latex(wynik_y) + '$')
    elif B[0] == C[0]:
        # print("piąty")
        f = sp.Rational(C[1] - A[1]) / (C[0] - A[0]) * (x - A[0]) + A[1]
        g = sp.Rational(A[1] - B[1]) / (A[0] - B[0]) * (x - B[0]) + B[1]
        if B[1] > C[1]:
            # print("B jest wyżej")
            wynik_y = sp.integrate(z_y, (y, f, g), (x, A[0], C[0]))
            calka_y = f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(f).replace('x','y')}}}^{{{sp.latex(g).replace('x','y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy"
        else:
            # print("C jest wyżej")
            wynik_y = sp.integrate(z_y, (y, g, f), (x, A[0], C[0]))
            calka_y = f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(g).replace('x','y')}}}^{{{sp.latex(f).replace('x','y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy"
        # if wynik_y == pol_int:
        #     print("SUKCES")
        # return (
        #     f'Obliczyć ${zadanie}$ gdzie $D$ - trójkąt $ABC$ dla $A=({A[0]},{A[1]}), B=({B[0]},{B[1]}), C=({C[0]},{C[1]})$',
        #     '$' + calka_y + ' = ' + sp.latex(wynik_y) + '$')
    else:
        # print("szósty")
        f = sp.Rational(C[1] - A[1]) / (C[0] - A[0]) * (x - A[0]) + A[1]
        g = sp.Rational(C[1] - B[1]) / (C[0] - B[0]) * (x - B[0]) + B[1]
        h = sp.Rational(A[1] - B[1]) / (A[0] - B[0]) * (x - B[0]) + B[1]
        # print("f = ", f)
        # print("g = ", g)
        # print("h = ", h)
        if A[1] + (B[0] - A[0]) / (C[0] - A[0]) * (C[1] - A[1]) > B[1]:
            # print("środkowy poniżej")
            wynik_y = sp.integrate(z_y, (y, h, f), (x, A[0], B[0])) + sp.integrate(z_y, (y, g, f), (x, B[0], C[0]))
            calka_y = (
                    f"\\int\\limits_{{{A[0]}}}^{{{B[0]}}}\\left(\\int\\limits_{{{sp.latex(h).replace('x','y')}}}^{{{sp.latex(f).replace('x','y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy + " +
                    f"\\int\\limits_{{{B[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(g).replace('x','y')}}}^{{{sp.latex(f).replace('x','y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy")
        else:
            # print("środkowy powyżej")
            wynik_y = sp.integrate(z_y, (y, f, h), (x, A[0], B[0])) + sp.integrate(z_y, (y, f, g), (x, B[0], C[0]))
            calka_y = (
                    f"\\int\\limits_{{{A[0]}}}^{{{B[0]}}}\\left(\\int\\limits_{{{sp.latex(f).replace('x','y')}}}^{{{sp.latex(h).replace('x','y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy + " +
                    f"\\int\\limits_{{{B[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(f).replace('x','y')}}}^{{{sp.latex(g).replace('x','y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy")
        # if wynik_y == pol_int:
        #     print("SUKCES")
    A[0], A[1] = A[1], A[0]
    B[0], B[1] = B[1], B[0]
    C[0], C[1] = C[1], C[0]
    # wynik_y = 1
    if wynik_y != wynik_x:
        print('\n \x1b[1;7;31m' + '!!!Różne wyniki względem osi!!!' + '\x1b[0m \n ')
    return (
        f'Obliczyć ${zadanie}$ gdzie $D$ - trójkąt $ABC$ dla $A=({A[0]},{A[1]}), B=({B[0]},{B[1]}), C=({C[0]},{C[1]})$',
        'Względem $Ox:$ $' + calka_x + ' = ' + sp.latex(wynik_x) + '$ \\\\' +
        'Względem $Oy:$ $' + calka_y + ' = ' + sp.latex(wynik_y) + '$ \\\\')


if __name__ == "__main__":
    start = time.time()
    polecenie, rozwiazanie = calka_podwojna_po_trojkacie()
    print(polecenie, '\n', rozwiazanie)
    print(f'czas generowania: {round(time.time() - start, 3)}s')
