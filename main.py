from flask import Flask
from flask_restful import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage
import apps.CalculatingTasks.logic as logicCT
import apps.LinearDependence.logic as logicLD


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('file',
                    type=FileStorage,
                    location='files',
                    required=True
                    )


class LinearDependence(Resource):

    def get(self):
        pass

    def post(self):
        args = parser.parse_args()
        obj_ld = logicLD.LinearDependence(args["file"])
        response = obj_ld.get_lin_dep_vect()
        return response


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
