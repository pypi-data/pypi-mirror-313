import os  # do tworzenia katalogów
import random
import sys  # do wysyłania komunikatów w czerwonym kolorze
import time

''' Następne linijki likwidują konflikt z innymi modułami 
Strasznie to głupie - powiązane z plt.rc('text', usetex=False)
Chodzi o konfikt generowania wykresów używających TeX - matplotlib i problematycznych Sympy Plot'''
import matplotlib.pyplot as plt

''' Poprzednie linijki likwidują konflikt z innymi modułami 
Strasznie to głupie - powiązane z plt.rc('text', usetex=False)
Chodzi o konfikt generowania wykresów używających TeX - matplotlib i problematycznych Sympy Plot'''
import sympy as sp
from spb import plot, plot_parametric

x = sp.Symbol('x', real=True)
y = sp.Symbol('y', real=True)

# from sympy.integrals.intpoly import polytope_integrate, Polygon # do testów - coś źle liczy dla
# A = [-3, -1]
# B = [-1, 0]
# C = [-1, 3]
# z = 3*x-3 * y

def calka_podwojna(typ: int = 1, nr_zadania: int = 1):
    if not os.path.exists('pics'):
        os.makedirs('pics')
        print(" ! Tworzę katalog pics ", file=sys.stderr)
    ''' Następne linijki likwidują konflikt z innymi modułami
    Strasznie to głupie - powiązane z plt.rc('text', usetex=False)
    Chodzi o konfikt generowania wykresów używających TeX - matplotlib i problematycznych Sympy Plot'''
    plt.rc('text', usetex=False)
    ''' Poprzednie linijki likwidują konflikt z innymi modułami 
    Strasznie to głupie - powiązane z plt.rc('text', usetex=False)
    Chodzi o konfikt generowania wykresów używających TeX - matplotlib i problematycznych Sympy Plot'''
    if not os.path.exists('pics'):
        os.makedirs('pics')
        print(" ! Tworzę katalog pics ", file=sys.stderr)

    if typ == 1:
        a, b = [random.choice(
            [-3, -2, -1, 0, sp.Rational(1, 2), 1, sp.Rational(3, 2), 2, 3]) for _ in
            range(2)]
        c = random.choice([-1, 0, 1, 2])
        while True:
            A = [random.choice([-3, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4]) for _ in range(2)]
            B = [random.choice([-3, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4]) for _ in range(2)]
            C = [random.choice([-3, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4]) for _ in range(2)]
            if (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0]):  # pole trójkąta != 0
                break

        # A = [0, 0]  # pamietaj o sortowaniu
        # B = [1, 2]
        # C = [2, 3]
        A_s, B_s, C_s = A, B, C
        A, B, C = sorted([A, B, C])
        # a, b, c = sp.Rational(1,2), -2, 1
        # A[0], A[1] = A[1], A[0]
        # B[0], B[1] = B[1], B[0]
        # C[0], C[1] = C[1], C[0]
        # a,b = b,a
        # a = 3
        # b= -2
        # c = 1
        z = a * x + b * y + c  # do liczenia względem x
        z_y = b * x + a * y + c  # do liczenia względem y
        # z = 3*x -2*y +1
        # print(A, B, C, a, b, c)
        # pol_int = polytope_integrate(Polygon(A, B, C), z)
        # print(pol_int)
        zadanie = f"\\iint\\limits_D\\left({sp.latex(z)}\\right)dx\\,dy"
        # print(A, B, C)
        if A[0] == B[0]:
            # print("pierwszy")
            f = sp.Rational((C[1] - A[1]), (C[0] - A[0])) * (x - A[0]) + A[1]
            g = sp.Rational((C[1] - B[1]), (C[0] - B[0])) * (x - B[0]) + B[1]
            if A[1] > B[1]:
                # print("f jest wyżej")
                print("1 - Jak to widzisz to niedobrze. Daj znać autorowi. - Sortowanie!!!")
                wynik_x = sp.integrate(z, (y, g, f), (x, A[0], C[0]))
                calka_x = f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(g)}}}^{{{sp.latex(f)}}}\\left({sp.latex(z)}\\right)dy\\right)dx"
            else:
                # print("g jest wyżej")
                wynik_x = sp.integrate(z, (y, f, g), (x, A[0], C[0]))
                calka_x = (
                        f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(f)}}}^{{{sp.latex(g)}}}\\left({sp.latex(z)}\\right)dy\\right)dx" +
                        f"\n\t=\ldots=\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left({sp.latex(sp.integrate(z, (y, f, g)).expand())}\\right)dx")
                szerokosc = max(A[0], B[0], C[0]) + 1 - (min(A[0], B[0], C[0]) - 1)
                wysokosc = max(A[1], B[1], C[1]) + 1 - (min(A[1], B[1], C[1]) - 1)
                p1 = plot(f,  # plot a symbolic expression to force to use 2D plot
                          # markers=[
                          #     {"args": [[A[0], A[0]], [-10, 10]], 'label': f'x={A[0]}'},  # prosta pionowa
                          #     {"args": [A[0], A[1]], "marker": "o",
                          #      "linestyle": "None", 'markersize': '10', 'label': 'A'},
                          #     {"args": [B[0], B[1]], "marker": "o",
                          #      "linestyle": "None", 'markersize': '10', 'label': 'B'},
                          #     {"args": [C[0], C[1]], "marker": "o",
                          #      "linestyle": "None", 'markersize': '10', 'label': 'C'},
                          # ],
                          xlim=(min(A[0], B[0], C[0]) - 1 if szerokosc > wysokosc
                                else (min(A[0], B[0], C[0]) + max(A[0], B[0], C[0])) / 2 - wysokosc / 2,
                                max(A[0], B[0], C[0]) + 1 if szerokosc > wysokosc
                                else (min(A[0], B[0], C[0]) + max(A[0], B[0], C[0])) / 2 + wysokosc / 2),
                          ylim=((min(A[1], B[1], C[1]) + max(A[1], B[1], C[1])) / 2 - szerokosc / 2 if
                                szerokosc > wysokosc else
                                min(A[1], B[1], C[1]) - 1,
                                (min(A[1], B[1], C[1]) + max(A[1], B[1], C[1])) / 2 + szerokosc / 2
                                if szerokosc > wysokosc else max(A[1], B[1], C[1]) + 1),
                          aspect=(1, 1),
                          label=f'$y={sp.latex(f)}$',
                          show=False,
                          title=f'Obszar całkowania względem osi $Ox$',
                          xlabel="x",
                          ylabel="y",
                          # use_latex=True,
                          size=(4.5, 4.5),

                          )

                p2 = plot(g,  # plot a symbolic expression to force to use 2D plot
                          markers=[
                              {"args": [[A[0], A[0]], [-10, 10]], 'label': f'$x={A[0]}$'},  # prosta pionowa
                              {"args": [A_s[0], A_s[1]], "marker": "o",
                               "linestyle": "None", 'markersize': '10', 'label': f'A={A_s[0], A_s[1]}'},
                              {"args": [B_s[0], B_s[1]], "marker": "o",
                               "linestyle": "None", 'markersize': '10', 'label': f'B={B_s[0], B_s[1]}'},
                              {"args": [C_s[0], C_s[1]], "marker": "o",
                               "linestyle": "None", 'markersize': '10', 'label': f'C={C_s[0], C_s[1]}'},
                          ],
                          label=f'$y={sp.latex(g)}$',
                          show=False,
                          # use_latex=True,
                          size=(4.5, 4.5),

                          )
                p1.append(p2[0])
                p1.append(p2[1])
                p1.append(p2[2])
                p1.append(p2[3])
                p1.append(p2[4])
                # p1.show()
                p1.save(f'./pics/calka_podwojna{nr_zadania}x.pdf')
                p1.save(f'./pics/calka_podwojna{nr_zadania}x.png')
                p1.close()
                p2.close()

            # if wynik_x == pol_int:
            #     print("SUKCES")
            # return (
            #     f'Obliczyć $${zadanie}$$ gdzie $D$ - trójkąt $ABC$  dla $A=({A[0]},{A[1]}), B=({B[0]},{B[1]}), C=({C[0]},{C[1]})$',
            #     '$' + calka_x + ' = ' + sp.latex(wynik_x) + '$')
        elif B[0] == C[0]:
            # print("drugi")
            f = sp.Rational((C[1] - A[1]), (C[0] - A[0])) * (x - A[0]) + A[1]
            g = sp.Rational((A[1] - B[1]), (A[0] - B[0])) * (x - B[0]) + B[1]
            if B[1] > C[1]:
                # print("B jest wyżej")
                print("2 - Jak to widzisz to niedobrze. Daj znać autorowi. - Sortowanie!!!")
                wynik_x = sp.integrate(z, (y, f, g), (x, A[0], C[0]))
                calka_x = f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(f)}}}^{{{sp.latex(g)}}}\\left({sp.latex(z)}\\right)dy\\right)dx"
            else:
                # print("C jest wyżej")
                wynik_x = sp.integrate(z, (y, g, f), (x, A[0], C[0]))
                calka_x = (
                        f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(g)}}}^{{{sp.latex(f)}}}\\left({sp.latex(z)}\\right)dy\\right)dx" +
                        f"\n\t=\ldots=\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left({sp.latex(sp.integrate(z, (y, g, f)).expand())}\\right)dx")

                szerokosc = max(A[0], B[0], C[0]) + 1 - (min(A[0], B[0], C[0]) - 1)
                wysokosc = max(A[1], B[1], C[1]) + 1 - (min(A[1], B[1], C[1]) - 1)
                p1 = plot(f,  # plot a symbolic expression to force to use 2D plot
                          # markers=[
                          #     {"args": [[A[0], A[0]], [-10, 10]], 'label': f'x={A[0]}'},  # prosta pionowa
                          #     {"args": [A[0], A[1]], "marker": "o",
                          #      "linestyle": "None", 'markersize': '10', 'label': 'A'},
                          #     {"args": [B[0], B[1]], "marker": "o",
                          #      "linestyle": "None", 'markersize': '10', 'label': 'B'},
                          #     {"args": [C[0], C[1]], "marker": "o",
                          #      "linestyle": "None", 'markersize': '10', 'label': 'C'},
                          # ],
                          xlim=(
                              min(A[0], B[0], C[0]) - 1 if szerokosc > wysokosc else (min(A[0], B[0], C[0]) + max(A[0],
                                                                                                                  B[0],
                                                                                                                  C[
                                                                                                                      0])) / 2 - wysokosc / 2,
                              max(A[0], B[0], C[0]) + 1 if szerokosc > wysokosc else (min(A[0], B[0], C[0]) + max(A[0],
                                                                                                                  B[0],
                                                                                                                  C[
                                                                                                                      0])) / 2 + wysokosc / 2),
                          ylim=((min(A[1], B[1], C[1]) + max(A[1], B[1],
                                                             C[
                                                                 1])) / 2 - szerokosc / 2 if szerokosc > wysokosc else min(
                              A[1], B[1], C[1]) - 1,
                                (min(A[1], B[1], C[1]) + max(A[1], B[1],
                                                             C[
                                                                 1])) / 2 + szerokosc / 2 if szerokosc > wysokosc else max(
                                    A[1], B[1], C[1]) + 1),
                          aspect=(1, 1),
                          label=f'$y={sp.latex(f)}$',
                          show=False,
                          title=f'Obszar całkowania względem osi $Ox$',
                          xlabel="x",
                          ylabel="y",
                          # use_latex=True,
                          size=(4.5, 4.5),

                          )
                p2 = plot(g,  # plot a symbolic expression to force to use 2D plot
                          markers=[
                              {"args": [[B[0], B[0]], [-10, 10]], 'label': f'$x={B[0]}$'},  # prosta pionowa
                              {"args": [A_s[0], A_s[1]], "marker": "o",
                               "linestyle": "None", 'markersize': '10', 'label': f'A={A_s[0], A_s[1]}'},
                              {"args": [B_s[0], B_s[1]], "marker": "o",
                               "linestyle": "None", 'markersize': '10', 'label': f'B={B_s[0], B_s[1]}'},
                              {"args": [C_s[0], C_s[1]], "marker": "o",
                               "linestyle": "None", 'markersize': '10', 'label': f'C={C_s[0], C_s[1]}'},
                          ],
                          label=f'$y={sp.latex(g)}$',
                          show=False,
                          # use_latex=True,
                          size=(4.5, 4.5),

                          )
                p1.append(p2[0])
                p1.append(p2[1])
                p1.append(p2[2])
                p1.append(p2[3])
                p1.append(p2[4])
                # p1.show()
                p1.save(f'./pics/calka_podwojna{nr_zadania}x.pdf')
                p1.save(f'./pics/calka_podwojna{nr_zadania}x.png')
                p1.close()
                p2.close()

            # if wynik_x == pol_int:
            #     print("SUKCES")
            # return (
            #     f'Obliczyć $${zadanie}$$ gdzie $D$ - trójkąt $ABC$ dla $A=({A[0]},{A[1]}), B=({B[0]},{B[1]}), C=({C[0]},{C[1]})$',
            #     '$' + calka_x + ' = ' + sp.latex(wynik_x) + '$')
        else:
            # print("trzeci")
            f = sp.Rational((C[1] - A[1]), (C[0] - A[0])) * (x - A[0]) + A[1]
            g = sp.Rational((C[1] - B[1]), (C[0] - B[0])) * (x - B[0]) + B[1]
            h = sp.Rational((A[1] - B[1]), (A[0] - B[0])) * (x - B[0]) + B[1]
            # print("f = ", f)
            # print("g = ", g)
            # print("h = ", h)
            if A[1] + (B[0] - A[0]) / (C[0] - A[0]) * (C[1] - A[1]) > B[1]:
                # print("środkowy poniżej")
                wynik_x = sp.integrate(z, (y, h, f), (x, A[0], B[0])) + sp.integrate(z, (y, g, f), (x, B[0], C[0]))
                calka_x = (
                        f"\\int\\limits_{{{A[0]}}}^{{{B[0]}}}\\left(\\int\\limits_{{{sp.latex(h)}}}^{{{sp.latex(f)}}}\\left({sp.latex(z)}\\right)dy\\right)dx + " +
                        f"\\int\\limits_{{{B[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(g)}}}^{{{sp.latex(f)}}}\\left({sp.latex(z)}\\right)dy\\right)dx" +
                        f"\n\t=\ldots=\\int\\limits_{{{A[0]}}}^{{{B[0]}}}\\left( {sp.latex(sp.integrate(z, (y, h, f)).expand())}   \\right)dx + " +
                        f"\\int\\limits_{{{B[0]}}}^{{{C[0]}}}\\left(  {sp.latex(sp.integrate(z, (y, g, f)).expand())}    \\right)dx"
                )
            else:
                # print("środkowy powyżej")
                wynik_x = sp.integrate(z, (y, f, h), (x, A[0], B[0])) + sp.integrate(z, (y, f, g), (x, B[0], C[0]))
                calka_x = (
                        f"\\int\\limits_{{{A[0]}}}^{{{B[0]}}}\\left(\\int\\limits_{{{sp.latex(f)}}}^{{{sp.latex(h)}}}\\left({sp.latex(z)}\\right)dy\\right)dx + " +
                        f"\\int\\limits_{{{B[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(f)}}}^{{{sp.latex(g)}}}\\left({sp.latex(z)}\\right)dy\\right)dx" +
                        f"\n\t=\ldots=\\int\\limits_{{{A[0]}}}^{{{B[0]}}}\\left( {sp.latex(sp.integrate(z, (y, f, h)).expand())}   \\right)dx + " +
                        f"\\int\\limits_{{{B[0]}}}^{{{C[0]}}}\\left(  {sp.latex(sp.integrate(z, (y, f, g)).expand())}    \\right)dx"
                )
            szerokosc = max(A[0], B[0], C[0]) + 1 - (min(A[0], B[0], C[0]) - 1)
            wysokosc = max(A[1], B[1], C[1]) + 1 - (min(A[1], B[1], C[1]) - 1)
            p1 = plot(f,  # plot a symbolic expression to force to use 2D plot
                      # markers=[
                      #     {"args": [[A[0], A[0]], [-10, 10]], 'label': f'x={A[0]}'},  # prosta pionowa
                      #     {"args": [A[0], A[1]], "marker": "o",
                      #      "linestyle": "None", 'markersize': '10', 'label': 'A'},
                      #     {"args": [B[0], B[1]], "marker": "o",
                      #      "linestyle": "None", 'markersize': '10', 'label': 'B'},
                      #     {"args": [C[0], C[1]], "marker": "o",
                      #      "linestyle": "None", 'markersize': '10', 'label': 'C'},
                      # ],
                      xlim=(
                          min(A[0], B[0], C[0]) - 1 if szerokosc > wysokosc else (min(A[0], B[0], C[0]) + max(A[0],
                                                                                                              B[0],
                                                                                                              C[
                                                                                                                  0])) / 2 - wysokosc / 2,
                          max(A[0], B[0], C[0]) + 1 if szerokosc > wysokosc else (min(A[0], B[0], C[0]) + max(A[0],
                                                                                                              B[0],
                                                                                                              C[
                                                                                                                  0])) / 2 + wysokosc / 2),
                      ylim=(
                          (min(A[1], B[1], C[1]) + max(A[1], B[1],
                                                       C[1])) / 2 - szerokosc / 2 if szerokosc > wysokosc else min(
                              A[1], B[1], C[1]) - 1,
                          (min(A[1], B[1], C[1]) + max(A[1], B[1],
                                                       C[1])) / 2 + szerokosc / 2 if szerokosc > wysokosc else max(
                              A[1], B[1], C[1]) + 1),
                      aspect=(1, 1),
                      label=f'$y={sp.latex(f)}$',
                      show=False,
                      title='Obszar całkowania względem osi $Ox$',
                      xlabel="x",
                      ylabel="y",
                      # use_latex=True,
                      size=(4.5, 4.5),

                      )
            p2 = plot(h,  # plot a symbolic expression to force to use 2D plot
                      label=f'$y={sp.latex(h)}$',
                      show=False,
                      size=(4.5, 4.5),

                      # use_latex=True
                      )
            p3 = plot(g,  # plot a symbolic expression to force to use 2D plot
                      markers=[
                          {"args": [A_s[0], A_s[1]], "marker": "o",
                           "linestyle": "None", 'markersize': '10', 'label': f'A={A_s[0], A_s[1]}'},
                          {"args": [B_s[0], B_s[1]], "marker": "o",
                           "linestyle": "None", 'markersize': '10', 'label': f'B={B_s[0], B_s[1]}'},
                          {"args": [C_s[0], C_s[1]], "marker": "o",
                           "linestyle": "None", 'markersize': '10', 'label': f'C={C_s[0], C_s[1]}'},
                      ],
                      label=f'$y={sp.latex(g)}$',
                      # use_latex=True,
                      size=(4.5, 4.5),

                      show=False,

                      )
            p1.append(p2[0])
            p1.append(p3[0])
            p1.append(p3[1])
            p1.append(p3[2])
            p1.append(p3[3])
            # p1.show()
            p1.save(f'./pics/calka_podwojna{nr_zadania}x.pdf')
            p1.save(f'./pics/calka_podwojna{nr_zadania}x.png')
            p1.close()
            p2.close()
            p3.close()
            # if wynik_x == pol_int:
            #     print("SUKCES")
        ''' zamieniam x i y miejscami - raczej można to zrobić lepiej '''
        A[0], A[1] = A[1], A[0]
        B[0], B[1] = B[1], B[0]
        C[0], C[1] = C[1], C[0]
        A, B, C = sorted([A, B, C])

        # print(A, B, C)
        # pol_int = polytope_integrate(Polygon(A, B, C), z)
        # print(pol_int)
        # zadanie = f"\\iint\\limits_D\\left({sp.latex(z)}\\right)dx\\,dy"
        if A[0] == B[0]:
            # print("czwarty")
            f = sp.Rational((C[1] - A[1]), (C[0] - A[0])) * (x - A[0]) + A[1]
            g = sp.Rational((C[1] - B[1]), (C[0] - B[0])) * (x - B[0]) + B[1]
            if A[1] > B[1]:
                # print("f jest wyżej")
                print("4 - Jak to widzisz to niedobrze. Daj znać autorowi. - Sortowanie!!!")
                wynik_y = sp.integrate(z_y, (y, g, f), (x, A[0], C[0]))
                calka_y = f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(g).replace('x', 'y')}}}^{{{sp.latex(f).replace('x', 'y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy"
            else:
                # print("g jest wyżej")
                wynik_y = sp.integrate(z_y, (y, f, g), (x, A[0], C[0]))
                calka_y = (
                        f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(f).replace('x', 'y')}}}^{{{sp.latex(g).replace('x', 'y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy" +
                        f"\n\t=\ldots=\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left({sp.latex(sp.integrate(z_y, (y, f, g)).expand()).replace('x', 'y')}\\right)dy")

                szerokosc = max(A[0], B[0], C[0]) + 1 - (min(A[0], B[0], C[0]) - 1)
                wysokosc = max(A[1], B[1], C[1]) + 1 - (min(A[1], B[1], C[1]) - 1)
                p1 = plot(f,  # plot a symbolic expression to force to use 2D plot
                          # markers=[
                          #     {"args": [[A[0], A[0]], [-10, 10]], 'label': f'x={A[0]}'},  # prosta pionowa
                          #     {"args": [A[0], A[1]], "marker": "o",
                          #      "linestyle": "None", 'markersize': '10', 'label': 'A'},
                          #     {"args": [B[0], B[1]], "marker": "o",
                          #      "linestyle": "None", 'markersize': '10', 'label': 'B'},
                          #     {"args": [C[0], C[1]], "marker": "o",
                          #      "linestyle": "None", 'markersize': '10', 'label': 'C'},
                          # ],
                          xlim=(
                              max(A[0], B[0], C[0]) + 1 if szerokosc > wysokosc else (min(A[0], B[0], C[0]) + max(A[0],
                                                                                                                  B[0],
                                                                                                                  C[
                                                                                                                      0])) / 2 + wysokosc / 2,
                              min(A[0], B[0], C[0]) - 1 if szerokosc > wysokosc else (min(A[0], B[0], C[0]) + max(A[0],
                                                                                                                  B[0],
                                                                                                                  C[
                                                                                                                      0])) / 2 - wysokosc / 2),
                          ylim=((min(A[1], B[1], C[1]) + max(A[1], B[1],
                                                             C[
                                                                 1])) / 2 - szerokosc / 2 if szerokosc > wysokosc else min(
                              A[1], B[1], C[1]) - 1,
                                (min(A[1], B[1], C[1]) + max(A[1], B[1],
                                                             C[
                                                                 1])) / 2 + szerokosc / 2 if szerokosc > wysokosc else max(
                                    A[1], B[1], C[1]) + 1),
                          aspect=(1, 1),
                          label='$x = $' + f'${sp.latex(f)}$'.replace('x', 'y'),
                          show=False,
                          title=f'Obszar całkowania względem osi $Oy$',
                          xlabel="y",
                          ylabel="x",
                          # use_latex=True,
                          size=(4.5, 4.5),

                          )
                p2 = plot(g,  # plot a symbolic expression to force to use 2D plot
                          markers=[
                              {"args": [[A[0], A[0]], [-10, 10]], 'label': f'$y={A[0]}$'},  # prosta pionowa
                              {"args": [A_s[0], A_s[1]], "marker": "o",
                               "linestyle": "None", 'markersize': '10', 'label': f'A={A_s[1], A_s[0]}'},
                              {"args": [B_s[0], B_s[1]], "marker": "o",
                               "linestyle": "None", 'markersize': '10', 'label': f'B={B_s[1], B_s[0]}'},
                              {"args": [C_s[0], C_s[1]], "marker": "o",
                               "linestyle": "None", 'markersize': '10', 'label': f'C={C_s[1], C_s[0]}'},
                          ],
                          label='$x = $' + f'${sp.latex(g)}$'.replace('x', 'y'),
                          show=False,
                          # use_latex=True,
                          size=(4.5, 4.5),

                          )
                p1.append(p2[0])
                p1.append(p2[1])
                p1.append(p2[2])
                p1.append(p2[3])
                p1.append(p2[4])
                # p1.show()
                p1.save(f'./pics/calka_podwojna{nr_zadania}y.pdf')
                p1.save(f'./pics/calka_podwojna{nr_zadania}y.png')
                p1.close()
                p2.close()

            # if wynik_y == pol_int:
            #     print("SUKCES")
            # return (
            #     f'Obliczyć $${zadanie}$$ gdzie $D$ - trójkąt $ABC$  dla $A=({A[0]},{A[1]}), B=({B[0]},{B[1]}), C=({C[0]},{C[1]})$',
            #     '$' + calka_y + ' = ' + sp.latex(wynik_y) + '$')
        elif B[0] == C[0]:
            # print("piąty")
            f = sp.Rational((C[1] - A[1]), (C[0] - A[0])) * (x - A[0]) + A[1]
            g = sp.Rational((A[1] - B[1]), (A[0] - B[0])) * (x - B[0]) + B[1]
            if B[1] > C[1]:
                # print("B jest wyżej")
                print("5 - Jak to widzisz to niedobrze. Daj znać autorowi. - Sortowanie!!!")
                wynik_y = sp.integrate(z_y, (y, f, g), (x, A[0], C[0]))
                calka_y = f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(f).replace('x', 'y')}}}^{{{sp.latex(g).replace('x', 'y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy"
            else:
                # print("C jest wyżej")
                wynik_y = sp.integrate(z_y, (y, g, f), (x, A[0], C[0]))
                calka_y = (
                        f"\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(g).replace('x', 'y')}}}^{{{sp.latex(f).replace('x', 'y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy" +
                        f"\n\t=\ldots=\\int\\limits_{{{A[0]}}}^{{{C[0]}}}\\left({sp.latex(sp.integrate(z_y, (y, g, f)).expand()).replace('x', 'y')}\\right)dy")

                szerokosc = max(A[0], B[0], C[0]) + 1 - (min(A[0], B[0], C[0]) - 1)
                wysokosc = max(A[1], B[1], C[1]) + 1 - (min(A[1], B[1], C[1]) - 1)
                p1 = plot(f,  # plot a symbolic expression to force to use 2D plot
                          # markers=[
                          #     {"args": [[A[0], A[0]], [-10, 10]], 'label': f'x={A[0]}'},  # prosta pionowa
                          #     {"args": [A[0], A[1]], "marker": "o",
                          #      "linestyle": "None", 'markersize': '10', 'label': 'A'},
                          #     {"args": [B[0], B[1]], "marker": "o",
                          #      "linestyle": "None", 'markersize': '10', 'label': 'B'},
                          #     {"args": [C[0], C[1]], "marker": "o",
                          #      "linestyle": "None", 'markersize': '10', 'label': 'C'},
                          # ],
                          xlim=(
                              max(A[0], B[0], C[0]) + 1 if szerokosc > wysokosc else (min(A[0], B[0], C[0]) + max(A[0],
                                                                                                                  B[0],
                                                                                                                  C[
                                                                                                                      0])) / 2 + wysokosc / 2,
                              min(A[0], B[0], C[0]) - 1 if szerokosc > wysokosc else (min(A[0], B[0], C[0]) + max(A[0],
                                                                                                                  B[0],
                                                                                                                  C[
                                                                                                                      0])) / 2 - wysokosc / 2),
                          ylim=((min(A[1], B[1], C[1]) + max(A[1], B[1],
                                                             C[
                                                                 1])) / 2 - szerokosc / 2 if szerokosc > wysokosc else min(
                              A[1], B[1], C[1]) - 1,
                                (min(A[1], B[1], C[1]) + max(A[1], B[1],
                                                             C[
                                                                 1])) / 2 + szerokosc / 2 if szerokosc > wysokosc else max(
                                    A[1], B[1], C[1]) + 1),
                          aspect=(1, 1),
                          label='$x = $' + f'${sp.latex(f)}$'.replace('x', 'y'),
                          show=False,
                          title=f'Obszar całkowania względem osi $Oy$',
                          xlabel="y",
                          ylabel="x",
                          # use_latex=True,
                          size=(4.5, 4.5),

                          )
                p2 = plot(g,  # plot a symbolic expression to force to use 2D plot
                          markers=[
                              {"args": [[B[0], B[0]], [-10, 10]], 'label': f'$y={B[0]}$'},  # prosta pionowa
                              {"args": [A_s[0], A_s[1]], "marker": "o",
                               "linestyle": "None", 'markersize': '10', 'label': f'A={A_s[1], A_s[0]}'},
                              {"args": [B_s[0], B_s[1]], "marker": "o",
                               "linestyle": "None", 'markersize': '10', 'label': f'B={B_s[1], B_s[0]}'},
                              {"args": [C_s[0], C_s[1]], "marker": "o",
                               "linestyle": "None", 'markersize': '10', 'label': f'C={C_s[1], C_s[0]}'},
                          ],
                          label='$x = $' + f'${sp.latex(g)}$'.replace('x', 'y'),
                          show=False,
                          # use_latex=True,
                          size=(4.5, 4.5),

                          )
                p1.append(p2[0])
                p1.append(p2[1])
                p1.append(p2[2])
                p1.append(p2[3])
                p1.append(p2[4])
                # p1.show()
                p1.save(f'./pics/calka_podwojna{nr_zadania}y.pdf')
                p1.save(f'./pics/calka_podwojna{nr_zadania}y.png')
                p1.close()
                p2.close()
            # if wynik_y == pol_int:
            #     print("SUKCES")
            # return (
            #     f'Obliczyć $${zadanie}$$ gdzie $D$ - trójkąt $ABC$ dla $A=({A[0]},{A[1]}), B=({B[0]},{B[1]}), C=({C[0]},{C[1]})$',
            #     '$' + calka_y + ' = ' + sp.latex(wynik_y) + '$')
        else:
            # print("szósty")
            f = sp.Rational((C[1] - A[1]), (C[0] - A[0])) * (x - A[0]) + A[1]
            g = sp.Rational((C[1] - B[1]), (C[0] - B[0])) * (x - B[0]) + B[1]
            h = sp.Rational((A[1] - B[1]), (A[0] - B[0])) * (x - B[0]) + B[1]
            # print("f = ", f)
            # print("g = ", g)
            # print("h = ", h)
            if A[1] + (B[0] - A[0]) / (C[0] - A[0]) * (C[1] - A[1]) > B[1]:
                # print("środkowy poniżej")
                wynik_y = sp.integrate(z_y, (y, h, f), (x, A[0], B[0])) + sp.integrate(z_y, (y, g, f), (x, B[0], C[0]))
                calka_y = (
                        f"\\int\\limits_{{{A[0]}}}^{{{B[0]}}}\\left(\\int\\limits_{{{sp.latex(h).replace('x', 'y')}}}^{{{sp.latex(f).replace('x', 'y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy + " +
                        f"\\int\\limits_{{{B[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(g).replace('x', 'y')}}}^{{{sp.latex(f).replace('x', 'y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy" +
                        f"\n\t=\ldots=\\int\\limits_{{{A[0]}}}^{{{B[0]}}}\\left(  {sp.latex(sp.integrate(z_y, (y, h, f)).expand()).replace('x', 'y')}  \\right)dy + " +
                        f"\\int\\limits_{{{B[0]}}}^{{{C[0]}}}\\left(  {sp.latex(sp.integrate(z_y, (y, g, f)).expand()).replace('x', 'y')}  \\right)dy")
            else:
                # print("środkowy powyżej")
                wynik_y = sp.integrate(z_y, (y, f, h), (x, A[0], B[0])) + sp.integrate(z_y, (y, f, g), (x, B[0], C[0]))
                calka_y = (
                        f"\\int\\limits_{{{A[0]}}}^{{{B[0]}}}\\left(\\int\\limits_{{{sp.latex(f).replace('x', 'y')}}}^{{{sp.latex(h).replace('x', 'y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy + " +
                        f"\\int\\limits_{{{B[0]}}}^{{{C[0]}}}\\left(\\int\\limits_{{{sp.latex(f).replace('x', 'y')}}}^{{{sp.latex(g).replace('x', 'y')}}}\\left({sp.latex(z)}\\right)dx\\right)dy" +
                        f"\n\t=\ldots=\\int\\limits_{{{A[0]}}}^{{{B[0]}}}\\left(  {sp.latex(sp.integrate(z_y, (y, f, h)).expand()).replace('x', 'y')}  \\right)dy + " +
                        f"\\int\\limits_{{{B[0]}}}^{{{C[0]}}}\\left(  {sp.latex(sp.integrate(z_y, (y, f, g)).expand()).replace('x', 'y')}  \\right)dy")
            # if wynik_y == pol_int:
            #     print("SUKCES")
            szerokosc = max(A[0], B[0], C[0]) + 1 - (min(A[0], B[0], C[0]) - 1)
            wysokosc = max(A[1], B[1], C[1]) + 1 - (min(A[1], B[1], C[1]) - 1)
            p1 = plot(f,  # plot a symbolic expression to force to use 2D plot
                      # markers=[
                      #     {"args": [[A[0], A[0]], [-10, 10]], 'label': f'x={A[0]}'},  # prosta pionowa
                      #     {"args": [A[0], A[1]], "marker": "o",
                      #      "linestyle": "None", 'markersize': '10', 'label': 'A'},
                      #     {"args": [B[0], B[1]], "marker": "o",
                      #      "linestyle": "None", 'markersize': '10', 'label': 'B'},
                      #     {"args": [C[0], C[1]], "marker": "o",
                      #      "linestyle": "None", 'markersize': '10', 'label': 'C'},
                      # ],
                      xlim=(
                          max(A[0], B[0], C[0]) + 1 if szerokosc > wysokosc else (min(A[0], B[0], C[0]) + max(A[0],
                                                                                                              B[0],
                                                                                                              C[
                                                                                                                  0])) / 2 + wysokosc / 2,
                          min(A[0], B[0], C[0]) - 1 if szerokosc > wysokosc else (min(A[0], B[0], C[0]) + max(A[0],
                                                                                                              B[0],
                                                                                                              C[
                                                                                                                  0])) / 2 - wysokosc / 2),
                      ylim=(
                          (min(A[1], B[1], C[1]) + max(A[1], B[1],
                                                       C[1])) / 2 - szerokosc / 2 if szerokosc > wysokosc else min(
                              A[1], B[1], C[1]) - 1,
                          (min(A[1], B[1], C[1]) + max(A[1], B[1],
                                                       C[1])) / 2 + szerokosc / 2 if szerokosc > wysokosc else max(
                              A[1], B[1], C[1]) + 1),
                      aspect=(1, 1),
                      label='$x = $' + f'${sp.latex(f)}$'.replace('x', 'y'),
                      show=False,
                      title='Obszar całkowania względem osi $Oy$',
                      xlabel="y",
                      ylabel="x",
                      # use_latex=True
                      size=(4.5, 4.5),

                      )
            p2 = plot(h,  # plot a symbolic expression to force to use 2D plot
                      label='$x = $' + f'${sp.latex(h)}$'.replace('x', 'y'),
                      show=False,
                      size=(4.5, 4.5),

                      # use_latex=True
                      )
            p3 = plot(g,  # plot a symbolic expression to force to use 2D plot
                      markers=[
                          {"args": [A_s[0], A_s[1]], "marker": "o",
                           "linestyle": "None", 'markersize': '10', 'label': f'A={A_s[1], A_s[0]}'},
                          {"args": [B_s[0], B_s[1]], "marker": "o",
                           "linestyle": "None", 'markersize': '10', 'label': f'B={B_s[1], B_s[0]}'},
                          {"args": [C_s[0], C_s[1]], "marker": "o",
                           "linestyle": "None", 'markersize': '10', 'label': f'C={C_s[1], C_s[0]}'},
                      ],
                      label='$x = $' + f'${sp.latex(g)}$'.replace('x', 'y'),
                      # use_latex=True,
                      size=(4.5, 4.5),

                      show=False,
                      )
            p1.append(p2[0])
            p1.append(p3[0])
            p1.append(p3[1])
            p1.append(p3[2])
            p1.append(p3[3])
            # p1.show()
            p1.save(f'./pics/calka_podwojna{nr_zadania}y.pdf')
            p1.save(f'./pics/calka_podwojna{nr_zadania}y.png')
            p1.close()
            p2.close()
            p3.close()
        A[0], A[1] = A[1], A[0]
        B[0], B[1] = B[1], B[0]
        C[0], C[1] = C[1], C[0]
        # wynik_y = 1
        if wynik_y != wynik_x:
            print('\n \x1b[1;7;31m' + '!!!Różne wyniki względem osi!!!  -  Posortowałeś punkty ABC?' + '\x1b[0m \n ')
        return (
            f'Obliczyć $${zadanie}$$ gdzie $D$ - trójkąt $ABC$ dla $A=({A_s[0]},{A_s[1]}), B=({B_s[0]},{B_s[1]}), C=({C_s[0]},{C_s[1]})$',
            f'\\includegraphics[width=60mm]{{../pics/calka_podwojna{nr_zadania}x}}\n' +
            f'\t\\includegraphics[width=60mm]{{../pics/calka_podwojna{nr_zadania}y}}\\\\\n' +
            '\tWzględem $Ox:$ $' + calka_x + ' = \ldots = ' + sp.latex(wynik_x) + '$ \\\\\n' +
            '\tWzględem $Oy:$ $' + calka_y + ' = \ldots = ' + sp.latex(wynik_y) + '$ \\\\')
    if typ == 2:
        wzgledem_xy = random.choice(['x', 'y'])
        # wzgledem_xy = 'y'
        if wzgledem_xy == 'x':
            while True:
                a, d = [
                    random.choice([-3, -2, -1, sp.Rational(1, 2), 1, sp.Rational(3, 2), 2, 3])
                    for _ in range(2)]
                b, c, e = [
                    random.choice([-3, -2, -1, sp.Rational(1, 2), 0, 0, 0, 0, 0, 1, sp.Rational(3, 2), 2, 3])
                    for _ in range(3)]
                # a = -3 # sp.Rational(1, 2)
                # b = -1
                # c = 3
                # d = -1
                # e = 0
                # a, b, c = -1, 3, -3 #, -1/2, -3
                # d, e = sp.Rational(1, 2), -3
                # print(a, b, c, d, e)
                f = a * x ** 2 + b * x + c
                g = d * x + e

                roz = sp.solve(f - g)
                # print((roz[0].is_Rational),type(roz[1]))
                # print(roz)

                if len(roz) == 2 and all([roz[i].is_integer for i in range(2)]):
                    break
            while True:
                A, B = [random.choice(
                    [-3, -2, -1, sp.Rational(1, 2), 1, 0, 0, 0, sp.Rational(3, 2), 2, 3]) for _ in
                    range(2)]
                if A ** 2 + B ** 2 > 0:
                    break

            C = random.choice([-1, 0, 0, 0, 1, 2])
            z = A * x + B * y + C
            # print(f,g,roz,sep="\n")
            szerokosc = max(roz) - min(roz)
            wysokosc = max(f.subs(x, roz[0]), f.subs(x, roz[1])) + (b ** 2 - 4 * a * c) / (4 * a) if a > 0 else \
                - (b ** 2 - 4 * a * c) / (4 * a) - (min(f.subs(x, roz[0]), f.subs(x, roz[1])))
            y_min = - (b ** 2 - 4 * a * c) / (4 * a) if a > 0 else min(f.subs(x, roz[0]), f.subs(x, roz[1]))
            y_max = max(f.subs(x, roz[0]), f.subs(x, roz[1])) if a > 0 else - (b ** 2 - 4 * a * c) / (4 * a)
            p = plot(f,
                     g,
                     (x, -100, 100),  # inaczej obcina dziedzinę funkcji do -10,10
                     n=50000,  # powiązane w linijką wyżej. Inaczej wykres nie jest gładki.

                     markers=[
                         {"args": [roz[0], f.subs(x, roz[0])], "marker": "o",
                          "linestyle": "None", 'markersize': '10', 'label': f'A={roz[0], f.subs(x, roz[0])}'},
                         {"args": [roz[1], f.subs(x, roz[1])], "marker": "o",
                          "linestyle": "None", 'markersize': '10', 'label': f'B={roz[1], f.subs(x, roz[1])}'},
                         {"args": [-b / (2 * a), f.subs(x, -b / (2 * a))], "marker": "o",
                          "linestyle": "None", 'markersize': '10',
                          'label': f'W={sp.Rational(-b, 2 * a), (f.subs(x, sp.Rational(-b, 2 * a)))}'},
                     ],
                     xlim=(min(roz) - 1 if szerokosc > wysokosc else (min(roz) + max(roz)) / 2 - wysokosc / 2 - 1,
                           max(roz) + 1 if szerokosc > wysokosc else (min(roz) + max(roz)) / 2 + wysokosc / 2 + 1),
                     ylim=((y_min + y_max) / 2 - szerokosc / 2 - 1 if szerokosc > wysokosc else y_min - 1,
                           (y_min + y_max) / 2 + szerokosc / 2 + 1 if szerokosc > wysokosc else y_max + 1),
                     # aspect=(1, 1),
                     title='Obszar całkowania względem $Ox$',
                     # title = f"{round(szerokosc), round(wysokosc), round(roz[0]), round (roz[1]), round(y_min), round( y_max)}",
                     label=(f'y=${sp.latex(f)}$', f'y=${sp.latex(g)}$'),

                     show=False,
                     # use_latex=True,
                     size=(4.5, 4.5),

                     xlabel="x",
                     ylabel="y",
                     aspect=(1, 1),
                     )

            p.save(f'./pics/calka_podwojna{nr_zadania}x.pdf')
            p.save(f'./pics/calka_podwojna{nr_zadania}x.png')
            p.close()

            f_i = sp.solve(y - f, x)
            g_i = sp.solve(y - g, x)

            # print((y_min + y_max) / 2 - szerokosc / 2 + 1 if szerokosc > wysokosc else y_min - 1,
            #       (y_min + y_max) / 2 + szerokosc / 2 - 1 if szerokosc > wysokosc else y_max + 1)
            p = plot(f_i[0], f_i[1], g_i,
                     (y, -100, 100),  # inaczej obcina dziedzinę funkcji do -10,10
                     markers=[
                         {"args": [f.subs(x, roz[0]), roz[0]], "marker": "o",
                          "linestyle": "None", 'markersize': '10', 'label': f'A={roz[0], f.subs(x, roz[0])}'},
                         {"args": [f.subs(x, roz[1]), roz[1]], "marker": "o",
                          "linestyle": "None", 'markersize': '10', 'label': f'B={roz[1], f.subs(x, roz[1])}'},
                         {"args": [f.subs(x, -b / (2 * a)), -b / (2 * a)], "marker": "o",
                          "linestyle": "None", 'markersize': '10',
                          'label': f'W={sp.Rational(-b, 2 * a), (f.subs(x, sp.Rational(-b, 2 * a)))}'},
                     ],

                     xlim=((y_min + y_max) / 2 + szerokosc / 2 + 1 if szerokosc > wysokosc else y_max + 1,
                           (y_min + y_max) / 2 - szerokosc / 2 - 1 if szerokosc > wysokosc else y_min - 1),
                     ylim=(min(roz) - 1 if szerokosc > wysokosc else (min(roz) + max(roz)) / 2 - wysokosc / 2 - 1,
                           max(roz) + 1 if szerokosc > wysokosc else (min(roz) + max(roz)) / 2 + wysokosc / 2 + 1),

                     label=(f'x=${sp.latex(f_i[0])}$', f'x=${sp.latex(f_i[1])}$', f'x=${sp.latex(g_i[0])}$'),
                     n=50000,  # dużo by nie było przerwy przy wierzchołku
                     title=f'Obszar całkowania względem osi Oy',
                     xlabel="y",
                     ylabel="x",
                     aspect=(1, 1),
                     show=False,
                     # use_latex=True,
                     size=(4.5, 4.5),
                     )
            p.save(f'./pics/calka_podwojna{nr_zadania}y.pdf')
            p.save(f'./pics/calka_podwojna{nr_zadania}y.png')
            p.close()
            # print(sp.Rational(-b, (2 * a)), (f.subs(x, -b / (2 * a))))

            wynik_x = sp.integrate(z, (y, f, g), (x, min(roz), max(roz))) * (1 if a > 0 else -1)
            calka_x = (
                    f"\\int\\limits_{{{min(roz)}}}^{{{max(roz)}}}\\left(\\int\\limits_{{{sp.latex(f) if a > 0 else sp.latex(g)}}}^{{{sp.latex(g) if a > 0 else sp.latex(f)}}}\\left({sp.latex(z)}\\right)dy\\right)dx" +
                    f"\n\t=\ldots=\\int\\limits_{{{min(roz)}}}^{{{max(roz)}}}\\left({sp.latex(sp.integrate(z, (y, f, g)).expand()) if a > 0 else sp.latex(sp.integrate(z, (y, g, f)).expand())}\\right)dx")

            zadanie = f"\\iint\\limits_D\\left({sp.latex(z)}\\right)dx\\,dy"

            if a > 0 and d > 0:
                if min(roz) < - b / (2 * a) < max(roz):
                    wynik_y = (sp.integrate(z, (x, f_i[0], f_i[1]),
                                            (y, f.subs(x, sp.Rational(-b, (2 * a))), f.subs(x, min(roz)))) +
                               sp.integrate(z, (x, g_i[0], f_i[1]), (y, f.subs(x, min(roz)), f.subs(x, max(roz)))))
                    calka_y = (
                            f"\\int\\limits_{{{f.subs(x, sp.Rational(-b, (2 * a)))}}}^{{{f.subs(x, min(roz))}}}\\left(\\int\\limits_{{{sp.latex(f_i[0])}}}^{{{sp.latex(f_i[1])}}}\\left({sp.latex(z)}\\right)dx\\right)dy + " +
                            f"\n\t\t\\int\\limits_{{{f.subs(x, min(roz))}}}^{{{f.subs(x, max(roz))} }}\\left(\\int\\limits_{{{sp.latex(g_i[0])}}}^{{{sp.latex(f_i[1])}}}\\left({sp.latex(z)}\\right)dx\\right)dy" +
                            f"\n\t=\ldots=\\int\\limits_{{{f.subs(x, sp.Rational(-b, (2 * a)))}}}^{{{f.subs(x, min(roz))}}}\\left({sp.latex(sp.integrate(z, (x, f_i[0], f_i[1])).expand())}\\right)dy +" +
                            f"\n\t\t\\int\\limits_{{{f.subs(x, min(roz))}}}^{{{f.subs(x, max(roz))}}}\\left({sp.latex(sp.integrate(z, (x, g_i[0], f_i[1])).expand())}\\right)dx")

                else:
                    wynik_y = sp.integrate(z, (x, g_i[0], f_i[1]), (y, f.subs(x, min(roz)), f.subs(x, max(roz))))
                    calka_y = (
                            f"\\int\\limits_{{{f.subs(x, min(roz))}}}^{{{f.subs(x, max(roz))}}}\\left(\\int\\limits_{{{sp.latex(g_i[0])}}}^{{{sp.latex(f_i[1])}}}\\left({sp.latex(z)}\\right)dx\\right)dy" +
                            f"\n\t=\ldots=\\int\\limits_{{{f.subs(x, min(roz))}}}^{{{f.subs(x, max(roz))}}}\\left({sp.latex(sp.integrate(z, (x, g_i[0], f_i[1])).expand())}\\right)dy")
                return (
                    f'Obliczyć $${zadanie}$$ gdzie $D$ - obszar ograniczony krzywymi $y={sp.latex(f)}$, oraz $y={sp.latex(g)}$',
                    f'\\includegraphics[width=45mm]{{../pics/calka_podwojna{nr_zadania}x}}\n' +
                    f'\t\\includegraphics[width=45mm]{{../pics/calka_podwojna{nr_zadania}y}}\\\\\n' +
                    '\tWzględem $Ox:$ $' + calka_x + ' = \ldots = ' + sp.latex(wynik_x) + '$ \\\\\n' +
                    '\tWzględem $Oy:$ $' + calka_y + ' = \ldots = ' + sp.latex(wynik_y) + '$ \\\\')


            else:
                return (
                    f'Obliczyć $${zadanie}$$ gdzie $D$ - obszar ograniczony krzywymi $y={sp.latex(f)}$, oraz $y={sp.latex(g)}$',
                    f'\\includegraphics[width=45mm]{{../pics/calka_podwojna{nr_zadania}x}}\n' +
                    f'\t\\includegraphics[width=45mm]{{../pics/calka_podwojna{nr_zadania}y}}\\\\\n' +
                    '\tWzględem $Ox:$ $' + calka_x + ' = \ldots = ' + sp.latex(wynik_x) + '$ \\\\')


        else:
            while True:
                a, d = [
                    random.choice([-3, -2, -1, sp.Rational(1, 2), 1, sp.Rational(3, 2), 2, 3])
                    for _ in range(2)]
                b, c, e = [
                    random.choice([-3, -2, -1, sp.Rational(1, 2), 0, 0, 0, 0, 1, sp.Rational(3, 2), 2, 3])
                    for _ in range(3)]

                # a, b, c = 2, 0, 0  # , -1/2, -3
                # d, e = 2, 0  # sp.Rational(1, 2), -3
                # print(a, b, c, d, e)
                f = a * y ** 2 + b * y + c
                g = d * y + e
                # Bug
                roz = sp.solve(f - g)
                # print((roz[0].is_Rational),type(roz[1]))
                # print(roz)

                if len(roz) == 2 and all([roz[i].is_integer for i in range(2)]):
                    break
            while True:
                A, B = [random.choice(
                    [-3, -2, -1, sp.Rational(1, 2), 1, 0, 0, 0, sp.Rational(3, 2), 2, 3]) for _ in
                    range(2)]
                if A ** 2 + B ** 2 > 0:
                    break
            C = random.choice([-1, 0, 0, 0, 1, 2])
            # A, B, C = sp.Rational(3, 2), 1, 2
            z = A * x + B * y + C
            # Bug
            # z = sp.Rational(3, 2) * x + y + 2
            x_min = - (b ** 2 - 4 * a * c) / (4 * a) if a > 0 else min(f.subs(y, roz[0]), f.subs(y, roz[1]))
            x_max = max(f.subs(y, roz[0]), f.subs(y, roz[1])) if a > 0 else - (b ** 2 - 4 * a * c) / (4 * a)
            szerokosc = max(f.subs(y, roz[0]), f.subs(y, roz[1])) + (b ** 2 - 4 * a * c) / (4 * a) if a > 0 else \
                - (b ** 2 - 4 * a * c) / (4 * a) - (min(f.subs(y, roz[0]), f.subs(y, roz[1])))

            wysokosc = max(roz) - min(roz)
            # print(x_min, x_max)
            # print(szerokosc, wysokosc)
            f_i = sp.solve(x - f, y)
            g_i = sp.solve(x - g, y)
            p = plot_parametric((x, f_i[0]), (x, f_i[1]), (x, g_i),
                                (x, -100, 100),
                                n=50000,
                                xlabel="x",
                                ylabel="y",
                                use_cm=False,
                                label=(f'y=${sp.latex(f_i[0])}$', f'y=${sp.latex(f_i[1])}$', f'y=${sp.latex(g_i[0])}$'),
                                markers=[
                                    {"args": [f.subs(y, roz[0]), roz[0]], "marker": "o",
                                     "linestyle": "None", 'markersize': '10',
                                     'label': f'A={f.subs(y, roz[0]), roz[0]}'},
                                    {"args": [f.subs(y, roz[1]), roz[1]], "marker": "o",
                                     "linestyle": "None", 'markersize': '10',
                                     'label': f'B={f.subs(y, roz[1]), roz[1]}'},
                                    {"args": [f.subs(y, -b / (2 * a)), -b / (2 * a)], "marker": "o",
                                     "linestyle": "None", 'markersize': '10',
                                     'label': f'W={(f.subs(y, sp.Rational(-b, 2 * a))), sp.Rational(-b, 2 * a)}'},
                                ],
                                # xlim=(min(roz) - 1 if szerokosc > wysokosc else (min(roz) + max(
                                #         roz)) / 2 - wysokosc / 2 - 1,
                                #     max(roz) + 1 if szerokosc > wysokosc else (min(roz) + max(
                                #         roz)) / 2 + wysokosc / 2 + 1),
                                # ylim=((x_min + x_max) / 2 - szerokosc / 2 - 1 if szerokosc > wysokosc else x_min - 1,
                                #       (x_min + x_max) / 2 + szerokosc / 2 + 1 if szerokosc > wysokosc else x_max + 1),
                                xlim=((x_min + x_max) / 2 - szerokosc / 2 - 1 if szerokosc > wysokosc else x_min - 1,
                                      (x_min + x_max) / 2 + szerokosc / 2 + 1 if szerokosc > wysokosc else x_max + 1),
                                ylim=(
                                    min(roz) - 1 if szerokosc > wysokosc else (min(roz) + max(
                                        roz)) / 2 - wysokosc / 2 - 1,
                                    max(roz) + 1 if szerokosc > wysokosc else (min(roz) + max(
                                        roz)) / 2 + wysokosc / 2 + 1),

                                # aspect=(1, 1),
                                title=f'Obszar całkowania względem osi Ox',
                                show=False,
                                # use_latex=True,
                                size=(4.5, 4.5),
                                )
            p.save(f'./pics/calka_podwojna{nr_zadania}x.pdf')
            p.save(f'./pics/calka_podwojna{nr_zadania}x.png')
            p.close()

            y_min = x_min
            y_max = x_max
            # print((y_min + y_max) / 2 - szerokosc / 2 + 1 if szerokosc > wysokosc else y_min - 1,
            #       (y_min + y_max) / 2 + szerokosc / 2 - 1 if szerokosc > wysokosc else y_max + 1)
            p = plot_parametric((y, f), (y, g),
                                (y, -100, 100),  # inaczej obcina dziedzinę funkcji do -10,10
                                use_cm=False,
                                markers=[
                                    {"args": [roz[0], f.subs(y, roz[0])], "marker": "o",
                                     "linestyle": "None", 'markersize': '10',
                                     'label': f'A={f.subs(y, roz[0]), roz[0]}'},
                                    {"args": [roz[1], f.subs(y, roz[1])], "marker": "o",
                                     "linestyle": "None", 'markersize': '10',
                                     'label': f'B={f.subs(y, roz[1]), roz[1]}'},
                                    {"args": [-b / (2 * a), f.subs(y, -b / (2 * a))], "marker": "o",
                                     "linestyle": "None", 'markersize': '10',
                                     'label': f'W={f.subs(y, sp.Rational(-b, 2 * a)), (sp.Rational(-b, 2 * a))}'},
                                ],
                                # xlim=((x_min + x_max) / 2 - szerokosc / 2 - 1 if szerokosc > wysokosc else x_min - 1,
                                #       (x_min + x_max) / 2 + szerokosc / 2 + 1 if szerokosc > wysokosc else x_max + 1),
                                # ylim=(
                                #     min(roz) - 1 if szerokosc > wysokosc else (min(roz) + max(
                                #         roz)) / 2 - wysokosc / 2 - 1,
                                #     max(roz) + 1 if szerokosc > wysokosc else (min(roz) + max(
                                #         roz)) / 2 + wysokosc / 2 + 1),
                                xlim=(max(roz) + 1 if szerokosc > wysokosc else (min(roz) + max(
                                    roz)) / 2 + wysokosc / 2 + 1,
                                      min(roz) - 1 if szerokosc > wysokosc else (min(roz) + max(
                                          roz)) / 2 - wysokosc / 2 - 1),
                                ylim=((x_min + x_max) / 2 - szerokosc / 2 - 1 if szerokosc > wysokosc else x_min - 1,
                                      (x_min + x_max) / 2 + szerokosc / 2 + 1 if szerokosc > wysokosc else x_max + 1),
                                label=(f'x=${sp.latex(f)}$', f'x=${sp.latex(g)}$'),

                                n=100000,  # dużo by nie było przerwy przy wierzchołku
                                title=f'Obszar całkowania względem osi Oy',
                                xlabel="y",
                                ylabel="x",
                                # aspect=(1, 1),
                                show=False,
                                # use_latex=True,
                                size=(4.5, 4.5),
                                )
            # print(sp.Rational(-b, 2 * a),f.subs(y, sp.Rational(-b, 2 * a)))
            p.save(f'./pics/calka_podwojna{nr_zadania}y.pdf')
            p.save(f'./pics/calka_podwojna{nr_zadania}y.png')
            p.close()

            wynik_y = sp.integrate(z, (x, f, g), (y, min(roz), max(roz))) * (1 if a > 0 else -1)
            calka_y = (
                    f"\\int\\limits_{{{min(roz)}}}^{{{max(roz)}}}\\left(\\int\\limits_{{{sp.latex(f) if a > 0 else sp.latex(g)}}}^{{{sp.latex(g) if a > 0 else sp.latex(f)}}}\\left({sp.latex(z)}\\right)dx\\right)dy" +
                    f"\n\t=\ldots=\\int\\limits_{{{min(roz)}}}^{{{max(roz)}}}\\left({sp.latex(sp.integrate(z, (x, f, g)).expand()) if a > 0 else sp.latex(sp.integrate(z, (x, g, f)).expand())}\\right)dy")

            zadanie = f"\\iint\\limits_D\\left({sp.latex(z)}\\right)dx\\,dy"
            return (
                f'Obliczyć $${zadanie}$$ gdzie $D$ - obszar ograniczony krzywymi $x={sp.latex(f)}$, oraz $x={sp.latex(g)}$',
                f'\\includegraphics[width=45mm]{{../pics/calka_podwojna{nr_zadania}x}}\n' +
                f'\t\\includegraphics[width=45mm]{{../pics/calka_podwojna{nr_zadania}y}}\\\\\n' +
                '\tWzględem $Oy:$ $' + calka_y + ' = \ldots = ' + sp.latex(wynik_y) + '$ \\\\')

        return ('', '')

    else:
        return ('Nie ma takiego przypadku w całce podwójnej', '')


if __name__ == "__main__":
    start = time.time()
    for i in range(1):
        polecenie, rozwiazanie = calka_podwojna(typ=2, nr_zadania=i)
        print(polecenie, '\n', rozwiazanie)
    print(f'czas generowania: {round(time.time() - start, 3)}s')
