import numpy as np
from operator import itemgetter
from time import time
from math import exp
from sklearn.metrics import euclidean_distances

from micro_cluster import MicroCluster


class SOStream:

    # Constructor
    def __init__(self, data, alpha, min_pts, merge_threshold, lambda_t, fade_threshold):
        self.clusters = []
        self.data = data
        self.alpha = alpha
        self.minPts = min_pts
        self.merge_threshold = merge_threshold
        self.lambda_t = lambda_t
        self.fade_threshold = fade_threshold
        self.number_of_merged_clusters = 0
        self.number_of_faded_clusters = 0

    # Finding neighbors of winner cluster
    def find_neighbors(self, winner_cluster):

        # If number of clusters is greater than minPts
        if len(self.clusters) >= self.minPts:

            # Current clusters
            clusters = self.clusters

            # distances list
            distances_from_winner = {}

            # Calculating distances from winner cluster for each cluster
            for cluster in clusters:

                # If current cluster is not the winner then
                # calculate distance from winner cluster
                if clusters.index(cluster) != clusters.index(winner_cluster):
                    # Calculating distance using euclidean distance
                    distance = euclidean_distances(winner_cluster.centroid, cluster.centroid)
                    distances_from_winner[clusters.index(cluster)] = distance

            # Sorting distances
            sorted_distances_from_winner = sorted(distances_from_winner.items(), key=itemgetter(1))

            # Updating radius of winner cluster
            if len(sorted_distances_from_winner) <= 2:
                radius = sorted_distances_from_winner[self.minPts - 2][1]
            else:
                radius = sorted_distances_from_winner[self.minPts - 1][1]
            winner_cluster.set_radius(radius)

            # Neighbors of winner cluster list
            winner_cluster_neighbors = []

            # Finding neighbors of winner cluster.
            # If distance of current cluster from winner cluster
            # is less than radius of winner cluster then it is
            # neighbor of winner cluster
            for d in sorted_distances_from_winner:
                if d[1] <= radius:
                    winner_cluster_neighbors.append(clusters[d[0]])

            # Return neighbors list
            return winner_cluster_neighbors
        else:
            return 0

    # Finding neighbors of winner cluster that
    # overlap with it
    def find_overlap(self, winner_cluster, winner_cluster_neighbors):
        # Current clusters
        clusters = self.clusters

        # overlapping clusters list
        overlapping_clusters = []

        # Finding overlapping clusters from winner cluster's neighbors
        for cluster in winner_cluster_neighbors:

            # If current cluster is not the winner then
            # calculate distance from winner cluster
            if clusters.index(winner_cluster) != clusters.index(cluster):

                # Calculate distance between winner cluster and
                # current cluster using euclidean distance
                distance = euclidean_distances(winner_cluster.centroid, cluster.centroid)

                # If distance of current cluster from winner cluster
                # is less than radius of winner cluster plus current cluster
                # then it is overlapping with winner cluster
                if distance - (winner_cluster.radius + cluster.radius) < 0:
                    # Insert current cluster to overlapping list
                    overlapping_clusters.append(cluster)

        # Return overlapping clusters list
        return overlapping_clusters

    # Merging winner cluster with overlapping clusters
    # that satisfy constraints
    def merge_clusters(self, winner_cluster, overlapping_clusters):

        # checking each overlapping cluster
        for cluster in overlapping_clusters:

            # Calculating distance between winner cluster and
            # current cluster using euclidean distance
            distance = euclidean_distances(winner_cluster.centroid, cluster.centroid)

            # If distance of current cluster from winner is
            # less than given merge_threshold
            if distance < self.merge_threshold:

                # Number of merged clusters will increase by one
                self.number_of_merged_clusters += 1

                # Parameters
                wi = winner_cluster.number_of_data_points
                ai = winner_cluster.centroid
                wj = cluster.number_of_data_points
                bi = cluster.centroid

                # Calculating new centroid for merged clusters
                new_centroid = np.add(wi * ai, wj * bi) / (wi + wj)

                # Parameters
                cy = new_centroid
                ci = winner_cluster.centroid
                cj = cluster.centroid
                ri = winner_cluster.radius
                rj = cluster.radius

                # Calculating distance between new centroid and
                # winner cluster's centroid using euclidean distance
                distance1 = euclidean_distances(cy, ci)

                # Calculating distance between new centroid and
                # current cluster's (the cluster that we want to merge with winner cluster)
                # centroid using euclidean distance
                distance2 = euclidean_distances(cy, cj)

                # New radius will be maximum between (distance1 + ri), (distance2 + rj)
                new_radius = max(distance1 + ri, distance2 + rj)

                # Creating new cluster that created by merging
                merged_cluster = MicroCluster(
                    # number of points is sum of winner cluster and merging cluster points
                    number_of_data_points=wi + wj,
                    radius=new_radius,
                    centroid=new_centroid,
                    current_timestamp=time()
                )

                # merging points of winner cluster and merging cluster
                merged_cluster.merge_data_points(winner_cluster.data_points, cluster.data_points)

                # inserting new merged cluster to clusters
                self.clusters.append(merged_cluster)

                # removing current cluster that
                # merged with winner cluster
                self.clusters.remove(cluster)

                # removing winner cluster if its present
                if winner_cluster in self.clusters:
                    self.clusters.remove(winner_cluster)

    # Updating winner cluster and it's neighbors when
    # new data point is adding
    def update_cluster(self, winner_cluster, data_point, winner_cluster_neighbors):

        # Current point belongs to winner cluster
        # so number of points in winner cluster must be increase by one
        winner_cluster.number_of_data_points += 1

        # Inserting current point to winner cluster
        winner_cluster.insert(data_point.index[0])

        # updating time
        winner_cluster.update_last_edited_time(time())

        # updating neighbors of winner cluster
        for cluster in winner_cluster_neighbors:
            # Previous centroid of current cluster
            last_centroid = cluster.centroid

            # width = radius ^ 2
            winner_width = winner_cluster.radius ** 2

            # Calculating Beta
            beta = exp(-(euclidean_distances(last_centroid, winner_cluster.centroid)) / (2 * winner_width))

            # adjusting current cluster's centroid
            cluster.centroid = self.adjust_centroid(last_centroid, winner_cluster.centroid, beta)

        # Return neighbors list
        return winner_cluster_neighbors

    # fading clusters
    def fading_all(self):

        # fading each cluster that it's fade value is
        # less than given fade_threshold
        for cluster in self.clusters:

            # Calculating fade value
            ft = cluster.fading(time(), self.lambda_t)

            # Fading current cluster if it's fade value is
            # less than given fade_threshold
            if ft < self.fade_threshold:
                # Number of faded clusters will increase by one
                self.number_of_faded_clusters += 1

                # remove current cluster
                self.clusters.remove(cluster)

    # adjusting cluster's centroid
    def adjust_centroid(self, last_centroid, winner_cluster_centroid, beta):

        # centroid(t+1) = centroid(t) + alpha*beta*(centroid_winner(t)-centroid(t))
        return np.add(last_centroid, self.alpha * beta * np.subtract(winner_cluster_centroid, last_centroid))

    # Getting minimum distance between sample and clusters
    def min_distance(self, sample):

        # Current clusters
        clusters = self.clusters

        # distances list
        distances = {}

        # Calculating distances from sample for each cluster
        for cluster in clusters:
            # Calculating distance using euclidean distance
            distances[clusters.index(cluster)] = euclidean_distances(sample, cluster.centroid)

        # Sort distances
        sorted_distances = sorted(distances.items(), key=itemgetter(1))

        # Return minimum distance
        return clusters[sorted_distances[0][0]]

    # Inserting a cluster to clusters list
    def insert(self, micro_cluster):
        self.clusters.append(micro_cluster)

    # Getting list of clusters centroids
    def get_centroids_of_clusters(self):

        # clusters centroids list
        centroids = []

        # for each cluster append its centroid to list
        for cluster in self.clusters:
            centroids.append(cluster.centroid)

        # Return clusters centroids
        return centroids

    # Calculating purity
    def calculate_purity(self, data, unique_label):

        # Current clusters
        clusters = self.clusters

        sum = 0

        # for each cluster
        for cluster in clusters:

            # labels list
            labels = np.array([])

            # for each data point in cluster's data points
            for data_point in cluster.data_points:

                # insert labels of data points
                labels = np.append(labels, data.iloc[data_point:data_point + 1, 2])

            # unique labels and count
            unq_label, counts = np.unique(labels, return_counts=True)
            d = dict(zip(unique_label, counts))
            dominant_label_count = max(d.items(), key=itemgetter(1))[1]

            # sum = sigma(i=1 to k) (|Ndi| / |Ni|)
            sum += float(dominant_label_count) / cluster.number_of_data_points

        # Purity = sum/k * 100%
        purity = (sum / len(clusters)) * 100

        # Return purity
        return purity

    # Get data
    def get_data(self):
        return self.data

    # Get alpha
    def get_alpha(self):
        return self.alpha

    # Get minPts
    def get_min_pts(self):
        return self.minPts

    # Get merge threshold
    def get_merge_threshold(self):
        return self.merge_threshold

    # Get merge threshold
    def get_fade_threshold(self):
        return self.fade_threshold

    # Get lambda
    def get_lambda_t(self):
        return self.lambda_t

    # Get clusters list
    def get_clusters(self):
        return self.clusters

    # Get total number of merged clusters
    def get_number_of_merged_clusters(self):
        return self.number_of_merged_clusters

    # Get total number of faded clusters
    def get_number_of_faded_clusters(self):
        return self.number_of_faded_clusters
