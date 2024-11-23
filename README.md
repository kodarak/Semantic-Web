# Лабораторна робота №01: Технології Semantic Web

## Автор
- **ПІБ**: Гарбар Ілля
- **Група**: ІПЗ-м11
- **Дисципліна**: Технології Semantic Web

## Завдання 1: RDF моделювання
Змоделювати наступні твердження як RDF:
1. Латунь – це сплав міді та цинку
2. SPIEGEL — німецький інформаційний журнал зі штаб-квартирою в Гамбурзі
3. Есе складається зі вступу, основної частини та висновку
4. Павло знає, що Олена живе в Полтаві
5. Олена каже, що її друг живе в Києві
6. Стефан думає, що Анна знає, що він знає її батька
7. Іван знає, що Рим є столицею Італії

➡️ Рішення: [lab01_task1.rdf](Lab01/lab01_task1.rdf)

## Код та пояснення

### 1. Опис просторів імен (Namespaces)
```xml
<rdf:RDF
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    xmlns:ex="http://example.org/terms#">
```
- `rdf:` - стандартний простір імен RDF
- `ex:` - наш власний простір імен для прикладів

### 2. Латунь як сплав
```xml
<rdf:Description rdf:about="http://example.org/brass">
    <ex:isAlloyOf rdf:resource="http://example.org/copper"/>
    <ex:isAlloyOf rdf:resource="http://example.org/zinc"/>
</rdf:Description>
```
- Описує латунь через її компоненти
- Використовує відношення `isAlloyOf`
- Посилається на мідь та цинк

### 3. Журнал SPIEGEL
```xml
<rdf:Description rdf:about="http://example.org/spiegel">
    <ex:type>Magazine</ex:type>
    <ex:nationality>German</ex:nationality>
    <ex:headquarters>Hamburg</ex:headquarters>
</rdf:Description>
```
- Визначає тип (журнал)
- Вказує національність (німецький)
- Зазначає розташування (Гамбург)

### 4. Структура есе
```xml
<rdf:Description rdf:about="http://example.org/essay">
    <ex:hasPart rdf:resource="http://example.org/essay/intro"/>
    <ex:hasPart rdf:resource="http://example.org/essay/main"/>
    <ex:hasPart rdf:resource="http://example.org/essay/conclusion"/>
</rdf:Description>
```
- Описує три частини есе
- Використовує відношення `hasPart`
- Кожна частина має власний ресурс

### 5. Павло знає про Олену
```xml
<rdf:Description rdf:about="http://example.org/pavlo">
    <ex:knows>
        <rdf:Description rdf:about="http://example.org/olena">
            <ex:livesIn>Poltava</ex:livesIn>
        </rdf:Description>
    </ex:knows>
</rdf:Description>
```
- Вкладений опис (Павло → знає → Олена)
- Використовує `knows` для зв'язку
- Додає інформацію про місце проживання

### 6. Олена про друга
```xml
<rdf:Description rdf:about="http://example.org/olena">
    <ex:says>
        <rdf:Description rdf:about="http://example.org/friend">
            <ex:livesIn>Kyiv</ex:livesIn>
        </rdf:Description>
    </ex:says>
</rdf:Description>
```
- Описує твердження Олени
- Використовує `says` для передачі інформації
- Вказує місце проживання друга

### 7. Стефан, Анна та її батько
```xml
<rdf:Description rdf:about="http://example.org/stefan">
    <ex:thinks>
        <rdf:Description rdf:about="http://example.org/anna">
            <ex:knows>
                <rdf:Description rdf:about="http://example.org/stefan">
                    <ex:knows rdf:resource="http://example.org/anna-father"/>
                </rdf:Description>
            </ex:knows>
        </rdf:Description>
    </ex:thinks>
</rdf:Description>
```
- Складна вкладена структура
- Декілька рівнів знань
- Використовує `thinks` та `knows`

### 8. Іван про Рим
```xml
<rdf:Description rdf:about="http://example.org/ivan">
    <ex:knows>
        <rdf:Description rdf:about="http://example.org/rome">
            <ex:isCapitalOf rdf:resource="http://example.org/italy"/>
        </rdf:Description>
    </ex:knows>
</rdf:Description>
```
- Описує знання про столицю
- Використовує `isCapitalOf`
- Зв'язує Рим та Італію

