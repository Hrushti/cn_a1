# functions for encrypting and decrypting files
import os

# plain text -> simply returns without encrypting or decrypting the file's content
def plain_text_encode(file):
    return
def plain_text_decode(file):
    return

# transpose (reverse)
def transpose_encode_decode(file):
    curr_file = file.split('.')
    f1 = open(curr_file[0] + '1.' + curr_file[1], 'w')
    f2 = open(file, 'r')

    for each_line in f2:
        each_word = each_line.split()
        for i in range(len(each_word)):
            word = each_word[i]
            f1.write(word[::-1])
            if (i != len(each_word) - 1):
                f1.write(' ')
        f1.write('\n')

    f1.truncate()
    f1.close()
    f2.close()
    try:
        os.remove('./' + file)
    except:
        os.remove(file)
    # alice removed, alice1 exists

    # open alice1
    f1 = open(curr_file[0] + '1.' + curr_file[1], 'r')
    # open alice
    f2 = open(file, 'w')

    for each_line in f1:
        each_word = each_line.split()
        for i in range(len(each_word)):
            word = each_word[i]
            f2.write(word)
            if (i != len(each_word) - 1):
                f2.write(' ')
        f2.write('\n')

    f2.truncate()
    f2.close()
    f1.close()
    try:
        os.remove('./' + curr_file[0] + '1.' + curr_file[1])
    except:
        os.remove(curr_file[0] + '1.' + curr_file[1])

    # try:
    #     os.replace('./' + curr_file[0] + '1.' + curr_file[1], './' + file)
    # except:
    #     os.replace(curr_file[0] + '1.' + curr_file[1], file)
    #     print('---replaced')


# Substitue (Caesar cypher)
def substitute_encode(file):
    curr_file = file.split('.')
    # f1 is alice1
    f1 = open(curr_file[0] + '1.' + curr_file[1], 'w')
    # f2 is alice
    f2 = open(file, 'r')

    f3 = f2.read(1)
    while f3:
        f1.write(chr((ord(f3) + 2) % 256))
        f3 = f2.read(1)

    f1.close()
    f2.close()

    # remove alice
    try:
        os.remove('./' + file)
    except:
        os.remove(file)
    
    # replace alice1 with alice
    # open alice1
    f1 = open(curr_file[0] + '1.' + curr_file[1], 'r')
    # open alice
    f2 = open(file, 'w')

    for each_line in f1:
        each_word = each_line.split()
        for i in range(len(each_word)):
            word = each_word[i]
            f2.write(word)
            if (i != len(each_word) - 1):
                f2.write(' ')
        f2.write('\n')

    f2.truncate()
    f2.close()
    f1.close()
    try:
        os.remove('./' + curr_file[0] + '1.' + curr_file[1])
    except:
        os.remove(curr_file[0] + '1.' + curr_file[1])

def substitute_decode(file):
    curr_file = file.split('.')
    # f1 is alice1
    f1 = open(curr_file[0] + '1.' + curr_file[1], 'w')
    # f2 is alice
    f2 = open(file, 'r')

    f3 = f2.read(1)
    while f3:
        f1.write(chr((ord(f3) - 2) % 256))
        f3 = f2.read(1)

    f1.close()
    f2.close()

    # remove alice
    try:
        os.remove('./' + file)
    except:
        os.remove(file)
    
    # replace alice1 with alice
    # open alice1
    f1 = open(curr_file[0] + '1.' + curr_file[1], 'r')
    # open alice
    f2 = open(file, 'w')

    for each_line in f1:
        each_word = each_line.split()
        for i in range(len(each_word)):
            word = each_word[i]
            f2.write(word)
            if (i != len(each_word) - 1):
                f2.write(' ')
        f2.write('\n')

    f2.truncate()
    f2.close()
    f1.close()
    try:
        os.remove('./' + curr_file[0] + '1.' + curr_file[1])
    except:
        os.remove(curr_file[0] + '1.' + curr_file[1])
