import traceback
import logging
import json
import time
import os
import uuid

import grpc

from achatbot.common.factory import EngineClass
from achatbot.common.interface import IAudioStream
from achatbot.modules.speech.audio_stream import AudioStreamEnvInit
from achatbot.modules.speech.player import PlayerEnvInit
from achatbot.modules.speech.tts import TTSEnvInit
from achatbot.common.grpc.idl.tts_pb2 import (
    LoadModelRequest, LoadModelResponse,
    SynthesizeRequest, SynthesizeResponse,
)
from achatbot.common.grpc.idl.tts_pb2_grpc import TTSStub
from achatbot.common.grpc.interceptors.authentication_client import add_authentication
from achatbot.common.logger import Logger
from achatbot.common.types import SessionCtx
from achatbot.common.session import Session

from dotenv import load_dotenv
load_dotenv(override=True)

Logger.init(
    os.getenv("LOG_LEVEL", "debug").upper(),
    app_name="chat-bot-tts-client",
    is_file=False,
    is_console=True)


def load_model(channel):
    tag = os.getenv("TTS_TAG", "tts_edge")
    is_reload = bool(os.getenv("IS_RELOAD", None))
    kwargs = TTSEnvInit.map_config_func[tag]()
    tts_stub = TTSStub(channel)
    request = LoadModelRequest(tts_tag=tag, is_reload=is_reload, json_kwargs=json.dumps(kwargs))
    logging.debug(request)
    response = tts_stub.LoadModel(request)
    logging.debug(response)


def synthesize_us(channel):
    tts_stub = TTSStub(channel)
    request_data = SynthesizeRequest(tts_text="你好，我是机器人")
    response_iterator = tts_stub.SynthesizeUS(request_data)
    for response in response_iterator:
        yield response.tts_audio


logging.basicConfig(level=logging.DEBUG)

"""
TTS_TAG=tts_edge IS_RELOAD=1 python -m achatbot.cmd.grpc.speaker.client
TTS_TAG=tts_g IS_RELOAD=1 python -m achatbot.cmd.grpc.speaker.client
TTS_TAG=tts_coqui IS_RELOAD=1 python -m achatbot.cmd.grpc.speaker.client
TTS_TAG=tts_chat IS_RELOAD=1 python -m achatbot.cmd.grpc.speaker.client
TTS_TAG=tts_cosy_voice IS_RELOAD=1 python -m achatbot.cmd.grpc.speaker.client
"""
if __name__ == "__main__":
    try:
        client_id = str(uuid.uuid4())
        session = Session(**SessionCtx(client_id).__dict__)
        # todo: up to the rpc gateway to auth
        token = "oligei-tts"
        authentication = add_authentication('authorization', token)
        port = os.getenv('PORT', "50052")
        channel = grpc.insecure_channel(f'localhost:{port}')
        channel = grpc.intercept_channel(channel, authentication)

        load_model(channel)
        tts_audio_iter = synthesize_us(channel)

        audio_out_stream: IAudioStream | EngineClass = AudioStreamEnvInit.initAudioOutStreamEngine()
        player = PlayerEnvInit.initPlayerEngine()
        player.set_out_stream(audio_out_stream)
        player.open()
        player.start(session)
        for tts_audio in tts_audio_iter:
            logging.debug(f"play tts_chunk len:{len(tts_audio)}")
            session.ctx.state["tts_chunk"] = tts_audio
            player.play_audio(session)
        player.stop(session)
    except grpc.RpcError as e:
        logging.error(f"grpc.RpcError: {e}")
    except Exception as e:
        tb_str = traceback.format_exc()
        logging.error(f"Exception: {e}; traceback: {tb_str}")
    finally:
        channel and channel.close()
        player and player.close()
