# generator_zadan

Utworzone na użytek własny. Licencja poniżej. 

Pakiet __`generator_zadan`__ zawiera zdefiniowane funkcje generujące różnego typu zadania dla studentów pierwszego roku uczelni technicznej.

Wszystkie funkcje generujące oparte są na losowo generowanych danych, by uzyskać maksymalną różnorodność w zakresie danego typu zadania.

Zadania mają mieć __eleganckie__ parametry i wyniki mają być __przyjazne__ dla człowieka.

Z biegiem czasu pewnie będzie więcej typów.


## Instalacja

```
pip install generator_zadan
```
lub (nawet lepsze, bo od razu można generować zestawy)

```
git clone https://github.com/DyonOylloug/generator_zadan
cd generator_zadan
pip install .
```

## Jak to działa?

Funkcje zwracają zadanie w formacie krotki składającej się z dwóch części:

- Polecenie w formacie __`LaTeX`__ 
- Rozwiązanie w formacie __`LaTeX`__  (może zawierać obrazy)

Np.

```
import generator_zadan.generatory as gz

zadanie = gz.rownanie_prostej()
zadanie
```

    ('Wyznaczyć równanie prostej przechodzącej przez punkty\n\t\\[\n\t\tP_1 = (5, 5, 3), \\quad P_2 = (2, -1, 5).\n\t\\]\n\tObliczyć odległość wyznaczonej prostej od punktu\n\t\\[\n\t\tP_3 = (5, 2, 1).\n\t\\]',
     '$l\\colon  \\frac{x - 5}{-3}= \\frac{y - 5}{-6}= \\frac{z - 3}{2}; \\qquad d(P_3,l) = 3$')



W bardziej czytelnej postaci wygląda to następująco


```
print(zadanie[0])  # pierwszy element to polecenie
print('-'*80)      # oddzielenie części
print(zadanie[1])  # drugi element to rozwiązanie
```

    Wyznaczyć równanie prostej przechodzącej przez punkty
    	\[
    		P_1 = (5, 5, 3), \quad P_2 = (2, -1, 5).
    	\]
    	Obliczyć odległość wyznaczonej prostej od punktu
    	\[
    		P_3 = (5, 2, 1).
    	\]
    --------------------------------------------------------------------------------
    $l\colon  \frac{x - 5}{-3}= \frac{y - 5}{-6}= \frac{z - 3}{2}; \qquad d(P_3,l) = 3$
    

Docelowa forma wygląda następująco

> **Zadanie**
> 
> Wyznaczyć równanie prostej przechodzącej przez punkty
> 
> $$	P_1 = (5, 5, 3), \quad P_2 = (2, -1, 5).$$
> 
> Obliczyć odległość wyznaczonej prostej od punktu
> 
> $$	P_3 = (5, 2, 1).$$


> **Rozwiązanie**
> 
> $$l\colon  \frac{x - 5}{-3}= \frac{y - 5}{-6}= \frac{z - 3}{2}; \qquad d(P_3,l) = 3$$
 





I to w zasadzie tyle. 
Więcej przykładów w odpowiednich sekcjach tematyczynych [dokumentacji](https://generator-zadan.readthedocs.io/en/latest/index.html). 

W sekcji [Generuj zestaw zadań](https://generator-zadan.readthedocs.io/en/latest/generuj_zestaw.html) 
po uruchomieniu interaktywnej sesji notebooka można wygenerować swój zestaw.


## Dokumentacja

-  Dokumentacja na stronie [readthedocs.](https://generator-zadan.readthedocs.io/en/latest/index.html)

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`generator_zadan` was created by Adam Bohonos. It is licensed under the terms of the MIT license.

## Credits

`generator_zadan` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
