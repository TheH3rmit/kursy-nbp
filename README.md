# kursy-nbp
Projekt semestralny na przedmiot wprowadzenie do przetwarzania w chmurze

## Cel projektu
Celem projektu jest stworzenie automatycznego systemu
pobierania, przetwarzania i publikowania kursów walut
z API Narodowego Banku Polskiego.

## Skład zespołu
- Jakub - GitHub: @TheH3rmit 
- Marcel - Github: @Marcelinder
- Filip - Github: @filip11990

## Podział obowiązków

## Architektura projektu

``` mermaid
flowchart TD
    A["GitHub Actions<br/>Harmonogram / ręcznie"]
    B["Python - pobieranie danych"]
    C["NBP REST API"]
    D["Walidacja i transformacja<br/>Kontrola duplikatów"]
    E[("CSV - historia kursów")]
    F["Generowanie HTML i wykresów"]
    G["Zapis zmian do repozytorium"]
    H["GitHub Pages"]

    A --> B
    B -->|"Żądanie HTTP"| C
    C -->|"Kursy EUR, USD, GBP"| B
    B --> D
    D --> E
    E --> F
    F --> G
    G --> H
```
