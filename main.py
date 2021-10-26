from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import pandas as pd
import numpy as np
import apps.CalculatingTasks.logic as logic
import asyncio
from codetiming import Timer


app = Flask(__name__)
api = Api(app)


class LinearDependence(Resource):

    def get(self):
        # Читаем файл
        data_csv = pd.read_csv(r"C:\Users\confi\PycharmProjects\Test_work_for_IOT\apps\LinearDependence\csv\data.csv")
        # Очищаем данные от дат и пустых значений в файле
        df = data_csv.drop("Unnamed: 0", axis=1)
        df = df[~df[df.columns[0]].isna()]

        matrix = df.values
        res = np.nonzero(np.isclose(np.abs(np.corrcoef(matrix) - np.eye(matrix.shape[0])), 1.))

        return {"res": str(res)}

    def post(self):
        pass


class CalculatingTasks(Resource):

    async def fetch_factorial(self, name, number):
        f = 1
        for i in range(2, number + 1):
            print(f"Task {name}: Compute factorial({i})...")
            await asyncio.sleep(1)
            f *= i
        print(f"Task {name}: factorial({number}) = {f}")

    async def main(self):
        # показывает текущее количество
        # задач на вычисление, которые
        # на текущий
        # момент в работе.

        # Создание очереди работы
        # work_queue = asyncio.Queue()
        tasks = []
        # Помещение работы в очередь
        for i, work in enumerate([15, 10, 5, 2]):
            tasks.append(asyncio.create_task(self.fetch_factorial(str(i), work)))

        # Запуск задач
        with Timer(text="\nTotal elapsed time: {:.1f}"):
            await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)

        return tasks

    def get(self):
        # ct_obj = logic.CT()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        res = asyncio.run(self.main())
        print(asyncio.all_tasks(loop))
        # return {"done": done, "pending": pending}
        return {"tasks": ""}

    def post(self):
        pass


api.add_resource(LinearDependence, '/linear_dependence')  # Route_1
api.add_resource(CalculatingTasks, '/calculating_tasks')  # Route_2

if __name__ == '__main__':
    app.run()
