# SPARQL запит для пошуку найстарішого міста України

## Опис завдання
Використовуючи відкритий SPARQL endpoint http://dbpedia.org/sparql, створено запит для визначення назви найстарішого міста України.

## Код запиту
```sparql
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?cityName ?foundingDate
WHERE {
    ?city a dbo:City ;
          rdfs:label ?cityName ;
          dbo:country dbr:Ukraine ;
          dbo:foundingDate ?foundingDate .
    
    FILTER(LANG(?cityName) = "uk")
}
ORDER BY ?foundingDate
LIMIT 1
```

## Детальний розбір запиту

### 1. Префікси
```sparql
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
```
- `dbo:` - онтологія DBpedia, містить визначення класів та властивостей
- `dbr:` - ресурси DBpedia, використовується для конкретних сутностей
- `rdfs:` - словник RDF Schema, використовується для метаданих

### 2. Вибір даних
```sparql
SELECT DISTINCT ?cityName ?foundingDate
```
- `DISTINCT` - забезпечує унікальність результатів
- `?cityName` - змінна для назви міста
- `?foundingDate` - змінна для дати заснування

### 3. Умови пошуку
```sparql
WHERE {
    ?city a dbo:City ;
          rdfs:label ?cityName ;
          dbo:country dbr:Ukraine ;
          dbo:foundingDate ?foundingDate .
```
- `?city a dbo:City` - шукаємо сутності типу "місто"
- `rdfs:label ?cityName` - отримуємо назву міста
- `dbo:country dbr:Ukraine` - фільтруємо міста України
- `dbo:foundingDate ?foundingDate` - отримуємо дату заснування

### 4. Фільтрація
```sparql
FILTER(LANG(?cityName) = "uk")
```
- Фільтрує результати, залишаючи тільки назви українською мовою

### 5. Сортування та обмеження
```sparql
ORDER BY ?foundingDate
LIMIT 1
```
- `ORDER BY ?foundingDate` - сортує результати за датою заснування (від найстарішого)
- `LIMIT 1` - обмежує результат одним записом (найстаріше місто)

## Результат
![image](https://github.com/user-attachments/assets/b4ca3f9b-cbf3-40ba-96fe-1db01a26f551)

# Пошук українських IT-компаній

## Опис завдання
Використовуючи бібліотеки RdfLib, SPARQLWrapper та відкритий endpoint написати Python-скрипт, який буде повертати підприємства України, які мають відношення до IT галузі. Компанії необхідно впорядкувати за датою заснування.

## Опис проекту

Скрипт збирає дані про українські IT-компанії, включаючи:
- Назву компанії
- Дату заснування
- Галузь діяльності
- Опис компанії українською мовою

## Залежності

```bash
pip install sparqlwrapper pandas rdflib
```

## Структура коду

### 1. Основні компоненти

#### create_rdf_graph(companies)
- Створює RDF граф з даними про компанії
- Використовує namespace'и для структурування даних
- Додає інформацію про кожну компанію в граф

#### execute_sparql_query(endpoint_url, query)
- Виконує SPARQL-запити до DBpedia
- Обробляє помилки підключення
- Повертає результати у форматі JSON

#### get_ukrainian_it_companies()
- Містить SPARQL-запит для пошуку компаній
- Фільтрує компанії за різними критеріями:
  - Належність до України
  - IT-специфіка
  - Наявність українського опису

#### process_results(results)
- Обробляє результати SPARQL-запиту
- Видаляє дублікати
- Форматує дати та галузі

### 2. Допоміжні функції

#### sort_companies(companies)
- Сортує компанії за датою заснування
- Використовує pandas для обробки дат
- Переміщує компанії з невідомою датою в кінець списку

#### format_output(companies)
- Форматує дані для виведення
- Обмежує довжину опису
- Створює структурований вивід

#### save_to_rdf(graph, output_formats)
- Зберігає RDF граф у різних форматах
- Підтримує формати: XML, Turtle, JSON-LD
- Обробляє помилки збереження

## SPARQL-запит

Основні компоненти запиту:
1. **Пошук компаній**:
   ```sparql
   ?company a dbo:Company
   ```

2. **Зв'язок з Україною**:
   ```sparql
   ?company dbo:location|dbo:country|dbp:country dbr:Ukraine
   ```

3. **IT-специфічні фільтри**:
   ```sparql
   CONTAINS(STR(?industry), "software")
   CONTAINS(STR(?category), "technology_companies")
   ```

## Результат
![image](https://github.com/user-attachments/assets/ea7be216-223e-48a5-b8a3-ae0be514f956)
