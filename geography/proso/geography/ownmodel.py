from proso.models.prediction import SimplePredictiveModel


class AverageModel(SimplePredictiveModel):

    """
    Predicts the probability of the correct answer equal to the global success rate.
    """

    _correct = 0
    _total = 0.0

    def simple_predict(self, user, place_asked, time, **kwargs):
        return self._correct / max(self._total, 1.0)

    def simple_update(self, prediction, user, place_asked, correct, time, **kwargs):
        self._total += 1.0
        self._correct += correct
