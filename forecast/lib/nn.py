import json
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import MinMaxScaler
from analysis.models import Algorithm, Result
from forecast.models import File

def infer(pk_algo: int, pk_file: int):

    algo = Algorithm.objects.get(pk=pk_algo)
    file = File.objects.get(pk=pk_file)
    result = Result.objects.get(algo=algo)
    window = int(algo.window)
    step = int(algo.step)
    model = torch.load(result.model, map_location=torch.device('cpu'))
    data = pd.read_csv(file.path)  # 待预测数据集路径
    try:
        training_features = data[json.loads(result.algo.selected)].values  # 将选择的特征从数据集中抽取出来
        training_goal = data[result.algo.target].values  # 将目标从数据集中抽取出来
    except:
        return None
    # 数据标准化
    scaler_features = MinMaxScaler()
    scaler_goal = MinMaxScaler()
    # scaler_goal.fit(training_goal.reshape(-1, 1))
    training_features_normalized = scaler_features.fit_transform(training_features)
    input_dim = training_features_normalized.shape[1]

    # 准备输入序列
    X_predict = training_features_normalized[-window:] #取出最后training_window个元素
    X_predict = torch.tensor(np.array(X_predict, dtype=np.float32))
    X_predict = X_predict.resize(1, window, input_dim)
    Y_predictions = model(X_predict)
    print(Y_predictions.detach().numpy())

    print(Y_predictions)

    plt.switch_backend('Agg')
    plt.clf()

    forecast = Y_predictions.flatten()
    training_window = training_goal[-window:]

    plt.plot(list(range(window, window + int(step))), forecast, label='Prediction', linestyle='--')
    plt.plot(list(range(window)), training_window, label='Training Data', linestyle='-')
    plt.xlabel('Serial')
    plt.ylabel(result.algo.target)
    plt.title(algo.neuralNetwork+' Model Prediction')
    plt.legend()

    path = "result/forecast_" + algo.neuralNetwork + "_" + file.name + '.png'
    plt.savefig(path)

    return forecast, path
