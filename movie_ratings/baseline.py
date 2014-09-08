def load_data(filename):
    """
    Returns a list of data points.
    Each data point is a list representing:
        [movie, user, rating]
    """
    with open(filename) as f:
        lines = f.readlines()
    lines.pop(0)  # pop the header
    return [map(int, line.split(',')) for line in lines]


def rmse(a, b):
    """ Returns RMSE between two lists. """
    return (sum([(i - j) ** 2 for i, j in zip(a, b)]) / float(len(a))) ** 0.5


class ModelBaseline(object):
    """ Returns an average rating for each movie """
    def train(self, X):
        sums = {}  # dict containng the sum of ratings for each movie
        counts = {}  # dict containing the number of ratings for each movie
        for movie, _, value in X:
            if movie not in counts:
                counts[movie] = sums[movie] = 0
            sums[movie] += value
            counts[movie] += 1
        self.avg_ratings = {}  # dict containing the average ratings of movies
        for movie in counts:
            self.avg_ratings[movie] = float(sums[movie]) / counts[movie]

    def predict(self, X):
        return [self.avg_ratings.get(movie, 0) for movie, _, _ in X]

    def test(self, X):
        predicted = self.predict(X)
        real = [val for _, _, val in X]
        return rmse(real, predicted)


if __name__ == "__main__":
    train = load_data("ratings-train.csv")
    test = load_data("ratings-test.csv")
    print "Training the baseline predictor on %s data points..." % len(train)
    print "This predictor always predicts the average rating for each movie."
    m = ModelBaseline()
    m.train(train)
    print "The test set contains %s data points." % len(test)
    print "RMSE on the test set is %.4f" % m.test(test)
