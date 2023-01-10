# chatbot-api
The project represents a Data API used by data scientists to further improve an existing chatbot. Requests are sent by a
background job which pushes the customer data and consent via HTTP.


## How to run
To run this project, you need to have `Docker` and `Compose` installed.

The docker-compose commands are already abstracted through Makefile rules for simplicity. Run the following commands to:

1. Build the app: `make build-app`
2. Run the app: `make run-app`
3. Shut down the app: `make kill-app`

Now the Data API app should be running by default at `http://0.0.0.0:80`, together with a PostgreSQL database that it is
connected to. The app and the database each run in their own container.

The default database's settings can be found in `.env`. Feel free to change those according to your needs by having your
own `.env` file locally.

To remove the persistent volume created by the database container, and hence delete the database contents, run:
- Find db volume name: `docker volume ls`
- Delete db volume: `docker volume rm <volume_name>`


## Development

To further develop the project, you should create a virtual environment with virtualenv or anaconda, and then
install both the project requirements and the development requirements inside of it:

- Create environment: `conda create <env_name> python=3.9`
- Activate environment: `conda activate <env_name>`
- Install requirements : `pip install -r requirements.txt`
- Install development requirements: `pip install -r requirements-dev.txt`

You can find additional `Makefile` rules to help with checking the code quality in `makefiles/Makefile.python`.


## Manual testing

To manually test the API, you can go to `http://0.0.0.0:80/docs` while the app is running. It will display a default UI
to manually test each endpoint by inputting valid data. The UI also displays the status codes and responses.

To check the content of the database after each request, you should:
1. Enter the db container: `docker exec -it postgres-db bash`.
2. Connect to PostgreSQL as user `postgres`: `psql -U postgres`
3. Get access to the `chatbotapi` db: `\c chatbotapi`
4. Retrieve the records of interest after each request: e.g. `SELECT * from user_inputs;`

<mark> Sometimes, especially after deleting the database persistent volume, there might be an error stating that the
relation `user_inputs` does not exist. In this case: kill, re-build and re-start the app. </mark>


## Unit testing

To run the unit tests in the development virtual environment, run the command: `python -m pytest tests`

## TODO
- Add docstrings & comments
