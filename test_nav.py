# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 16:59:03 2021

@author: 987am
"""

from test_world import *

def show(L):
    'Prints out input 2D list'
    for i in range(len(L)):
        for j in range(len(L[0])):
            if (i,j) != (bd.boty,bd.botx): 
                print(L[i][j]+'\t',end='')
            else: print("B"+'\t',end = '')
        print()
    print()

def kill_wump(d,kn):
    bd.kill_wump(d, kn)

def move(d):
    'Moves bot in direction'
    bd.move(d)
    knowns[bd.boty][bd.botx] = '0'
    return bd.boty,bd.botx,d

def free_move(x,y,L):
    '''
    The bot either knows it is completely safe or knows the locations of
    all nearby dangers and can move freely
    '''
    d = ''
    if y-1 >=0 and (not L[y-1][x].isalpha() or L[y-1][x]=='G'):
        d = 'n'
    elif x+1 < len(L[0]) and not (L[y][x+1].isalpha() or L[y][x+1]=='G'):
        d = 'e'
    elif y+1 <len(L) and not (L[y+1][x].isalpha() or L[y+1][x]=='G'):
        d = 's'
    elif x-1 >= 0 and not (L[y][x-1].isalpha() or L[y][x-1]=='G'):
        d = 'w'
    move(d)
    show(L)
    return d

def look(unk,kn,x,y,d,check):
        '''
        This function translates the query result into changes in the 
        spaces surrounding the bot in the unknowns list
        '''
        back = False
        q = bd.query()
        nbrval = []
        dirs = []
        for i in get_nbrs(x, y, kn, False):
            nbrval.append(kn[i[1]][i[2]])
            dirs.append(i[0])
        if bd.board[y][x].visited and inv(d) in dirs and nbrval[dirs.index(inv(d))] =='0'and q==0:
            q = 0
            back = True
        t = q
        zlist = []
        hole = False
        glitter = False
        wump = False
        gold = False
        cg = 0
        cw = 0
        ch = 0
    
        
        if q-8>=0:
            q-=8
            knowns[y][x] = "G"
            gold = True
        if q-4>=0:
            q-=4
            glitter = True
            cg = surr(unk,kn,glitter,wump,hole,x,y)
        
        if q-2>=0 and 'W' not in nbrval:
            q-=2
            if 'W' not in nbrval: wump = True
            cw = surr(unk,kn,glitter,wump,hole,x,y)
        elif 'W' in nbrval:
            kill_wump(dirs[nbrval.index('W')], kn)
           
        if q-1==0 and 'H' not in nbrval:
            q-=1
            hole = True
            ch = surr(unk,kn,glitter,wump,hole,x,y)
            
        if t == 0 and not knowns[y][x] == '0':
            knowns[y][x] == '0'
            for i in get_nbrs(x, y, kn,True):
                if kn[i[1]][i[2]] == '-':
                    zlist.append(i)
        elif t == 0 and not back and not check: 
            d = free_move(x,y,kn)
        elif t>0: check = True
                    
        return [{'G':gold,'g':glitter,'w':wump,'h':hole},zlist,{'g':cg,'w':cw,'h':ch},check,d]

def get_nbrs(x,y,L,dash): #list of tuples in form (dir,y,x)
    '''
    Returns a list of tuples containing the direction,y,x of each existing
    neighbor of a point. Boolean value dash allows this function to return
    unexplored points if desired.
    '''
    out = []
    if not dash:
        loc = max(0,x-1) #west
        if loc != x and L[y][loc] != '-':
            out.append(('w',y,loc))
        loc = min(len(L[0])-1,x+1) # east
        if loc != x and L[y][loc] != '-':
            out.append(('e',y,loc))
        loc = max(0,y-1) # north
        if loc != y and L[loc][x] != '-':
            out.append(('n',loc,x))
        loc = min(len(L)-1,y+1) # south
        if loc != y and L[loc][x] != '-':
            out.append(('s',loc,x))
    else: #want to include dashes
        loc = max(0,x-1) #west
        if loc != x:
            out.append(('w',y,loc))
        loc = min(len(L[0])-1,x+1) # east
        if loc != x:
            out.append(('e',y,loc))
        loc = max(0,y-1) # north
        if loc != y:
            out.append(('n',loc,x))
        loc = min(len(L)-1,y+1) # south
        if loc != y:
            out.append(('s',loc,x))
    
    return out
    
def inv(d):
    'Just inverts input direction'
    if d == 'n':
        return 's'
    if d == 's':
        return 'n'
    if d == 'e':
        return 'w'
    if d == 'w':
        return 'e'

def surr(unk,kn,g,w,h,x,y):
    '''
    This function updates the unknowns list according to the query output
    with either 'h','w',or 'g' to represent the possibility of a hole,
    wumpus, or gold respectively. This function can also reset all
    neighboring spaces to a '-' if the query return a zero.
    '''
    over = False
    go = True
    rep = ''
    if g: rep += 'g'
    if w: rep += 'w'
    if h: rep += 'h'
    if not g and not w and not h: 
        rep += '-'
        over = True
    count = 0
    for i in get_nbrs(x, y, kn, False):
        if kn[i[1]][i[2]].lower() in rep:
            go = False
    if go:
        loc = max(0,x-1) #left
        if loc != x and kn[y][loc] == '-':
            if unk[y][loc] == '-'or over:
                unk[y][loc] = rep
                count +=1
            else: unk[y][loc] += rep
        loc = min(len(unk[0])-1,x+1) # right
        if loc != x and kn[y][loc] == '-':
            if unk[y][loc] == '-'or over:
                unk[y][loc] = rep
                count +=1
            else: unk[y][loc] += rep
        loc = max(0,y-1) # up
        if loc != y and kn[loc][x] == '-':
            if unk[loc][x] == '-'or over:
                unk[loc][x] = rep
                count +=1
            else: unk[loc][x] += rep
        loc = min(len(unk)-1,y+1) # down
        if loc != y and kn[loc][x] == '-':
            if unk[loc][x] == '-'or over:
                unk[loc][x] = rep
                count +=1
            else: unk[loc][x] += rep
    
    return count

def check(typ,d,unk,kn,x,y):
    '''
    This function is to determine how the bot should move and query the 
    board in order to pinpoint the location of a danger. The bot first
    moves back to safety and then moves into an unexplored space if there
    is one nearby. Next the bot will move until it finds itself next to 
    a previously determined possible location of a danger. The bot then
    will query the board from this new location and update the unknowns
    list accordingly. Finally, this function calls the confirm function
    to pinpoint the location of the danger.
    '''
    
    un_nbrs = get_nbrs(x, y, unk,False)
    bkd = inv(d)
    y,x,bkd=move(bkd)
    
    nbrs = get_nbrs(x, y, kn,True)
    
    for n in nbrs:
        if kn[n[1]][n[2]]=='-' and not unk[n[1]][n[2]].isalpha():
              y,x,d=move(n[0])
              break
    
    T = look(unk,kn, x, y,d,True)      
    #if checking:
    #T = look(unk,kn, x, y,bkd,True)
    if T[2][typ] == 0: surr(unk, kn,T[0]['g'],T[0]['w'],T[0]['h'], x, y)
    knpts = []
    for pt in get_nbrs(x, y, kn, False):
        knpts.append(kn[pt[1]][pt[2]])
    if typ.upper not in knpts: confirm(unk,kn,typ)
    return d

def confirm(unk,kn,typ):
    '''
    After changing the unknowns list according to a signal and moving to
    another location and updating the unknowns list again, this function
    takes the unknowns list and derives the location of the type and
    updates the knowns list accordingly
    '''
    count = 0
    cx = -1
    cy = -1
    tx = cx
    ty = cy
    for y in range(len(unk)):
        for x in range(len(unk[0])):
            if typ in unk[y][x]:
                count +=1
                tx = x
                ty = y
            if unk[y][x].count(typ) > 1:
                cx = x
                cy = y
    if count == 1:
        cx = tx
        cy = ty
    
    if cx>-1: kn[cy][cx] = typ.upper()
    
            
def clear(L,typ):
    '''
    Clear the input list of all occurrences of an input string (typ) by
    either removing typ from the existing string or replacing it with a
    "-"
    '''
    for i in range(len(L)):
        for j in range(len(L[i])):
            if typ in L[i][j]: L[i][j] = L[i][j].replace(typ,"")
            if len(L[i][j])<1: L[i][j] = '-'

def free_move2(x,y,kn,d):
    '''
    Recursive implementation of free_move function desgined to move the
    bot until it either detects a danger or lands on gold
    '''
    if not bd.board[y][x].visited and bd.query()>0 and bd.query()!=8:
        return d
    else:
        d = [free_move(x,y,kn)]
        x = bd.botx
        y = bd.boty
        return free_move2(x,y,kn,d)

def goback(L):
    '''
    Moves the bot back to the bottom left(southwest) corner after finding
    the gold
    '''
    t=''
    while bd.boty != len(bd.board) and bd.botx !=0 and t!='no':
        if bd.boty+1<len(bd.board) and bd.board[bd.boty+1][bd.botx].visited:
            move('s')
        elif bd.botx-1>-1 and bd.board[bd.boty][bd.botx-1].visited:
            move('w')
        elif bd.boty-1>-1 and bd.board[bd.boty-1][bd.botx].visited:
            move('n')
        elif bd.botx+1<len(bd.board[0]) and bd.board[bd.boty][bd.botx+1].visited:
            move('e')
        show(L)
        t = input('continue?')

if __name__ == '__main__':
    bd = Board()
    knowns = [] 
    unknowns = []
    for i in range(len(bd.board)):
        knowns.append(['-']*len(bd.board[0]))
        unknowns.append(['-']*len(bd.board[0]))
    
    bd.show()
    d = 'n'
    r = ''
    killed = False
    gold = False
    while not gold and r != 'no':
    
        knowns[bd.boty][bd.botx] = '0'
        #show(knowns)
        props,z,v,chk,d = look(unknowns,knowns,bd.botx,bd.boty,d,False)
        if chk:
            while props['h']: 
                check('h',d,unknowns,knowns,bd.botx,bd.boty)
                free_move2(bd.botx, bd.boty, knowns,[d])
                clear(unknowns,'h')
                props,z,v,chk,d = look(unknowns,knowns,bd.botx,bd.boty,d,True)
                show(knowns)
                show(unknowns)
            if props['w']: 
                d = check('w',d,unknowns,knowns,bd.botx,bd.boty)
                free_move2(bd.botx, bd.boty, knowns,[d])
                clear(unknowns,'w')
                clear(unknowns,'h')
                props,z,v,chk,d = look(unknowns,knowns,bd.botx,bd.boty,d,True)
                show(knowns)
                show(unknowns)
            v = [d]
            if props['h']:
                d = check('h',d,unknowns,knowns,bd.botx,bd.boty)
                [d]=[free_move2(bd.botx, bd.boty, knowns,v)]
                clear(unknowns,'h')
                props,z,v,chk,d = look(unknowns,knowns,bd.botx,bd.boty,d[0],True)
                show(knowns)
                show(unknowns)
            if props['g']: 
                check('g',d,unknowns,knowns,bd.botx,bd.boty)
                #free_move2(bd.botx, bd.boty, knowns,[d])
                while bd.query()-8<0:
                    free_move(bd.botx,bd.boty,knowns)
                clear(unknowns,'g')
                clear(unknowns,'h')
                props,z,v,chk,d = look(unknowns,knowns,bd.botx,bd.boty,d,True)
                show(knowns)
                show(unknowns)
        #clear(unknowns,'h')
        
        clear(unknowns,'h')
        show(knowns)
        show(unknowns)
        gold = props['G']
        r = input("continue?")
    
    clear(knowns,'G')
    knowns[bd.boty][bd.botx] = '0'
    goback(knowns)
    if (bd.boty,bd.botx) == (len(bd.board)-1,0): print("Success!")
    
    
