import os
from threading import Thread
from config import app
from event.config import listen_for_messages

thread = Thread(target=listen_for_messages)

thread.daemon = True
thread.start()

if(__name__ == "__main__"):
    app.run(debug= os.environ.get("IS_DEBUG") == "True", 
        host= os.environ.get('HOST'),
        port=os.environ.get('PORT'))
