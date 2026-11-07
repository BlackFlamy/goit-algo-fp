"""Завдання 1. Однозв'язний список: реверсування, сортування злиттям, об'єднання відсортованих списків."""


class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    @classmethod
    def from_iterable(cls, values):
        ll = cls()
        for v in values:
            ll.insert_at_end(v)
        return ll

    def to_list(self):
        result, cur = [], self.head
        while cur:
            result.append(cur.data)
            cur = cur.next
        return result

    def __str__(self):
        return " -> ".join(map(str, self.to_list())) or "(порожній)"

    # 1. Реверсування: змінюємо посилання next кожного вузла
    def reverse(self):
        prev, cur = None, self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    # 2. Сортування злиттям: O(n log n), без додаткових масивів
    def sort(self):
        self.head = _merge_sort(self.head)


def _split(head):
    """Ділить список навпіл методом повільного/швидкого вказівника."""
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    middle = slow.next
    slow.next = None
    return head, middle


def _merge_nodes(a, b):
    """Зливає два відсортовані ланцюжки вузлів в один (ітеративно)."""
    dummy = tail = Node()
    while a and b:
        if a.data <= b.data:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next


def _merge_sort(head):
    if head is None or head.next is None:
        return head
    left, right = _split(head)
    return _merge_nodes(_merge_sort(left), _merge_sort(right))


# 3. Об'єднання двох відсортованих списків в один відсортований
def merge_sorted_lists(list1, list2):
    merged = LinkedList()
    merged.head = _merge_nodes(list1.head, list2.head)
    # вузли тепер належать новому списку
    list1.head = list2.head = None
    return merged


if __name__ == "__main__":
    ll = LinkedList.from_iterable([5, 3, 8, 1, 9, 2])
    print("Початковий список:   ", ll)

    ll.reverse()
    print("Після реверсування:  ", ll)

    ll.sort()
    print("Після сортування:    ", ll)

    a = LinkedList.from_iterable([1, 4, 7, 10])
    b = LinkedList.from_iterable([2, 3, 8, 12, 15])
    print("\nСписок A:", a)
    print("Список B:", b)
    print("Об'єднаний:", merge_sorted_lists(a, b))
