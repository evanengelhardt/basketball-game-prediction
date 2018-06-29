from data_retrieval.data_access import dataloader as data
from main import variables as var
from algorithms.neural_net.neural_net import NeuralNet


def run_neural_net(raw_data, sizes):
    print("Getting Data for Neural Net\n")

    train_set, test_set, favorite_set = data.load_games(var.ALGORITHM_INFO['train_size'],
                                                        var.ALGORITHM_INFO['test_size'], raw_data)

    print("Running Neural Net")

    nn = NeuralNet(sizes)

    nn.stoch_grad(train_set, 10, 10, .2, test_data=test_set)




