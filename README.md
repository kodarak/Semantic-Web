# Лабораторна робота №01: Технології Semantic Web

## Автор
- **ПІБ**: [Ваше ПІБ]
- **Група**: [Ваша група]
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

➡️ Рішення: [lab01_task1.rdf](lab01_task1.rdf)

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

## Файли
- `README.md` - цей файл з поясненнями
- `lab01.rdf` - RDF-код завдання
