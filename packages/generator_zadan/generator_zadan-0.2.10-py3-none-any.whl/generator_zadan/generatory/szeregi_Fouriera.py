import os
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
import numpy as np
import sympy as sp
from matplotlib.backends.backend_pdf import PdfPages
from spb import plot_piecewise




def szereg_Fouriera(
        typ_l: int = 1,
        typ_p: int = 1,
        bez_wykresu: bool = False,
        tylko_koncowy: bool = False,
        nr_zadania: int = 1):
    ''' Następne linijki likwidują konflikt z innymi modułami
    Strasznie to głupie - powiązane z plt.rc('text', usetex=False)
    Chodzi o konfikt generowania wykresów używających TeX - matplotlib i problematycznych Sympy Plot'''
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    ''' Poprzednie linijki likwidują konflikt z innymi modułami 
    Strasznie to głupie - powiązane z plt.rc('text', usetex=False)
    Chodzi o konfikt generowania wykresów używających TeX - matplotlib i problematycznych Sympy Plot'''

    if bez_wykresu is not True and not os.path.exists('pics'):
        os.makedirs('pics')
        print(" ! Tworzę katalog pics ", file=sys.stderr)
    x = sp.Symbol('x', Real=True)
    n = sp.symbols('n', integer=True, positive=True)
    okres_z_pi = random.choice([False, True])

    if typ_l == 0:  # by nie wypadła funkcja stała
        if typ_p == 0:
            while True:
                a = random.randint(-2, 2)
                b = random.randint(-2, 2)
                if a != b:
                    f_left = a * x / x
                    f_right = b * x / x
                    break
        else:
            a = random.randint(-2, 2)
            f_left = a * x / x

    if typ_l == 1:  # by nie wypadła funkcja stała
        f_left = (-1) ** random.randint(0, 1) * random.randint(1, 2) * x + random.randint(-2, 2) * x / x
    if typ_l == 2:
        f_left = (-1) ** random.randint(0, 1) * x ** 2
    if typ_l == 3:
        f_left = (-1) ** random.randint(0, 1) * sp.sin(x)
    if typ_l == 4:
        f_left = (-1) ** random.randint(0, 1) * sp.cos(x)
    if typ_p == 0:  # by nie wypadła funkcja stała
        if typ_l == 0:
            while True:
                a = random.randint(-2, 2)
                b = random.randint(-2, 2)
                if a != b:
                    f_left = a * x / x
                    f_right = b * x / x
                    break
        else:
            b = random.randint(-2, 2)
            f_right = b * x / x
    if typ_p == 1:  # by nie wypadła funkcja stała
        f_right = (-1) ** random.randint(0, 1) * random.randint(1, 2) * x + random.randint(-2, 2) * x / x
    if typ_p == 2:
        f_right = (-1) ** random.randint(0, 1) * x ** 2
    if typ_p == 3:
        f_right = (-1) ** random.randint(0, 1) * sp.sin(x)
    if typ_p == 4:
        f_right = (-1) ** random.randint(0, 1) * sp.cos(x)
    T = random.randint(1, 2) if okres_z_pi is False else random.randint(1, 3) * sp.pi / 2

    lewostronnie_0 = random.choice([False, True])
    lewostronnie_T = random.choice([False, True])
    # print(typ_l, f_left, typ_p, f_right, lewostronnie_0, lewostronnie_T)
    funkcja = [[(f_left.subs(x, x - 2 * i * T), (x < (2 * i) * T if lewostronnie_0 else x <= (2 * i) * T)),
                (f_right.subs(x, x - 2 * i * T), (x < (2 * i + 1) * T if lewostronnie_T else x <= (2 * i + 1) * T))] for
               i in range(-9, 10, 1)]
    f = sp.Piecewise(*sum(funkcja, []))

    a0 = (
        T ** (-1) * sp.integrate(f, (x, -T, T)).simplify() if okres_z_pi else sp.Rational(1, T) * sp.integrate(f, (
            x, -T, T)).simplify())
    an = (
        T ** (-1) * sp.integrate(f * sp.cos(n * sp.pi * x / T),
                                 (x, -T, T)).simplify() if okres_z_pi else sp.Rational(1,
                                                                                       T) * sp.integrate(
            f * sp.cos(n * sp.pi * x / T), (x, -T, T)).simplify())
    # n = sp.symbols('n', integer=True, positive=True)
    bn = (
        T ** (-1) * sp.integrate(f * sp.sin(n * sp.pi * x / T),
                                 (x, -T, T)).simplify() if okres_z_pi else sp.Rational(1,
                                                                                       T) * sp.integrate(
            f * sp.sin(n * sp.pi * x / T), (x, -T, T)).simplify())



    def F_n(ile_wyrazow: int):
        return a0 / 2 + sum(
            [an.subs(n, i) * sp.cos(i * sp.pi * x / T) + bn.subs(n, i) * sp.sin(i * sp.pi * x / T) for i in
             range(1, ile_wyrazow + 1)])
    if bez_wykresu is not True or tylko_koncowy is True:
        if not os.path.exists('pics'):
            os.makedirs('pics')
            print(" ! Tworzę katalog pics ", file=sys.stderr)
        with PdfPages(f'./pics/szereg_Fouriera_{nr_zadania}.pdf') as pdf:
            if tylko_koncowy is not True:
                wykres = plot_piecewise(f, {"alpha": 0},  # niewidzialny dla pierwszej strony w odpowiedziach
                                        xlim=(
                                            (max(-10, -4.4 * T), min(4.4 * T, 10)) if okres_z_pi is False else (
                                                -3 * sp.pi - 0.2, 3 * sp.pi + 0.2)),
                                        size=(10, 2.5),
                                        adaptive=False,
                                        nb_of_points=1000,
                                        dots=True,
                                        legend=True,
                                        label=[f"$f(x)$"],
                                        ylabel='',
                                        title=f'Funkcja $f(x)$',
                                        show=False)
                ax = wykres.ax
                plt.legend(loc='center right')
                if okres_z_pi:
                    ax.set_xticks([0.5 * i * np.pi for i in range(-6, 7)])
                    ax.set_xticks(list(ax.get_xticks()),
                                  ["$-3\pi$", "$-\\frac{5}{2}\pi$", "$-2\pi$", "$-\\frac{3}{2}\pi$", "$-\pi$",
                                   "$-\\frac{1}{2}\pi$",
                                   "$0$", "$\\frac{1}{2}\pi$", "$\pi$", '$\\frac{3}{2}\pi$', '$2\pi$', '$\\frac{5}{2}\pi$',
                                   '$3\pi$']);
                pdf.savefig(bbox_inches="tight")
                wykres.close()
                wykres = plot_piecewise(f,
                                        xlim=(
                                            (max(-10, -4.4 * T), min(4.4 * T, 10)) if okres_z_pi is False else (
                                                -3 * sp.pi - 0.2, 3 * sp.pi + 0.2)),
                                        size=(10, 2.5),
                                        adaptive=False,
                                        nb_of_points=1000,
                                        dots=True,
                                        legend=True,
                                        label=[f"$f(x)$"],
                                        ylabel='',
                                        title=f'Funkcja $f(x)$',
                                        show=False)
                ax = wykres.ax
                plt.legend(loc='center right')
                if okres_z_pi:
                    ax.set_xticks([0.5 * i * np.pi for i in range(-6, 7)])
                    ax.set_xticks(list(ax.get_xticks()),
                                  ["$-3\pi$", "$-\\frac{5}{2}\pi$", "$-2\pi$", "$-\\frac{3}{2}\pi$", "$-\pi$",
                                   "$-\\frac{1}{2}\pi$",
                                   "$0$", "$\\frac{1}{2}\pi$", "$\pi$", '$\\frac{3}{2}\pi$', '$2\pi$', '$\\frac{5}{2}\pi$',
                                   '$3\pi$']);
                # wykres.save(f'./pics/szereg_Fouriera_{nr_zadania}_funkcja.pdf', dpi=300, bbox_inches="tight")
                pdf.savefig(bbox_inches="tight")
                wykres.close()

                # if a0 != 0:
                wykres = plot_piecewise(f, a0 / 2,
                                        xlim=(
                                            (max(-10, -4.4 * T), min(4.4 * T, 10)) if okres_z_pi is False else (
                                                -3 * sp.pi - 0.2, 3 * sp.pi + 0.2)),
                                        size=(10, 2.5),
                                        nb_of_points=1000,
                                        dots=True,
                                        legend=True,
                                        label=["$f(x)$", "$\\frac{a_0}{2}$"],
                                        ylabel='',
                                        title=f'Funkcja $f(x)$ i zerowy element jej szeregu Fouriera',
                                        show=False)
                ax = wykres.ax
                plt.legend(loc='center right')
                if okres_z_pi:
                    ax.set_xticks([0.5 * i * np.pi for i in range(-6, 7)])
                    ax.set_xticks(list(ax.get_xticks()),
                                  ["$-3\pi$", "$-\\frac{5}{2}\pi$", "$-2\pi$", "$-\\frac{3}{2}\pi$", "$-\pi$",
                                   "$-\\frac{1}{2}\pi$",
                                   "$0$", "$\\frac{1}{2}\pi$", "$\pi$", '$\\frac{3}{2}\pi$', '$2\pi$', '$\\frac{5}{2}\pi$',
                                   '$3\pi$']);
                # wykres.save(f'./pics/Szereg_Fouriera_{nr_zadania}_0.png', dpi=300, bbox_inches="tight")
                pdf.savefig(bbox_inches="tight")
                wykres.close()

                wykres = plot_piecewise(f, F_n(1),
                                        xlim=(
                                            (max(-10, -4.4 * T), min(4.4 * T, 10)) if okres_z_pi is False else (
                                                -3 * sp.pi - 0.2, 3 * sp.pi + 0.2)),
                                        size=(10, 2.5),
                                        nb_of_points=1000,
                                        dots=True,
                                        legend=True,
                                        label=["$f(x)$", f"$S_1(x)$"],
                                        ylabel='',
                                        title=f'Funkcja $f(x)$ i $S_1(x)$ jej szeregu Fouriera',
                                        show=False)
                ax = wykres.ax
                plt.legend(loc='center right')
                if okres_z_pi:
                    ax.set_xticks([0.5 * i * np.pi for i in range(-6, 7)])
                    ax.set_xticks(list(ax.get_xticks()),
                                  ["$-3\pi$", "$-\\frac{5}{2}\pi$", "$-2\pi$", "$-\\frac{3}{2}\pi$", "$-\pi$", "$-\\frac{1}{2}\pi$",
                                   "$0$", "$\\frac{1}{2}\pi$", "$\pi$", '$\\frac{3}{2}\pi$', '$2\pi$', '$\\frac{5}{2}\pi$',
                                   '$3\pi$']);
                # wykres.save(f'./pics/Szereg_Fouriera_{nr_zadania}_1.png', dpi=300, bbox_inches="tight")
                pdf.savefig(bbox_inches="tight")
                wykres.close()
            #
            if tylko_koncowy is not True:
                for ile_wyrazow in range(2, 20, 1):
                    wykres = plot_piecewise(f, F_n(ile_wyrazow),
                                            xlim=(
                                                (max(-10, -4.4 * T), min(4.4 * T, 10)) if okres_z_pi is False else (
                                                    -3 * sp.pi - 0.2, 3 * sp.pi + 0.2)),
                                            size=(10, 2.5),
                                            nb_of_points=1000 * ile_wyrazow,
                                            dots=True,
                                            legend=True,
                                            label=["$f(x)$", f"$S_{{{ile_wyrazow}}}(x)$"],
                                            ylabel='',
                                            title=f'Funkcja $f(x)$ i $S_{{{ile_wyrazow}}}(x)$  jej szeregu Fouriera',
                                            show=False)
                    ax = wykres.ax
                    plt.legend(loc='center right')
                    if okres_z_pi:
                        ax.set_xticks([0.5 * i * np.pi for i in range(-6, 7)])
                        ax.set_xticks(list(ax.get_xticks()),
                                      ["$-3\pi$", "$-\\frac{5}{2}\pi$", "$-2\pi$", "$-\\frac{3}{2}\pi$", "$-\pi$",
                                       "$-\\frac{1}{2}\pi$",
                                       "$0$", "$\\frac{1}{2}\pi$", "$\pi$", '$\\frac{3}{2}\pi$', '$2\pi$', '$\\frac{5}{2}\pi$',
                                       '$3\pi$']);
                    # wykres.save(f'./pics/Szereg_Fouriera_{nr_zadania}_{ile_wyrazow}.png', dpi=300, bbox_inches="tight")
                    pdf.savefig(bbox_inches="tight")
                    wykres.close()
            if tylko_koncowy is not True:
                for ile_wyrazow in range(20, 110, 10):
                    wykres = plot_piecewise(f, F_n(ile_wyrazow),
                                            xlim=(
                                                (max(-10, -4.4 * T), min(4.4 * T, 10)) if okres_z_pi is False else (
                                                    -3 * sp.pi - 0.2, 3 * sp.pi + 0.2)),
                                            size=(10, 2.5),
                                            nb_of_points=1000 * ile_wyrazow,
                                            dots=True,
                                            legend=True,
                                            label=["$f(x)$", f"$S_{{{ile_wyrazow}}}(x)$"],
                                            ylabel='',
                                            title=f'Funkcja $f(x)$ i $S_{{{ile_wyrazow}}}(x)$ jej szeregu Fouriera',
                                            show=False)
                    ax = wykres.ax
                    plt.legend(loc='center right')
                    if okres_z_pi:
                        ax.set_xticks([0.5 * i * np.pi for i in range(-6, 7)])
                        ax.set_xticks(list(ax.get_xticks()),
                                      ["$-3\pi$", "$-\\frac{5}{2}\pi$", "$-2\pi$", "$-\\frac{3}{2}\pi$", "$-\pi$",
                                       "$-\\frac{1}{2}\pi$",
                                       "$0$", "$\\frac{1}{2}\pi$", "$\pi$", '$\\frac{3}{2}\pi$', '$2\pi$', '$\\frac{5}{2}\pi$',
                                       '$3\pi$']);
                   # wykres.save(f'./pics/Szereg_Fouriera_{nr_zadania}_{ile_wyrazow}.png', dpi=300, bbox_inches="tight")
                    pdf.savefig(bbox_inches="tight")
                    wykres.close()
            if tylko_koncowy is not True:
                for ile_wyrazow in range(200, 1001, 800):
                    wykres = plot_piecewise(f, F_n(ile_wyrazow),
                                            xlim=(
                                                (max(-10, -4.4 * T), min(4.4 * T, 10)) if okres_z_pi is False else (
                                                    -3 * sp.pi - 0.2, 3 * sp.pi + 0.2)),
                                            size=(10, 2.5),
                                            nb_of_points=1000 * ile_wyrazow,
                                            dots=True,
                                            legend=True,
                                            label=["$f(x)$", f"$S_{{{ile_wyrazow}}}(x)$"],
                                            ylabel='',
                                            title=f'Funkcja $f(x)$ i $S_{{{ile_wyrazow}}}(x)$ jej szeregu Fouriera',
                                            show=False)
                    ax = wykres.ax
                    plt.legend(loc='center right')
                    if okres_z_pi:
                        ax.set_xticks([0.5 * i * np.pi for i in range(-6, 7)])
                        ax.set_xticks(list(ax.get_xticks()),
                                      ["$-3\pi$", "$-\\frac{5}{2}\pi$", "$-2\pi$", "$-\\frac{3}{2}\pi$", "$-\pi$",
                                       "$-\\frac{1}{2}\pi$",
                                       "$0$", "$\\frac{1}{2}\pi$", "$\pi$", '$\\frac{3}{2}\pi$', '$2\pi$', '$\\frac{5}{2}\pi$',
                                       '$3\pi$']);
                   # wykres.save(f'./pics/Szereg_Fouriera_{nr_zadania}_{ile_wyrazow}.png', dpi=300, bbox_inches="tight")
                    pdf.savefig(bbox_inches="tight")
            if tylko_koncowy is True:
                wykres = plot_piecewise(f,
                                        xlim=(
                                            (max(-10, -4.4 * T), min(4.4 * T, 10)) if okres_z_pi is False else (
                                                -3 * sp.pi - 0.2, 3 * sp.pi + 0.2)),
                                        size=(10, 2.5),
                                        adaptive=False,
                                        nb_of_points=1000,
                                        dots=True,
                                        legend=True,
                                        label=[f"$f(x)$"],
                                        ylabel='',
                                        title=f'Funkcja $f(x)$',
                                        show=False)
                ax = wykres.ax
                plt.legend(loc='center right')
                if okres_z_pi:
                    ax.set_xticks([0.5 * i * np.pi for i in range(-6, 7)])
                    ax.set_xticks(list(ax.get_xticks()),
                                  ["$-3\pi$", "$-\\frac{5}{2}\pi$", "$-2\pi$", "$-\\frac{3}{2}\pi$", "$-\pi$",
                                   "$-\\frac{1}{2}\pi$",
                                   "$0$", "$\\frac{1}{2}\pi$", "$\pi$", '$\\frac{3}{2}\pi$', '$2\pi$', '$\\frac{5}{2}\pi$',
                                   '$3\pi$']);
                wykres.save(f'./pics/szereg_Fouriera_{nr_zadania}_funkcja.png', dpi=300, bbox_inches="tight")
                wykres.close()

            srednia_T = sp.Rational(1, 2) * (sp.limit(f_left, x, -T, '+') + sp.limit(f_right, x, T, '-'))
            srednia_0 = sp.Rational(1, 2) * (sp.limit(f_left, x, 0, '-') + sp.limit(f_right, x, 0, '+'))
            funkcja = [[(f_left.subs(x, x - 2 * i * T), x < (2 * i) * T), (srednia_0, sp.Eq(x, (2 * i) * T)),
                        (f_right.subs(x, x - 2 * i * T), x < (2 * i + 1) * T), (srednia_T, sp.Eq(x, (2 * i + 1) * T))] for
                       i in range(-9, 10, 1)]
            f = sp.Piecewise(*sum(funkcja, []))
            wykres = plot_piecewise(f, {"color": "C1"},
                                    xlim=(
                                        (max(-10, -4.4 * T), min(4.4 * T, 10)) if okres_z_pi is False else (
                                            -3 * sp.pi - 0.2, 3 * sp.pi + 0.2)),
                                    size=(10, 2.5),
                                    nb_of_points=1000,
                                    dots=True,
                                    legend=True,
                                    label=["$S_{{{\\infty}}}(x)$"],
                                    ylabel='',
                                    title=f'Suma szeregu Fouriera funkcji $f(x)$',
                                    show=False)
            ax = wykres.ax
            plt.legend(loc='center right')
            if okres_z_pi:
                ax.set_xticks([0.5 * i * np.pi for i in range(-6, 7)])
                ax.set_xticks(list(ax.get_xticks()),
                              ["$-3\pi$", "$-\\frac{5}{2}\pi$", "$-2\pi$", "$-\\frac{3}{2}\pi$", "$-\pi$",
                               "$-\\frac{1}{2}\pi$",
                               "$0$", "$\\frac{1}{2}\pi$", "$\pi$", '$\\frac{3}{2}\pi$', '$2\pi$', '$\\frac{5}{2}\pi$',
                               '$3\pi$']);
            if tylko_koncowy is True:
                wykres.save(f'./pics/szereg_Fouriera_{nr_zadania}_inf.png', dpi=300, bbox_inches="tight")
            pdf.savefig(bbox_inches="tight")
            wykres.close()

    if lewostronnie_0 and lewostronnie_T:
        funkcja = (f'\t\t\t{sp.latex(f_left)} & \\textnormal{{ dla }} & x\\in\\left[{sp.latex(-T)},0\\right)\\\\\n'
                   f'\t\t\t{sp.latex(f_right)} & \\textnormal{{ dla }} & x\\in\\left[0,{sp.latex(T)}\\right)\n')
    if lewostronnie_0 and not lewostronnie_T:
        funkcja = (f'\t\t\t{sp.latex(f_left)} & \\textnormal{{ dla }} & x\\in\\left({sp.latex(-T)},0\\right)\\\\\n'
                   f'\t\t\t{sp.latex(f_right)} & \\textnormal{{ dla }} & x\\in\\left[0,{sp.latex(T)}\\right]\n')
    if not lewostronnie_0 and lewostronnie_T:
        funkcja = (f'\t\t\t{sp.latex(f_left)} & \\textnormal{{ dla }} & x\\in\\left[{sp.latex(-T)},0\\right]\\\\\n'
                   f'\t\t\t{sp.latex(f_right)} & \\textnormal{{ dla }} & x\\in\\left(0,{sp.latex(T)}\\right)\n')
    if not lewostronnie_0 and not lewostronnie_T:
        funkcja = (f'\t\t\t{sp.latex(f_left)} & \\textnormal{{ dla }} & x\\in\\left({sp.latex(-T)},0\\right]\\\\\n'
                   f'\t\t\t{sp.latex(f_right)} & \\textnormal{{ dla }} & x\\in\\left(0,{sp.latex(T)}\\right]\n')

    if tylko_koncowy is True:
        return (f'Rozwinąć w szereg Fouriera funkcję \n'
                f'\t\\[\n'
                f'\t\tf(x)=\\left\\{{\\begin{{matrix}}\n' +
                funkcja +
                f'\t\t\\end{{matrix}}\\right.\n'
                f'\t\\]\n'
                f'o okresie zasadniczym $2T={sp.latex(2*T)}.$'
                f' Naszkicować wykres funkcji, do której zbieżny jest uzyskany szereg.',
                f'$a_0={sp.latex(a0)},\\quad a_n={sp.latex(an)},\\quad b_n={sp.latex(bn)},$\\\\\n'
                f'\t$S(x) = {sp.latex(F_n(5)) if an == 0 or bn == 0 else sp.latex(F_n(3))} + \\dots $\\\\\n'
                f'\t\\includegraphics[width = 224pt]{{../pics/szereg_Fouriera_{nr_zadania}_funkcja}}\n'
                f'\t\\includegraphics[width = 224pt]{{../pics/szereg_Fouriera_{nr_zadania}_inf}}\n')
    elif bez_wykresu is True:
        return (f'Rozwinąć w szereg Fouriera funkcję \n'
                f'\t\\[\n'
                f'\t\tf(x)=\\left\\{{\\begin{{matrix}}\n' +
                funkcja +
                f'\t\t\\end{{matrix}}\\right.\n'
                f'\t\\]\n'
                f'o okresie zasadniczym $2T={sp.latex(2*T)}.$\n'
                f'Naszkicować wykres funkcji, do której zbieżny jest uzyskany szereg.',
                f'$a_0={sp.latex(a0)},\\quad a_n={sp.latex(an)},\\quad b_n={sp.latex(bn)},$\\\\\n'
                f'\t$S(x) = {sp.latex(F_n(5)) if an == 0 or bn == 0 else sp.latex(F_n(3))} + \\dots $')
    else:
        return (f'Rozwinąć w szereg Fouriera funkcję \n'
                f'\t\\[\n'
                f'\t\tf(x)=\\left\\{{\\begin{{matrix}}\n' +
                funkcja +
                f'\t\t\\end{{matrix}}\\right.\n'
                f'\t\\]\n'
                f'o okresie zasadniczym $2T={sp.latex(2*T)}.$'
                f' Naszkicować wykres funkcji, do której zbieżny jest uzyskany szereg.',
                f'$a_0={sp.latex(a0)},\\quad a_n={sp.latex(an)},\\quad b_n={sp.latex(bn)},$\\\\\n'
                f'\t$S(x) = {sp.latex(F_n(5)) if an == 0 or bn == 0 else sp.latex(F_n(3))} + \\dots $\\\\\n'
                f'\t\\animategraphics[height=5.3cm,controls=true]{{0.5}}\n'
                f'\t {{szereg_Fouriera_{nr_zadania}}}{{0}}{{100}}')



if __name__ == "__main__":  # to się uruchamia tylko, gdy plik jest uruchamiany jako program, a nie ładowany jako moduł
    start_time = time.time()
    for i in range(1):
        polecenie, rozwiazanie = szereg_Fouriera(typ_l=0, typ_p=0, bez_wykresu=True, nr_zadania=1)
        print(polecenie, '\n', rozwiazanie)
    print("Czas generowania --- %s seconds ---" % (time.time() - start_time))
