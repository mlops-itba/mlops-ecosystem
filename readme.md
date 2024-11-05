# Instalación de env conda
```bash
conda create -n mlops-env python=3.12
conda activate mlops-env
pip install mlflow
conda install -c conda-forge psycopg2
```


# Definición de variables de entorno
Desde carpeta del repo

```bash
# Seteo de variables
export REPO_FOLDER=${PWD}
set -o allexport && source .env && set +o allexport

# Verificarlo
echo $postgres_data_folder
```

# PSQL DB

### Bajar imagen
```bash
docker pull postgres
```

### Correr imagen
```bash
docker run -d \
    --name mlops-postgres \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v $postgres_data_folder:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres
```

### Verificar funcionamiento, y manejo del contenedor
```bash
docker ps

docker ps -a

docker exec -it mlops-postgres /bin/bash

root@08487b094f8a$  psql -U postgres

postgres   exit

root@08487b094f8a$  exit

docker kill mlops-postgres

docker container rm mlops-postgres
```

Si tiene instalado psql:
```bash
export PGPASSWORD=$POSTGRES_PASSWORD 
psql -U postgres -h localhost -p 5432
```

### Create MLFLOW DB

```sql
CREATE DATABASE mlflow_db;
CREATE USER mlflow_user WITH ENCRYPTED PASSWORD 'mlflow';
GRANT ALL PRIVILEGES ON DATABASE mlflow_db TO mlflow_user;
```


# Mlflow server


```bash
# desde la carpeta del proyecto

mlflow server --backend-store-uri postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST/$MLFLOW_POSTGRES_DB --default-artifact-root $MLFLOW_ARTIFACTS_PATH -h 0.0.0.0 -p 8002
```
Abrir browser en http://localhost:8002/

# Airbyte

### Tutorial
https://docs.airbyte.com/using-airbyte/getting-started/oss-quickstart

### Esto quedo obsoleto?
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
IP localhost no funciona, usar ip local (192.x.x.x)


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

```sql
CREATE DATABASE mlops;
CREATE USER "jganzaba@itba.edu.ar" WITH ENCRYPTED PASSWORD 'airbyte';
GRANT ALL PRIVILEGES ON DATABASE mlops TO "jganzaba@itba.edu.ar";
GRANT ALL ON SCHEMA public TO "jganzaba@itba.edu.ar";
GRANT USAGE ON SCHEMA public TO "jganzaba@itba.edu.ar";
ALTER DATABASE mlops OWNER TO "jganzaba@itba.edu.ar";

\du 
```

# dbT
### Crear entorno

```bash
conda create -n mlops-dbt python=3.9
conda activate mlops-dbt
pip install dbt-postgres

dbt --version
```

Con el siguiente comando se crea el repo y se configura la db
```bash
dbt init db_postgres
cd db_postgres
```

Verificar archivo de configuración `~/.dbt/profiles.yml` 


```yaml
dbt_elt:
  outputs:
    dev:
      type: postgres
      threads: 1
      host: localhost
      port: 5432
      user: postgres
      pass: mysecretpassword
      dbname: mlops
      schema: target
```

### Testear conexión y correr
```bash
dbt debug

dbt run
```



# Mongo (Opcional)

### Desde cloud gratis
https://cloud.mongodb.com/v2/653ac4dcf923b06a3d61bfcc#/overview

### Desde docker
```bash

docker pull mongo

docker run \
    --name mlops-mongo \
    -v $mongo_data_folder:/data/db \
    -p 27017:27017 \
    mongo

docker exec -it mlops-mongo /bin/bash

pip install pymongo

```

Se puede testear desde `source/test_mongo.py`

```bash
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