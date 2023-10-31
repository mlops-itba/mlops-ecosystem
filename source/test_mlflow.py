# %%
%env MLFLOW_TRACKING_URI=http://localhost:8000
# %%
import mlflow
import os
import tempfile
# %%
mlflow.set_experiment('test_ecosystem')
# %%
with mlflow.start_run():
    mlflow.log_param('MLFLOW_TRACKING_URI', os.getenv('MLFLOW_TRACKING_URI'))
    with tempfile.NamedTemporaryFile('w+t', suffix='.txt') as f:
        f.writelines('Hola que tal')
        f.flush()
        mlflow.log_artifact(f.name, 'files_folder')
# %%

        print(f.name)
# %%
