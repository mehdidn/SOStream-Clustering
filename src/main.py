import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from time import time
from sklearn.metrics import euclidean_distances

from SOStream import SOStream
from micro_cluster import MicroCluster

# Main function
if __name__ == '__main__':

    # Read data set
    data = pd.read_csv('../Data/Dataset_2.csv', header=None)

    # Random permutation
    data = data.reindex(np.random.permutation(data.index))

    # Get labels from given data
    data_frame_label = np.array(data.iloc[:, 2])

    # Unique labels
    unique_label = np.unique(data_frame_label)

    # Delete third column from data
    # that explains label
    data_frame = data.drop([2], axis=1)

    # Create SOSTream object
    sostream = SOStream(data=data_frame,
                        alpha=0.1,
                        min_pts=3,
                        merge_threshold=9,
                        lambda_t=0.3,
                        fade_threshold=10
                        )

    # clusters list
    clusters = dict()

    # purities list
    purities = dict()

    # Start of processing time
    start_time = time()

    # Insert data points one by one
    for i in range(len(data_frame)):

        # Get one data point
        data_point = data_frame[i:i + 1]

        # Current time
        t = time()

        # If number of current clusters is greater than minPts
        if len(sostream.get_clusters()) - 1 >= sostream.minPts:

            # Get winner cluster
            winner_cluster = sostream.min_distance(data_point)

            # Get neighbors of winner cluster
            winner_cluster_neighbors = sostream.find_neighbors(winner_cluster)

            # Calculate distance between current data point and
            # centroid of winner cluster using euclidean distance
            distance = euclidean_distances(data_point, winner_cluster.centroid)

            # If distance is less than radius of winner cluster
            if distance <= winner_cluster.radius:

                # Update neighbors of winner cluster
                winner_cluster_neighbors = sostream.update_cluster(winner_cluster,
                                                                   data_point,
                                                                   winner_cluster_neighbors)

            # If distance is greater than radius of winner cluster
            else:

                # Create new cluster from current data point
                new_micro_cluster = MicroCluster(number_of_data_points=1,
                                                 radius=0,
                                                 centroid=data_point,
                                                 current_timestamp=t
                                                 )

                # Insert current data point to new cluster
                new_micro_cluster.insert(data_point.index[0])

                # insert new cluster to list of clusters
                sostream.insert(new_micro_cluster)

            # Get overlapping list from winner cluster and its neighbors
            overlapping = sostream.find_overlap(winner_cluster, winner_cluster_neighbors)

            # If more than zero neighbors overlap with winner cluster
            if len(overlapping) > 0:

                # merge winner cluster with overlapped cluster
                sostream.merge_clusters(winner_cluster, overlapping)

        # If number of current clusters is less than minPts
        else:

            # Create new cluster from current data point
            new_micro_cluster = MicroCluster(number_of_data_points=1,
                                             radius=0,
                                             centroid=data_point,
                                             current_timestamp=t
                                             )

            # Insert current data point to new cluster
            new_micro_cluster.insert(data_point.index[0])

            # Insert new cluster to list of clusters
            sostream.insert(new_micro_cluster)

        # Each 20 steps fade older clusters
        if i % 20 == 0:
            sostream.fading_all()

        # Each 25 steps save changes of
        # number of clusters and purities
        if i % 25 == 0 and i != 0:

            # Number of clusters at i'th step
            clusters[i] = len(sostream.get_clusters())

            # Calculate purity
            purity = sostream.calculate_purity(data=data, unique_label=unique_label)

            # Purity at i'th step
            purities[i] = purity

    # Number of clusters at current data point index's step
    clusters[len(data_frame)] = len(sostream.get_clusters())

    # Purity at current data point index's step
    purities[len(data_frame)] = sostream.calculate_purity(data=data, unique_label=unique_label)

    # Plot changes happened to number of
    # clusters over the process time
    y_pos = list(clusters.keys())
    plt.xlabel('number of received data', color='darkblue')
    plt.ylabel('number of clusters', color='darkblue')
    plt.plot(y_pos, clusters.values(), color='darkblue')    # line plot
    plt.show()
    plt.xlabel('number of received data', color='darkblue')
    plt.ylabel('number of clusters', color='darkblue')
    plt.bar(y_pos, clusters.values(), width=10, color='darkblue', align='center', alpha=0.3)    # bar plot
    plt.show()

    # Plot changes happened to
    # purity over the process time
    y_pos = list(purities.keys())
    plt.xlabel('number of received data', color='purple')
    plt.ylabel('purity', color='purple')
    plt.plot(y_pos, purities.values(), color='purple')      # line plot
    plt.show()
    plt.xlabel('number of received data', color='purple')
    plt.ylabel('purity', color='purple')
    plt.bar(y_pos, purities.values(), width=10, color='purple', align='center', alpha=0.3)      # bar plot
    plt.show()

    # Plot data points
    # with blue color
    data.plot.scatter(x=0, y=1)
    plt.scatter(data.loc[:, 0], data.loc[:, 1], color='blue', s=100)

    # Plot centroids of the latest
    # clusters on data points
    # with red color
    centroids_of_clusters = sostream.get_centroids_of_clusters()
    for centroid in centroids_of_clusters:
        plt.scatter(centroid[0], centroid[1], color='red', s=100)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

    # Calculate average purity
    purity_sum = 0
    purity_counter = 0
    for purity in purities:
        purity_counter += 1
        purity_sum += purities[purity]
    average_purity = purity_sum / purity_counter

    # Process time = tc - t0
    process_time = time() - start_time

    # Print results
    print("Process time =: ", '{0:.2f}'.format(process_time))
    print("Final number of clusters: ", len(sostream.get_clusters()))
    print("Number of faded clusters: ", sostream.get_number_of_faded_clusters())
    print("Number of merged clusters: ", sostream.get_number_of_merged_clusters())
    print("Average purity: ", '{0:.2f}'.format(average_purity))
