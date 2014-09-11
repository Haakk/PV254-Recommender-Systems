from argparse import ArgumentParser
from os import path, makedirs
import matplotlib.pyplot as plt
import proso.geography.answers as answers
import proso.models.environment as environment
import proso.geography.evaluate as evaluate
import proso.models.prediction as model
import proso.geography.ownmodel as ownmodel
import proso.models.optimize as optimize


# Place here models you want to evaluate. Keys in the following dictionary
# represent names and values are pairs: the instance of the predictive model
# and the instance of the used environment (or None).
MODELS_TO_EVALUATE = {
    'global_succcess': (ownmodel.AverageModel(), None),
    'default': (model.PriorCurrentPredictiveModel(), environment.InMemoryEnvironment())
}

# Place here models you want to optimize. Keys in the following dictionary
# represent names and values are pairs: the class of the model and the class of
# the used environment.
#
# All parameters in the constructors of predictive model and the environment
# has to have default values.
MODELS_TO_OPTIMIZE = {
    'default': (model.PriorCurrentPredictiveModel, environment.InMemoryEnvironment)
}

DESTINATION = 'dest'


def parser_init():
    parser = ArgumentParser()
    parser.add_argument(
        '-g',
        '--graphs',
        action='store_true',
        help='plot calibration graphs and save them to the destination directory')
    parser.add_argument(
        '-s',
        '--sample',
        type=float,
        metavar='FLOAT',
        help="don't use all dataset, but only a sample defined as a number from the interval (0, 1)")
    parser.add_argument(
        '-l',
        '--load',
        type=str,
        metavar='FILE',
        required=True,
        help='path to the source file containing dataset')
    parser.add_argument(
        '-d',
        '--destination',
        type=str,
        metavar='FILE',
        default=DESTINATION,
        help='directory where auxiliary files are saved')
    parser.add_argument(
        '-p',
        '--progress',
        action='store_true',
        help='show progress bar')
    parser.add_argument(
        '-m',
        '--model',
        choices=MODELS_TO_EVALUATE.keys(),
        help='restrict the evaluation only for the given model')
    parser.add_argument(
        '-o',
        '--optimize',
        choices=MODELS_TO_OPTIMIZE.keys(),
        help='start trivial optimization of the given model according to RMSE using alternating grid search')
    parser.add_argument(
        '--param_names',
        nargs='+',
        metavar='STRING',
        type=str,
        help='names of the parameters for the optimization')
    parser.add_argument(
        '--param_min',
        nargs='+',
        metavar='FLOAT',
        type=float,
        help='minimal values of parameters for the optimization')
    parser.add_argument(
        '--param_max',
        nargs='+',
        metavar='FLOAT',
        type=float,
        help='maximum values of parameters for the optimization')
    parser.add_argument(
        '--param_steps',
        nargs='+',
        metavar='FLOAT',
        type=float,
        help='minimum steps ')
    return parser


def savefig(args, fig, name):
    if not path.exists(args.destination):
        makedirs(args.destination)
    fig.savefig(args.destination + '/' + name + '.png')


def print_evaluation(args, name, m, e, data):
    print name
    evaluator = evaluate.Evaluator(data, m, e)
    evaluator.prepare(stdout=args.progress)
    brier_rel, brier_res, brier_unc = evaluator.brier()
    result = {
        'rmse': evaluator.rmse(),
        'll': evaluator.logloss(),
        'auc': evaluator.auc(),
        'brier_reliability': brier_rel,
        'brier_resolution': brier_res,
        'brier_uncertainty': brier_unc
    }
    print "\tRMSE:\t\t\t", result['rmse']
    print "\tLL:\t\t\t", result['ll']
    print "\tAUC:\t\t\t", result['auc']
    print "\tBrier reliability:\t", result['brier_reliability']
    print "\tBrier resolution:\t", result['brier_resolution']
    print "\tBrier uncertainty:\t", result['brier_uncertainty']
    if args.graphs is not None:
        fig = plt.figure()
        evaluator.calibration_graphs(fig)
        fig.tight_layout()
        savefig(args, fig, str(name))
    print
    return result


def action_evaluate(args, data):
    if args.model is None:
        result = {}
        for name, (m, e) in MODELS_TO_EVALUATE.iteritems():
            result[name] = print_evaluation(args, name, m, e, data)
        print '----------------------------------------------------------------------'
        print '  BEST'
        print '----------------------------------------------------------------------'
        print "\tRMSE:\t\t\t", max(result.items(), key=lambda x: - x[1]['rmse'])[0]
        print "\tLL:\t\t\t", max(result.items(), key=lambda x: - x[1]['ll'])[0]
        print "\tAUC:\t\t\t", max(result.items(), key=lambda x: x[1]['auc'])[0]
        print "\tBrier reliability:\t",  max(result.items(), key=lambda x: - x[1]['brier_reliability'])[0]
        print "\tBrier resolution:\t",  max(result.items(), key=lambda x: x[1]['brier_resolution'])[0]
    else:
        print_evaluation(
            args,
            args.model,
            MODELS_TO_EVALUATE[args.model][0],
            MODELS_TO_EVALUATE[args.model][1], data)


def action_optimize(args, data):
    if args.param_min is None or len(args.param_min) == 0:
        raise Exception("Can't optimize without lower bounds for parameters defined via --param_min.")
    if args.param_max is None or len(args.param_max) == 0:
        raise Exception("Can't optimize without upper bounds for parameters defined via --param_max.")
    if len(args.param_max) != len(args.param_min):
        raise Exception("Can't optimize when lower and upper bounds for parameters differ in length.")
    if args.param_names is not None and len(args.param_names) != len(args.param_min):
        raise Exception("Can't optimize when the number of parameter names don't match to the length of bounds.")
    model_func, env_func = MODELS_TO_OPTIMIZE[args.optimize]
    def optimize_model(opt_args):
        m = model_func(**dict(zip(args.param_names, opt_args))) if args.param_names is not None else model_func(*opt_args)
        evaluator = evaluate.Evaluator(data, m, env_func())
        evaluator.prepare(stdout=args.progress)
        rmse = evaluator.rmse()
        if args.progress:
            print "RMSE:", rmse
            if args.param_names:
                for n, v in zip(args.param_names, opt_args):
                    print "\t* ", n, ":\t", v
            else:
                for v in opt_args:
                    print "\t* ", v
        return rmse
    optimized = optimize.alternating_grid(optimize_model, zip(args.param_min, args.param_max), minimum_steps=args.param_steps)
    print '----------------------------------------------------------------------'
    print '  OPTIMIZED'
    print '----------------------------------------------------------------------'
    print "RMSE:", optimized[0]
    if args.param_names:
        for n, v in zip(args.param_names, optimized[1]):
            print "\t* ", n, ":\t", v
    else:
        for v in optimized[1]:
            print "\t* ", v


def main():
    parser = parser_init()
    args = parser.parse_args()
    data = answers.from_csv(args.load)
    if args.sample is not None:
        data, other = answers.sample(data, args.sample)
    if args.optimize is None:
        action_evaluate(args, data)
    else:
        action_optimize(args, data)


if __name__ == "__main__":
    main()

