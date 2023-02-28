# RESTful API for a Dog Adoption Web app (in progress)

### Live OpenAPI docs : <ins>[Furry Forever API](http://64.227.129.68/docs)<ins>

This has been hosted on a Ubuntu VM for now which utilizes 4 gunicorn worker threads and sits behind nginx which is set to reload with system restart.
<br><br>

## Getting Started for local deployment
<br>
### Clone the repo

```bash
mkdir furryforever // use any name 
cd furryforever 
git clone https://github.com/42eggs/furryforever-api
```
<br>
### Create virtual environment and activate

Use `python3` if `python` is unrecognized. 
You need **python v3** to run this.

For **Windows**:

```bash
python -m venv venv  //creates a folder named venv
venv\Scripts\activate
```

For **Linux/Unix**:

```bash
python -m venv venv  //creates a folder named venv
source venv/bin/activate
```
<br>
### Install the requirements and set up environment variables

```bash
cd furryforever-api
pip install -r requirements.txt
```
Rename `.env-example` to `.env` and fill up the given values
<br>
### Apply DB migrations and run tests


```bash
alembic upgrade head
pytest -s -v
```
<br>


### Launch the app
This will run the app on the default ASGI server (uvicorn)

```bash
uvicorn app.main:app --reload
```

This will launch the app on `http://localhost:8000/` unless mentioned otherwise.
<br><br><br>



## Notes:

- With each push or PR on the **main** repo, `test-deploy.yml` will run which is a very basic CI/CD workflow just to make sure all tests pass and everything gets updated on the ubuntu VM.

- Future plans include more test coverage, dockerizing everything and start building a frontend.
