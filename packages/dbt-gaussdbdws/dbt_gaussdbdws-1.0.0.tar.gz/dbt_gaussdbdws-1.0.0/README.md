<p align="center">
  <img src="https://raw.githubusercontent.com/dbt-labs/dbt/ec7dee39f793aa4f7dd3dae37282cc87664813e4/etc/dbt-logo-full.svg" alt="dbt logo" width="500"/>
</p>
<p align="center">
  <a href="https://github.com/dbt-labs/dbt-core/actions/workflows/main.yml">
    <img src="https://github.com/dbt-labs/dbt-core/actions/workflows/main.yml/badge.svg?event=push" alt="CI Badge"/>
  </a>
</p>

**[dbt](https://www.getdbt.com/)** enables data analysts and engineers to transform their data using the same practices that software engineers use to build applications.

dbt is the T in ELT. Organize, cleanse, denormalize, filter, rename, and pre-aggregate the raw data in your warehouse so that it's ready for analysis.

## dbt-gaussdbdws

The `dbt-gaussdbdws` package contains all of the code enabling dbt to work with huawei gaussdb or gaussdb(dws) database. For
more information on using dbt with dbt-gaussdbdws, consult [the docs](https://docs.getdbt.com/docs/profile-gaussdbdws).

## Getting started

- [Install dbt](https://docs.getdbt.com/docs/installation)
- Read the [introduction](https://docs.getdbt.com/docs/introduction/) and [viewpoint](https://docs.getdbt.com/docs/about/viewpoint/)

### `psycopg2-binary` vs. `psycopg2`

By default, `dbt-gaussdbdws` installs `psycopg2-binary`. This is great for development, and even testing, as it does not require any OS dependencies; it's a pre-built wheel. However, building `psycopg2` from source will grant performance improvements that are desired in a production environment. In order to install `psycopg2`, use the following steps:

```bash
if [[ $(pip show psycopg2-binary) ]]; then
    PSYCOPG2_VERSION=$(pip show psycopg2-binary | grep Version | cut -d " " -f 2)
    pip uninstall -y psycopg2-binary
    pip install psycopg2==$PSYCOPG2_VERSION
fi
```

This ensures the version of `psycopg2` will match that of `psycopg2-binary`.
**Note:** The native PostgreSQL driver cannot connect to GaussDB directly. If you need to use the PostgreSQL native driver, you must set `password_encryption_type: 1` (compatibility mode supporting both MD5 and SHA256) to enable the PostgreSQL native driver.

###  `GaussDB psycopg2`
It is recommended to use the following approach: GaussDB uses SHA256 as the default encryption method for user passwords, while the PostgreSQL native driver defaults to MD5 for password encryption. Follow the steps below to prepare the required drivers and dependencies and load the driver.

1.You can obtain the required package from the release bundle. The package is named as:
`GaussDB-Kernel_<database_version>_<OS_version>_64bit_Python.tar.gz`.
- psycopg2：Contains the psycopg2 library files.
- lib：Contains the psycopg2 library files.

2.Follow the steps below to load the driver:
```bash
# Extract the driver package, for example: GaussDB-Kernel_xxx.x.x_Hce_64bit_Python.tar.gz
tar -zxvf GaussDB-Kernel_xxx.x.x_Hce_64bit_Python.tar.gz

# Uninstall psycopg2-binary
pip uninstall -y psycopg2-binary

# Install psycopg2 by copying it to the site-packages directory of the Python installation using the root user
cp psycopg2 $(python3 -c 'import site; print(site.getsitepackages()[0])') -r

# Grant permissions
chmod 755 $(python3 -c 'import site; print(site.getsitepackages()[0])')/psycopg2 -R

# Verify the existence of the psycopg2 directory
ls -ltr $(python3 -c 'import site; print(site.getsitepackages()[0])') | grep psycopg2

# To add the psycopg2 directory to the $PYTHONPATH environment variable and make it effective
export PYTHONPATH=$(python3 -c 'import site; print(site.getsitepackages()[0])'):$PYTHONPATH

# For non-database users, you need to add the extracted lib directory to the LD_LIBRARY_PATH environment variable
export LD_LIBRARY_PATH=/root/lib:$LD_LIBRARY_PATH

# To verify that the configuration is correct and there are no errors
(.venv) [root@ecs-euleros-dev ~]# python3
Python 3.9.9 (main, Jun 19 2024, 02:50:21)
[GCC 10.3.1] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import psycopg2

```


## Contribute

See `CONTRIBUTING.md` for a detailed overview of contributing a code change to this adapter.

## Join the dbt Community

- Be part of the conversation in the [dbt Community Slack](http://community.getdbt.com/)
- Read more on the [dbt Community Discourse](https://discourse.getdbt.com)

## Reporting bugs and contributing code

- Want to report a bug or request a feature? Let us know on [Slack](http://community.getdbt.com/), or open [an issue](https://github.com/dbt-labs/dbt-gaussdbdws/issues/new)
- Want to help us build dbt? Check out the [Contributing Guide](https://github.com/dbt-labs/dbt-gaussdbdws/blob/main/CONTRIBUTING.md)

## Code of Conduct

Everyone interacting in the dbt project's codebases, issue trackers, chat rooms, and mailing lists is expected to follow the [dbt Code of Conduct](https://community.getdbt.com/code-of-conduct).
