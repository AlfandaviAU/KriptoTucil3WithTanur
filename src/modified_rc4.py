# TBA : Modifikasi RC4

def mod_rc4(srctext : str, key : str) -> str:
    # KSA
    listS = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + listS[i] + ord(key[i % len(key)])) % 256
        listS[i], listS[j] = listS[j], listS[i]

    # KSA EDIT 1
    scrambleMore = [i for i in range(len(key))]
    for i in range(256):
        j = ((j+listS[i]) ^ (ord(key[i % len(key)])+scrambleMore[i % len(key)])) % 256
        listS[i], listS[j] = listS[j], listS[i]

    # KSA EDIT 2
    lhoKokLagi = [i for i in range(len(key)+10)]
    for i in range(256):
        j = ((j+listS[i]) ^ (ord(key[i % len(key)])+lhoKokLagi[i % len(key)+10])) % 256
        if (j%2 == 0 and listS[i]%2 == 0):
            j = (int((j+listS[i])/2 + 50)) % 256
        else:
            j = (int((j+listS[i])//2 + 25)) % 256
        listS[i], listS[j] = listS[j], listS[i]

    # KSA EDIT 3
    indexToSwap = 0
    for i in range(256):
        if (i%3 == 0):
            indexToSwap = int(i/3) % 256
        elif (i%3 == 1):
            indexToSwap = (256 - int((i*578 + 274)//37)) % 256
        elif (i%3 == 2):
            indexToSwap = (351 - int((i*836 + 487)//47)) % 256
        j = (j + listS[indexToSwap] + ord(key[indexToSwap % len(key)])) % 256
        listS[i], listS[j] = listS[j], listS[i]
    
    # KSA EDIT 4
    for i in range(256):
        if (i%4 == 0):
            indexToSwap = int(i/4) % 256
        elif (i%4 == 1):
            indexToSwap = (256 - int((i*578 + 274)//37)) % 256
        elif (i%4 == 2):
            indexToSwap = (351 - int((i*836 + 487)//47)) % 256
        elif (i%4 == 3):
            indexToSwap = (783 - int((i*1374 + 7382)//47)) % 256
        indexToSwap = (indexToSwap ^ listS[indexToSwap]) % 256
        j = (j + listS[indexToSwap] + ord(key[indexToSwap % len(key)])) % 256
        listS[i], listS[j] = listS[j], listS[i]


    # PRGA
    i = 0
    j = 0
    resulttext = ""
    for k in range(len(srctext)):
        i = (i + 1) % 256
        j = (j + listS[i]) % 256
        listS[i], listS[j] = listS[j], listS[i]
        t = (listS[i] + listS[j]) % 256
        u = listS[t]
        resulttext += chr(u ^ ord(srctext[k]))

    return resulttext


# a = input("pteks\n")
# b = input("key\n")
# c = mod_rc4(a,b)
# print(c)
# d = mod_rc4(c,b)
# print(d)