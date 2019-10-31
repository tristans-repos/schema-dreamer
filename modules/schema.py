from SPARQLWrapper import SPARQLWrapper
import modules.misc


class Meta:
    def __init__(self, filter_set_edges=[], filter_set_vertices=[]):
        self.name = "Meta class"
        self.filter_set_edges = filter_set_edges
        self.filter_set_vertices = filter_set_vertices

    def filter_query_pred_gen(self):
        filter_query_pred = ""
        for i in range(len(self.filter_set_edges)):
            if len(self.filter_set_edges) == 0:
                break
            elif len(self.filter_set_edges) == 1:
                string = "FILTER(regex(?pred£, ££))"
                filter_query_pred = string.replace("££", str(self.filter_set_edges[0]))
            elif i == 0:
                filter_query_pred = "FILTER("
                string = "regex(?pred£, ££)"
                filter_query_pred = filter_query_pred + string.replace("££", str(self.filter_set_edges[i]))
            elif i < len(self.filter_set_edges) - 1:
                string = "||regex(?pred£, ££)"
                filter_query_pred = filter_query_pred + string.replace("££", str(self.filter_set_edges[i]))
            elif i == len(self.filter_set_edges) - 1:
                string = "||regex(?pred£, ££))"
                filter_query_pred = filter_query_pred + string.replace("££", str(self.filter_set_edges[i]))

        return filter_query_pred

    def filter_query_pred_inv_gen(self):
        filter_query_pred_inv = ""
        for i in range(len(self.filter_set_edges)):
            if len(self.filter_set_edges) == 0:
                break
            elif len(self.filter_set_edges) == 1:
                string = "FILTER(regex(?pred_inv£, ££))"
                filter_query_pred_inv = string.replace("££", str(self.filter_set_edges[0]))
            elif i == 0:
                filter_query_pred_inv = "FILTER("
                string = "regex(?pred_inv£, ££)"
                filter_query_pred_inv = filter_query_pred_inv + string.replace("££", str(self.filter_set_edges[i]))
            elif i < len(self.filter_set_edges) - 1:
                string = "||regex(?pred_inv£, ££)"
                filter_query_pred_inv = filter_query_pred_inv + string.replace("££", str(self.filter_set_edges[i]))
            elif i == len(self.filter_set_edges) - 1:
                string = "||regex(?pred_inv£, ££))"
                filter_query_pred_inv = filter_query_pred_inv + string.replace("££", str(self.filter_set_edges[i]))
        
        return filter_query_pred_inv

    def filter_query_vertex_gen(self):
        filter_query_vertex = ""
        for i in range(len(self.filter_set_vertices)):
            if len(self.filter_set_vertices) == 0:
                break
            elif len(self.filter_set_vertices) == 1:
                string = "FILTER(regex(?n£, ££))"
                filter_query_vertex = string.replace("££", str(self.filter_set_vertices[0]))
            elif i == 0:
                filter_query_vertex = "FILTER("
                string = "regex(?n£, ££)"
                filter_query_vertex = filter_query_vertex + string.replace("££", str(self.filter_set_vertices[i]))
            elif i < len(self.filter_set_vertices) - 1:
                string = "||regex(?n£, ££)"
                filter_query_vertex = filter_query_vertex + string.replace("££", str(self.filter_set_vertices[i]))
            elif i == len(self.filter_set_vertices) - 1:
                string = "||regex(?n£, ££))"
                filter_query_vertex = filter_query_vertex + string.replace("££", str(self.filter_set_vertices[i]))
        
        return filter_query_vertex

    def cypher_url_gen(self, sparql_query):
        wrapper = SPARQLWrapper("http://dbpedia.org/sparql")
        wrapper.setQuery(sparql_query)
        wrapper.setReturnFormat("csv")
        query_result = wrapper.query()
        url = query_result.geturl()

        return url

    def run(self):
        iri_set = self.get_iris()
        for iri in iri_set:
            sparql_query = self.sparql_query_gen(iri)
            url = self.cypher_url_gen(sparql_query)
            cypher_query = self.cypher_query_gen(url, iri)
            modules.misc.commit_cypher_query(cypher_query)

    def get_iris(self):
        output = modules.misc.commit_cypher_query_numpy("""
MATCH (x:etl)
RETURN x.iri
        """)
        output = [i[0] for i in output]
        
        return output

    def sparql_query_gen(self, node_iri):
        filter_query_pred = self.filter_query_pred_gen()
        filter_query_pred_inv = self.filter_query_pred_inv_gen()
        filter_query_vertex = self.filter_query_vertex_gen()

        query_open = """
SELECT ?pred1 ?pred_inv1 ?n1 
    WHERE {
        """

        query_a = """
        { {
            <""" + node_iri + """> ?pred1 ?n1
        } UNION {
            ?n1 ?pred_inv1 <""" + node_iri + """>
        } } .
        """
        query_b = """
        { {
            """ + filter_query_pred.replace("£", "1") + """
            <""" + node_iri + """> ?pred1 ?n1
        } UNION {
            """ + filter_query_pred_inv.replace("£", "1") + """
            ?n1 ?pred_inv1 <""" + node_iri + """>
        } } .
        """
        query_c = """
        { {
            """ + filter_query_vertex.replace("£", "1") + """
            <""" + node_iri + """> ?pred1 ?n1
        } UNION {
            """ + filter_query_vertex.replace("£", "1") + """
            ?n1 ?pred_inv1 <""" + node_iri + """>
        } } .
        """
        query_d = """
        { {
            """ + filter_query_pred.replace("£", "1") + filter_query_vertex.replace("£", "1") + """
            <""" + node_iri + """> ?pred1 ?n1
        } UNION {
            """ + filter_query_pred_inv.replace("£", "1") + filter_query_vertex.replace("£", "1") + """
            ?n1 ?pred_inv1 <""" + node_iri + """>
        } } .
        """
        query_close = """
    }
        """

        if len(self.filter_set_edges) == 0 and len(self.filter_set_vertices) == 0:
            query = query_open + query_a + query_close
        elif len(self.filter_set_vertices) == 0:
            query = query_open + query_b + query_close
        elif len(self.filter_set_edges) == 0:
            query = query_open + query_c + query_close
        elif len(self.filter_set_edges) != 0 and len(self.filter_set_vertices) != 0:
            query = query_open + query_d + query_close

        print(query)
        return query

    def cypher_query_gen(self, url, node_iri):
        query_part1 = """WITH \"""" + url + """\" AS url\n\nLOAD CSV WITH HEADERS FROM url AS row

MATCH (n0 {iri: \"""" + node_iri + """\"})
"""

        query_part2 = """
MERGE (n1:meta {iri: row.n1})
FOREACH (x IN CASE WHEN row.pred1 IS NULL THEN [] ELSE [1] END | MERGE (n0)-[p:pred {iri: row.pred1}]->(n1))
FOREACH (x IN CASE WHEN row.pred_inv1 IS NULL THEN [] ELSE [1] END | MERGE (n0)<-[p:pred {iri: row.pred_inv1}]-(n1))
"""

        query = query_part1 + query_part2

        print(query)
        return query


# class Compute:


# class EntityRecognition:


# class Abstraction:
