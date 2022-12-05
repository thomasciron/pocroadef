class Instance:
    def __init__(self, index):
        with open("Instances/instance_"+str(index)+".txt", "r") as f:
            data = f.read().split("\n")
        truck_dimensions = data[0].split(" ")
        self.truck = Truck(int(truck_dimensions[1]), int(truck_dimensions[2]))
        self.items = []
        for i in range(1,len(data)):
            self.items.append(Item(data[i].split(" ")))


class Truck:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y

    def __str__(self):
        return "Truck : " + str(self.size_x) + " x " + str(self.size_x)


class Item:
    def __init__(self, data):
        self.id = int(data[0])
        self.copies = int(data[1])
        self.length = int(data[2])
        self.width = int(data[3])
        self.orientation_forced = bool(data[4])
        self.supplier = int(data[5])
        self.dock = int(data[6])

    def __str__(self):
        return "objet " + str(self.id)


# Un exemple d'utilisation de l'instance
"""
for i in range(100):
    instance = Instance(i)
    solve(instance)
"""