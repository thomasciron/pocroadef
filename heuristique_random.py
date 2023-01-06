import copy
import random

from solution import *
from instance import *


def pop(item, items, index):
    """Enlève un exemplaire de l'objet"""

    if items[index].copies <= 1:
        items.remove(item)
    else:
        items[index].copies -= 1
    return items


class HeuristiqueRandom:
    def __init__(self, instance):
        self.instance = instance
        self.truck_size = self.instance.truck.size_x, self.instance.truck.size_y
        self.insertion_point = (0, 0)
        self.insertion_mode = 1
        self.selected_items = []
        self.truck_count = 0
        self.maxY = 0
        self.solution = None

    def try_insert(self, item):
        x, y = self.insertion_point
        width = item.width * self.insertion_mode
        self.maxY = max(self.maxY, y + item.length)

        # Si on dépasse du camion on change et on reset
        if self.maxY > self.truck_size[1]:
            self.truck_count += 1
            self.insertion_mode = 1
            self.insertion_point = (0, 0)
            self.maxY = 0
            self.insert(item)

        # Si on dépasse en X on change de ligne et on inverse le remplissage
        elif 0 > x + width or x + width > self.truck_size[0]:
            self.insertion_mode *= -1
            self.insertion_point = (0 + (self.insertion_mode == -1) * self.truck_size[0], self.maxY)
            self.insert(item)

        else:
            self.insert(item)

    def insert(self, item):
        """Ne marche pas si un item ne rentre pas dans un camion vide"""
        x, y = self.insertion_point
        width = item.width * self.insertion_mode
        self.selected_items.append(ItemSelected(x, y, width, item.length, False, item.id, self.truck_count))
        self.insertion_point = (x + width, y)

    def solve(self):
        items_left = self.instance.items
        while len(items_left) > 0:
            index = random.randint(0, len(items_left)-1)
            item = items_left[index]
            self.try_insert(item)
            items_left = pop(item, items_left, index)
        self.solution = Solution(self.instance, self.selected_items, self.truck_count +1)


if __name__ == '__main__':
    instance1 = Instance(1)
    test = HeuristiqueRandom(instance1)
    test.solve()
    test.solution.draw_solution()
    print(test.truck_count)


