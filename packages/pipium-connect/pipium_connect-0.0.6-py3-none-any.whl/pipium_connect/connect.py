from pipium_connect.connect_options_model import ConnectOptions
from pipium_connect.input_model import Input
from pipium_connect.model_model import Models
from pipium_connect.observer_model import Observer
from pipium_connect.output_model import Output
from pipium_connect.previous_value_model import PreviousValue
from typing import Dict
import asyncio
import requests
import signal
import socketio
import sys
import traceback


sio = socketio.Client()


def connect(
    api_key: str,
    models: Models,
    options: ConnectOptions = ConnectOptions(),
):
    """Connect to models Pipium.

    Args:
        api_key (str): API key for the user the models will be added to. Create one in the [Pipium settings](https://pipium.com/settings).
        models (Models): A dictionary of `Model` objects, indexed by their ID.
    """

    server_url = get_server_url(options)

    log(f"Connecting to Pipium")

    sio.connect(
        f"{server_url}?api-key={api_key}",
        transports=["websocket"],
    )

    @sio.on("pp-connect")
    def handle_connected():
        payload = {
            "source": "user",
            "models": [
                {
                    "id": id,
                    **recursively_remove_none_from_dict(model.asdict()),
                }
                for id, model in models.items()
            ],
        }

        sio.emit("pp-init", payload)

    @sio.on("pp-disconnect")
    def handle_disconnected():
        log("Disconnected")

    @sio.on("pp-run")
    def handle_run(connection_input: dict):
        input = connection_input_to_input(connection_input)

        id = input.id
        user_id = input.user_id
        pipe_id = input.pipe_id
        layer_id = input.layer_id
        model_id = input.model_id
        result_id = input.result_id

        def emit_error(message: str):
            payload = {
                "id": id,
                "user_id": user_id,
                "pipe_id": pipe_id,
                "layer_id": layer_id,
                "model_id": model_id,
                "result_id": result_id,
                "message": create_error_message(message),
            }
            log("Emitting error")
            sio.emit("pp-error", payload)

        model = models.get(input.local_model_id)

        if not model:
            error = f"Model {model_id} not found"
            log(error)
            emit_error(error)

        def emit_start():
            start = {
                "id": id,
                "user_id": user_id,
                "pipe_id": pipe_id,
                "model_id": model_id,
                "layer_id": layer_id,
                "result_id": result_id,
            }
            log("Emitting start")
            sio.emit("pp-start", start)

        def emit_result(value: Output):
            payload = {
                "value": value,
                "id": id,
                "user_id": user_id,
                "pipe_id": pipe_id,
                "layer_id": layer_id,
                "model_id": model_id,
                "result_id": result_id,
                "mime_type": model.types.output,
            }
            log("Emitting result")
            sio.emit("pp-result", payload)

        def emit_complete():
            payload = {
                "id": id,
                "user_id": user_id,
                "pipe_id": pipe_id,
                "layer_id": layer_id,
                "model_id": model_id,
                "result_id": result_id,
            }
            log("Emitting complete")
            sio.emit("pp-complete", payload)

        if not model:
            log(f"Model {model_id} not found")
            emit_complete()
            return

        def create_error_message(native_error_message: str) -> str:
            return f'The model threw an error "{native_error_message}"'

        def on_error(error: Exception):
            native_error_message = get_error_message(error)
            error_message = create_error_message(native_error_message)
            log(error_message)
            emit_error(native_error_message)

        if not model.run_sync and not model.run_async:
            log("No run function found")
            emit_complete()
            return

        emit_start()

        if model.run_sync:
            log("Starting sync run")
            try:
                output = model.run_sync(input)
                values = output if isinstance(output, list) else [output]
                for value in values:
                    emit_result(value)
                emit_complete()
            except Exception as error:
                on_error(error)
                traceback.print_exc()
                return

        if model.run_async:
            log("Starting async run")
            try:
                model.run_async(
                    input,
                    Observer(
                        next=emit_result,
                        error=on_error,
                        complete=emit_complete,
                    ),
                )
            except Exception as error:
                on_error(error)
                traceback.print_exc()
                return

    @sio.on("pp-log")
    def handle_log(message: str):
        log(message)

    @sio.on("pp-log-error")
    def handle_log(message: str):
        log(message)

    @sio.on("exception")
    def handle_exception(message: str):
        log(message)

    asyncio.run(exit_on_disconnected())


def log(message: str):
    print(f"[Pipium] {message}")
    sys.stdout.flush()


def get_error_message(error) -> str:
    if isinstance(error, Exception) or isinstance(error, str):
        return str(error)

    return "Unknown error"


def connection_input_to_input(
    connection_input: dict,
):
    previous_values = connection_input.pop("previous_values")

    return Input(
        **connection_input,
        text=try_string_decode(connection_input["binary"]),
        previous_values=[
            connection_previous_value_to_previous_value(previous_value)
            for previous_value in previous_values
        ],
    )


def get_server_url(options: ConnectOptions):
    if options.server_url:
        return options.server_url

    return "https://server-production-00001-pq8-vauf4uyfmq-ey.a.run.app"


def try_string_decode(binary):
    try:
        return binary.decode("utf-8")
    except UnicodeDecodeError:
        return ""


def connection_previous_value_to_previous_value(connection_previous_value: dict):
    return PreviousValue(
        **connection_previous_value,
        binary=lambda: fetch_binary(connection_previous_value["uri"]),
        json=lambda: fetch_json(connection_previous_value["uri"]),
        text=lambda: fetch_text(connection_previous_value["uri"]),
    )


def recursively_remove_none_from_dict(dictionary):
    if not isinstance(dictionary, Dict):
        return dictionary

    return {
        key: recursively_remove_none_from_dict(value)
        for key, value in dictionary.items()
        if value is not None
    }


def fetch_binary(uri):
    response = requests.get(uri)
    return response.content


def fetch_json(uri):
    response = requests.get(uri)
    return response.json()


def fetch_text(uri):
    response = requests.get(uri)
    return response.text


async def exit_on_disconnected():
    # Taken from sio.wait()
    if sio.eio.state != "connected":
        exit()
        return

    await asyncio.sleep(1)
    await exit_on_disconnected()


def exit():
    sio.disconnect()
    sys.exit(0)


def signal_exit_handler(_, __):
    exit()


for sig in [signal.SIGINT, signal.SIGTERM]:
    signal.signal(sig, signal_exit_handler)
