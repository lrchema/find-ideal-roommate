from math import sqrt
from __init__ import dbconn

def distance(sc, u2):
    total = 0
    if sc[0] != u2[0]: # gender
        total += 1
    total += ((sc[1]-u2[1])/u2[1])**2 # age
    if sc[2] != u2[2]: # city
        total += 1
    if sc[3] != u2[3]: # area
        total += 1
    if sc[4] != u2[4]: # lang
        total += 1
    if sc[5] != u2[5]: # food_pref
        total += 1
    if sc[6] != u2[6]: # shift
        total += 1
    if sc[7] != u2[7]: # drinker
        total += 1
    if sc[8] != u2[8]: # passions
        total += 1
    
    return sqrt(total)
    
def get_top_k(sc, k=3):
    conn = dbconn()
    conn.reconnect()
    cur = conn.cursor()
    cur.execute("select gender, age, room_city, room_area, lang, food_pref, shift, drinker, passions, userid from user_info where have_roof=1 and room_area=%s and gender=%s",(sc[3], sc[0]))
    usersList = list(cur.fetchall())
    print(len(usersList))
    conn.close()
    print(usersList[0])
    print(distance(sc, usersList[0]))

    def distance_wrapper(u):
        # print(distance(sc, u), sc, u)
        return distance(sc, u)

    usersList.sort(key=distance_wrapper)
    res = []
    for i in range(k):
        res.append(usersList[i][-1])    
        
    return res

