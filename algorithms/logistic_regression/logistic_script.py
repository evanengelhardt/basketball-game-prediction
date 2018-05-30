import numpy as np

import data_retrieval.data_access.dataloader as data
import evaluation.evaluation_script as eval
from algorithms.logistic_regression.logistic_regression import LogisticRegression
from main import variables as var


def run_logistic_reg(raw_data):

    train_set, test_set, favorite_set = data.load_games(var.ALGORITHM_INFO['train_size'],
                                                        var.ALGORITHM_INFO['test_size'], raw_data)

    print("Running logistic regression on file\n")

    log_reg = LogisticRegression()

    log_reg.learn(x_train=train_set[0], y_train=train_set[1], epochs=var.ALGORITHM_INFO['epochs'],
                  init_wgt=var.ALGORITHM_INFO['init_wgt'], learn_step=var.ALGORITHM_INFO['learn_step'],
                  sample_size=2000)

    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    print(log_reg.weights)

    predictions = log_reg.predict(test_set[0])
    error = eval.get_error(test_set[1], predictions)
    favorite_predicted = eval.predicted_favorite(favorite_set, predictions)
    underdog_predicted = eval.predicted_underdog(favorite_set, predictions)
    fav_pred_correct = eval.favorite_pct(favorite_set, predictions, test_set[1])
    ud_pred_correct = eval.underdog_pct(favorite_set, predictions, test_set[1])



    print("\nPredicted the favorite {} percent of the time".format(favorite_predicted))
    print("Correctly chose favorite {} percent of time".format(fav_pred_correct))

    print("\nPredicted the underdog {} percent of the time".format(underdog_predicted))
    print("Correctly chose underdog {} percent of time".format(ud_pred_correct))

    print('Total error for Logistic Regression: ' + str(error))
