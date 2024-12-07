import unittest
import CryptoSqlite as sqlite3
import os

class TestCryptoSqlite(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.dbname = "test.db"
        cls.encrypt_dbname = "entest.db"
        cls.decrypt_dbname = "detest.db"
        cls.key = '123456'
        cls.newkey = '654321'

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.dbname)
        os.remove(cls.encrypt_dbname)
        os.remove(cls.decrypt_dbname)

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_0_create(self):
        conn = sqlite3.connect(self.dbname)

        cur = conn.cursor()
        cur.execute("CREATE TABLE movie(title, year, score)")
        res = cur.execute("SELECT name FROM sqlite_master")

        self.assertEqual(res.fetchone()[0],'movie')

        cur.close()
        conn.close()
    
    def test_1_encrypt(self):
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        cur.execute(f"ATTACH DATABASE '{self.encrypt_dbname}' AS encrypted KEY '{self.key}'")
        cur.execute("SELECT sqlcipher_export('encrypted')")
        cur.execute("DETACH DATABASE encrypted")

        self.assertTrue(os.path.exists(self.encrypt_dbname))

        cur.close()
        conn.close()


    def test_2_decrypt(self):
        conn = sqlite3.connect(self.encrypt_dbname)
        cur = conn.cursor()
        cur.execute(f"PRAGMA key='{self.key}'") 
        res = cur.execute("SELECT name FROM sqlite_master")

        self.assertEqual(res.fetchone()[0],'movie')

        cur.close()
        conn.close()

    def test_3_export_plain(self):
        con = sqlite3.connect(self.encrypt_dbname)


        cur = con.cursor()
        dbname = 'plaindb'
        cur.execute(f"PRAGMA key='{self.key}'")
        cur.execute(f"ATTACH DATABASE '{self.decrypt_dbname}' AS {dbname} KEY ''")
        cur.execute(f"SELECT sqlcipher_export('{dbname}')")
        cur.execute(f"DETACH DATABASE {dbname}")
        cur.close()
        con.close()

        con = sqlite3.connect(self.decrypt_dbname)

        cur = con.cursor()
        res = cur.execute("SELECT name FROM sqlite_master")
        self.assertEqual(res.fetchone()[0],'movie')

    def test_4_rekey(self):
        conn = sqlite3.connect(self.encrypt_dbname)
        cur = conn.cursor()
        cur.execute(f"PRAGMA key='{self.key}'") 
        cur.execute(f"PRAGMA rekey='{self.newkey}'") 
        cur.close()
        conn.close()

        conn = sqlite3.connect(self.encrypt_dbname)
        with self.assertRaises(sqlite3.ProgrammingError):
            cur.execute(f"PRAGMA key='{self.key}'") 
        

if __name__ == '__main__':
    unittest.main()
 