# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import requests
from ovos_plugin_manager.templates.tts import TTS
from ovos_utils.log import LOG


def get_cotovia_demo(text, voice="sabela", lang="gl"):
    assert voice in ["sabela", "iago", "david"]
    url = 'http://gate.gts.uvigo.es:56666/index.php'
    headers = {
        'User-Agent': 'OpenVoiceOS (OVOS) plugin',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://gtm.uvigo.es',
        'Connection': 'keep-alive',
        'Referer': 'http://gtm.uvigo.es/',
    }
    data = {
        'encoding': 'PCM_SIGNED',
        'sampleRate': '16000',
        'bytesPerValue': '2',
        'language': lang,
        'voice': voice,
        'mimeType': 'audio/x-wav',
        'canales': 'none',
        'text': text,
        'texto_a_voz': 'Listen',
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Request failed with status code {response.status_code}")


class CotoviaRemoteTTSPlugin(TTS):
    """Interface to remote cotovia TTS demo."""

    def __init__(self, config=None):
        super().__init__(config=config, audio_ext='wav')
        if self.voice == "default":
            self.voice = "sabela"
        if self.lang.split("-")[0] not in ["es", "gl"]:
            raise ValueError(f"unsupported language: {self.lang}")

    def get_tts(self, sentence, wav_file, lang=None, voice=None):
        """Fetch tts audio using cotovia

        Arguments:
            sentence (str): Sentence to generate audio for
            wav_file (str): output file path
        Returns:
            Tuple ((str) written file, None)
        """
        # optional kwargs, OPM will send them if they are in message.data
        lang = (lang or self.lang).split("-")[0]
        if lang not in ["es", "gl"]:
            LOG.warning(f"Unsupported language! using default 'gl'")
            lang = "gl"
        voice = voice or self.voice

        if voice.lower() not in ["sabela", "iago", "david"]:
            LOG.warning(f"Unknown voice! using default {self.voice}")
            voice = self.voice

        data = get_cotovia_demo(sentence, voice=voice, lang=lang)
        with open(wav_file, "wb") as f:
            f.write(data)

        return (wav_file, None)  # No phonemes

    @property
    def available_languages(self) -> set:
        """Return languages supported by this TTS implementation in this state
        This property should be overridden by the derived class to advertise
        what languages that engine supports.
        Returns:
            set: supported languages
        """
        return {"gl", "es"}


CotoviaRemoteTTSPluginConfig = {
    lang: [
        {"lang": lang, "voice": "iago",
         "meta": {"gender": "male", "display_name": f"Iago",
                  "offline": True, "priority": 60}},
        {"lang": lang, "voice": "david",
         "meta": {"gender": "male", "display_name": f"David",
                  "offline": True, "priority": 60}},
        {"lang": lang, "voice": "sabela",
         "meta": {"gender": "female", "display_name": f"Sabela",
                  "offline": True, "priority": 55}}
    ] for lang in ["es-es", "es-gl"]
}

if __name__ == "__main__":
    test = 'Esta é unha demostración de Cotovía, un sistema de conversión texto-voz desenvolvido polo Grupo de Tecnoloxías Multimedia da Universidade de Vigo, e o Centro Ramón Piñeiro para a investigación en humanidades. Iago e Sabela son máis apropiados para galego, e David para castelán.'

    tts = CotoviaRemoteTTSPlugin({"lang": "gl"})
    tts.get_tts(test, "test.wav", voice="iago")
