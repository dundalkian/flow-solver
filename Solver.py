import itertools

my_list = [1,2,3,4]
for pair in itertools.combinations(my_list, 2):
    print(pair)