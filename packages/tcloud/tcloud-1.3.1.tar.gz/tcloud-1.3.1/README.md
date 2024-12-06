# Tobiko Cloud CLI

## Configuration

The configuration for the `tcloud` CLI tool should be stored either in the `$HOME/.tcloud/tcloud.yml` file or in the `tcloud.yml` file located in the project folder.

Below is an example of `tcloud.yml` configuration:
```yaml
projects:
    <Project name>:
        url: <The project URL>
        token: <The access token>
        gateway: <The name of the SQLMesh gateway to use with this project>
        extras: <Optional - Any extras that should be installed with sqlmesh-enterprise>
        pip_executable: <Optional - The path to the pip executable to use. Ex: `uv pip` or `pip3`. Must install packages to the python environment running the tcloud command>
default_project: <The name of a project to use by default>
```

Alternatively, the target project can be configured using the `TCLOUD_URL`, `TCLOUD_TOKEN`, `TCLOUD_GATEWAY`, `TCLOUD_EXTRAS`, and `TCLOUD_PIP_EXECUTABLE` environment variables.

## Running self-hosted executors

The `tcloud` CLI tool allows you to run SQLMesh executor processes which can perform cadence model evaluations and plan applications outside the Tobiko Cloud environment.

To launch an executor process responsible for runs: `tcloud executor run`.

To launch an executor process responsible for plan applications: `tcloud executor plan`.

Any number of executors, of either type, can be launched as needed. The actual number should be determined by the specific requirements of a given project. For instance, a project with numerous users frequently applying changes concurrently may benefit from a higher number of `plan` executors.

The gateway / connection configuration can be provided using environment variables as described in the [documentation](https://sqlmesh.readthedocs.io/en/latest/guides/configuration/?h=environment+varia#overrides).
