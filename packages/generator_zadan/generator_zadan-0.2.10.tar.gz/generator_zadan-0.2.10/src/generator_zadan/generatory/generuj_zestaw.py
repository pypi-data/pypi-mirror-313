import datetime  # do pobierania daty
import textwrap

import babel.dates  # do ładnego generowania daty


def dodaj_zadanie(zadanie, warstwa):
    polecenie, rozwiazanie = zadanie
    polecenie = '\\item ' + polecenie + '\n'
    polecenie = textwrap.indent(polecenie, prefix='\t\t')
    rozwiazanie = f'\\zOdpowiedziami{{\\kolorodpowiedzi}}{{ocg{warstwa}}}\n\t{{{rozwiazanie}}}\n\n'
    rozwiazanie = textwrap.indent(rozwiazanie, prefix='\t\t\t')
    return polecenie + rozwiazanie


def generuj_LaTeX(kierunek,
                  grupa,
                  przedmiot,
                  semestr,
                  kolokwium,
                  data,
                  kolor_odpowiedzi,
                  *zadania):
    plik_tex = ('% !TeX spellcheck = pl_PL-Polish\n'
                '\\documentclass[a4paper,12pt]{article}\n'  # można zmieniać rozmiar czcionki
                '\\linespread{1.3} %odstepy miedzy liniami\n'
                '\\usepackage[a4paper, lmargin=2cm, rmargin=2cm, tmargin=2cm, bmargin=2cm]{geometry}\n'
                '\\usepackage{amsfonts}\n'
                '\\usepackage{amsmath}\n'
                '\\usepackage{color}\n'
                '\\usepackage{enumitem}\n'
                '\\usepackage{fancyhdr}\n'
                '\\usepackage{float}\n'
                '\\usepackage{graphicx}\n'  # do pdf
                '\\usepackage{ifthen}\n'
                '\\usepackage[utf8]{inputenc}\n'
                '\\usepackage{lmodern}\n'
                '\\usepackage{ocgx}\n'
                # '\\usepackage{pgf}\n'  # niepotrzebne gdy importujemy pdf-y
                '\\usepackage{polski}\n'
                '\\usepackage{tcolorbox}\n'
                '\\tcbuselibrary{most}\n'
                '\\tcbuselibrary{skins}\n'
                '\\tcbuselibrary{raster}\n'
                '% brak - bez odpowiedzi i bez miejsca, white - bez odpowiedzi z miejscem, red = odpowiedzi ukryte ale dostepne\n'
                f'\\newcommand{{\kolorodpowiedzi}}{{{kolor_odpowiedzi}}}\n'
                '\\renewcommand{\\footrulewidth}{0.4pt}% linia pozioma na końcu strony - default is 0pt\n'
                '\\DeclareFontShape{OMX}{cmex}{m}{n}\n'
                '    {<-7.5> cmex7\n'
                '    <7.5-8.5> cmex8\n'
                '    <8.5-9.5> cmex9\n'
                '    <9.5-> cmex10}{}\n'
                '\\DeclareSymbolFont{largesymbols}{OMX}{cmex}{m}{n}\n\n'
                # '\\newcommand{\\zOdpowiedziami}[1]{\n'
                # '\t\\ifthenelse{\\equal{#1}{brak}}{\\hphantom}{\n'
                # '\t\t\\ifthenelse{\\equal{#1}{white}}{\\vphantom}{\n'
                # '\t\t\t\\textcolor{\\kolorodpowiedzi}}}}\n\n'
                '\n'
                '\\newcommand{\\ukryte}{1}  % domyślnie odpowiedzi są do pokazywania po kliknięciu\n'
                '\\ifthenelse{\\equal{\\kolorodpowiedzi}{red}}  % ukrywamy od pokazywania gdy kolor jest red\n'
                '\t{\\renewcommand{\\ukryte}{0}}{}\n\n'
                '\\newcommand{\\zOdpowiedziami}[3]{\n'
                '\t\\ifthenelse{\\equal{#1}{brak}}{}{\n'
                '\t\t\\ifthenelse{\\equal{#1}{white}}{\\vphantom{#3}}{\n'
                '\t\t\t\\switchocg{#2}{\\textcolor{\\kolorodpowiedzi}{\\\\Rozwiązanie: }}\n'
                '\t\t\t\t\\begin{ocg}{Warstwa odpowiedzi}{#2}{\\ukryte}\n'
                '\t\t\t\t\t\\textcolor{\kolorodpowiedzi}{#3}\n'
                '\t\t\t\t\\end{ocg}}}}\n\n'
    
                '\\pdfinfo{/Author (https://generator-zadan.readthedocs.io)}\n\n'

                '\\begin{document}\n'
                '    \\pagestyle{fancy}\n'
                '    \\setlength{\headheight}{27.29453pt}\n'
                '    \\fancyhead{}\n'
                '    \\fancyhead[L]{\\textbf{' + kierunek + '\\\\' + przedmiot + ' - ' + grupa + '}}\n'
                                                                                                 '    \\fancyhead[R]{\\textbf{' + kolokwium + '\\\\ ' + data + '}}' + '\n' +
                '    \\fancyfoot{}' + '\n' +
                '    \\fancyfoot[R]{\\tiny\\textbf{' +
                babel.dates.format_datetime(datetime.datetime.now(), "d MMMM yyyy, HH:mm", locale='pl_PL') + '}}\n' +
                '%    \hspace{1cm}\n' +
                r'    \begin{enumerate}[label= \textbf{Zadanie \arabic*. },' +
                ' leftmargin=1cm, align=left, itemsep=0pt]' + '\n'
                )
    for n, zadanie in enumerate(zadania):
        plik_tex += dodaj_zadanie(zadanie, n)

    plik_tex += (r'    \end{enumerate}' + '\n'
                 + '\end{document}')
    return plik_tex
