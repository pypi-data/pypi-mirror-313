from musurgia.magicrandom import Random
from musurgia.tests.utils_for_tests import PdfTestCase


class TestRandom(PdfTestCase):
    def test_counter(self):
        r = Random(pool=['a', 'b', 'c'], periodicity=1, seed=20)
        assert r.counter == 0
        assert next(r) == 'c'

        assert r.counter == 1
        assert next(r) == 'a'
        assert r.counter == 2

    def test_forbidden_list(self):
        with self.assertRaises(TypeError):
            Random(pool=[1, 2, 3], forbidden_list="[2]")

        r = Random(pool=[1, 3, 2, 4, 5, 6], periodicity=4, seed=20, forbidden_list=[2, 3, 1])
        previous_forbidden_list = r.forbidden_list[:]
        el1 = next(r)
        assert el1 not in previous_forbidden_list
        assert r.forbidden_list == [2, 3, 1] + [el1]
        previous_forbidden_list = r.forbidden_list[:]
        el2 = next(r)
        assert r not in previous_forbidden_list
        assert r.forbidden_list == [3, 1] + [el1, el2]
        previous_forbidden_list = r.forbidden_list[:]
        el3 = next(r)
        assert el3 not in previous_forbidden_list
        assert r.forbidden_list == [1] + [el1, el2, el3]

    def test_periodicity(self):
        with self.assertRaises(TypeError):
            Random(pool=[1, 2, 3], periodicity=-1)
        with self.assertRaises(TypeError):
            Random(pool=[1, 2, 3], periodicity=1.6)

        assert Random(pool=[1, 2, 3, 4]).periodicity == 2
        assert Random(pool=[1]).periodicity == 0
        assert Random(pool=[1, 2, 3, 4], periodicity=5).periodicity == 3

    def test_pool(self):
        with self.assertRaises(TypeError):
            Random(pool=3)
        with self.assertRaises(TypeError):
            Random(pool=None)
        assert Random(pool=[1, 2, 3, 2, 1]).pool == [1, 2, 3]

    def test_seed(self):
        assert Random(pool=[1, 2, 3], periodicity=0).seed == None
        assert Random(pool=[1, 2, 3], periodicity=0, seed=10).seed == 10
        assert Random(pool=[1, 2, 3], periodicity=0, seed='Can be a string too').seed == 'Can be a string too'

    def test_get_previous_elements(self):
        r = Random(pool=[1, 3, 2, 4, 5], periodicity=2, seed=20)
        assert [r.__next__() for _ in range(20)] == [3, 2, 1, 5, 3, 1, 4, 3, 2, 4, 5, 3, 2, 4, 1, 5, 4, 1, 3, 5]

        assert r.get_previous_elements() == [3, 2, 1, 5, 3, 1, 4, 3, 2, 4, 5, 3, 2, 4, 1, 5, 4, 1, 3, 5]
