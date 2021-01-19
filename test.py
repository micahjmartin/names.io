from names import Names


n = Names("names.db")

with open("test.txt") as fil:

    for i in n.get_names(fil.read()):
        print(i)