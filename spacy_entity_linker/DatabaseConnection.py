import sqlite3
import os

MAX_DEPTH_CHAIN = 10
P_INSTANCE_OF = 31
P_SUBCLASS = 279

MAX_ITEMS_CACHE = 100000

conn = None
entity_cache = {}
chain_cache = {}

DB_DEFAULT_PATH = os.path.abspath(__file__ + '/../../data_spacy_entity_linker/wikidb_filtered.db')

wikidata_instance = None


def get_wikidata_instance():
    global wikidata_instance

    if wikidata_instance is None:
        wikidata_instance = WikidataQueryController()

    return wikidata_instance


class WikidataQueryController:

    def __init__(self):
        self.conn = None

        self.cache = {
            "entity": {},
            "chain": {},
            "name": {}
        }

        self.init_database_connection()

    def _get_cached_value(self, cache_type, key):
        return self.cache[cache_type][key]

    def _is_cached(self, cache_type, key):
        return key in self.cache[cache_type]

    def _add_to_cache(self, cache_type, key, value):
        if len(self.cache[cache_type]) < MAX_ITEMS_CACHE:
            self.cache[cache_type][key] = value

    def init_database_connection(self, path=DB_DEFAULT_PATH):
        self.conn = sqlite3.connect(path)

    def clear_cache(self):
        self.cache["entity"].clear()
        self.cache["chain"].clear()
        self.cache["name"].clear()

    def get_entities_from_alias(self, alias):
        c = self.conn.cursor()
        if self._is_cached("entity", alias):
            return self._get_cached_value("entity", alias).copy()

        query_alias = """SELECT j.item_id,j.en_label, j.en_description,j.views,j.inlinks,a.en_alias from aliases as a
            LEFT JOIN joined as j ON a.item_id = j.item_id
            WHERE a.en_alias_lowercase = ? and j.item_id NOT NULL"""

        c.execute(query_alias, [alias.lower()])
        fetched_rows = c.fetchall()

        self._add_to_cache("entity", alias, fetched_rows)
        return fetched_rows

    def get_instances_of(self, item_id, properties=[P_INSTANCE_OF, P_SUBCLASS], count=1000):
        query = "SELECT source_item_id from statements where target_item_id={} and edge_property_id IN ({}) LIMIT {}".format(
            item_id, ",".join([str(prop) for prop in properties]), count)

        c = self.conn.cursor()
        c.execute(query)

        res = c.fetchall()

        return [e[0] for e in res]

    def get_entity_name(self, item_id):
        if self._is_cached("name", item_id):
            return self._get_cached_value("name", item_id)

        c = self.conn.cursor()
        query = "SELECT en_label from joined WHERE item_id=?"
        c.execute(query, [item_id])
        res = c.fetchone()

        if res and len(res):
            if res[0] == None:
                self._add_to_cache("name", item_id, 'no label')
            else:
                self._add_to_cache("name", item_id, res[0])
        else:
            self._add_to_cache("name", item_id, '<none>')

        return self._get_cached_value("name", item_id)

    def get_entity(self, item_id):
        c = self.conn.cursor()
        query = "SELECT j.item_id,j.en_label,j.en_description,j.views,j.inlinks from joined as j " \
                "WHERE j.item_id=={}".format(item_id)

        res = c.execute(query)

        return res.fetchone()

    def get_children(self, item_id, limit=100):
        c = self.conn.cursor()
        query = "SELECT j.item_id,j.en_label,j.en_description,j.views,j.inlinks from joined as j " \
                "JOIN statements as s on j.item_id=s.source_item_id " \
                "WHERE s.target_item_id={} and s.edge_property_id IN (279,31) LIMIT {}".format(item_id, limit)

        res = c.execute(query)

        return res.fetchall()

    def get_parents(self, item_id, limit=100):
        c = self.conn.cursor()
        query = "SELECT j.item_id,j.en_label,j.en_description,j.views,j.inlinks from joined as j " \
                "JOIN statements as s on j.item_id=s.target_item_id " \
                "WHERE s.source_item_id={} and s.edge_property_id IN (279,31) LIMIT {}".format(item_id, limit)

        res = c.execute(query)

        return res.fetchall()

    def get_categories(self, item_id, max_depth=10):
        chain = []
        edges = []
        self._append_chain_elements(item_id, 0, chain, edges, max_depth, [P_INSTANCE_OF, P_SUBCLASS])
        return [el[0] for el in chain]

    def get_chain(self, item_id, max_depth=10, property=P_INSTANCE_OF):
        chain = []
        edges = []
        self._append_chain_elements(item_id, 0, chain, edges, max_depth, property)
        return chain

    def get_recursive_edges(self, item_id):
        chain = []
        edges = []
        self._append_chain_elements(self, item_id, 0, chain, edges)
        return edges

    def _append_chain_elements(self, item_id, level=0, chain=[], edges=[], max_depth=10, property=P_INSTANCE_OF):
        properties = property
        if type(property) != list:
            properties = [property]

        if self._is_cached("chain", (item_id, max_depth)):
            chain += self._get_cached_value("chain", (item_id, max_depth)).copy()
            return

        # prevent infinite recursion
        if level >= max_depth:
            return

        c = self.conn.cursor()

        query = "SELECT target_item_id,edge_property_id from statements where source_item_id={} and edge_property_id IN ({})".format(
            item_id, ",".join([str(prop) for prop in properties]))

        # set value for current item in order to prevent infinite recursion
        self._add_to_cache("chain", (item_id, max_depth), [])

        for target_item in c.execute(query):

            chain_ids = [el[0] for el in chain]

            if not (target_item[0] in chain_ids):
                chain += [(target_item[0], level + 1)]
                edges.append((item_id, target_item[0], target_item[1]))
                self._append_chain_elements(target_item[0], level=level + 1, chain=chain, edges=edges,
                                            max_depth=max_depth,
                                            property=property)

        self._add_to_cache("chain", (item_id, max_depth), chain)


if __name__ == '__main__':
    queryInstance = WikidataQueryController()

    queryInstance.init_database_connection()
    print(queryInstance.get_categories(13191, max_depth=1))
    print(queryInstance.get_categories(13191, max_depth=1))
