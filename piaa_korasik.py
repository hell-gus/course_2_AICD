from collections import deque
from colorama import init, Fore, Style

# Инициализация colorama
init(autoreset=True)

class Node:
    def __init__(self):
        self.children = {}      # Дочерние узлы (ключ - символ, значение - узел)
        self.fail = None        # Суффиксная ссылка
        self.output = []        # Индексы шаблонов, заканчивающихся в этом узле


class AhoCorasick:
    def __init__(self):
        self.root = Node()      # Корневой узел
        self.patterns = []      # Список шаблонов для поиска

    def add_patterns(self, patterns):
        """Добавляет шаблоны в префиксное дерево"""
        self.patterns = patterns
        print(f"\n{Fore.CYAN}Добавление {len(patterns)} шаблонов в дерево...{Style.RESET_ALL}")
        for i, pattern in enumerate(patterns):
            print(f"    {Fore.CYAN}Добавляем шаблон #{i + 1}: '{pattern}'{Style.RESET_ALL}")
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
        queue = deque()
        print(f"\n{Fore.YELLOW}Построение суффиксных ссылок...{Style.RESET_ALL}")

        # Инициализация: fail-ссылки потомков root ведут в root
        for char, child in self.root.children.items():
            child.fail = self.root
            queue.append(child)
            print(f"    Узел '{char}': fail -> root")

        # BFS для построения fail-ссылок
        while queue:
            current = queue.popleft()

            for char, child in current.children.items():
                print(f"\n    Обрабатываем узел по символу '{char}'")
                fail_node = current.fail

                while fail_node and char not in fail_node.children:
                    print(f"        fail-ссылка от текущего узла не содержит '{char}', идем вверх...")
                    fail_node = fail_node.fail

                if fail_node:
                    child.fail = fail_node.children[char]
                    print(f"        Найден fail-переход по '{char}', fail -> output {child.fail.output}")
                else:
                    child.fail = self.root
                    print(f"        fail-ссылка не найдена, устанавливаем на root")

                child.output += child.fail.output
                if child.output:
                    print(f"        Наследуем output: {child.output}")
                else:
                    print("        Output пуст")

                queue.append(child)

    def search(self, text):
        """Ищет все вхождения шаблонов в тексте"""
        node = self.root
        result = []
        print(f"\n{Fore.GREEN}Поиск в тексте: '{text}'{Style.RESET_ALL}")

        for i, char in enumerate(text):
            print(f"\nСимвол #{i + 1}: '{char}'")

            while node != self.root and char not in node.children:
                print(f"    Перехода по '{char}' нет, следуем по fail-ссылке...")
                node = node.fail

            if char in node.children:
                node = node.children[char]
                print(f"    Совершён переход по '{char}'")
            else:
                node = self.root
                print(f"    Символ '{char}' не найден, возвращаемся к root")

            for pattern_idx in node.output:
                pattern = self.patterns[pattern_idx - 1]
                start = i - len(pattern) + 2
                print(f"    >> Найден шаблон #{pattern_idx} '{pattern}' на позиции {start}")
                result.append((start, pattern_idx))

        print("\nПоиск завершен.")
        return sorted(result)

    def display_trie(self):
        """Визуально отображает дерево шаблонов"""
        def dfs(node, prefix='', is_last=True):
            connector = '└── ' if is_last else '├── '
            marker = f"{Fore.GREEN}[{','.join(map(str, node.output))}]{Style.RESET_ALL}" if node.output else ''
            print(f"{prefix}{connector}{marker}")

            children = list(node.children.items())
            for i, (char, child) in enumerate(children):
                is_last_child = i == len(children) - 1
                child_prefix = prefix + ('    ' if is_last else '│   ')
                print(f"{child_prefix}{Fore.CYAN}{char}{Style.RESET_ALL}")
                dfs(child, child_prefix, is_last_child)

        print(f"{Fore.MAGENTA}\nВизуализация дерева шаблонов:{Style.RESET_ALL}")
        dfs(self.root)


def main():
    print(f"{Fore.MAGENTA}=== АЛГОРИТМ АХО-КОРАСИКА ==={Style.RESET_ALL}")
    text = input("\nВведите текст для поиска:\n").strip()
    n = int(input("Введите количество шаблонов:\n"))
    print("Введите шаблоны (по одному в строке):")
    patterns = [input(f"{i+1}) ").strip() for i in range(n)]

    # Инициализация и поиск
    ac = AhoCorasick()
    ac.add_patterns(patterns)
    ac.display_trie()  # Визуализация дерева шаблонов
    ac.build_automaton()
    matches = ac.search(text)

    # Вывод результатов поиска
    if matches:
        print("\nРезультаты (позиция, номер шаблона):")
        for pos, idx in matches:
            print(f"  Позиция {pos}: #{idx} '{patterns[idx-1]}'")
    else:
        print("\nСовпадений не найдено.")


if __name__ == "__main__":
    main()
