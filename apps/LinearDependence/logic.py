import pandas as pd
import numpy as np


class LinearDependence:
    def __init__(self, csv_data):
        self.csv = csv_data

    def get_lin_dep_vect(self):
        # Читаем файл
        data_csv = pd.read_csv(self.csv)

        # Очищаем данные от дат и пустых значений в файле
        df = data_csv.drop("Unnamed: 0", axis=1)
        df = df[~df[df.columns[0]].isna()]

        # Получаем numpy матрицу
        matrix = df.values.T

        # Выполняем поиск линейно зависмых векторов
        results = np.nonzero(np.isclose(np.abs(np.corrcoef(matrix) - np.eye(matrix.shape[0])), 1.))

        response = {}
        if np.size(results) == 0:
            response = {"messages": "Не удалось найти линейно зависмые столбцы!"}
        else:
            response = {"messages": "Успех!",
                        "answer": sorted(list(set(results[0].tolist())))}

        return response
