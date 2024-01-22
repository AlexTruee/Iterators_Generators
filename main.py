
# 1. Написать итератор, который принимает список списков, и возвращает их плоское представление,
# т.е последовательность состоящую из вложенных элементов. Например

class FlatIterator:
    def __init__(self, main_list):
        self.main_list = main_list

    def __iter__(self):
        self.main_cursor = 0
        self.nested_cursor = -1
        return self

    def __next__(self):
        self.nested_cursor += 1
        if self.nested_cursor == len(self.main_list[self.main_cursor]):
            self.main_cursor += 1
            self.nested_cursor = 0
            if self.main_cursor == len(self.main_list):
                raise StopIteration
        return self.main_list[self.main_cursor][self.nested_cursor]


# 2. Написать генератор, который принимает список списков, и возвращает их плоское представление.
def flat_generator(main_list):
    for main_item in main_list:
        for current_item in main_item:
            yield current_item


# '3. * Написать итератор аналогичный итератору из задания 1, '
# 'но обрабатывающий списки с любым уровнем вложенности'
class FlatIteratorEnhanced:

    def __init__(self, main_list):
        self.main_list = main_list

    def __iter__(self):
        self.nested_list = []
        self.current_iterator = iter(self.main_list)
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


# '4. * Написать генератор аналогичный генератор из задания 2, '
# 'но обрабатывающий списки с любым уровнем вложенности'
def flat_generator_enhanced(main_list):
    for elem in main_list:
        if isinstance(elem, list):
            for sub_item in flat_generator_enhanced(elem):
                yield sub_item
        else:
            yield elem


if __name__ == '__main__':

    nested_list = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None],
    ]
    nested_list_gen = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f'],
        [1, 2, None],
    ]
    test_nested_list = [
        ['a', ['b', ['c']], 'd'],
        ['e', ['f', ['h', ['j', [False]], 1]]],
        [2, 3, None], [[[4, 5, 7], [5, 9]]]
    ]

    print('* Запускаем итератор')
    for item in FlatIterator(nested_list):
        print(item)

    print('-' * 20)
    print('* Запускаем  комперхеншн')
    flat_list = [item for item in FlatIterator(nested_list)]
    print(flat_list)

    print('-' * 20)
    print('* Запускаем  генератор')
    for item in flat_generator(nested_list_gen):
        print(item)

    print('-' * 20)
    print('Запускаем расширенный итератор')
    for item in FlatIteratorEnhanced(test_nested_list):
        print(item)

    print('-' * 20)
    print('* Запускаем  комперхеншн')
    flat_list = [item for item in FlatIteratorEnhanced(test_nested_list)]
    print(flat_list)

    print('-' * 20)
    print('Запускаем расширенный генератор')
    for item in flat_generator_enhanced(test_nested_list):
        print(item)


