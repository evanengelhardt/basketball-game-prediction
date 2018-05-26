

def get_accuracy(y_test, predictions):
    correct = 0
    for i in range(len(y_test)):
        if y_test[i] == predictions[i]:
            correct += 1
    return (correct / float(len(y_test))) * 100.0


def get_error(ytest, predictions):
    return 100.0-get_accuracy(ytest, predictions)


def predicted_favorite(favorites, predictions):
    return get_accuracy(favorites, predictions)


def prediction_spread(favorite, predictions, ytest):
    fav_correct = 0
    fav_pred = 0
    underdog_correct = 0
    underdog_pred = 0
    for i in range(len(favorite)):
        if favorite[i] == predictions[i]:
            fav_pred += 1
            if predictions[i] == ytest[i]:
                fav_correct += 1
        else:
            underdog_pred += 1
            if predictions[i] == ytest[i]:
                underdog_correct += 1

    return (fav_correct / fav_pred) * 100.0, (underdog_correct / underdog_pred) / 100.0
