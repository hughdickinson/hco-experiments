################################################################
# Tracks probabilities as they change temporally


class Tracker:
    """
    Keeps track of numbers and how they change
    """

    def __init__(self, value=None):
        """
            Initialize a tracker

            Args:
                value: (optional) initial value.
        """
        self._history = []
        self._current = value

        if value is not None:
            self._history.append(value)

        self.n = len(self._history)

    def add(self, value):
        """
            Add a value to the tracker

            Args:
                value: value to be added to the tracker
        """
        self._history.append(value)
        self._current = value

        self.n += 1

    def current(self):
        """
        Get current (most recent) value from tracker
        """
        return self._current

    def getHistory(self):
        """
        Get the history of values
        """
        return self._history[:]

    def size(self):
        """
        Returns how many values are in the tracker
        """
        return len(self._history)


class User_Score_Tracker(Tracker):
    """
        Modified tracker specifically for user scores
    """

    def __init__(self, label, epsilon):
        """
            Initialize a user score tracker

            Args:
                label: label for the tracker,
                       typically the annotation type
                epsilon: (float) initial user score value
        """
        super().__init__(epsilon)

        self.label = label
        self.epsilon = epsilon

        self.n_seen = 0
        self.n_matched = 0

    def calculateScore(self):
        n_matched = self.n_matched
        n_seen = self.n_seen

        score = n_matched / n_seen

        # TODO TEMPORARY FIX
        # Prevents a user from receiving a perfect 1.0 score
        # or a 0.0 score.
        # If the score is 1, then it is adjusted to:
        #   n
        # ------
        #  n+1
        # If the score is 0, then it is the complement of that:
        #       n
        # 1 - ------
        #      n+1

        if score == 0:
            score = 1 - (n_seen / (n_seen + 1))
        elif score == 1:
            score = n_seen / (n_seen + 1)

        return score

    def add(self, annotation):
        self.n_seen += 1

        if annotation == self.label:
            self.n_matched += 1

        score = self.calculateScore()
        super().add(score)


class Tracker_Collection:
    """
    Collection of multiple trackers
    """

    def __init__(self):
        """
            Initialize a Tracker Collection
        """
        self.trackers = {}

    def add(self, label, tracker):
        """
            Add a tracker to the collection

            Args:
                label: label, or key, for the tracker
                tracker: (Tracker) tracker to be added
        """
        if label in self.trackers:
            raise NameError(
                'Tracker with that label already \
                exists! Remove it first')

        if not isinstance(tracker, Tracker):
            raise ValueError

        self.trackers[label] = tracker

    def addNew(self, tracker_type, label, value):
        """
            Create a new tracker and add it to the collection

            Args:
                tracker_type: (type) type of tracker create
                label: label for the tracker
                value: initial value for the tracker
        """
        tracker = tracker_type(label, value)

        self.trackers[label] = tracker
        return tracker

    def remove(self, label):
        """
            Remove a tracker from the collection

            Args:
                label: label of tracker that should be removed
        """
        if label in self.trackers:
            tracker = self.trackers[label]
            del self.trackers[label]

            return tracker

    def get(self, label):
        """
            Get a tracker from the collection

            Args:
                label: label of tracker to be fetched
        """
        if label in self.trackers:
            return self.trackers[label]

    def getAll(self):
        """
            Get all trackers from the collection
        """
        return self.trackers

    def Generate(tracker_type, labels, value=None):
        """
            Generate a Tracker_Collection and create new
            Trackers for it with given labels

            Args:
                t_type: (type) Type of tracker to generate
                labels: labels for the new trackers
                value: initial value for the new trackers
        """
        trackers = Tracker_Collection()
        if type(labels) is not list:
            raise ValueError("Need list of labels to initialize trackers")

        for label in labels:
            tracker = tracker_type(label, value)
            trackers.add(label, tracker)

        return trackers


# class Labeled_Trackers:

#     def __init__(self, tracker, labels, value=None):
#         if type(labels) is not list:
#             raise ValueError("Need list of labels to initialize trackers")

#         self.trackers = {}

#         for label in labels:
#             self.add(tracker, label, value)

#     def add(self, tracker_type, label, value):
#         tracker = tracker_type(label, value)

#         self.trackers[label] = tracker
#         return tracker

#     def get(self, label):
#         return self.trackers[label]

#     def getAll(self):
#         return self.trackers
