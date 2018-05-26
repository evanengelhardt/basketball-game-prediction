import data_retrieval.dataloader as data
from algorithms.logistic_regression import LogisticRegression
import numpy as np
import evaluation.evaluation_script as eval



def run_logistic_reg(train_size, test_size, epoch, learn_step, raw_data):

    train_set, test_set, favorite_set = data.load_games(train_size, test_size, raw_data)

    print("Running logistic regression on file\n")

    log_reg = LogisticRegression()

    log_reg.learn(x_train=train_set[0], y_train=train_set[1], epochs=epoch, init_wgt=1, learn_step=learn_step,
                  sample_size=2000)

    np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
    print(log_reg.weights)

    predictions = log_reg.predict(test_set[0])
    error = eval.get_error(test_set[1], predictions)
    favorite_predicted = eval.predicted_favorite(favorite_set, predictions)
    prediction_spread = eval.prediction_spread(favorite_set, predictions, test_set[1])
    fav_pred_correct = prediction_spread[0]
    under_dog_pred_correct = prediction_spread[1]


    print("\nPredicted the favorite {} percent of the time".format(favorite_predicted))
    print("Correctly chose favorite {} percent of time".format(fav_pred_correct))

    print("\nPredicted the underdog {} percent of the time".format(100.0 - favorite_predicted))
    print("Correctly chose underdog {} percent of time".format(under_dog_pred_correct))

    print('Total error for Logistic Regression: ' + str(error))
