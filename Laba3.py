import time
from typing import List


# Реализация стека на основе массива
class ArrayStack:
    def __init__(self, size: int):
        self.size = size
        self.stack = [0] * size
        self.top = -1

    def push(self, value: int) -> None:
        if self.top + 1 < self.size:
            self.top += 1
            self.stack[self.top] = value
        else:
            raise OverflowError("Стек полон")

    def pop(self) -> int:
        if self.top >= 0:
            value = self.stack[self.top]
            self.top -= 1
            return value
        raise IndexError("Стек пуст")

    def is_empty(self) -> bool:
        return self.top == -1


# Реализация стека на основе связного списка
class Node:
    def __init__(self, data: int):
        self.data = data
        self.next = None


class LinkedListStack:
    def __init__(self):
        self.head = None

    def push(self, value: int) -> None:
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node

    def pop(self) -> int:
        if self.head is None:
            raise IndexError("Стек пуст")
        value = self.head.data
        self.head = self.head.next
        return value

    def is_empty(self) -> bool:
        return self.head is None


# Функция для моделирования сгибания и вычисления начальной нумерации
def compute_numbering(k: int, stack_type: str) -> List[int]:
    if k > 20:
        raise ValueError(f"Значение k={k} слишком велико. Максимально допустимое k=20 из-за ограничений памяти.")

    n = 2 ** k
    # Инициализация стека индексами от 0 до 2^k - 1
    if stack_type == "array":
        stack = ArrayStack(n)
    elif stack_type == "linked":
        stack = LinkedListStack()
    else:  # standard
        stack = []
    for i in range(n):
        if stack_type == "standard":
            stack.append(i)
        else:
            stack.push(i)
    for fold in range(k):
        half_size = n // (2 ** (fold + 1))
        if stack_type == "array":
            left = ArrayStack(half_size)
            right = ArrayStack(half_size)
        elif stack_type == "linked":
            left = LinkedListStack()
            right = LinkedListStack()
        else:
            left = []
            right = []
        for idx in range(half_size):
            if stack_type == "standard":
                if stack:
                    right.append(stack.pop())
                else:
                    raise IndexError("Попытка извлечь элемент из пустого стека")
            else:
                right.push(stack.pop())
        for idx in range(half_size):
            if stack_type == "standard":
                if stack:
                    left.append(stack.pop())
                else:
                    raise IndexError("Попытка извлечь элемент из пустого стека")
            else:
                left.push(stack.pop())
        while (not right.is_empty() if stack_type != "standard" else right):
            if stack_type == "standard":
                stack.append(right.pop())
            else:
                stack.push(right.pop())

        while (not left.is_empty() if stack_type != "standard" else left):
            if stack_type == "standard":
                stack.append(left.pop())
            else:
                stack.push(left.pop())
    result = [0] * n
    for i in range(n - 1, -1, -1):
        if stack_type == "standard":
            if stack:
                result[stack.pop()] = i + 1
            else:
                raise IndexError("Попытка извлечь элемент из пустого стека")
        else:
            result[stack.pop()] = i + 1

    return result
def test_performance(k_values: List[int]) -> None:
    print("\nСравнение производительности:")
    print(f"{'k':<5} {'Массив (с)':<12} {'Связный (с)':<12} {'Стандарт (с)':<12}")
    for k in k_values:
        try:
            # Массив
            start = time.time()
            compute_numbering(k, "array")
            array_time = time.time() - start

            # Связный список
            start = time.time()
            compute_numbering(k, "linked")
            linked_time = time.time() - start

            # Стандартная библиотека
            start = time.time()
            compute_numbering(k, "standard")
            standard_time = time.time() - start

            print(f"{k:<5} {array_time:<12.6f} {linked_time:<12.6f} {standard_time:<12.6f}")
        except ValueError as e:
            print(f"k={k}: {e}")
if __name__ == "__main__":
    print("Выполнил: Шишкалов Иван Дмитриевич, Группа: 090301-ПОВа-о24")
    k = 3
    print(f"\nНумерация для k={k}:")
    print("На основе массива:", compute_numbering(k, "array"))
    print("На основе связного списка:", compute_numbering(k, "linked"))
    print("Стандартная библиотека:", compute_numbering(k, "standard"))
    test_performance([12, 16, 20])