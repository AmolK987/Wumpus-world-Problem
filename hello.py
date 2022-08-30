def main(x, y):
    print("Hello world")
    end = False
    curr_x = 0
    curr_y = 0
    visited_list = []
    list = []
    numbers_list = []
    for i in range(0,y):
        for j in range(0,x):
            list.append(0)
        visited_list.append(list)

    for i in range(0,y):
        for j in range(0,x):
            list.append(0)
        numbers_list.append(list)
    

    found_gold = False
    places = []
    places_reverse = []
    while found_gold == False:
        step(curr_x, curr_x, visited_list, numbers_list, found_gold, places)
    for i in range(len(places)-1, -1, -1):
        if  i-1 > 0:
            if places[i] == "n" and places[i-1] == "s":
                i-=1
            elif places[i] == "s" and places[i-1] == "n":
                i-=1
            elif places[i] == "e" and places[i-1] == "w":
                i-=1
            elif places[i] == "w" and places[i-1] == "e":
                i-=1
        elif places[i] == "n":
            places_reverse.append("s")
        elif places[i] == "s":
            places_reverse.append("n")
        elif places[i] == "w":
            places_reverse.append("e")
        elif places[i] == "e":
            places.append("w")
    
    
    for i in places_reverse:
        print(i)


def step(curr_x, curr_y, visited_list, numbers_list, found_gold, places):
    if visited_list[curr_x][curr_y] == 0:
        i = int(input("input:"))
        numbers_list[curr_x][curr_y] = i
        visited_list[curr_x][curr_y] = 1
    else:
        i = numbers_list[curr_x][curr_y]
    breeze = False
    stentch = False
    glitter = False
    gold = False
    if (i - 8) >= 0:
        gold = True
        found_gold = True
        i -= 8
    
    if (i-4) >= 0:
        glitter = True
        i -= 4

    if (i - 2) >= 0:
        stentch = True
        i -= 2
    
    if (i - 1) >= 0:
        breeze = True
        i -= 1
    
    if i != 0:
        print("code failed")
        return

    if i == 0:
        if (curr_x + 1) < len(visited_list) and visited_list[curr_x+1][curr_y] == 0:
            print("n")
            places.append("n")
            curr_x += 1
            return
        elif (curr_y + 1) < len(visited_list[curr_x]) and visited_list[curr_x][curr_y+1] == 0:
            print("e")
            places.append("e")
            curr_y += 1
            return
        elif (curr_x-1) >= 0 and visited_list[curr_x-1][curr_y] == 0:
            print("s")
            places.append("s")
            curr_x -= 1
            return
        elif (curr_y -1) >= 0 and visited_list[curr_x][curr_y-1] == 0:
            print("w")
            places.append("w")
            curr_y -= 1
            return
        else:
            a = places.pop()
        
    
        


main(4, 4)