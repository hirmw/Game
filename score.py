
#
file = '/Users/richardwoodhouse/Desktop/PyGame/scores.txt'

def getScore():
    input_file = '/Users/richardwoodhouse/Desktop/PyGame/scores.txt'

    names = []
    namesX = []

    file = open(input_file)

    for scores in file:
        names.append(scores)

    newlist = [x.replace(',', '') for x in names]

    for y in newlist:
        z = y.split()
        namesX.append(z)

    newlist1 = [i for i in namesX]
    #newlist2 = [i for i in namesX]
#    newlist3 = zip(newlist2, newlist1)


 #or...
 #newlist3.append((newlist1, newlist2))
 #newlist.sort(reverse=True)
 #end or....

    #def sort(item):
    #    return item[1]

#    n = sorted(newlist3, key=sort, reverse=True)
    return newlist1
    print(n)

def writescore(score):

    print(score)

    out = open(file, 'a')
    out.write(str(score) + ',' + ' ')
    out.close()

#    file.write(“To add more lines.”)#    file.close()
