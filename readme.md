# PSQL DB
```bash
export postgres_data_folder=/Users/julian/Documents/mlops-itba/mlops-ecosystem/dbs/data/postgres
export mongo_data_folder=/Users/julian/Documents/mlops-itba/mlops-ecosystem/dbs/data/mongo
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=mysecretpassword
export POSTGRES_HOST=localhost:5432
export MLFLOW_POSTGRES_DB=mlflow_db
export MLFLOW_ARTIFACTS_PATH=/Users/julian/Documents/mlops-itba/mlops-ecosystem/mlflow_data
```

```bash
docker pull postgres
```

```bash
docker run -d \
    --name mlops-postgres \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v $postgres_data_folder:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres

docker ps

docker ps -a

docker exec -it mlops-postgres /bin/bash

root@08487b094f8a:/#  psql -U postgres

root@08487b094f8a:/#  exit

docker kill mlops-postgres

docker container rm mlops-postgres

postgres=# exit

psql -U postgres -h localhost -p 5432
```

# Create MLFLOW DB

```sql
CREATE DATABASE mlflow_db;
CREATE USER mlflow_user WITH ENCRYPTED PASSWORD 'mlflow';
GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO mlflow_user;
```


# Mlflow server

```bash
mlflow server --backend-store-uri postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST/$MLFLOW_POSTGRES_DB --default-artifact-root $MLFLOW_ARTIFACTS_PATH -h 0.0.0.0 -p 8001
```
Abrir browser en http://localhost:8001/

# Airbyte
```bash
# clone Airbyte from GitHub
git clone --depth=1 https://github.com/airbytehq/airbyte.git

# switch into Airbyte directory
cd airbyte

# start Airbyte
./run-ab-platform.sh
```
Abrir browser en http://localhost:8000/

username: `airbyte`
password: `password`

## Creación de source (csvs)
https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/peliculas_0.csv
https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/usuarios_0.csv
https://raw.githubusercontent.com/mlops-itba/Datos-RS/main/data/scores_0.csv

## Creación de destination (psql)

```bash
psql -U postgres -h localhost -p 5432
```

```sql
CREATE DATABASE mlops;
CREATE USER airbyte WITH ENCRYPTED PASSWORD 'airbyte';
GRANT ALL PRIVILEGES ON DATABASE mlops TO airbyte;
GRANT ALL ON SCHEMA public TO airbyte;
GRANT USAGE ON SCHEMA public TO airbyte;
ALTER DATABASE mlops OWNER TO airbyte;
```

# Mongo

```bash
docker pull mongo

docker run \
    --name mlops-mongo \
    -v $mongo_data_folder:/data/db \
    -p 27017:27017 \
    mongo

docker exec -it mlops-mongo /bin/bash
```

```
mongo
test> show dbs
test> use mlops
test> db.createUser({
    user: "airbyte",
    pwd: "airbyte",
    roles: [ { role: "userAdmin", db: "mlops" } ]
})

test> use admin
test> db.createUser(
  {
    user: "admin",
    pwd: "admin",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
  }
)
```
