alphabet = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя1234567890!@#$%^&*() "

def encode(text, password = 66):
    new_password = None
    i = 0
    lenpass = len(text)
    while True:
        while True:
            if password > 10000 / len(alphabet) - 10000 % len(alphabet):
                password = password - 10000 / len(alphabet) - 10000 % len(alphabet)
            else:
                break
        passpassword = str((alphabet.index(text[i]) + 1) * password)
        while True:
            if len(str(passpassword)) < 4:
               passpassword = str(0) + str(passpassword)
            else:
                if new_password == None:
                    new_password = passpassword
                else:
                    new_password = str(new_password) + passpassword
                break
        if lenpass * 4 == len(new_password):
            return str(new_password + "0000")
        if new_password == None:
            new_password = str((alphabet.index(text[0]) + 1) * password)
            i = 1
            continue
        i = i + 1


def decode(text,password = 66):
    text = str(text)
    answer = None
    while True:
        decoding = text[:4]
        text = text[4:]
        if decoding == "0000":
            return answer
        while True:
            if decoding[0] == "0":
                decoding = decoding[1:]
            else:
                decoding = int(decoding) / password
                break
        decoding = int(decoding)
        if answer == None:
            answer = str(alphabet[decoding-1])
        else:
            answer = str(answer) + str(alphabet[decoding-1])