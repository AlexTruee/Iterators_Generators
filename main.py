# 1. Написать итератор, который принимает список списков, и возвращает их плоское представление,
# т.е последовательность состоящую из вложенных элементов. Например
import types


class FlatIterator:
    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.main_cursor = 0
        self.nested_cursor = -1
        return self

    def __next__(self):
        self.nested_cursor += 1
        if self.nested_cursor == len(self.list_of_list[self.main_cursor]):
            self.main_cursor += 1
            self.nested_cursor = 0
            if self.main_cursor == len(self.list_of_list):
                raise StopIteration
        return self.list_of_list[self.main_cursor][self.nested_cursor]


def test_1(list_of_lists):
    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


# 2. Написать генератор, который принимает список списков, и возвращает их плоское представление.
def flat_generator(main_list):
    for main_item in main_list:
        for current_item in main_item:
            yield current_item


def test_2(list_of_lists):

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists), types.GeneratorType)


# '3. * Написать итератор аналогичный итератору из задания 1, '
# 'но обрабатывающий списки с любым уровнем вложенности'
class FlatIteratorEnhanced:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        self.nested_list = []
        self.current_iterator = iter(self.list_of_list)
        return self

    def __next__(self):
        while True:
            try:
                self.current_element = next(self.current_iterator)
            except StopIteration:
                if not self.nested_list:
                    raise StopIteration
                else:
                    self.current_iterator = self.nested_list.pop()
                    continue
            if isinstance(self.current_element, list):
                self.nested_list.append(self.current_iterator)
                self.current_iterator = iter(self.current_element)
            else:
                return self.current_element


def test_3(list_of_list):

    for flat_iterator_item, check_item in zip(
            FlatIteratorEnhanced(list_of_list),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIteratorEnhanced(list_of_list)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


# '4. * Написать генератор аналогичный генератор из задания 2, '
# 'но обрабатывающий списки с любым уровнем вложенности'
def flat_generator_enhanced(list_of_list):
    for elem in list_of_list:
        if isinstance(elem, list):
            for sub_item in flat_generator_enhanced(elem):
                yield sub_item
        else:
            yield elem


def test_4(list_of_lists):

    for flat_iterator_item, check_item in zip(
            flat_generator_enhanced(list_of_lists),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator_enhanced(list_of_lists)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator_enhanced(list_of_lists), types.GeneratorType)


if __name__ == '__main__':
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    try:
        test_1(list_of_lists_1)
        test_1(list_of_lists_1)
        test_2(list_of_lists_1)
        test_3(list_of_lists_2)
        test_4(list_of_lists_2)
        print('Все тесты прошли без ошибок')
    except AssertionError:
        print(f'Возникли ошибки')