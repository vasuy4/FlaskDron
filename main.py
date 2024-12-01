from flask_server import app, auto_update
from threading import Thread

if __name__ == '__main__':
    thread_auto_update = Thread(target=auto_update)
    thread_auto_update.start()
    app.run(debug=True)
    thread_auto_update.join()
