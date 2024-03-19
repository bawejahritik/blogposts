import unittest

from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a test node", "bold")
        node2 = TextNode("This is a test node", "bold")
        self.assertEqual(node1, node2)
    
    def test_neq_different_text(self):
        node1 = TextNode("This is a test node", "bold", "url")
        node2 = TextNode("This is another test node", "bold", "url")
        self.assertNotEqual(node1, node2)

    def test_neq_different_text_type(self):
        node1 = TextNode("This is a test node", "italic", "url")
        node2 = TextNode("This is another test node", "bold", "url")
        self.assertNotEqual(node1, node2)

    def test_neq_different_url(self):
        node1 = TextNode("This is a test node", "bold", "url")
        node2 = TextNode("This is another test node", "bold", "url2")
        self.assertNotEqual(node1, node2)

if __name__=="__main__":
    unittest.main()