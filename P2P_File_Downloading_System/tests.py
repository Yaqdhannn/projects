import unittest
import trackingserver
import client

# To run tests: python3 -m unittest tests.py

class Tests(unittest.TestCase):
    # test if create id creates id's incremently
    def test_create_id(self):
        self.assertEqual(trackingserver.create_id(), 1)
        self.assertEqual(trackingserver.create_id(), 2)
        self.assertEqual(trackingserver.create_id(), 3)
        self.assertEqual(trackingserver.create_id(), 4)

    # test if all_clients() return all correct client port
    def test_all_clients(self):
        # each client server array in the format: [Client ID, Port, [file1, file2, ...]]
        trackingserver.CLIENTS = [[1,1001,["test.txt","hello.txt"]],[2,1002,["file.txt"]],[3,1003,[]]]
        actual = trackingserver.all_clients()
        expected = ["1001","1002","1003"]
        self.assertEqual(actual,expected)

    # test if client_exists() return true when client exist
    def test_client_exists_true(self):
        self.assertTrue(trackingserver.client_exists(1001))
        self.assertTrue(trackingserver.client_exists(1002))
        self.assertTrue(trackingserver.client_exists(1003))

    # test if client_exists() return false when client exist does not exist
    def test_client_exists_false(self):
        self.assertFalse(trackingserver.client_exists(1000))
        self.assertFalse(trackingserver.client_exists(1004))
        self.assertFalse(trackingserver.client_exists(9999))
        
    # test if disconnect_client() removes the correct client from the list
    def test_disconnect_client(self):
        trackingserver.disconnect_client("1001")
        self.assertFalse(trackingserver.client_exists(1001))

        trackingserver.disconnect_client("1002")
        self.assertFalse(trackingserver.client_exists(1002))

        trackingserver.disconnect_client("1003")
        self.assertFalse(trackingserver.client_exists(1003))

    # test if update_list() adds new clients and updates current clients correctly
    def test_update_list(self):
        # msg format: client_port,file1,file2,file3,...
        # reset clients list
        trackingserver.CLIENTS = []
        # reset id counter
        trackingserver.id_counter = 1

        trackingserver.update_list(["1001","hello.txt","yo.txt"])
        expected = [[1,1001,["hello.txt","yo.txt"]]]
        self.assertEqual(trackingserver.CLIENTS, expected)

        trackingserver.update_list(["1001","hello.txt","yo.txt","newfile.txt"])
        expected = [[1,1001,["hello.txt","yo.txt","newfile.txt"]]]
        self.assertEqual(trackingserver.CLIENTS, expected)

        trackingserver.update_list(["1002","sherlock.txt","hello.txt"])
        expected = [[1,1001,["hello.txt","yo.txt","newfile.txt"]],[2,1002,["sherlock.txt","hello.txt"]]]
        self.assertEqual(trackingserver.CLIENTS, expected)
    
    # test if find_file() returns the correct client(s) who have the file
    def test_find_file(self):
        # reset clients list
        trackingserver.CLIENTS = []
        # reset id counter
        trackingserver.id_counter = 1

        trackingserver.update_list(["1001","hello.txt","yo.txt","newfile.txt"])
        trackingserver.update_list(["1002","sherlock.txt","hello.txt"])

        expected = ["1001"]
        self.assertEqual(trackingserver.find_file("yo.txt"), expected)

        expected = ["1002"]
        self.assertEqual(trackingserver.find_file("sherlock.txt"), expected)

        # if both clients share the file
        expected = ["1001","1002"]
        self.assertEqual(trackingserver.find_file("hello.txt"), expected)
    
    # test if ichecksum() return 0 if data is correct and not 0 if data is corrupted
    def test_ichecksum(self):
        data = "test\n"
        val = client.ichecksum(data)
        self.assertEqual(client.ichecksum(data, val), 0)

        data = "test\nCORRUPTED"
        self.assertNotEqual(client.ichecksum(data, val), 0)
    
    # test if get_minimum_load() returns the correct port with the minimum load
    def test_get_minimum_load(self):
        # format: [[port, val],...]
        load = [[1001,99999],[1002,1]]
        expected = 1002
        self.assertEqual(client.get_minimum_load(load), expected)

        load = [[1001,99999],[1002,1],[1003,1]]
        expected = 1002
        self.assertEqual(client.get_minimum_load(load), expected)

        load = [[1001,5],[1002,10],[1003,2]]
        expected = 1003
        self.assertEqual(client.get_minimum_load(load), expected)
