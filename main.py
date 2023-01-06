import solution
import os

class Item:
    """
    An item has to be loaded in a truck.
    """
    def __init__(self, x, y, width, length, t, i, f = False):
        """
        @param x : x coord insertion point
        @param y : y coord insertion point
        @param width : item width
        @param length : item length
        @param t : truck code (string)
        @param i : index of the item in the truck items list (int)
        @pararm f : True if the item has been flipped, False otherwise
        """
        self.code = ""
        self.nb_copies = 0
        self.length = length
        self.width = width
        self.height = 0
        self.nesting_height = 0
        self.weight = 0
        self.max_stackability = 0
        self.forced_orientation = False
        self.plant_code = 0
        self.plant_dock_code = ""
        self.supplier_code = 0
        self.supplier_dock_code = 0
        self.stackability_code = 0
        self.max_weight = 0 # poids max au dessus de cet item si celui-ci est placé tout en bas d'une pile
        self.supplier_loading_order = 0
        self.supplier_dock_loading_order = 0
        self.plant_dock_loading_order = 0
        self.insertion_point = (x,y)
        self.size = (width, length)
        self.is_flipped = f
        self.index = i
        self.truck = t
        self.posX = -1
        self.posY = -1

    def isRotateXAxis(self):
        """
        Checks if the object is rotated regarding the X axis.
        @return isRotate : True if the object is rotated, False otherwise
        """
        return self.width > self.length # ?
    
    def flip(self):
        if self.forced_orientation:
            pass
        else:
            self.height, self.width = self.width, self.height

    def setPosition(self,posX, posY):
        self.insertion_point = (posX, posY)
        #self.posX = posX
        #self.posY = posY

    def __repr__(self):
        return "Item " + self.code + " dim : " + str(self.size[1]) + " x " + str(self.size[0]) + " in " + str(self.nb_copies) + " copies not placed."

class Volume:
    def __init__(self, length, width, posX = 0, posY=0):
        self.length = length
        self.width = width
        self.posX = posX
        self.posY = posY

class RectangleObject:
    def __init__(self, length, width, posX = 0, posY = 0):
        self.length = length
        self.width = width
        self.posX = posX
        self.poxY = posY

    def setPosition(self, posX, posY):
        self.posX = posX
        self.posY = posY

class ResidualVolume:
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.unusable = False
        self.posX = 0
        self.posY = 0

    def setUnusable(self, unusable):
        self.unusable = unusable

    def setPosition(self, posX, posY):
        self.posX = posX
        self.posY = posY
    
    def __repr__(self):
        return "Residual Volume dim "+str(self.length) + " x " + str(self.width) + " at pos ("+str(self.posX)+";"+str(self.posY)+")"

    def __str__(self):
        return repr(self)
    
def doesObjectFit(obj, volume):
    if obj.length <= volume.length and obj.width <= volume.width:
        return True
    else:
        return False

class Truck:
    def __init__(self):
        self.code = ""
        self.estimated_nb_copies = 0 # estimated number of copies of this truck needed to load affected items
        self.length = 0
        self.width = 0
        self.height = 0
        self.max_total_weight = 0
        self.max_density = 0 # weight area ratio for a pile
        self.stack_with_multiple_dock = 0 # à ignorer pour le moment : on considère donc que deux items peuvent être empilés s'ils partagent les même dock, plant dock, supplier, supplier dock et stackability code 
        self.residualVolumes = []
        self.items = []
        self.placedItems = []

    def get_nb_items_to_place(self):
        """
        Get the number of items to place. Use the number of copies, the length of items list is not relevant.
        """
        nb_items_to_place = 0
        for i in range(len(self.items)):
            nb_items_to_place += self.items[i].nb_copies
        return nb_items_to_place
    
    def placeObject(self, obj, volume, indiceObj):
        obj.setPosition(volume.posX, volume.posY)
        v1 = ResidualVolume(volume.length - obj.length, volume.width)
        v2 = ResidualVolume(volume.length, volume.width - obj.width)
        v1.setPosition(volume.posX + obj.length, volume.posY)
        v2.setPosition(volume.posX, volume.posY + obj.posY)
        self.residualVolumes.remove(volume)
        self.residualVolumes.append(v1)
        self.residualVolumes.append(v2)
        self.placedItems.append(obj)
        self.items[indiceObj].nb_copies -= 1
        if self.items[indiceObj].nb_copies == 0:
            self.items.remove(self.items[indiceObj])

    def mergeResidualSpaces(self):
        """
        Merge as many residual spaces as it can be. 
        For each pair of residual space, check if both have the same width or length.
        If it is the case, the two residual spaces are merged.
        Stop when all the residual spaces pairs can't be merged anymore.
        """
        hasMerged = True
        while hasMerged:
            hasMerged = False
            i = 0
            j = 0
            while i < len(self.residualVolumes):
                j = i + 1
                while j < len(self.residualVolumes):
                    if self.residualVolumes[i].width == self.residualVolumes[j].width:
                        if self.residualVolumes[i].posY == self.residualVolumes[j].posY:
                            self.residualVolumes[i].length += self.residualVolumes[j].length
                            self.residualVolumes[i].posX = min(self.residualVolumes[i].posX, self.residualVolumes[j].posX)
                            self.residualVolumes.remove(self.residualVolumes[j])
                            hasMerged = True
                    elif self.residualVolumes[i].length == self.residualVolumes[j].length:
                        if self.residualVolumes[i].posX == self.residualVolumes[j].posX:
                            self.residualVolumes[i].width += self.residualVolumes[j].width
                            self.residualVolumes[i].posY = min(self.residualVolumes[i].posY, self.residualVolumes[j].posY)
                            self.residualVolumes.remove(self.residualVolumes[j])
                            hasMerged = True
                    j += 1
                i += 1

    def compute(self):
        """
        main function
        PRD heuristic
        """
        canStillFit = True
        self.residualVolumes.append(ResidualVolume(self.length, self.width))
        while len(self.residualVolumes) != 0 and len(self.items) != 0 and canStillFit:
            indiceVolume = 0
            boolVolume = False
            bestObjectIndex = -1
            bestVolume = None
            bestObject = None #RectangleObject(0, 0,0,0)
            while indiceVolume <= len(self.residualVolumes) and not boolVolume:
                bestVolume = self.residualVolumes[indiceVolume]
                found = False
                if not bestVolume.unusable:
                    for i in range(len(self.items)):
                        if doesObjectFit(self.items[i], bestVolume):
                            bestObject = self.items[i]
                            bestObjectIndex = i
                            found = True
                            break
                        elif not self.items[i].forced_orientation:
                            copy = self.items[i]  # With rotation axis X
                            # Ecrire la methode isRotateXAxis()
                            if doesObjectFit(copy, bestVolume) and copy.isRotateXAxis():
                                bestObject = copy
                                bestObjectIndex = i
                                found = True
                                break
                            else:
                                copy = self.items[i]  # With rotation axis Y
                                if doesObjectFit(copy, bestVolume) and copy.isRotateYAxis():
                                    bestObject = copy
                                    bestObjectIndex = i
                                    found = True
                                    break
                if not found:
                    indiceVolume += 1
                else:
                    boolVolume = True
                    break
            if bestObject is not None and bestVolume is not None and bestObjectIndex != -1:
                # Ecrire placeObject et mergeResidualSpaces
                self.placeObject(bestObject, bestVolume, bestObjectIndex)
                self.mergeResidualSpaces()
            canStillFit = boolVolume
            self.compute()

    def __repr__(self):
        return "Truck " +self.code + " dim : " + str(self.length) + " x " + str(self.width) + " with following items:\n\t" + "\n\t".join([repr(self.items[i]) for i in range(len(self.items))])

