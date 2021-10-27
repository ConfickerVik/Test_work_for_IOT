from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import apps.CalculatingTasks.logic as logicCT
import apps.LinearDependence.logic as logicLD


app = Flask(__name__)
api = Api(app)


class LinearDependence(Resource):

    def get(self):
        obj_ld = logicLD.LinearDependence(r"C:\Users\confi\PycharmProjects\Test_work_for_IOT\apps\LinearDependence\csv\data.csv")
        response = obj_ld.get_lin_dep_vect()

        return response

    def post(self):
        pass


class CalculatingTasks(Resource):

    def get(self):
        thread_task_obj = logicCT.ThreadTask()
        ### loop = asyncio.new_event_loop()
        ### asyncio.set_event_loop(loop)
        ### res = asyncio.run(self.main())
        ### tasks_status = asyncio.all_tasks(loop)
        ### return {"done": done, "pending": pending}
        tasks_status = str(thread_task_obj.main())
        # сброс барьера
        thread_task_obj.barrier.abort()
        # блокируем основной поток программы
        # до завершения работы всех потоков
        for thread in thread_task_obj.threads:
            thread.join()
        return {"tasks": str(tasks_status)}

    def post(self):
        pass


api.add_resource(LinearDependence, '/linear_dependence')  # Route_1
api.add_resource(CalculatingTasks, '/calculating_tasks')  # Route_2

if __name__ == '__main__':
    app.run()
