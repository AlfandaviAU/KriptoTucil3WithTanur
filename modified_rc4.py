# TBA : Modifikasi RC4

def mod_rc4(srctext : "byte", key : str, encrypt : bool = True) -> "byte":
    # KSA
    listS = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + listS[i] + ord(key[i % len(key)])) % 256
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
