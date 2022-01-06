class MicroCluster:

    # Constructor
    def __init__(self, number_of_data_points, radius, centroid, current_timestamp):
        self.number_of_data_points = number_of_data_points
        self.radius = radius
        self.centroid = centroid
        self.creation_time = current_timestamp
        self.last_edited_time = current_timestamp
        self.data_points = []

    # Updating last time the cluster edited
    def update_last_edited_time(self, time):
        self.last_edited_time = time

    # Inserting data point to the cluster
    def insert(self, data_point_id):
        self.data_points.append(data_point_id)

    # Merging data points of two clusters
    def merge_data_points(self, data_points_1, data_points_2):
        self.data_points = data_points_1 + data_points_2

    # Calculate fading with given lambda and times
    def fading(self, current_time, lambda_t):

        # t = tc - t0
        t = current_time - self.creation_time

        # f(t) = 2 ^ (lambda * t)
        ft = 2 ** (lambda_t * t)

        # Return f(t)
        return ft

    # get radius of cluster
    def get_radius(self):
        return self.radius

    # set radius of cluster
    def set_radius(self, radius):
        self.radius = radius

    # get centroid of cluster
    def get_centroid(self):
        return self.centroid
a