class Instance:
    """
    An instance is a list of trucks.
    """
    def __init__(self, instance_path):
        self.trucks = []
        self.loadInstance(instance_path)

    def loadInstance(self, instance_path):
        """
        Load an instance from a path.
        @param instance_path : instance path (format : "datasetA/../loading.csv")
        @return instance : instance for a problem
        """
        with open(instance_path, "r") as f:
            content = f.read().split("\n")
        tmp_truck = Truck()
        nb_items = 0
        for i in range(len(content)):
            content[i] = content[i].split(";")
            if len(content[i])>1:
                if nb_items == 0:
                    tmp_truck.code = content[i][1]
                    tmp_truck.estimated_nb_copies = int(content[i][2])
                    tmp_truck.length = int(content[i][3])
                    tmp_truck.width = int(content[i][4])
                    tmp_truck.height = int(content[i][5])
                    tmp_truck.max_total_weight = int(content[i][6])
                    tmp_truck.max_density = int(content[i][7])
                    tmp_truck.stack_with_multiple_dock = content[i][8] # je ne connais pas le format de ça il y est pas dans les instances je crois
                    nb_items -= 1
                elif nb_items == -1:
                    nb_items = int(content[i][1])
                else:
                    tmp_item = Item(-1,-1,int(content[i][4]),int(content[i][3]), tmp_truck.code, len(tmp_truck.items))
                    tmp_item.code = content[i][1]
                    tmp_item.nb_copies = int(content[i][2])
                    #tmp_item.length = int(content[i][3])
                    #tmp_item.width = int(content[i][4])
                    tmp_item.height = int(content[i][5])
                    tmp_item.nesting_height = int(content[i][6])
                    tmp_item.weight = float(content[i][7])
                    tmp_item.max_stackability = int(content[i][8])
                    tmp_item.forced_orientation = (content[i][9] != "none")
                    tmp_item.plant_code = int(content[i][10])
                    tmp_item.plant_dock_code = content[i][11]
                    tmp_item.supplier_code = int(content[i][12])
                    tmp_item.supplier_dock_code = content[i][13]
                    tmp_item.stackability_code = content[i][14]
                    tmp_item.max_weight = int(content[i][15])
                    tmp_item.supplier_loading_order = int(content[i][16])
                    tmp_item.supplier_dock_loading_order = int(content[i][17])
                    tmp_item.plant_dock_loading_order = int(content[i][18])
                    tmp_truck.items.append(tmp_item)
                    nb_items -= 1
                    if nb_items == 0:
                        self.trucks.append(tmp_truck)
                        tmp_truck = Truck()

    def solve(self):
        """
        Solve an instance. Apply the PRD heuristic to each truck of the instance.
        """
        for i in range(len(self.trucks)):
            #print(self.trucks[i])
            #print(self.trucks[i].get_nb_items_to_place(), "items to place...")
            self.trucks[i].compute()
            #print("=>", len(self.trucks[i].placedItems),"items placed !")

if __name__=="__main__":
    """
    instance = Instance("datasetA/BY/loading.csv")
    instance.solve()
    sol = solution.Solution(instance)
    sol.solution_is_verified()

    exit()
    """
    list_instance_dirs = os.listdir("datasetA/")
    good_solutions = 0
    for instance_dir in list_instance_dirs:
        instance = Instance("datasetA/" + instance_dir +"/loading.csv")
        instance.solve()
        sol = solution.Solution(instance)
        if sol.solution_is_verified():
            good_solutions += 1
        else:
            print("Problème instance",instance_dir)
    print("Solution réalisables trouvées : " + str(good_solutions) + "/"+str(len(list_instance_dirs)) + " (" + format(good_solutions*100/len(list_instance_dirs), ".2f") + "%)")
