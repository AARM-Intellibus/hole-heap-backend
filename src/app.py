import os
from config import app

if(__name__ == "__main__"):
    app.run(debug= os.environ.get("IS_DEBUG") == "True", 
        host= os.environ.get('HOST'),
        port=os.environ.get('PORT'))