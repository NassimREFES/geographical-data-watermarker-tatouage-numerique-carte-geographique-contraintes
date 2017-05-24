import copy

def checkindex(key):
    """
    verifier si le key choisi pour le dictionnaire est un entier
    key = clÃ© de chaque items
    """
    if not isinstance(key, int): raise TypeError
    if key<0: raise IndexError

class Doc():
    """
    Doc est une representation d'un conteneur qui contient des sommets d'une carte
    avec leur informations respectif 
    """
    def __init__(self):
        self.__pos = [] # contient les coords
        self.__pos_objet = []        # contient numero des objets
        self.__pos_objet_sommet = [] # contient position des sommet dans l'objet
        self.__objet_type = [] # type de l'objet 
        self.list_sommet = {}
        self.max_pos = list([-1, -1])
        self.min_pos = list([-1, -1])

    def __getitem__(self, key):
        """
        recuperer la valeur (position en coordonnÃ©e xy) a l'indice - key -
        key = l'indice choisi ou bien tout la liste
        """
        try: checkindex(key)
        except TypeError: # Doc[:] est applÃ© alor en retourn tt les pos
            return self.__pos[:]
        try: return self.__pos[key]
        except KeyError:
            return key

    def __setitem__(self, key, value):
        """
        modifier la valeur a l'indice key
        key     = l'indice choisi
        value   = nouvelle valeur
        """
        checkindex(key)
        self.__pos[key] = value

    def __len__(self):
        """
        taille du document ( carte )
        """
        return len(self.__pos)

    def ajoute_sommet(self, pos_xy, pos_objet, pos_objet_sommet, objet_type):
        """
        ajoute un sommet dans le document ( carte )
        pos_xy           = position en cordonnÃ©e xy
        pos_objet        = numero de l'objet
        pos_objet_sommet = position du sommet dans l'objet
        objet_type       = type (geometrique) de l'objet 
        """
        # tout sommet dans le document
        s = complex(pos_xy[0], pos_xy[1])
        try:
            self.list_sommet[s].append(tuple([pos_xy, pos_objet, pos_objet_sommet]))
        except KeyError:
            self.list_sommet[s] = []
            self.list_sommet[s].append(tuple([pos_xy, pos_objet, pos_objet_sommet]))

        self.__pos.append(pos_xy)
        #super(self.__class__, self).append(pos_xy)
        self.__pos_objet.append(pos_objet)
        self.__pos_objet_sommet.append(pos_objet_sommet)
        self.__objet_type.append(objet_type)

        # borner les points du document dans un rectangle
        if self.max_pos == [-1, -1] and self.min_pos == [-1, -1]:
            self.max_pos = list(pos_xy)
            self.min_pos = list(pos_xy)
            return
        if self.max_pos[0] < pos_xy[0]:
            self.max_pos[0] = pos_xy[0]
        if self.max_pos[1] < pos_xy[1]:
            self.max_pos[1] = pos_xy[1]
        if pos_xy[0] < self.min_pos[0]:
            self.min_pos[0] = pos_xy[0]
        if pos_xy[1] < self.min_pos[1]:
            self.min_pos[1] = pos_xy[1]

    def ajoute_sommet_at(self, pos_xy, pos_objet, pos_objet_sommet, objet_type, index):
        """
        ajoute un sommet dans le document ( carte ) en position specifique
        pos_xy           = position en cordonnÃ©e xy
        pos_objet        = numero de l'objet
        pos_objet_sommet = position du sommet dans l'objet
        objet_type       = type (geometrique) de l'objet 
        index            = position dans le document
        """
        # tout sommet dans le document
        s = complex(pos_xy[0], pos_xy[1])
        try:
            self.list_sommet[s].append(tuple([pos_xy, pos_objet, pos_objet_sommet]))
        except KeyError:
            self.list_sommet[s] = []
            self.list_sommet[s].append(tuple([pos_xy, pos_objet, pos_objet_sommet]))

        self.__pos.insert(index, pos_xy)
        #super(self.__class__, self).append(pos_xy)
        self.__pos_objet.insert(index, pos_objet)
        self.__pos_objet_sommet.insert(index, pos_objet_sommet)
        self.__objet_type.insert(index, objet_type)

    def calcule_max_min_pos(self):
        """
        borner les points du document ( carte ) dans un rectangle
        """
        self.max_pos = list([-1, -1])
        self.min_pos = list([-1, -1])

        for i in range(0, len(self.__pos)):
            if self.max_pos == [-1, -1] and self.min_pos == [-1, -1]:
                self.max_pos = list(self.__pos[i])
                self.min_pos = list(self.__pos[i])
                continue
            if self.max_pos[0] < self.__pos[i][0]:
                self.max_pos[0] = self.__pos[i][0]
            if self.max_pos[1] < self.__pos[i][1]:
                self.max_pos[1] = self.__pos[i][1]
            if self.__pos[i][0] < self.min_pos[0]:
                self.min_pos[0] = self.__pos[i][0]
            if self.__pos[i][1] < self.min_pos[1]:
                self.min_pos[1] = self.__pos[i][1]

    def supprimer_sommet(self, index):
        """
        supprimer un sommet du document ( carte ) a l'indice donnÃ©e
        index = indice choisi
        """
        self.__test_index(index)
        s = complex(self.__pos[index][0],
                    self.__pos[index][1])

        if self.list_sommet[s]:
            l = self.list_sommet[s]
            for i in l:
                if i[1] == self.__pos_objet[index] and i[2] == self.__pos_objet_sommet[index]:
                    del i
                    break
            #del self.list_sommet[s]

        del self.__pos[index]
        del self.__pos_objet[index]
        del self.__pos_objet_sommet[index]
        del self.__objet_type[index]

    def index_of(self, obj):
        """
        recuperer l'indice d'un site
        """
        for i in range(0, len(self.__pos)):
            if obj[0] == self.__pos[i] and \
                obj[1] == self.__pos_objet[i] and obj[2] == self.__pos_objet_sommet[i]:
                return i

    def get_by_coord(self, coord):
        """
        recuperer tout les sites avec leur coordonnÃ©e xy
        coord = position en coordonnÃ©e xy
        """
        return self.list_sommet[complex(coord[0], coord[1])]

    def get(self, index):
        """
        recuperer un site (position xy du sommet + l'objet ou est contenu + position dans l'objet)
        a l'indice donnÃ©
        index = indice choisi
        """
        # avoir position xy du sommet + l'objet ou est contenu + position dans l'objet
        self.__test_index(index)
        return (self.__pos[index], self.__pos_objet[index], self.__pos_objet_sommet[index])

    def get_objet_type(self, index):
        """
        recuperer le type de l'objet
        index = indice choisi
        """
        self.__test_index(index)
        return self.__objet_type[index]

    def set(self, index, *arg):
        """
        modifier un site a l'indice index avec les arguments *arg
        index = indice choisi
        *arg = un site
        """
        # modifier un sommet
        self.__test_index(index)
        arg = arg[0]
        if len(arg) == 3:
            s = complex(self.__pos[index][0],
                        self.__pos[index][1])
            self.__pos[index] = tuple(arg[0])
            self.__pos_objet[index]          = arg[1]
            self.__pos_objet_sommet[index]   = arg[2]

            if self.list_sommet[s]:
                l = self.list_sommet[s]
                for i in l:
                    if i[1] == self.__pos_objet[index] and i[2] == self.__pos_objet_sommet[index]:
                        del i
                        break

            s = complex(arg[0][0], arg[0][1])
            try:
                self.list_sommet[s].append(tuple([arg[0], arg[1], arg[2]]))
            except KeyError:
                self.list_sommet[s] = []
                self.list_sommet[s].append(tuple([arg[0], arg[1], arg[2]]))
        else:
            raise Exception('Doc : number of arguments is not supported')

    def __test_index(self, index):
        """
        verifier l'indice donnÃ© 
        index = indice choisi
        """
        if index < 0 or index > len(self.__pos)-1:
            raise Exception('Doc : index out of range')



