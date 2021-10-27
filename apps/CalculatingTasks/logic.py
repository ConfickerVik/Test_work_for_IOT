import threading, time


class ThreadTask:
    def __init__(self):
        # число потоков, при использовании
        # барьеров оно должно быть постоянным
        self.NUM_THREADS = 3
        self.barrier = threading.Barrier(self.NUM_THREADS)
        self.threads = []

    def worker(self):
        th_name = threading.current_thread().name
        print(f'{th_name} в ожидании барьера с {self.barrier.n_waiting} другими\n')
        try:
            worker_id = self.barrier.wait()
        except threading.BrokenBarrierError:
            print(f'{th_name} сброшен\n')
        else:
            print(f'{th_name} прохождение барьера {worker_id}\n')

    def main(self):

        # создаем потоки
        for i in range(5):
            th = threading.Thread(name=f'Task-{i}',
                                  target=self.worker,
                                 )
            self.threads.append(th)
            print(f'Запуск {th.name}')
            th.start()
            time.sleep(1)

        return self.threads


# from concurrent.futures import ThreadPoolExecutor, wait, as_completed
# from time import sleep
# from random import randint
#
#
# def return_after_5_secs(num):
#     sleep(randint(1, 5))
#     return "Return of {}".format(num)
#
#
# pool = ThreadPoolExecutor(5)
# futures = []
# for x in range(5):
#     futures.append(pool.submit(return_after_5_secs, x))
#
# print(wait(futures))
# print(futures)


# import asyncio
# from codetiming import Timer
#
#
# async def fetch_factorial(name, number):
#     f = 1
#     for i in range(2, number + 1):
#         print(f"Task {name}: Compute factorial({i})...")
#         await asyncio.sleep(1)
#         f *= i
#     print(f"Task {name}: factorial({number}) = {f}")
#
#
# async def main(lst):
#     # показывает текущее количество
#     # задач на вычисление, которые
#     # на текущий
#     # момент в работе.
#
#     tasks = []
#     # Помещение работы в очередь
#     for i, work in enumerate(lst):
#         tasks.append(asyncio.ensure_future(fetch_factorial(str(i), work)))
#
#     # Создание очереди работы
#     # work_queue = asyncio.Queue()
#
#     # Запуск задач
#     with Timer(text="\nTotal elapsed time: {:.1f}"):
#         await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
#
#
# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# asyncio.ensure_future(main([15, 10, 5, 2]))
# # res = asyncio.run(main(tasks))
# tasks_status = asyncio.all_tasks(loop)
# print(tasks_status)
