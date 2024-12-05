"""
ML Server Starter

This script starts a machine learning server based on the configuration provided
in a YAML file. It dynamically loads a Flask application from the specified entry
point and launches a web server, supporting different types such as Gunicorn.

Usage:
    python server.py --config-file <path_to_config>

Options:
    --config-file (str): Path to the configuration YAML file.
"""
import click
import os
from gru.ml_serving.web_frameworks.flask_adapter import FlaskAdapter
from gru.ml_serving.servers.gunicorn import GunicornServer
from .ml_serving_config_reader import MLServingConfigReader

GUNICORN_TYPE = 'gunicorn'

@click.command()
@click.option('--config-file', type=click.Path(exists=True), help='Path to the config YAML file')
def serve(config_file):
    """
    Start the server based on the configuration provided in the YAML file.

    Parameters:
    - config_file (str): Path to the config YAML file.
    """
    try:
        config = MLServingConfigReader(config_file)
        for key, value in config.get_config('env_vars').items():
            click.echo(f'Setting environment variable: {key}={value}')
            os.environ[key] = value

        application = load_application(config)
        start_web_server(config, application)

    except Exception as e:
        click.echo(f"Error: {str(e)}")

def load_application(config: MLServingConfigReader):
    """
    Load the application module dynamically.

    Parameters:
    - entry_point (str): Path to the entry point module.

    Returns:
    - WebServerAdapter: The application instance.
    """
    try:
        serving_layer = config.get_config('serving_layer')
        if serving_layer == 'flask':
            framework_adapter = FlaskAdapter(config)
        else:
            raise Exception(f"Serving layer {serving_layer} is not supported yet")

        print(f"Loading {serving_layer} application from entrypoint: {config.get_config('entrypoint')}")
        return framework_adapter.load_application()

    except Exception as e:
        raise Exception(f"Error loading {serving_layer} application: {str(e)}")

def start_web_server(config: MLServingConfigReader, application):
    """
    Start the web server based on the specified configuration.

    Parameters:
    - config (MLServingConfigReader): The server configuration reader.
    - application: The Flask application instance.
    """
    try:
        webserver_config = config.get_config('webserver')
        type = webserver_config.get('type')
        config = webserver_config.get('config')
        if type == GUNICORN_TYPE:
            server = GunicornServer(application, config)
        else:
            raise Exception(f"The web server of type '{webserver_config.get('type')}' is not supported yet.")

        print(f"String webserver {type} with configuration: {config}")
        server.start()

    except Exception as e:
        raise RuntimeError(f"Error starting web server: {str(e)}")

if __name__ == '__main__':
    serve()
