# envappconfig

envappconfig is intended to provide simple configuration via environment variables, in the same spirit as argparse, which can be useful when developing and deploying [12-factor apps](https://12factor.net).

Features:
* Autogenerates usage output if an environment variable is missing
* Default settings for missing environment variables
* Functions that transform the environment variable string to the value type you need
* Environment variable prefixes

## Basic example

```python
from envappconfig import EnvAppConfig

env = EnvAppConfig(description='Amazing app')
env.add_env('port', default=1234, transform=int, help='The listen port')
env.add_env('mirror', help='The URL to mirror')
config = env.configure()

# Returns PORT from os.environ transformed to an int,
# or 1234 if PORT does not exist.
config.port

# Returns MIRROR from os.environ,
# or displays usage at env.configure()
# if MIRROR does not exist, then exits.
config.mirror
```

## Adding a prefix

If all the environment variables for the app have the same prefix, it can be specified with the `prefix` parameter.

```python
from envappconfig import EnvAppConfig

env = EnvAppConfig(prefix='MYAPP', description='Amazing app')
env.add_env('port', default=1234, transform=int, help='The listen port')
env.add_env('mirror', help='The URL to mirror')
config = env.configure()

# Returns MYAPP_PORT from os.environ transformed to an int,
# or 1234 if MYAPP_PORT does not exist.
config.port

# Returns MYAPP_MIRROR from os.environ,
# or displays usage at env.configure()
# if MYAPP_MIRROR does not exist, then exits.
config.mirror
```

## Custom transforms

The `transform` parameter can be used to specify normal transforms, like `int` or `float` (the default is `str`), but it can also take custom transform functions.  The transform function must take a single parameter, which will be filled in with the string value from the environment variable.

```python
env = EnvAppConfig(description='Amazing app')

# Double the timeout specified in the TIMEOUT environment variable,
# or default to 60.
env.add_env('timeout', default=60, transform=lambda x: int(x) * 2, help='Timeout in seconds')
...
```

## Adding more config values

Additional config values can be added to an existing namespace, which can be helpful when there's a config value that needs to be calculated based on other config values.

```python
from envappconfig import EnvAppConfig

env = EnvAppConfig(description='Amazing app')
env.add_env('bind', help='IP address to bind to')
env.add_env('port', default=1234, transform=int, help='The listen port')
config = env.configure()
config.listen = f'{config.bind}:{config.port}'

# Returns the combined bind:port string.
config.listen
```

## Forcing usage display

The environment variable usage output for an app can be forced by defining the `ENVAPPCONFIG_SHOW_USAGE` environment variable to any value.  This is basically like `--help` for apps that take command line parameters.  Forcing usage display can be useful when you've got a pre-built container for an app that uses envappconfig, and you need to see all the environment variable options.  For example:

```sh
docker run -it --rm -e ENVAPPCONFIG_SHOW_USAGE=1 amazing:latest
```

or in Kubernetes:

```yaml
env:
  - name: ENVAPPCONFIG_SHOW_USAGE
    value: "1"
```

## Command Line

There are a couple options for using envappconfig at the command line (eg. when testing).

### Prefix

If you've only got a couple environment variables to set, just put them before the command:

```sh
PORT=9999 NAME=foo python3 script_using_envappconfig.py
```

### dotenv

If you have more environment variables to set, consider using `dotenv`.  First put your environment variables in a file named `.env`:

```sh
PORT=9999
NAME=foo
```

Then call `dotenv` as follows, which will load up the variables from `.env` for this command:

```sh
dotenv run -- python3 script_using_envappconfig.py
```

You can install the `dotenv` command line tool with:

```sh
python3 -m pip install "python-dotenv[cli]"
```
