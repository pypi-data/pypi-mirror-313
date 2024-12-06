from dotenv import load_dotenv  # type: ignore
import asyncio
import os
import json
import websockets  # type: ignore
import numpy as np  # type: ignore
import soundfile as sf  # type: ignore
import ssl
import onnxruntime as ort  # type: ignore
import pyttsx3  # type: ignore
from typing import Optional
import jax #type: ignore
import jax.numpy as jnp #type: ignore
from flax import linen as nn #type: ignore
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


# Get configuration from environment
fastspeech_path = os.getenv("FASTSPEECH_MODEL_PATH")
hifigan_path = os.getenv("HIFIGAN_MODEL_PATH")
sample_rate = int(os.getenv("CAPIBARA_TTS_SAMPLE_RATE", 22050))
host = os.getenv("CAPIBARA_TTS_HOST", "localhost")
port = int(os.getenv("CAPIBARA_TTS_PORT", 8765))
cert_file = os.getenv("CAPIBARA_TTS_CERT_FILE")
key_file = os.getenv("CAPIBARA_TTS_KEY_FILE")

ssl_context = None
if cert_file and key_file:
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=cert_file, keyfile=key_file)

# Client connections
connected_clients = set()


class CapibaraTextToSpeech:
    def __init__(self, fastspeech_model_path: Optional[str], hifigan_model_path: Optional[str], sample_rate=22050):
        self.sample_rate = sample_rate

        # Validate model paths
        if not fastspeech_model_path or not hifigan_model_path:
            raise ValueError("FastSpeech and HiFi-GAN model paths must be provided.")

        # Load ONNX models
        try:
            self.fastspeech_session = ort.InferenceSession(fastspeech_model_path)
            self.hifigan_session = ort.InferenceSession(hifigan_model_path)
        except Exception as e:
            raise RuntimeError(f"Error loading ONNX models: {e}")

    def text_to_spectrogram(self, text: str) -> np.ndarray:
        if not self.fastspeech_session:
            raise RuntimeError("FastSpeech model is not loaded.")
        input_text = np.array([text], dtype=object)
        inputs = {self.fastspeech_session.get_inputs()[0].name: input_text}
        return np.clip(self.fastspeech_session.run(None, inputs)[0], -4.0, 4.0)

    def spectrogram_to_audio(self, spectrogram: np.ndarray) -> np.ndarray:
        if not self.hifigan_session:
            raise RuntimeError("HiFi-GAN model is not loaded.")
        inputs = {self.hifigan_session.get_inputs()[0].name: spectrogram}
        return self.hifigan_session.run(None, inputs)[0]

    async def handle_connection(self, websocket, path):
        connected_clients.add(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    user_text = data.get("text")

                    if not user_text:
                        await websocket.send(json.dumps({"error": "No valid text provided."}))
                        continue

                    spectrogram = self.text_to_spectrogram(user_text)
                    audio = self.spectrogram_to_audio(spectrogram)

                    # Send audio data as JSON
                    await websocket.send(json.dumps({"audio": audio.tolist(), "sample_rate": self.sample_rate}))
                except Exception as e:
                    await websocket.send(json.dumps({"error": str(e)}))
        except websockets.ConnectionClosed:
            print("Client disconnected.")
        finally:
            connected_clients.remove(websocket)

    def start_websocket_server(self, host="localhost", port=8765, ssl_context=None):
        start_server = websockets.serve(self.handle_connection, host, port, ssl=ssl_context)
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(start_server)
            loop.run_forever()
        except KeyboardInterrupt:
            print("Shutting down WebSocket server.")
        finally:
            loop.stop()

    def synthesize(self, text: str) -> bytes:
        """
        Generate audio from text using pyttsx3 as fallback.

        Args:
            text (str): Input text.

        Returns:
            bytes: Audio data in bytes.
        """
        synthesizer = pyttsx3.init()
        synthesizer.setProperty('rate', 150)
        synthesizer.setProperty('volume', 1)
        audio_file = "output_audio.wav"
        try:
            synthesizer.save_to_file(text, audio_file)
            synthesizer.runAndWait()
            with open(audio_file, 'rb') as f:
                return f.read()
        finally:
            if os.path.exists(audio_file):
                os.remove(audio_file)

    def generate_audio(self, text: str) -> bytes:
        """Generates audio from text using fallback synthesizer."""
        return self.synthesize(text)


if __name__ == "__main__":
    try:
        tts = CapibaraTextToSpeech(
            fastspeech_model_path=fastspeech_path,
            hifigan_model_path=hifigan_path,
            sample_rate=sample_rate
        )
        tts.start_websocket_server(host=host, port=port, ssl_context=ssl_context)
    except Exception as e:
        print(f"Error starting TTS server: {e}")
