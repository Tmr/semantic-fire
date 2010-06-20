from rdflib.Graph import ConjunctiveGraph
import uuid

class RdfDataExporter(object):
    def __init__(self):
       self.g = ConjunctiveGraph()

    def export(self, mainSubject, params, tuples):
        if params.has_key('subpredicate'):
            databag = mainSubject+"/"+str(uuid.uuid4())
            self.g.add((mainSubject, params['predicate'], databag))
            self.g.add((databag, 'rdf:type', params['databag_class']))
        for t in tuples:
          #print t
          if t.has_key('subject'):
              subject = t['subject']
          else:
              subject = mainSubject+"/"+str(uuid.uuid4())
              self.g.add((subject, 'rdf:type', params['datarow_class']))
          if not params.has_key('subpredicate'):
              if params['predicate'] != 'None':
                  self.g.add((mainSubject, params['predicate'], subject))
          else:
              self.g.add((databag, params['subpredicate'], subject))
          for predicate in t:
            if predicate != 'subject':
                self.g.add((subject, predicate, t[predicate]))

    def addTriple(self, s, p, o):
        self.g.add((s, p, o))

    def printTriples(self):
        for a in self.g.__iter__():
            print a

