def bubble_sort(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    for col in range(cols):

        i = 1
        while i < rows:
            j = rows - 1
            while j >= i:

                if matrix[j][col] < matrix[j - 1][col]:
                    x = matrix[j - 1][col]
                    matrix[j - 1][col] = matrix[j][col]
                    matrix[j][col] = x

                j -= 1

            i += 1

    return matrix

def row_average(row):
    return sum(row) / len(row)

def product(values):
    result = 1
    for v in values:
        result *= v
    return result

class Node:
    def __init__(self, order_type, client):
        self.order_type = order_type
        self.client = client
        self.next = None

class TaxiQueue:
    def __init__(self):
        self.head = None

    def add_order(self, order_type, client):
        new_node = Node(order_type, client)

        if order_type == "vip":
            new_node.next = self.head
            self.head = new_node
        else:
            if not self.head:
                self.head = new_node
                return

            p = self.head
            while p.next:
                p = p.next
            p.next = new_node

    def get_order(self):
        if not self.head:
            return None

        result = self.head
        self.head = self.head.next
        return result.order_type, result.client

    def show(self):
        p = self.head
        while p:
            print(f"[{p.order_type}] {p.client}")
            p = p.next

if __name__ == "__main__":

    m = [
        [40, 72, 6, 92, 98],
        [18, -33, -48, 81, 26],
        [1, -4, 6, -2, 0],
        [36, 9, 0, 4, 1],
        [-55, 2, 66, 70, -3]
    ]

    print("Початкова матриця:")
    for row in m:
        print(row)

    sorted_matrix = bubble_sort(m)

    print("\nВідсортована матриця:")
    for row in sorted_matrix:
        print(row)

    fi_values = [row_average(row) for row in sorted_matrix]

    print("\nЗначення fi(aij) - середні значення рядків:")
    for i, v in enumerate(fi_values):
        print(f"fi(row {i+1}) = {v:.1f}")

    F_value = product(fi_values)

    print(f"\nF(fi(aij)) = {F_value:.1f}")

    print("\n---------ЗАВДАННЯ 2----------")

    queue = TaxiQueue()

    queue.add_order("normal", "Клієнт 1")
    queue.add_order("vip", "VIP 1")
    queue.add_order("normal", "Клієнт 2")
    queue.add_order("vip", "VIP 2")

    print("Поточна черга:")
    queue.show()

    print("\nВодій отримав замовлення:")
    print(queue.get_order()) 

    print("\nЧерга після обслуговування:")
    queue.show()
