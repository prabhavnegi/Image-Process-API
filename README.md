Image Process API

                            
This API is made using Flask as the main server.


Asynchronous image processing uses celery for background processing and PostgreSQL to keep track of the status.

It takes a CSV file, processes every image, then comps it to 50%, and saves it as another CSV file.

The project uses local storage to store the files and PostgreSQL to maintain the status and final link of the output CSV file.


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`FLASK_APP `

`FLASK_ENV`

`FLASK_RUN_PORT`

`SQLALCHEMY_DATABASE_URI`




## Run Locally

Clone the project

```bash
  git clone https://github.com/prabhavnegi/Image-Process-API
```

Go to the project directory

```bash
  cd Image-Process-API
```

Create a virtual environment
```bash
  python -m venv venv
```
  # On Windows
```bash
  venv\Scripts\activate
```
  # On macOS/Linux
```bash
  source venv/bin/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Initialize database migration
```bash
  flask db init
```
```bash
  flask db migrate -m "Initial migration"
```
```bash
  flask db upgrade
```

Start your Redis server and PostgreSQL

Start Celery worker
  #On Windows
```bash
  celery -A server.celery worker --pool=solo --loglevel=info
```

Start flask application
``` 
  flask Run
```
## Documentation

[Low level Description and Postman collection](https://docs.google.com/document/d/1HxIX4x20ux83OvdoUCrqhxCfidefrRHtxlxsNsYOxaI/edit?usp=sharing)
