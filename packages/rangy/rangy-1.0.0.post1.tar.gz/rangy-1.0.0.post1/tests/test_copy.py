
import copy

from rangy import Rangy


def test_shallow_copy():
    rangy1 = Rangy(5)
    rangy_copy = copy.copy(rangy1)
    assert rangy1 == rangy_copy
    assert rangy1 is not rangy_copy

def test_deep_copy():
    rangy1 = Rangy("2-4")
    rangy_deepcopy = copy.deepcopy(rangy1)
    assert rangy1 == rangy_deepcopy
    assert rangy1 is not rangy_deepcopy