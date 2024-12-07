from ..core import EventType, JSON


def encode_string(data: str) -> bytes:
    return data.encode("utf-8")


def encode_num_to_four_bytes(num: int) -> bytes:
    return num.to_bytes(4, byteorder="big")


def encode_json(data):
    string = JSON.stringify(data)
    return encode_string(string)


def combine_buffers(*args: bytes) -> bytes:
    return b"".join(args)


def encode_ws_message(header_string, data):
    header_buffer = encode_string(header_string)
    return combine_buffers(header_buffer, data)


def decode_file_transfer_message(message: bytes) -> dict:
    # Bytes 2-38 are the environmentId, hence we start parsing after that
    execution_id = message[38:74].decode("utf-8")
    file_id = message[74:110].decode("utf-8")

    file_contents = message[110:]

    data = {
        "type": EventType.ServerToSdk.FILE_TRANSFER,
        "executionId": execution_id,
        "fileId": file_id,
        "fileContents": file_contents,
    }

    return data


def decode_json_message(message: bytes) -> dict:
    jsonData = message[38:].decode("utf-8")
    return JSON.parse(jsonData)
