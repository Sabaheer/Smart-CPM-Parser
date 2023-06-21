import unittest

import helper
from dashboard.EtihadDb import EtihadDb
from dashboard.EtihadUtils import EtihadUtils


class MyTestCase(unittest.TestCase):
    def xtest_something(self):
        db = EtihadDb("db.db")
        db.create_db()
        db.add_file("s1", "file1", "abcd")
        db.add_file("s1", "file2", "abcd")
        db.add_file("s1", "file2", "XXX")
        db.add_file("s2","file2", "abcd")
        db.add_file("s3", "file3", "abcd")
        db.add_file("s4", "file4", "abcd")
        result = db.get_file_list()
        self.assertEqual([('s1', 'file1', 'abcd'),('s1', 'file2', 'XXX'),('s2', 'file2', 'abcd'),('s3', 'file3', 'abcd'), ('s4', 'file4', 'abcd')] , result)
        self.assertEqual("XXX", db.get_file_content("s1", "file2"))


        db.add_error("source", "filename", "line", "field", "value", "error_type")
        errors = db.get_errors_by_source("source")
        self.assertEqual([('source', 'filename', 'line', 'field', 'value', 'error_type')], errors)

        sources = db.get_all_sources()
        self.assertEqual([('s1',), ('s2',), ('s3',), ('s4',)], sources)

    def test_prepare_data(self):
        db = EtihadDb("db.db")
        db.create_db()
        #db.add_file("etihad", "etihad_CPM1.txt", helper.load_file_simple("../test/data/CPM1.txt"))
        #db.add_file("etihad", "etihad_CPM2.txt", helper.load_file_simple("../test/data/CPM2.txt"))
        EtihadUtils().addFile("etihad_CPM1.txt", helper.load_file_simple("../test/data/CPM1.txt"))
        EtihadUtils().addFile("etihad_CPM2.txt", helper.load_file_simple("../test/data/CPM2.txt"))
        EtihadUtils().addFile("etihad_CPM3.txt", helper.load_file_simple("../test/data/CPM3.txt"))
        EtihadUtils().addFile("etihad_CPM4.txt", helper.load_file_simple("../test/data/CPM4.txt"))

        result = db.get_file_list()

    def test_create_empty(self):
        db = EtihadDb("db.db")
        db.create_db()

if __name__ == '__main__':
    unittest.main()