## Використані елементи RDF

### Основні компоненти
- `rdf:Description` - опис ресурсу
- `rdf:about` - ідентифікатор ресурсу
- `rdf:resource` - посилання на інший ресурс

### Відношення
- `isAlloyOf` - складові сплаву
- `hasPart` - частини документу
- `knows` - знання
- `says` - твердження
- `thinks` - думки
- `livesIn` - місце проживання
- `isCapitalOf` - статус столиці

## Перевірка
Код успішно пройшов перевірку в [W3C RDF Validator](https://www.w3.org/RDF/Validator/)
![image](https://github.com/user-attachments/assets/8a798e05-e0e7-473c-be9a-702225240a7a)

### Список триплетів
Валідатор виявив 17 правильних триплетів, що відповідають всім заданим твердженням:
- Опис латуні та її компонентів (2 триплети)
- Характеристики журналу SPIEGEL (3 триплети)
- Структура есе (3 триплети)
- Знання про місця проживання (4 триплети)
- Складні відносини між людьми (3 триплети)
- Знання про столицю (2 триплети)

## Завдання 2: Веб-сторінка з анотаціями

### Опис
Створено веб-сторінку про книгу з трьома типами анотацій:
1. JSON-LD
2. Microdata
3. RDFa

### Структура анотацій

### 1. JSON-LD
```json
{
  "@context": "https://schema.org",
  "@type": "Book",
  "name": "Хмарний Атлас",
  "author": {
    "@type": "Person",
    "name": "Девід Мітчелл"
  }
  // ...інші властивості
}
```

### 2. Microdata
```html

    Хмарний Атлас
    
        Девід Мітчелл
    

```

### 3. RDFa
```html

    978-3442267819
    509
    

```

### Перевірка
Код перевірено за допомогою:
1. [Google Rich Results Test](https://search.google.com/test/rich-results)
2. [Schema.org Validator](https://validator.schema.org/)

### Файли
- 📄 [lab01_task2.html](Lab01/lab01_task2.html) - HTML-сторінка з анотаціями

### Особливості реалізації
1. Використано схему "Lab01_task2" зі Schema.org
2. Додано різні типи метаданих:
   - Основна інформація про книгу
   - Дані про автора
   - Рейтинг та відгуки
   - Видавничі деталі
3. Стилізація для кращого відображення

### Результати тестування
✅ Всі три типи анотацій успішно валідовані
![image](https://github.com/user-attachments/assets/30b4ac1b-18fd-4fcc-ba10-74dfff04912e)
![image](https://github.com/user-attachments/assets/e866b132-20e3-4784-8fe1-23f96d3aa487)

## Лабораторна робота №01: Завдання 3 - RDF граф

### Умова завдання
Змоделювати наступну ситуацію як RDF граф:

Кейд живе за адресою 1516 Henry Street, Берклі, Каліфорнія 94709, США. Він має ступінь бакалавра біології в Каліфорнійському університеті з 2011 року. Його інтереси: птахи, екологія, довкілля, фотографія і подорожі. Він відвідав Канаду та Францію. 

Емма живе за адресою Carrer de la Guardia Civil 20, 46020 Valencia, Spain. Вона має ступінь магістра хімії в Університеті Валенсії з 2015 року. Її сфера знань включає управління відходами, токсичні відходи, забруднення повітря. Її інтереси: їзда на велосипеді, музика та подорожі. Вона відвідала Португалію, Італію, Францію, Німеччину, Данію та Швецію. 

Кейд знає Емму. Вони зустрілися в Парижі в серпні 2014 року.

### Використані технології та словники
- Python 3.x
- RDFLib бібліотека
- Словники:
  - FOAF (Friend of a Friend)
  - RDF (Resource Description Framework)
  - RDFS (RDF Schema)
  - XSD (XML Schema Definition)
  - Schema.org
  - Власний простір імен (http://example.org/)

### Файли проекту
- `lab01_task3.py` - основний Python скрипт
- `graph.ttl` - початковий RDF граф у форматі Turtle
- `modified_graph.ttl` - модифікований RDF граф

### Структура даних
1. **Простори імен**:
   ```python
   g.bind("foaf", FOAF)   # Для опису людей та їх зв'язків
   g.bind("rdf", RDF)     # Для базової RDF структури
   g.bind("rdfs", RDFS)   # Для RDF схеми
   g.bind("xsd", XSD)     # Для типів даних
   g.bind("schema", schema) # Для загальних схем
   g.bind("ex", ex)       # Власний простір імен
   ```

2. **Основні компоненти**:
   - Особисті дані (ім'я, адреса)
   - Освіта (університет, ступінь, рік)
   - Інтереси та хобі
   - Подорожі
   - Зв'язки між людьми

### Виконані завдання
1. Створено RDF граф з використанням різних словників
2. Виконано сериалізацію графу у формат Turtle
3. Додано нові дані:
   - Додано Німеччину до країн, які відвідав Кейд
   - Додано вік Емми (36 років)
4. Реалізовано різні типи вибірки даних:
   - Всі трійки графу
   - Трійки про Емму
   - Трійки з іменами людей

## Як використовувати

1. Встановлення залежностей:
```bash
pip install rdflib
```

2. Запуск скрипта:
```bash
python lab01_task3.py
```

## Результати виконання
1. Генерується файл `graph.ttl` з початковим RDF графом
   ![image](https://github.com/user-attachments/assets/74eb1fd9-d62c-47fb-89ef-16823ebadc25)
3. Створюється `modified_graph.ttl` з модифікованими даними
   ![image](https://github.com/user-attachments/assets/78aad1ec-9c20-4702-a75a-d6298eac62cf)
5. У консоль виводяться:
   - Всі трійки графу
     
     ![image](https://github.com/user-attachments/assets/a491e543-4351-4945-85bb-74cf831c452b)
   - Інформація про Емму
     
     ![image](https://github.com/user-attachments/assets/d9b0d12a-612b-4240-8f15-76acf79afdf2)
   - Імена всіх людей
     
     ![image](https://github.com/user-attachments/assets/84d7b15e-e515-4977-9e4f-e67a9e9a836c)

# Лабораторна робота №02: SPARQL Запити

## Завдання 1: Населення країн Східної Європи

### SPARQL Запит
```sparql
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX yago: <http://dbpedia.org/class/yago/>

SELECT DISTINCT ?country ?countryLabel ?population
WHERE {
    # Вибираємо країни Східної Європи
    ?country dct:subject dbc:Eastern_European_countries .
    
    # Отримуємо назву країни
    ?country rdfs:label ?countryLabel .
    FILTER(LANG(?countryLabel) = "en")
    
    # Отримуємо населення
    ?country dbo:populationTotal ?population .
}
ORDER BY DESC(?population)
```

### Пояснення запиту
1. **Префікси**:
   - `dbo:` - DBpedia онтологія
   - `dbr:` - DBpedia ресурси
   - `yago:` - YAGO класифікація

2. **Структура запиту**:
   - SELECT вибирає країну, її назву та населення
   - WHERE визначає умови пошуку
   - ORDER BY DESC сортує за спаданням населення

3. **Фільтри**:
   - Вибір лише англійських назв
   - Перевірка належності до Східної Європи

### Результат
**HTML**
![image](https://github.com/user-attachments/assets/9b715662-1178-4722-9d86-4e33c7d8b911)

**Spreadsheet**
![image](https://github.com/user-attachments/assets/bffd33ff-5ffd-46dc-bf39-8be6feb50bf8)

### Як використати
1. Відкрийте [DBpedia SPARQL endpoint](http://dbpedia.org/sparql)
2. Вставте запит
3. Натисніть "Execute"

### Особливості
- Дані оновлюються з Wikipedia
- Можливі розбіжності через різні дати оновлення
- Деякі країни можуть мати відсутні дані

## Файли
- `query1.sparql` - файл з SPARQL запитом
- `README.md` - документація

## Завдання 2: Країни на літеру "А" та їх мови

### SPARQL Запит

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dbc: <http://dbpedia.org/resource/Category:>
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT ?country ?label (GROUP_CONCAT(DISTINCT UCASE(?languageLabel); separator="|") as ?languages)
WHERE {
  ?country a <http://dbpedia.org/ontology/Country> ;
          rdfs:label ?label ;
          dct:subject ?category .
  
  FILTER(
    ?category = dbc:Countries_in_Europe ||
    ?category = dbc:Countries_in_North_America
  )
  
  OPTIONAL {
    ?country dbo:officialLanguage ?language .
    ?language rdfs:label ?languageLabel .
    FILTER(LANG(?languageLabel) = "en")
  }
  
  FILTER(LANG(?label) = "en")
  FILTER(STRSTARTS(?label, "A"))
}
GROUP BY ?country ?label
ORDER BY ?label
```

### Пояснення запиту
1. **Префікси**:

   - dbo: - DBpedia онтологія
   - dbr: - DBpedia ресурси
   - rdfs: - RDF Schema


2. **Структура запиту**:

   - SELECT вибирає країну, її назву та мови
   - WHERE визначає умови пошуку
   - GROUP BY групує результати за країною
   - ORDER BY сортує за назвою країни


3. **Фільтри**:

   - Вибір лише англійських назв
   - Початок назви на "A"
   - Належність до Європи або Північної Америки



### Результат
**HTML**
![image](https://github.com/user-attachments/assets/0fa83d84-4f5b-4474-bbdc-f29a68e6cb46)

### Як використати
1. Відкрийте [DBpedia SPARQL endpoint](http://dbpedia.org/sparql)
2. Вставте запит
3. Натисніть "Execute"

### Особливості
- Групування мов через символ "|"
- Перетворення назв мов у верхній регістр
- Включення країн без мов завдяки OPTIONAL

## Файли
- query2.sparql - файл з SPARQL запитом
- README.md - документація

## Завдання 3: Нобелівські лауреати

### SPARQL Запит
### 3.1 Лауреати за віком

```sparql
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?person ?personLabel ?birthDate
WHERE {
    ?person dbo:award dbr:Nobel_Prize_in_Physics ;
            rdfs:label ?personLabel ;
            dbo:birthDate ?birthDate .
    FILTER(LANG(?personLabel) = "en")
}
ORDER BY ?birthDate
```
### 3.2 Топ-10 університетів

```sparql
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?university ?universityLabel (COUNT(DISTINCT ?person) as ?laureateCount)
WHERE {
    ?person dbo:award dbr:Nobel_Prize_in_Physics ;
            dbo:almaMater ?university .
    ?university rdfs:label ?universityLabel .
    FILTER(LANG(?universityLabel) = "en")
}
GROUP BY ?university ?universityLabel
ORDER BY DESC(?laureateCount)
LIMIT 10
```

### 3.3 Лауреати-іммігранти

```sparql
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT (COUNT(DISTINCT ?person) as ?immigrantCount)
WHERE {
    ?person dbo:award dbr:Nobel_Prize_in_Physics ;
            dbo:birthPlace/dbo:country ?birthCountry ;
            dbo:almaMater ?university .
    ?university dbo:country ?universityCountry .
    FILTER(?birthCountry != ?universityCountry)
}
```

### Пояснення запиту
1. **Префікси**:

   - dbo: - DBpedia онтологія
   - dbr: - DBpedia ресурси
   - rdfs: - RDF Schema


2. **Структура запитів**:

   - Запит 3.1: Сортування за віком
   - Запит 3.2: Групування за університетами
   - Запит 3.3: Підрахунок іммігрантів



### Результат
**HTML**
![image](https://github.com/user-attachments/assets/eca74825-4ac8-4ff9-9ee5-1b1196530665)
![image](https://github.com/user-attachments/assets/af108994-708b-4a6f-bbf7-411f59f60c1b)
![image](https://github.com/user-attachments/assets/7cefb2ad-48c6-4528-8dc4-a2327fb881cd)

### Як використати
1. Відкрийте [DBpedia SPARQL endpoint](http://dbpedia.org/sparql)
2. Вставте запит
3. Натисніть "Execute"

### Особливості
- Можливі пропуски в даних
- Різні формати дат
- Потрібна перевірка результатів

## Файли
- query3_1.sparql - запит лауреатів
- query3_2.sparql - запит університетів
- query3_3.sparql - запит іммігрантів
- README.md - документація
