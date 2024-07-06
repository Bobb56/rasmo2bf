import sys, re, random



if len(sys.argv) < 3:
    print("Nombre insuffisant d'arguments")
    sys.exit()


defines = {} # dictionnaire qui contient les noms de "variables" affectés à un nombre


_int = int


def isNumber(nb):
    try:
        nb = _int(nb)
        return True
    except ValueError:
        return False



def int(x):
    if isNumber(x):
        return _int(x)
    else:
        return _int(defines[x])


#définition des fonctions d'action
def binarise(nb):
    nb = bin(nb)[2:]
    ret = '0'* (8-len(nb)) + nb
    if len(ret) != 8:
        print("/!\ ERREUR : Nombre binaire de taille", len(ret))
    return ret




def assemble():
    #assembleur de programme tasm
    f = open(sys.argv[1], 'r')
    txt = f.read()
    f.close()
    
    txt = txt.replace(';', ' ; ')
    
    toks = re.split(' |\t', txt)
    # détection des commentaires
    i = 0
    comm = False
    while i < len(toks):
        
        if len(toks[i])>0 and toks[i][0] == ';':
            comm = True
        
        
        if len(toks[i])>0 and '\n' in toks[i]:
            l = re.split('\n', toks[i])
            toks = toks[:i] + [l[0]]*(not comm) + l[1:] + toks[i+1:] # on prend en compte le mot avant le \n uniquement si on n'était pas en commentaire
            i += len(l) - 2 - (not comm)
            comm = False
        
        
        if comm:
            del toks[i]
        else:
            i+=1
                
    
    toks = [i for i in toks if len(i) > 0]
    
    # réunification des chaines de caractères
    isString = False
    string = ""
    i = 0
    while i < len(toks):
        if not isString and toks[i][0] == '\\' and toks[i][-1] == '\\' :
            toks[i] = toks[i][1:-1]
        
        elif not isString and toks[i][0] == '\\':
            isString = True
        
        elif isString and toks[i][-1] == '\\':
            toks[i] = string[1:] + ' ' + toks[i][:-1] # on enlève les \ au début et a la fin
            string = ""
            isString = False
        
        if isString :
            string += ' '*(string != "") + toks[i]
            del toks[i]
            i -= 1
        
        i += 1
    
        
    INSTRUCTIONS = ['ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'PRINTNUM', 'PRINT', 'SET', 'COP', 'INPUT', 'INPUTNUM', 'PUSH', 'POP', 'LABEL', 'GOTO', 'GT', 'LT', 'GTE', 'LTE', 'EQ', 'NOTEQ', 'AND', 'OR', 'XOR', 'NOT', 'JUMP', 'CALL', 'RETURN', 'INCR', 'DECR', 'RAND', 'SETCHUNK']
    txt2 = ""
    
    i = 0
    while i < len(toks):
        
        toks[i] = toks[i].upper()
        
        if toks[i] == 'DEFINE': # nommage de nombres
            defines.update({toks[i+1] : toks[i+2]})
        
        #définitions de macros
            
        elif toks[i] == 'PRINTSTRING': # code spécial pour la chaine de caractères
            chaine = toks[i+1]
            for char in chaine:
                txt2 += binarise(INSTRUCTIONS.index('SET'))[3:]
                txt2 += binarise(int(toks[i+2])) # premier argument : la case
                txt2 += binarise(ord(char))
                
                txt2 += binarise(INSTRUCTIONS.index('PRINT'))[3:]
                txt2 += binarise(int(toks[i+2]))
                txt2 += '0'*8
            
        elif toks[i] == 'FOR': # macro d'une boucle for
            
            txt2 += binarise(INSTRUCTIONS.index('SET'))[3:]
            txt2 += binarise(int(toks[i+3])) # premier argument
            txt2 += '0'*8 # deuxième argument
            
            txt2 += binarise(INSTRUCTIONS.index('LABEL'))[3:]
            txt2 += binarise(int(toks[i+1])) # premier argument
            txt2 += '0'*8
            
            txt2 += binarise(INSTRUCTIONS.index('SET'))[3:]
            txt2 += binarise(int(toks[i+5])) # premier argument
            txt2 += binarise(int(toks[i+4])) # deuxième argument
            
            txt2 += binarise(INSTRUCTIONS.index('GT'))[3:]
            txt2 += binarise(int(toks[i+5])) # premier argument
            txt2 += binarise(int(toks[i+3])) # deuxième argument
            
            
            txt2 += binarise(INSTRUCTIONS.index('JUMP'))[3:]
            txt2 += binarise(int(toks[i+5])) # premier argument
            txt2 += binarise(int(toks[i+2])) # deuxième argument
            
            i += 3 # cette pseudo-instruction a la taille de deux intructions
        
        elif toks[i] == 'ENDFOR':
            txt2 += binarise(INSTRUCTIONS.index('INCR'))[3:]
            txt2 += binarise(int(toks[i+3])) # premier argument
            txt2 += binarise(int(toks[i+4])) # deuxième argument
            
            txt2 += binarise(INSTRUCTIONS.index('GOTO'))[3:]
            txt2 += binarise(int(toks[i+1])) # premier argument
            txt2 += '0'*8
            
            txt2 += binarise(INSTRUCTIONS.index('LABEL'))[3:]
            txt2 += binarise(int(toks[i+2])) # premier argument
            txt2 += '0'*8
            
            i += 3
        
        elif toks[i] == 'WHILE':
            txt2 += binarise(INSTRUCTIONS.index('LABEL'))[3:]
            txt2 += binarise(int(toks[i+1])) # premier argument
            txt2 += '0'*8
            
            txt2 += binarise(INSTRUCTIONS.index('JUMP'))[3:]
            txt2 += binarise(int(toks[i+3])) # premier argument
            txt2 += binarise(int(toks[i+2])) # deuxième argument
            
            i += 3
        
        elif toks[i] == 'ENDWHILE':
            txt2 += binarise(INSTRUCTIONS.index('GOTO'))[3:]
            txt2 += binarise(int(toks[i+1])) # premier argument
            txt2 += '0'*8
            
            txt2 += binarise(INSTRUCTIONS.index('LABEL'))[3:]
            txt2 += binarise(int(toks[i+2])) # premier argument
            txt2 += '0'*8
        
        
        elif toks[i] == 'FUNCTIONDEF':
            txt2 += binarise(INSTRUCTIONS.index('GOTO'))[3:]
            txt2 += binarise(int(toks[i+2])) # premier argument
            txt2 += '0'*8
            
            txt2 += binarise(INSTRUCTIONS.index('LABEL'))[3:]
            txt2 += binarise(int(toks[i+1])) # premier argument
            txt2 += '0'*8
        
        elif toks[i] == 'FUNCTIONEND':
            txt2 += binarise(INSTRUCTIONS.index('RETURN'))[3:] + '0'*16
            
            txt2 += binarise(INSTRUCTIONS.index('LABEL'))[3:]
            txt2 += binarise(int(toks[i+1])) # premier argument
            txt2 += '0'*8
            
        else:
            txt2 += binarise(INSTRUCTIONS.index(toks[i].upper()))[3:] #commande
            #---------
            if toks[i+1] == '-': # premier argument
                txt2 += '0'*8
            else:
                txt2 += binarise(int(toks[i+1]))
            #---------
            if toks[i+2] == '-': # deuxième argument
                txt2 += '0'*8
            else:
                txt2 += binarise(int(toks[i+2]))
        
        i += 3

    
    return txt2



string = assemble()


int = _int

nbinst = int(len(string)/21)


# decompose le programme en séquence d'instructions
l = []
for i in range(nbinst):
    l.append(string[21*i:21*(i+1)])


def decomp(s): # prend en argument une chaine de 21 bits de long et le découpe en une liste de 3 nombres
    op = int(s[:5],2)+1 # le zéro est réservé à l'instruction qui fait rien
    arg1 = int(s[5:13],2)
    arg2 = int(s[13:21],2)
    return (op, arg1, arg2)


# décompose chaque chaine d'instructions en nombres intelligibles
for j in range(nbinst):
    l[j] = decomp(l[j])

l += [(41, 0, 0)] # dernière instruction indiquant la fin du programme, 41 prcq C marrant (:
nbinst += 1



# on rajoute des chunks vides derrière les JUMP pour permettre la transformation des numéros de label en numéro d'instructions dans le programme
i = 0
while i < len(l) :
    if l[i][0] == 26 : # le JUMP
        l.insert(i+1, (0, 0, 0))
        nbinst += 1
        i += 1
    
    i += 1



# Il faut calculer le nombre de gros chunks

nbgroschunks = nbinst//256 + 1


minichunk = lambda tuple: [tuple[0], tuple[1], tuple[2], 0, 0, 0]

memoire = []

# crée la mémoire associée au programme mais sans les adresses, sans la bonne taille (nombre entier de gros chunks) et sans les blocs à la droite de chaque gros chunk
for l2 in l:
    memoire += minichunk(l2)

# comble la mémoire à gauche avec de zéros
memoire = [0] * (nbgroschunks*256*6 - len(memoire)) + memoire


# on numérote les adresses maintenant
i = 3
ad = 255
while i < len(memoire):
    memoire[i] = ad
    i += 6
    
    if ad == 0:
        ad = 256
    
    ad -= 1

# on va rajouter les blocs à droite des gros chunks
memoire2 = []

i = 0
chunkad = nbgroschunks - 1

while i < len(memoire):
    if (i+1)%(256*6) == 0:
        memoire2.append(memoire[i])
        memoire2 += [0, 0, 0, 0, 0, chunkad]
        chunkad -= 1
    else:
        memoire2.append(memoire[i])
        
    i += 1



# maintenant on va modifier les arguments des labels et des goto pour qu'ils pointent directement vers les instructions où aller
labels = {} # dico qui contient des couples ((a,b), (c,d)) avec (a,b) le nom de label TASM et (c,d) l'adresse au sein du gros chunk le numéro de gros chunk

# parcourt une première fois le programme pour scanner tous les labels
i = 0
chunkno = nbgroschunks - 1

while i < len(memoire2): # i est toujours sur l'OP
    if memoire2[i] == 14: #label
        labels[(memoire2[i+1],memoire2[i+2])] = (memoire2[i+3],chunkno)
    
    if memoire2[i+3] == 0:
        chunkno -= 1
        i += 6
    
    i+=6





# parcourt une deuxième fois le programme pour remplacer les goto, jump, call par les nouveaux arguments
for i in range(0,len(memoire2), 6): # on a toujours la tête sur les OP
    if memoire2[i] == 14: # label
        memoire2[i], memoire2[i+1], memoire2[i+2] = 0,0,0 # pas d'arguments pour que ce soit plus rapide
    
    if memoire2[i] == 15: # goto
        memoire2[i+1], memoire2[i+2] = labels[(memoire2[i+1], memoire2[i+2])]
        
    if memoire2[i] == 27: # call
        memoire2[i+1], memoire2[i+2] = labels[(memoire2[i+1], memoire2[i+2])]
    
    if memoire2[i] == 26: # jump
        memoire2[i+7], memoire2[i+8] = labels[(memoire2[i+2], 0)] # ce label existe, ou alors le programme n'est pas correct, auquel cas : on s'en fout
        memoire2[i+2] = 0 # le chunk de base du jump ne contient plus l'adresse à aller, mais c'est maintenant le chunk d'après
    
    if memoire2[i] == 32 : #setchunk
        memoire2[i] = 14 # l'opcode du setchunk est devenu celui du label car le label est transformé en zéro (il sert à rien)



# on écrit dans le dernier chunk les arguments prêts pour retourner au tout début du programme
memoire2[len(memoire2)-2] = nbgroschunks-1
memoire2[len(memoire2)-3] = 255



# il faut maintenant générer le programme brainfuck qui va écrire ça dans la mémoire
prog = ""
for x in memoire2:
    prog += '+' * x + '>'



f = open(sys.argv[2], "w+")

count = 0 # pour mettre des retours à la ligne
i = 0
for i in prog:
    f.write(i)
    count += 1
    if count == 133:
        count = 0
        f.write('\n')


main = open("C:\\Program Files\\rasmo2bf\\main.bf", "r")
f.write(main.read())
main.close()


f.close()