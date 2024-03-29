from py2neo import Graph, Transaction
import logging


g = Graph("bolt://localhost:7687", auth=("neo4j", "cayley"))


def commit_cypher_query(cypher_query):
    tr = Transaction(g)
    tr.run(cypher_query)
    tr.commit()


def commit_cypher_query_set(cypher_query_set):
    tr = Transaction(g)
    for cypher_query in cypher_query_set:
        tr.run(cypher_query)
    tr.commit()


def commit_cypher_query_numpy(cypher_query):
    tr = Transaction(g)
    array = tr.run(cypher_query).to_ndarray()

    return array


class Enrich:
    def __init__(self):
        self.name = "Enrich class"

    def run(self):
        cypher_build_node_ids = """
MATCH (x)
SET (CASE left(x.iri,28) WHEN "http://dbpedia.org/resource/" THEN x END).id = toString(replace(x.iri,"http://dbpedia.org/resource/","")), (CASE left(x.iri,28) WHEN "http://dbpedia.org/resource/" THEN x END).prefix = "http://dbpedia.org/resource/"
SET (CASE left(x.iri,37) WHEN "http://dbpedia.org/resource/Category:" THEN x END).id = toString(replace(x.iri,"http://dbpedia.org/resource/Category:","")), (CASE left(x.iri,37) WHEN "http://dbpedia.org/resource/Category:" THEN x END).prefix = "http://dbpedia.org/resource/Category:"
SET (CASE left(x.iri,28) WHEN "http://dbpedia.org/ontology/" THEN x END).id = toString(replace(x.iri,"http://dbpedia.org/ontology/","")), (CASE left(x.iri,28) WHEN "http://dbpedia.org/ontology/" THEN x END).prefix = "http://dbpedia.org/ontology/"
SET (CASE left(x.iri,30) WHEN "http://www.w3.org/2002/07/owl#" THEN x END).id = toString(replace(x.iri,"http://www.w3.org/2002/07/owl#","")), (CASE left(x.iri,30) WHEN "http://www.w3.org/2002/07/owl#" THEN x END).prefix = "http://www.w3.org/2002/07/owl#"
"""

        cypher_build_edge_ids = """
MATCH (x)-[y]->(z)
SET (CASE left(y.iri,25) WHEN "http://purl.org/dc/terms/" THEN y END).id = toString(replace(y.iri,"http://purl.org/dc/terms/","")), (CASE left(y.iri,25) WHEN "http://purl.org/dc/terms/" THEN y END).prefix = "http://purl.org/dc/terms/"
SET (CASE left(y.iri,36) WHEN "http://www.w3.org/2004/02/skos/core#" THEN y END).id = toString(replace(y.iri,"http://www.w3.org/2004/02/skos/core#","")), (CASE left(y.iri,36) WHEN "http://www.w3.org/2004/02/skos/core#" THEN y END).prefix = "http://www.w3.org/2004/02/skos/core#"
SET (CASE left(y.iri,43) WHEN "http://www.w3.org/1999/02/22-rdf-syntax-ns#" THEN y END).id = toString(replace(y.iri,"http://www.w3.org/1999/02/22-rdf-syntax-ns#","")), (CASE left(y.iri,43) WHEN "http://www.w3.org/1999/02/22-rdf-syntax-ns#" THEN y END).prefix = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
SET (CASE left(y.iri,37) WHEN "http://www.w3.org/2000/01/rdf-schema#" THEN y END).id = toString(replace(y.iri,"http://www.w3.org/2000/01/rdf-schema#","")), (CASE left(y.iri,37) WHEN "http://www.w3.org/2000/01/rdf-schema#" THEN y END).prefix = "http://www.w3.org/2000/01/rdf-schema#"
"""

        cypher_build_article_labels = """
MATCH (x {prefix: "http://dbpedia.org/resource/"})
SET x:article
"""

        cypher_build_category_labels = """
MATCH (x {prefix: "http://dbpedia.org/resource/Category:"})
SET x:category
"""

        cypher_build_ontology_labels = """
MATCH (x {prefix: "http://dbpedia.org/ontology/"})
SET x:ontology
"""

        cypher_build_owl_labels = """
MATCH (x {prefix: "http://www.w3.org/2002/07/owl#"})
SET x:owl
"""

        cypher_query_set = [cypher_build_node_ids, cypher_build_edge_ids, cypher_build_article_labels, cypher_build_category_labels, cypher_build_ontology_labels, cypher_build_owl_labels]
        logging.info(cypher_query_set)
        commit_cypher_query_set(cypher_query_set)
