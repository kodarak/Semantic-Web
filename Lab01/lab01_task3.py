from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD, RDFS

def create_rdf_graph():
    # Створюємо граф
    g = Graph()

    # Визначаємо простори імен
    ex = Namespace("http://example.org/")
    schema = Namespace("http://schema.org/")
    
    # Зв'язуємо префікси з просторами імен
    g.bind("foaf", FOAF)  # Friend of a Friend vocabulary
    g.bind("rdf", RDF)    # RDF vocabulary
    g.bind("rdfs", RDFS)  # RDF Schema vocabulary
    g.bind("xsd", XSD)    # XML Schema Datatypes
    g.bind("ex", ex)      # Our custom namespace
    g.bind("schema", schema)  # Schema.org vocabulary

    # Створюємо URI для людей
    cade = URIRef("http://example.org/person/cade")
    emma = URIRef("http://example.org/person/emma")

    # === Інформація про Кейда ===
    # Базова інформація (використання FOAF)
    g.add((cade, RDF.type, FOAF.Person))
    g.add((cade, FOAF.name, Literal("Cade", lang="en")))
    g.add((cade, FOAF.age, Literal(30, datatype=XSD.integer)))

    # Адреса (використання schema.org)
    g.add((cade, schema.address, Literal("1516 Henry Street, Berkeley, California 94709, USA")))

    # Освіта (використання власного простору імен)
    education = URIRef("http://example.org/education/cade_biology")
    g.add((cade, ex.education, education))
    g.add((education, ex.degree, Literal("Bachelor in Biology")))
    g.add((education, ex.university, Literal("University of California")))
    g.add((education, ex.graduationYear, Literal("2011", datatype=XSD.gYear)))

    # Інтереси (використання FOAF)
    interests = ["birds", "ecology", "environment", "photography", "travel"]
    for interest in interests:
        g.add((cade, FOAF.interest, Literal(interest, lang="en")))

    # Подорожі (власний простір імен)
    visited = URIRef("http://example.org/travels/cade")
    for country in ["Canada", "France"]:
        g.add((cade, ex.visited, Literal(country, lang="en")))

    # === Інформація про Емму ===
    # Базова інформація (FOAF)
    g.add((emma, RDF.type, FOAF.Person))
    g.add((emma, FOAF.name, Literal("Emma", lang="en")))
    g.add((emma, schema.address, Literal("Carrer de la Guardia Civil 20, 46020 Valencia, Spain")))

    # Освіта (власний простір імен)
    emma_edu = URIRef("http://example.org/education/emma_chemistry")
    g.add((emma, ex.education, emma_edu))
    g.add((emma_edu, ex.degree, Literal("Master in Chemistry")))
    g.add((emma_edu, ex.university, Literal("University of Valencia")))
    g.add((emma_edu, ex.graduationYear, Literal("2015", datatype=XSD.gYear)))

    # Сфера знань (власний простір імен)
    expertise = ["waste management", "toxic waste", "air pollution"]
    for know in expertise:
        g.add((emma, ex.expertise, Literal(know, lang="en")))

    # Інтереси (FOAF)
    for interest in ["cycling", "music", "travel"]:
        g.add((emma, FOAF.interest, Literal(interest, lang="en")))

    # Подорожі (власний простір імен)
    countries = ["Portugal", "Italy", "France", "Germany", "Denmark", "Sweden"]
    for country in countries:
        g.add((emma, ex.visited, Literal(country, lang="en")))

    # === Зв'язок між Кейдом та Еммою ===
    # Використання FOAF для зв'язків між людьми
    g.add((cade, FOAF.knows, emma))
    
    # Деталі зустрічі (власний простір імен)
    meeting = URIRef("http://example.org/meeting/cade_emma")
    g.add((meeting, ex.location, Literal("Paris", lang="en")))
    g.add((meeting, ex.date, Literal("2014-08", datatype=XSD.gYearMonth)))
    g.add((cade, ex.meeting, meeting))
    g.add((emma, ex.meeting, meeting))

    return g

def main():
    # Створюємо початковий граф
    g = create_rdf_graph()
    
    print("Зберігаємо початковий граф...")
    g.serialize("graph.ttl", format="turtle")

    # Читаємо та модифікуємо
    print("\nМодифікуємо граф...")
    modified_g = Graph()
    modified_g.parse("graph.ttl", format="turtle")

    # Додаємо нові дані
    cade = URIRef("http://example.org/person/cade")
    emma = URIRef("http://example.org/person/emma")
    ex = Namespace("http://example.org/")
    schema = Namespace("http://schema.org/")

    modified_g.add((cade, ex.visited, Literal("Germany", lang="en")))
    modified_g.add((emma, schema.age, Literal(36, datatype=XSD.integer)))

    # Зберігаємо модифікований граф
    modified_g.serialize("modified_graph.ttl", format="turtle")

    # Виводимо результати
    print("\nУсі трійки графу:")
    print("-" * 80)
    for s, p, o in modified_g:
        print(f"{s} {p} {o}")

    print("\nТрійки про Емму:")
    print("-" * 80)
    for s, p, o in modified_g.triples((emma, None, None)):
        print(f"{s} {p} {o}")

    print("\nТрійки з іменами людей (FOAF):")
    print("-" * 80)
    for s, p, o in modified_g.triples((None, FOAF.name, None)):
        print(f"{s} {p} {o}")

if __name__ == "__main__":
    main()