import unittest

class UHlibsTestCase(unittest.TestCase):
    maxDiff = None

    def assertFhContains(self, fh, s):
        """asserts filehandle `fh` contains string `s`:

        ```
            with mock_stdout() as _stdout:
                print("hello")
            self.assertFhContains(_stdout, "hello")
        ```
        """
        fh.flush()
        fh.seek(0)
        contents = fh.read()
        self.assertTrue(s in contents)

    def assertFhEquals(self, fh, s):
        """asserts filehandle `fh` contains string `s` exactly:

        ```
            with mock_stdout() as _stdout:
                print("hello")
            self.assertFhEquals(_stdout, "hello\\n")
        ```
        """
        fh.flush()
        fh.seek(0)
        contents = fh.read()
        self.assertEqual(s, contents)

