from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import datetime
import pandas as pd
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, FOAF

def create_rdf_graph(companies):
    """Створення RDF графу з даними про компанії"""
    # Ініціалізація графу
    g = Graph()
    
    # Визначення namespace'ів
    company_ns = Namespace("http://example.org/company/")
    dbo = Namespace("http://dbpedia.org/ontology/")
    
    # Додавання префіксів
    g.bind("company", company_ns)
    g.bind("dbo", dbo)
    g.bind("foaf", FOAF)
    
    for i, company in enumerate(companies):
        # Створення URI для компанії
        company_uri = URIRef(company_ns[str(i)])
        
        # Додавання базової інформації
        g.add((company_uri, RDF.type, dbo.Company))
        g.add((company_uri, FOAF.name, Literal(company['name'], lang='uk')))
        
        # Додавання дати заснування
        if company['founding_date'] != 'Невідомо':
            g.add((company_uri, dbo.foundingDate, 
                  Literal(company['founding_date'], datatype=XSD.date)))
        
        # Додавання опису
        if company['description'] != 'Опис відсутній':
            g.add((company_uri, dbo.abstract, 
                  Literal(company['description'], lang='uk')))
        
        # Додавання галузі
        g.add((company_uri, dbo.industry, 
               Literal(company['industry'])))
    
    return g

def execute_sparql_query(endpoint_url, query):
    """Виконує SPARQL запит до вказаного endpoint"""
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    try:
        return sparql.query().convert()
    except Exception as e:
        print(f"Помилка при виконанні запиту до {endpoint_url}: {e}")
        return None

def get_ukrainian_it_companies():
    """Отримує дані про українські IT-компанії з DBpedia"""
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX dbp: <http://dbpedia.org/property/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX category: <http://dbpedia.org/resource/Category:>

    SELECT DISTINCT ?companyName ?foundingDate ?description ?industry
    WHERE {
        # [Тут той самий SPARQL запит, що був раніше]
        # Основна інформація про компанію
        {
            ?company a dbo:Company ;
                    rdfs:label ?companyName .
        } UNION {
            ?company rdf:type dbo:Company ;
                    rdfs:label ?companyName .
        }
        
        # Зв'язок з Україною
        {
            ?company dbo:location dbr:Ukraine
        } UNION {
            ?company dbo:country dbr:Ukraine
        } UNION {
            ?company dbp:country dbr:Ukraine
        } UNION {
            ?company dbp:location dbr:Ukraine
        } UNION {
            ?company dbo:headquarter dbr:Ukraine
        }
        
        # IT-специфічні фільтри
        {
            ?company dbo:industry ?industry .
            FILTER(
                CONTAINS(LCASE(STR(?industry)), "software") ||
                CONTAINS(LCASE(STR(?industry)), "computer") ||
                CONTAINS(LCASE(STR(?industry)), "technology") ||
                CONTAINS(LCASE(STR(?industry)), "programming") ||
                CONTAINS(LCASE(STR(?industry)), "internet") ||
                CONTAINS(LCASE(STR(?industry)), "digital") ||
                CONTAINS(LCASE(STR(?industry)), "information technology")
            )
        } UNION {
            ?company dct:subject ?category .
            FILTER(
                CONTAINS(LCASE(STR(?category)), "software_companies") ||
                CONTAINS(LCASE(STR(?category)), "information_technology_companies") ||
                CONTAINS(LCASE(STR(?category)), "technology_companies") ||
                CONTAINS(LCASE(STR(?category)), "internet_companies")
            )
        }
        
        # Отримання дати заснування
        {
            ?company dbo:foundingDate ?foundingDate
        } UNION {
            ?company dbp:founded ?foundingDate
        } UNION {
            ?company dbo:foundingYear ?foundingDate
        } UNION {
            ?company dbp:foundation ?foundingDate
        } UNION {
            ?company dbo:established ?foundingDate
        }
        
        # Отримання опису
        OPTIONAL {
            ?company dbo:abstract ?description .
            FILTER(LANG(?description) = "uk")
        }
        
        # Фільтрація мови
        FILTER(LANG(?companyName) = "uk")
    }
    ORDER BY ?foundingDate
    """
    
    results = execute_sparql_query("http://dbpedia.org/sparql", query)
    return process_results(results) if results else []

def process_results(results):
    """Обробка результатів запиту"""
    companies = []
    seen_names = set()
    
    for result in results["results"]["bindings"]:
        name = result['companyName']['value']
        
        if name in seen_names:
            continue
        seen_names.add(name)
        
        founding_date = result.get('foundingDate', {}).get('value', 'Невідомо')
        if founding_date != 'Невідомо':
            try:
                if 'T' in founding_date:
                    founding_date = datetime.fromisoformat(founding_date.split('T')[0]).strftime('%Y-%m-%d')
                elif len(founding_date) == 4:
                    founding_date = f"{founding_date}-01-01"
            except ValueError:
                founding_date = 'Невідомо'
        
        industry = result.get('industry', {}).get('value', 'Галузь не вказана')
        if 'http' in industry:
            industry = industry.split('/')[-1].replace('_', ' ').title()
        
        company = {
            'name': name,
            'founding_date': founding_date,
            'description': result.get('description', {}).get('value', 'Опис відсутній'),
            'industry': industry
        }
        companies.append(company)
    
    return sort_companies(companies)

def sort_companies(companies):
    """Сортування компаній за датою заснування"""
    df = pd.DataFrame(companies)
    df['date_for_sorting'] = pd.to_datetime(
        df['founding_date'].replace('Невідомо', 'NaT'),
        errors='coerce'
    )
    df = df.sort_values('date_for_sorting', na_position='last')
    return df.drop('date_for_sorting', axis=1).to_dict('records')

def save_to_rdf(graph, output_formats=['xml', 'turtle', 'json-ld']):
    """Зберігання RDF графу у різних форматах"""
    for format_name in output_formats:
        filename = f"ukrainian_it_companies.{format_name}"
        try:
            graph.serialize(destination=filename, format=format_name)
            print(f"Дані збережено у форматі {format_name}: {filename}")
        except Exception as e:
            print(f"Помилка при збереженні у форматі {format_name}: {e}")

def format_output(companies):
    """Форматування виводу результатів"""
    if not companies:
        return "Компанії не знайдено"
    
    formatted_output = [
        f"Знайдено українських IT-компаній: {len(companies)}",
        "="*50
    ]
    
    for i, company in enumerate(companies, 1):
        formatted_output.extend([
            f"{i}. Назва: {company['name']}",
            f"   Дата заснування: {company['founding_date']}",
            f"   Галузь: {company['industry']}",
            f"   Опис: {company['description'][:200]}..." 
            if len(company['description']) > 200 
            else f"   Опис: {company['description']}",
            "-"*50
        ])
    
    return "\n".join(formatted_output)

def main():
    print("Отримання даних про українські IT-компанії...")
    companies = get_ukrainian_it_companies()
    
    # Створення RDF графу
    print("Створення RDF графу...")
    graph = create_rdf_graph(companies)
    
    # Збереження даних у різних RDF форматах
    save_to_rdf(graph)
    
    # Виведення результатів
    print(format_output(companies))

if __name__ == "__main__":
    main()
