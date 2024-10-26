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
