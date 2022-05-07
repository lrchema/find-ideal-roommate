currAnimal = None #This is the global variable that stores current logged in user

class Animal():

    def __init__(self, email, name, password, species=None, image=None, isSetup=False):
        self.email = email
        self.name = name
        self.password = password
        self.species = species
        self.image = image
        self.isSetup = isSetup

    def insert(self):
        query = "insert into animals (name, email, password, issetup) values (%s, %s, %s, %s)"
        vals = (self.name, self.email, self.password, self.isSetup)
        return (query, vals)

    def profileSetup(self):
        self.isSetup = True
        query = "update animals set species=%s, image=%s, issetup=%s where email=%s"
        vals = (self.species, self.image, self.isSetup, self.email)
        return (query, vals)
    
    def __str__(self) -> str:
        return self.name+", "+self.email+", "+str(self.species)+", "+str(self.image)+", "+str(self.isSetup)

