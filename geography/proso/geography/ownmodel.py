from proso.geography.model import PredictiveModel


class RollingSuccessModel(PredictiveModel):

    """
    Predicts the probability of the correct answer equal to the rolling success rate.
    """

    def prepare(self, user_id, place_asked_id, options, question_type, inserted, environment):
        if environment.has_answer(user_id=user_id, place_id=place_asked_id):
            return environment.rolling_success(user_id=user_id, place_id=place_asked_id)
        elif environment.has_answer(user_id=user_id):
            return environment.rolling_success(user_id=user_id)
        else:
            return environment.rolling_success(place_id=place_asked_id)

    def predict(self, user_id, place_asked_id, options, question_type, inserted, data):
        return data

    def update(self, answer, environment, data, prediction):
        pass


class AverageModelWithoutEnvironment(PredictiveModel):

    """
    Predicts the probability of the correct answer equal to the global success rate.
    It doesn't use environment.
    """

    _correct = 0
    _all = 0

    def prepare(self, user_id, place_asked_id, options, question_type, inserted, environment):
        return self._correct/ float(max(self._all, 1))

    def predict(self, user_id, place_asked_id, options, question_type, inserted, data):
        return data

    def update(self, answer, environment, data, prediction):
        self._correct += (answer['place_asked'] == answer['place_answered'])
        self._all += 1


class AverageModel(PredictiveModel):

    """
    Predicts the probability of the correct answer equal to the global success rate.
    """

    def prepare(self, user_id, place_asked_id, options, question_type, inserted, environment):
        return environment.read('correct', default=0) / float(environment.read('all', default=1))

    def predict(self, user_id, place_asked_id, options, question_type, inserted, data):
        return data

    def update(self, answer, environment, data, prediction):
        environment.update(
            'correct',
            0,
            lambda x: x + (answer['place_asked'] == answer['place_answered']))
        environment.update(
            'all',
            0,
            lambda x: x + 1)
