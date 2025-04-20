# Класс узла префиксного дерева для алгоритма Ахо-Корасик
class Node:
    def __init__(self):
        self.children = {}      # Дочерние узлы (ключ - символ, значение - узел)
        self.fail = None       # Суффиксная ссылка
        self.output = []       # Индексы шаблонов, заканчивающихся в этом узле


class AhoCorasick:
    def __init__(self):
        self.root = Node()     # Корневой узел
        self.patterns = []    # Список шаблонов для поиска

    def add_patterns(self, patterns):
        """Добавляет шаблоны в префиксное дерево"""
        self.patterns = patterns
        print(f"\nДобавление {len(patterns)} шаблонов в дерево...")
        for i, pattern in enumerate(patterns):
            print(f"    Добавляем шаблон #{i + 1}: '{pattern}'")
            self._add_pattern(pattern, i + 1)  # Индексация с 1

    def _add_pattern(self, pattern, index):
        """Добавляет один шаблон в дерево"""
        node = self.root
        for char in pattern:
            if char not in node.children:
                node.children[char] = Node()
            node = node.children[char]
        node.output.append(index)  # Помечаем конечный узел

    def build_automaton(self):
        """Строит конечный автомат с суффиксными ссылками"""
        from collections import deque
        queue = deque()
        print("\nПостроение суффиксных ссылок...")

        # Инициализация: fail-ссылки потомков root ведут в root
        for char, child in self.root.children.items():
            child.fail = self.root
            queue.append(child)
            print(f"    Узел '{char}': fail -> root")

        # BFS для построения fail-ссылок
        while queue:
            current = queue.popleft()

            for char, child in current.children.items():
                fail_node = current.fail

                # Ищем первый узел в fail-цепочке с переходом по char
                while fail_node and char not in fail_node.children:
                    fail_node = fail_node.fail

                child.fail = fail_node.children[char] if fail_node else self.root
                child.output += child.fail.output  # Наследуем output

                print(f"    Узел '{char}': fail -> {child.fail.output if child.fail else 'root'}")
                queue.append(child)

    def search(self, text):
        """Ищет все вхождения шаблонов в тексте"""
        node = self.root
        result = []
        print(f"\nПоиск в тексте: '{text}'")

        for i, char in enumerate(text):
            # Переход по fail-ссылкам при несоответствии
            while node != self.root and char not in node.children:
                node = node.fail

            node = node.children.get(char, self.root)

            # Добавляем найденные шаблоны в результат
            for pattern_idx in node.output:
                pattern = self.patterns[pattern_idx - 1]
                start = i - len(pattern) + 2  # +2 для корректной позиции
                print(f"    Найден #{pattern_idx} '{pattern}' на позиции {start}")
                result.append((start, pattern_idx))

        print("\nПоиск завершен.")
        return sorted(result)

    def calculate_longest_chains(self):
        """Вычисляет и отображает информацию о самых длинных цепочках fail и output ссылок"""
        from collections import deque

        def reconstruct_chain(node, only_with_output=False):
            """Реконструирует цепочку по fail-ссылкам"""
            chain = []
            visited = set()
            while node and node.fail and id(node) not in visited:
                visited.add(id(node))
                if not only_with_output or node.output:
                    parent = node.fail
                    symbol = next((k for k, v in parent.children.items() if v == node), '?')
                    chain.append((symbol, node.output[:]))
                node = node.fail
            return chain[::-1]  # от корня к листу

        max_fail_len = 0
        max_output_len = 0
        max_fail_node = None
        max_output_node = None

        queue = deque([(self.root, 0)])
        while queue:
            node, depth = queue.popleft()

            fail_chain = reconstruct_chain(node)
            output_chain = reconstruct_chain(node, only_with_output=True)

            if len(fail_chain) > max_fail_len:
                max_fail_len = len(fail_chain)
                max_fail_node = node

            if len(output_chain) > max_output_len:
                max_output_len = len(output_chain)
                max_output_node = node

            for child in node.children.values():
                queue.append((child, depth + 1))

        print("\n--- АНАЛИЗ ЦЕПОЧЕК ---")
        print(f"\n[FAIL] Самая длинная цепочка fail-ссылок ({max_fail_len}):")
        chain = reconstruct_chain(max_fail_node)
        for i, (symbol, output) in enumerate(chain):
            print(f"  Уровень {i+1}: символ '{symbol}' | output = {output}")

        print(f"\n[OUTPUT] Самая длинная цепочка output-ссылок ({max_output_len}):")
        chain = reconstruct_chain(max_output_node, only_with_output=True)
        for i, (symbol, output) in enumerate(chain):
            print(f"  Уровень {i+1}: символ '{symbol}' | output = {output}")

        return max_fail_len, max_output_len


def main():
    print("=== АЛГОРИТМ АХО-КОРАСИКА ===")
    text = input("\nВведите текст для поиска:\n").strip()
    n = int(input("Введите количество шаблонов:\n"))
    print("Введите шаблоны (по одному в строке):")
    patterns = [input(f"{i+1}) ").strip() for i in range(n)]

    # Инициализация и поиск
    ac = AhoCorasick()
    ac.add_patterns(patterns)
    ac.build_automaton()
    matches = ac.search(text)

    # Вычисление длин цепочек
    max_fail, max_output = ac.calculate_longest_chains()
    print(f"\nДлина самой длинной цепочки из суффиксных ссылок: {max_fail}")
    print(f"Длина самой длинной цепочки из конечных ссылок: {max_output}")

    # Вывод результатов поиска
    if matches:
        print("\nРезультаты (позиция, номер шаблона):")
        for pos, idx in matches:
            print(f"  Позиция {pos}: #{idx} '{patterns[idx-1]}'")
    else:
        print("\nСовпадений не найдено.")


if __name__ == "__main__":
    main()
