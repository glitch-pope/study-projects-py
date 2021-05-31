fourths = [4, 44, 444, 4444, 44444]
fourfive = []
fourfive = fourths

rank = len(str(max(fourths)))
while rank > 0:
    for number in sorted(fourths, reverse=True):
        if len(str(number)) >= rank:
            fourfive.append(number + 10 ** (rank - 1))
    rank -= 1
    
for number in sorted(fourfive):
    print(number)
    