# Development notes

## Developing locally

1. Clone [aws-mwaa-local-runner](https://github.com/aws/aws-mwaa-local-runner) and follow the installation directions. 

### Provider

To install the airflow-mcd provider to your local MWAA instance, follow these steps.

2. Run `make package` from this repo to build the wheel.
3. Copy the built wheel into `aws-mwaa-local-runner/requirements/` directory:
```
cp airflow-mcd/dist/airflow_mcd-0.1.7.dev1+g6f94b5f.d20230725-py3-none-any.whl aws-mwaa-local-runner/requirements/
```
4. Add this line to `aws-mwaa-local-runner/requirements/requirements.txt`, updating the wheel's name:
```
airflow_mcd @ file:///usr/local/airflow/requirements/airflow_mcd-0.1.7.dev[REPLACE_ME]-py3-none-any.whl
```

_Note: you will want to replace '+' with '%2B'_ in the file name or else Airflow will complain.

5. Run Airflow. For instance, `./mwaa-local-env start`. Repeat steps 2-4 as needed.

_Note: I found that sometimes it is necessary to remove the Docker container after updating the wheel file. I suspect the packages are cached and not always re-installed. You can do this with `docker rm aws-mwaa-local-runner-2_5-local-runner-1`._

6. Update README :)

### Operators

Developing operators locally (e.g. without publishing) is a bit clunky, but hopefully this guide will be a good v0 starting point:

2. Make any necessary changes to the `airflow_mcd`.
3. Copy the package into the `dags` directory from step 1. For instance, `cp -r ~/Dev/airflow-mcd/airflow_mcd/ dags/airflow_mcd/`.
4. Replace (or append) requirements in the `dags` directory in step 1.

   At a minimum this should include the dependencies from `airflow-mcd/requirements.txt`.
5. Run Airflow. For instance, `./mwaa-local-env start`. Repeat steps 2-4 as needed.
6. Update README :)

Pro Tip - To point the `SessionHook` to our DEV endpoint you can add https://api.dev.getmontecarlo.com/graphql 
as the `Host` in your connection.

See the README.md for details on existing operator and hook usage.
