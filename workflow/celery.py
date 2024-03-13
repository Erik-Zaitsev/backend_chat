from celery import Celery


app = Celery(
    'tasks', 
    broker='redis://192.168.239.21:6379/0',
    backend='redis://192.168.239.21:6379/0',
    include=['workflow.tasks'])

if __name__ == '__main__':
    app.start()

