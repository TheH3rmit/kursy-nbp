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

#### Jakub – Automatyzacja i przetwarzanie danych
- Konfiguracja repozytorium i GitHub Actions.
- Przygotowanie harmonogramu uruchamiania w dni robocze.
- Implementacja pobierania kursów EUR, USD i GBP z API NBP.
- Walidacja i transformacja pobranych danych.
- Idempotentny zapis kursów do plików CSV.
- Obsługa dni bez tabel kursowych.
- Integracja komponentów projektu.

#### Andrzej – Dane historyczne
- Pobranie historii kursów z co najmniej trzech miesięcy.
- Uzupełnienie plików CSV danymi historycznymi.
- Sprawdzenie poprawności dat i kompletności danych.

#### Marcel – Prezentacja danych
- Generowanie strony HTML z aktualnymi kursami.
- Przygotowanie wykresów historycznych.
- Konfiguracja i publikacja strony przez GitHub Pages.

#### Filip – Dokumentacja i kosztorys
- Przygotowanie dokumentacji potoku danych w README.
- Opis architektury i schematu systemu.
- Wyjaśnienie wyboru harmonogramu UTC.
- Opis odpowiedników rozwiązania w AWS i Azure.
- Przygotowanie szacunkowego kosztorysu miesięcznego.

### Zadania wspólne
- Weryfikacja poprawności działania systemu.
- Przygotowanie prezentacji końcowej.
- Demonstracja działającego projektu.

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
