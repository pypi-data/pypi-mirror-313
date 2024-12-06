from avocado import Test

from autils.archive import ar


class Ar(Test):
    def test_is_ar(self):
        self.assertTrue(ar.Ar(self.get_data("hello.deb")).is_valid())

    def test_is_not_ar(self):
        self.assertFalse(ar.Ar(self.get_data("hello.rpm")).is_valid())

    def test_iter(self):
        path = self.get_data("hello.deb")
        expected = [
            ("debian-binary", 4, 68),
            ("control.tar.xz", 1868, 132),
            ("data.tar.xz", 54072, 2060),
        ]
        for count, member in enumerate(ar.Ar(path)):
            self.assertEqual(expected[count][0], member.identifier)
            self.assertEqual(expected[count][1], member.size)
            self.assertEqual(expected[count][2], member.offset)

    def test_list(self):
        path = self.get_data("hello.deb")
        self.assertEqual(
            ar.Ar(path).list(), ["debian-binary", "control.tar.xz", "data.tar.xz"]
        )

    def test_read_member(self):
        path = self.get_data("guaca.a")
        self.assertEqual(ar.Ar(path).read_member("shopping"), b"avocados, salt")
        self.assertEqual(ar.Ar(path).read_member("recipe"), b"cut, mix")
