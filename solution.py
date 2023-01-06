import tkinter as tk
from instance import *


class ItemSelected:
    def __init__(self, x, y, wdt, lght, is_flipped, i, t):
        self.insertion_point = (x, y)
        self.size = (wdt, lght)
        self.is_flipped = is_flipped
        self.index = i
        self.truck = t


class Solution:
    def __init__(self, instance, item_list, truck_count=0):
        self.instance = instance
        self.item_list = item_list
        self.map = [[] for i in range(truck_count)]
        self.make_map()

    def make_map(self):
        for item in self.item_list:
            self.map[item.truck].append(item)

    def draw_solution(self):
        draw_truck_contain((self.instance.truck.size_x, self.instance.truck.size_y), self.map[0])
        draw_truck_contain((self.instance.truck.size_x, self.instance.truck.size_y), self.map[1])

    def item_flip_is_verified(self, item):
        """Verifie que la contrainte de flip est respecté (True si respecté False sinon)"""
        instance_constaint = self.instance.items[item.index].orientation_forced
        # seul cas bloquant on a pas le droit de flip mais on l'a fait
        if instance_constaint and item.is_flipped:
            return False
        else:
            return True

    def item_is_in_truck(self, item):
        """Indique si l'oject dépasse du camion"""
        max_x, max_y = item.insertion_point[0] + item.size[0], item.insertion_point[1] + item.size[1]
        if max_x > self.instance.truck.size_x or max_y > self.instance.truck.size_y:
            return False
        else:
            return True

    def order_is_verified(self):
        """Indique si la contrainte de l'ordre est verifiée"""
        max_index = len(self.item_list)
        for reference in range(max_index - 1):
            for comparaison in range(reference + 1, max_index):

                item_ref = self.item_list[reference]
                item_comp = self.item_list[comparaison]

                # On compare les items que s'ils sont dans le même truck
                if item_ref.truck == item_comp.truck:
                    supplier_ref = self.instance.items[item_ref.index].supplier
                    supplier_comp = self.instance.items[item_comp.index].supplier

                    dock_ref = self.instance.items[item_ref.index].dock
                    dock_comp = self.instance.items[item_comp.index].dock

                    different_supplier = supplier_ref != supplier_comp
                    different_dock = dock_ref != dock_comp

                    # On test les contraintes que si les docks ou les suppliers sont différents
                    if different_supplier or different_dock:
                        # axe de reference de la contrainte
                        axis = 0

                        insertion_point_ref = item_ref.insertion_point[axis]
                        insertion_point_comp = item_comp.insertion_point[axis]

                        # Bloquant 1 : notre item de ref est plus loin que le comparé mais à un supplier plus petit
                        if insertion_point_ref > insertion_point_comp and supplier_ref < supplier_comp:
                            print("Item de reference (", reference, ")",
                                  "a un PI sup mais supplier inf avec l'item' : ", comparaison)
                            return False

                        # Bloquant 2 : notre item de ref est moins loin que le comparé mais à un supplier plus grand
                        if insertion_point_ref < insertion_point_comp and supplier_ref > supplier_comp:
                            print("Item de reference (", reference, ")",
                                  "a un PI inf mais supplier sup avec l'item' : ", comparaison)
                            return False

                        # Bloquant 3 : notre item de ref est plus loin que le comparé mais à un dock plus petit
                        if insertion_point_ref > insertion_point_comp and dock_ref < dock_comp:
                            print("Item de reference (", reference, ")",
                                  "a un PI sup mais dock inf avec l'item' : ", comparaison)
                            return False

                        # Bloquant 4 : notre item de ref est moins loin que le comparé mais à un dock plus grand
                        if insertion_point_ref < insertion_point_comp and dock_ref > dock_comp:
                            print("Item de reference (", reference, ")",
                                  "a un PI inf mais dock sup avec l'item' : ", comparaison)
                            return False
        return True

    def solution_is_verified(self):
        """Indique si la solution est valide et prompte quelle contrainte ne passe pas le cas échéant"""
        # On test les conditions propres aux items
        for id_item in range(len(self.item_list)):
            if not self.item_flip_is_verified(self.item_list[id_item]):
                print("L'item ", id_item, "a été flip alors qu'il n'aurait pas du l'être")
                return False
            if not self.item_is_in_truck(self.item_list[id_item]):
                print("L'item ", id_item, "dépasse les dimensions du camion")
                return False

        # Si tout ok pour les items alors on verifie l'ordre
        return self.order_is_verified()

def draw_item(canva,origin,size,color='lightblue'):
    canva.create_rectangle(origin[0], origin[1], origin[0]+size[0], origin[1]+size[1], fill=color)

def draw_truck_contain(root, index,truck_size, items):
    cnv_size = 350, 350
    scale = (min(cnv_size) / max(truck_size)) *0.9

    displayed_truck = (truck_size[0] * scale, truck_size[1] * scale)
    cnv = tk.Canvas(root, width=cnv_size[0], height=cnv_size[1], bg="ivory")
    x0 = cnv_size[0] // 2 - displayed_truck[0] // 2
    y0 = cnv_size[1] // 2 - displayed_truck[1] // 2

    draw_item(cnv, (x0, y0), displayed_truck, "white")
    for item in items:
        new_size = tuple([scale*x for x in item.size])
        new_insertion_point = tuple([scale*x for x in item.insertion_point])
        draw_item(cnv, (x0+new_insertion_point[0], y0+new_insertion_point[1]), new_size)
    cnv.grid(column=index % 5,row=index //5)

def draw_ten_truck():
    root = tk.Tk()
    for k in range(10):
        draw_truck_contain(root, k, (1000, 2000),
                           [ItemSelected(0, 0, 100, 200, False, 0, 0), ItemSelected(100, 0, 100, 200, False, 0, 0)])

    root.mainloop()


if __name__ == '__main__':
    draw_ten_truck()



