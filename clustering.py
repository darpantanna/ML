import sys
import os
import random
import math
import pandas as pd
# import time
from sklearn import preprocessing


# start = time.time()

# Calculate Euclidean Distance
def eDistance(cluster, centroid):
    dist = 0
    for i in range(0, len(cluster)):
        dist += (cluster[i] - centroid[i]) ** 2
    return math.sqrt(dist)


# Calculate SSE
def SSE(cluster, centroid):
    err = 0.0
    for i in range(0, len(cluster)):
        for j in range(0, len(cluster[i])):
            err += eDistance(cluster[i][j], centroid[i]) ** 2

    return err


def clusterDistance(cluster1, cluster2):
    distance = 0
    for i in range(0, len(cluster1)):
        for j in range(0, len(cluster2)):
            distance += eDistance(cluster1[i], cluster2[j])

    return distance / (len(cluster1) * len(cluster2))


# compute centroids
def calculateCentroid(cluster):
    latitude = 0.0
    longitude = 0.0
    reviewCount = 0.0
    checkins = 0.0

    for i in range(0, len(cluster)):
        latitude += cluster[i][0]
        longitude += cluster[i][1]
        reviewCount += cluster[i][2]
        checkins += cluster[i][3]

    latitude = latitude / len(cluster)
    longitude = longitude / len(cluster)
    reviewCount = (reviewCount / len(cluster))
    checkins = (checkins / len(cluster))

    return [latitude, longitude, reviewCount, checkins]


def agglo(X, K):
    numClusters = len(X)
    clusters = [[] for y in range(len(X))]
    for i in range(0, len(X)):
        clusters[i].append(X[i])

    distanceArray = [[float("inf") for x in range(numClusters)] for y in range(numClusters)]
    for i in range(0, len(distanceArray) - 1):
        for j in range(i + 1, numClusters):
            distanceArray[i][j] = clusterDistance(clusters[i], clusters[j])

    while 1:
        if numClusters == K:
            break
        # Find smallest distance
        minDistance = float("inf")
        minPair = [-1, -1]
        for i in range(0, len(distanceArray) - 1):
            for j in range(i + 1, len(clusters)):
                distance = distanceArray[i][j]
                if distance < minDistance:
                    minDistance = distance
                    minPair[0] = i
                    minPair[1] = j
        # Merge the smallest distance

        clusters[minPair[0]] = clusters[minPair[0]] + clusters[minPair[1]]
        clusters.pop(minPair[1])
        distanceArray.pop(minPair[1])
        for i in range(0, len(distanceArray)):
            distanceArray[i].pop(minPair[1])
        numClusters = numClusters - 1

        for j in range(minPair[0] + 1, numClusters):
            distanceArray[minPair[0]][j] = clusterDistance(clusters[minPair[0]], clusters[j])
        # Recalculate Distance array with new cluster
        for i in range(0, minPair[0]):
            distanceArray[i][minPair[0]] = clusterDistance(clusters[minPair[0]], clusters[i])


    clusterCentroids = []
    for i in range(0, K):
        clusterCentroids.append(calculateCentroid(clusters[i]))
    err = SSE(clusters, clusterCentroids)

    print("WC-SSE=%0.2f") % (err)
    for i in range(0, K):
        print ("Centroid%d=%s") % (i + 1, clusterCentroids[i])


# km computing
def kmeans(Data, k):
    clusterCentroids = []  # clusterCentroids[i] is the cluster centroid of cluster i

    for i in range(0, k):
        index = random.randint(0, len(Data))
        latitude = Data[index][0]
        longitude = Data[index][1]
        reviewCount = (Data[index][2])
        checkins = (Data[index][3])
        clusterCentroids.append([latitude, longitude, reviewCount, checkins])

    #for i in range(0, k):
        #print clusterCentroids[i]
    err = float("inf")

    while (1):
        # Calculate distance from centroids
        distanceArray = [[0.0 for x in range(len(Data))] for y in range(k)]
        for i in range(len(clusterCentroids)):
            for j in range(len(Data)):
                distanceArray[i][j] = eDistance(clusterCentroids[i], Data[j])
        # Assign points to clusters
        clusterArray = []
        minIndex = 0
        for i in range(len(distanceArray[0])):
            min = float("inf")
            for j in range(len(distanceArray)):
                if distanceArray[j][i] < min:
                    min = distanceArray[j][i]
                    minIndex = j
            clusterArray.append(minIndex)

        clusters = [[] for x in range(k)]
        for i in range(len(clusterArray)):
            clusters[clusterArray[i]].append(Data[i])

        clusterCentroids = []
        for i in range(len(clusters)):

            if len(clusters[i]) != 0:
                cluster = calculateCentroid(clusters[i])
                latitude = cluster[0]
                longitude = cluster[1]
                reviewCount = cluster[2]
                checkins = cluster[3]
                clusterCentroids.append([latitude, longitude, reviewCount, checkins])

            else:
                index = random.randint(0, len(Data))
                print "Random Points: %d" % index
                latitude = Data[index][0]
                longitude = Data[index][1]
                reviewCount = Data[index][2]
                checkins = Data[index][3]
                clusterCentroids.append([latitude, longitude, reviewCount, checkins])
                print "Added a new cluster"

        oldErr = err
        err = SSE(clusters, clusterCentroids)
        # print ("Error:%.2f") % (err)
        if oldErr == err:
            break

    print ("WC-SSE=%.2f") % (err)
    # Print final Centroids
    for i in range(0, k):
        print ("Centroid%d=%s") % (i + 1, clusterCentroids[i])


# Input validation
if len(sys.argv) < 4:
    print("Usage: clustering.py datasetPath K model")
    sys.exit()

datasetPath = sys.argv[1]
if os.path.exists(datasetPath):
    datasetPath = sys.argv[1]
else:
    print("Invalid data path")
    sys.exit()

K = 0
if sys.argv[2].isdigit():
    K = sys.argv[2]
    K = int(K)
else:
    print("K has to be an integer greater than or equal to 1")
    sys.exit()

# Put data in correct format & covert it to matrix
data = pd.read_csv(datasetPath, sep=',', quotechar='"', header=0)
data = data[['latitude', 'longitude', 'reviewCount', 'checkins']]
X = data.as_matrix()
#X = preprocessing.scale(X)

#for i in range(0, len(X)):
 #   X[i][2] = math.log(X[i][2])
 #   X[i][3] = math.log(X[i][3])


# Decide and use model type
model = sys.argv[3]
# modelType = "k-means"
if model == "km":
    # modelType = "k-means"
    kmeans(X, K)

elif model == "ac":
    # modelType = "Agglomerative clustering"
    agglo(X, K)

