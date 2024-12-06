from hyperopt import fmin, tpe, hp, Trials
from hyperopt.pyll.base import scope


def optimize_model(objective, space, max_evals=100):
    trials = Trials()
    best_params = fmin(fn=objective, space=space,
                       algo=tpe.suggest, max_evals=max_evals,
                       trials=trials)

    return best_params, trials
