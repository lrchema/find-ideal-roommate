curruser_info = None #This is the global variable that stores current logged in user

class user_info():

    def __init__(self,username,email,  password, is_profile_setup=False,name=None, Gender=None,age=None,Lang=None,room_city=None, 
                 room_area=None,dist_to_transport=None,Food_pref=None,drinker=None,Shift=None, profile_picture=None,En_suite_bathroom=None,Passions=None,have_roof=None):
   
        self.username=username
        self.email = email
        self.password = password
        self.is_profile_Setup = is_profile_setup
        self.name=name
        self.Gender=Gender
        self.age=age
        self.Lang=Lang
        self.room_city=room_city
        self.room_area=room_area
        self.dist_to_transport=dist_to_transport
        self.food_pref=Food_pref
        self.drinker=drinker
        self.shift=Shift
        self.profile_picture=profile_picture
        self.En_suite_bathroom=En_suite_bathroom
        self.Passions=Passions
        self.have_roof=have_roof



    def insert(self):
        print(self.username)
        print(self.password)
        query = "insert into user_info (username, email, password, is_profile_setup) values (%s, %s, %s, %s)"
        vals = (self.username, self.email, self.password, self.is_profile_Setup)

        return (query, vals)

    def profileSetup(self):
        print(self.username)
        print(self.password)
        self.is_profile_setup = True
        # query = "update user_info set  profile_picture=%s, is_profile_setup=%s where username=%s"
        # vals = ( self.profile_picture, self.is_profile_setup, self.email)
        query = "update user_info set  profile_picture =%s,name =%s, email =%s, Gender =%s, Lang =%s,age =%s,food_pref =%s,drinker =%s,shift =%s,is_profile_setup=%s where username=%s"
        vals = (self.profile_picture,self.name,self.email,self.Gender,self.Lang,self.age,self.food_pref,self.drinker,self.shift,self.is_profile_setup,self.username)
        return (query, vals)
    


    def __str__(self) -> str:
        return self.username+",  "+self.email+", "+str(self.profile_picture) 

