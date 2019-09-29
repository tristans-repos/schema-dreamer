# import sys
# print(sys.executable)

import builders, cleaners
from py2neo import Database, Graph, Transaction

db = Database("bolt://localhost:7687", auth=("neo4j", "cayley"))
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


commit_cypher_query("""
	MATCH (x)
	DETACH DELETE (x)
	""")


# sch1 = builders.PairwiseSchemaBuilder("http://dbpedia.org/resource/Television", "http://dbpedia.org/resource/Netflix", filter_set_edges=["dct:subject", "skos:broader"], filter_set_vertices=[])
# commit_cypher_query_set(sch1.cypher_query_set_gen(2))
# commit_cypher_query_set(sch1.cypher_query_set_gen(3))
# commit_cypher_query_set(sch1.cypher_query_set_gen(4))


# sch2a = builders.ParentSchemaBuilder("http://dbpedia.org/resource/Netflix", filter_set_edges=["dct:subject", "skos:broader", "rdf:type"], filter_set_vertices=[])
# commit_cypher_query_set(sch2a.cypher_query_set_gen(2))

# sch2b = builders.ParentSchemaBuilder("http://dbpedia.org/resource/Television", filter_set_edges=["dct:subject", "skos:broader", "rdf:type"], filter_set_vertices=[])
# commit_cypher_query_set(sch2b.cypher_query_set_gen(2))


sch3a = builders.PopulateSchemaBuilder("http://dbpedia.org/resource/Category:Complex_systems_theory", filter_set_edges=["dct:subject", "skos:broader"], filter_set_vertices=[])
commit_cypher_query_set(sch3a.cypher_query_set_gen(1))

sch3b = builders.PopulateSchemaBuilder("http://dbpedia.org/resource/Category:Systems_theory", filter_set_edges=["dct:subject", "skos:broader"], filter_set_vertices=[])
commit_cypher_query_set(sch3b.cypher_query_set_gen(1))

cl1 = cleaners.LeafSchemaCleaner(["http://dbpedia.org/resource/Category:Complex_systems_theory", "http://dbpedia.org/resource/Category:Systems_theory"])
commit_cypher_query_set(cl1.cypher_query_set_gen(1))