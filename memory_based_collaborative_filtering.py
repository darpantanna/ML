import pandas as pd
import math
import json

uR = 'user_ratings.json'
d = 'dishes.csv'

with open(uR) as f:
    user_data = json.load(f)

for u in user_data:
    user_data[u].sort(key=lambda x: x[0])

dId = str(int(input("Enter dish ID: ")))
uId = str(int(input("Enter user ID: ")))

dishes = user_data[uId]
has = 1


def vSpace(v1, v2):
    k = 0
    l = 0
    num = 0.0
    den1 = 0
    den2 = 0

    while k < len(v1) and l < len(v2):
        curr1 = v1[k]
        id1 = curr1[0]
        curr2 = v2[l]
        id2 = curr2[0]
        if id1 == id2:
            r1 = curr1[1]
            r2 = curr2[1]
            num += r1 * r2
            den1 += r1 * r1
            den2 += r2 * r2
            k += 1
            l += 1
        elif id1 > id2:
            l += 1
        else:
            k += 1

    if num == 0:
        return 0
    else:
        return num / (math.sqrt(den1) * math.sqrt(den2))


def estimate(uD, dD, u_data):
    currAvg = avg(u_data[uD])
    num = 0.0
    den = 0.0

    for l in u_data:
        isRelevant = False
        rating = 0.0
        for k in range(len(u_data[l])):
            if int(u_data[l][k][0]) == int(dD):
                isRelevant = True
                rating = u_data[l][k][1]
                break

        if l == uD or not isRelevant:
            continue

        weight = vSpace(u_data[uD], u_data[l])
        num += weight * (rating - avg(u_data[l]))
        den += abs(weight)

    if den == 0:
        return currAvg
    else:
        return currAvg + (num / den)


def avg(v1):
    s = 0.0
    count = 0.0
    for k in range(len(v1)):
        s += v1[k][1]
        count = count + 1
    s = s/count
    return s


for i in range(len(dishes)):
    if int(dishes[i][0]) == int(dId):
        has = 0
        print "Rating: " + str(dishes[i][1]) + " (existing)"
        break


if has == 1:
    score = estimate(uId, dId, user_data)
    print "Rating: " + str(score) + " (estimated)"


u2 = str(int(input("\nEnter user ID: ")))
ing = int(input("Enter number of ingredients: "))
ingredients = []
for i in range(ing):
    curr = raw_input("Enter I" + str(i + 1) + ": ")
    ingredients.append(curr.lower())

ingredients.sort()

dishesData = pd.read_csv(d, sep=',', quotechar='\"', header=0)
dish_data = dishesData.values
column = list(dishesData.columns.values)

# print column
m = {}
c = 0
for i in column:
    m.update({i: c})
    c = c + 1

check = False
# print dish_data

# Print sorted map
# for key, value in sorted(m.iteritems(), key=lambda (k, v): (v, k)):
#   print "%s: %s" % (key, value)

dishesWithIngredients = []
hasRated = []

for i in range(len(dish_data)):
        check = False
        for j in range(len(ingredients)):
            if dish_data[i][m[ingredients[j]]] == 1:
                check = True
            elif dish_data[i][m[ingredients[j]]] == 0:
                check = False
                break

        if check:
            dishesWithIngredients.append(dish_data[i][1])
            hasRated.append(dish_data[i][0])


# print dishesWithIngredients

d2 = user_data[u2]
removedDishes = []
rId = []
finalRating = 0.0
# print d2
co = 0
m = 0.0
flag = 0
if not hasRated:
    print "\nNo dish with specified ingredients"
else:
    for i in range(len(d2)):
        if int(d2[i][0]) in hasRated:
            hasRated.remove(d2[i][0])
            removedDishes.append(dishesWithIngredients[co])
            rId.append(dish_data[i][0])
            dishesWithIngredients.remove(dishesWithIngredients[co])
            co = co+1

    if not hasRated:
        print "\nNo new dish with specified ingredients"
        print "Your best-rated dish:"
        for j in range(len(d2)):
            if int(d2[i][0]) in removedDishes:
                finalRating = d2[i][1]
                if m < finalRating:
                    m = finalRating
                    flag = j
        print removedDishes[flag]

    else:
        # print d2
        # print hasRated
        m = 0.0
        fl = 0
        ca = 0
        for p in hasRated:
            r = estimate(u2, p, user_data)
            if m < r:
                m = r
                fl = ca
            ca += 1

        print "\nSuggested dish:"
        print dishesWithIngredients[fl]
