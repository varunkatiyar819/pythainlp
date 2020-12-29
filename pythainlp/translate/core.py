# -*- coding: utf-8 -*-
import os
import tarfile
from collections import defaultdict

from pythainlp.corpus import download, get_corpus_path
from pythainlp.tools import get_full_data_path, get_pythainlp_data_path

from fairseq.models.transformer import TransformerModel
from sacremoses import MosesTokenizer

_en_tokenizer = MosesTokenizer("en")

_model = None
_model_name = None

# SCB_1M-MT_OPUS+TBASE_en-th_moses-spm_130000-16000_v1.0.tar.gz
_EN_TH_FILE_NAME = (
    "SCB_1M-MT_OPUS+TBASE_en-th_moses-spm_130000-16000_v1.0"
)
# SCB_1M-MT_OPUS+TBASE_th-en_spm-spm_32000-joined_v1.0.tar.gz
_TH_EN_FILE_NAME = "SCB_1M-MT_OPUS+TBASE_th-en_spm-spm_32000-joined_v1.0"


def _download_install(name):
    if get_corpus_path(name) is None:
        download(name, force=True, version="1.0")
        tar = tarfile.open(get_corpus_path(name), "r:gz")
        tar.extractall()
        tar.close()
    if not os.path.exists(get_full_data_path(name)):
        os.mkdir(get_full_data_path(name))
        with tarfile.open(get_corpus_path(name)) as tar:
            tar.extractall(path=get_full_data_path(name))


def download_model_all() -> None:
    """
    Download Model
    """
    _download_install("scb_1m_th-en_spm")
    _download_install("scb_1m_en-th_moses")


def _get_translate_path(model: str, *path: str) -> str:
    return os.path.join(get_full_data_path(model), *path)


def _scb_en_th_model_init():
    global _model, _model_name

    if _model_name != "scb_1m_en-th_moses":
        del _model
        _model_name = "scb_1m_en-th_moses"
        _download_install(_model_name)
        _model = TransformerModel.from_pretrained(
            model_name_or_path=_get_translate_path(
                _model_name, _EN_TH_FILE_NAME, "models",
            ),
            checkpoint_file="checkpoint.pt",
            data_name_or_path=_get_translate_path(
                _model_name, _EN_TH_FILE_NAME, "vocab",
            ),
        )


def _scb_en_th_translate(text: str) -> str:
    global _model, _model_name

    _scb_en_th_model_init()

    tokens = " ".join(_en_tokenizer.tokenize(text))
    translated = _model.translate(tokens)
    return translated.replace(' ', '').replace('▁', ' ').strip()


def _scb_th_en_model_init():
    global _model, _model_name

    if _model_name != "scb_1m_th-en_spm":
        del _model
        _model_name = "scb_1m_th-en_spm"
        _download_install(_model_name)
        _model = TransformerModel.from_pretrained(
            model_name_or_path=_get_translate_path(
                _model_name, _TH_EN_FILE_NAME, "models",
            ),
            checkpoint_file="checkpoint.pt",
            data_name_or_path=_get_translate_path(
                _model_name, _TH_EN_FILE_NAME, "vocab",
            ),
            bpe="sentencepiece",
            sentencepiece_model=_get_translate_path(
                _model_name, _TH_EN_FILE_NAME, "bpe", "spm.th.model",
            ),
        )


def _scb_th_en_translate(text: str) -> str:
    global _model, _model_name

    _scb_th_en_model_init()

    return _model.translate(text)


def translate(text: str, source: str, target: str) -> str:
    """
    Translate Language

    :param str text: input text in source language
    :param str source: source language ("en" or "th")
    :param str target: target language ("en" or "th")

    :return: translated text in target language
    :rtype: str
    """
    translated = None

    if source == "th" and target == "en":
        translated = _scb_th_en_translate(text)
    elif source == "en" and target == "th":
        translated = _scb_en_th_translate(text)
    else:
        return ValueError("The combination of the arguments isn't allowed.")

    return translated

class Translate:
    def __init__(self):
        self._model = None
        self._model_name = None
    def _scb_en_th_model_init(self):
        if self._model_name != "scb_1m_en-th_moses":
            self._model_name = "scb_1m_en-th_moses"
            _download_install(self._model_name)
            self._model = TransformerModel.from_pretrained(
                model_name_or_path=_get_translate_path(
                    self._model_name, _EN_TH_FILE_NAME, "models",
                ),
                checkpoint_file="checkpoint.pt",
                data_name_or_path=_get_translate_path(
                    self._model_name, _EN_TH_FILE_NAME, "vocab",
                ),
            )
    def _scb_en_th_translate(self, text: str) -> str:
        self._scb_en_th_model_init()
        tokens = " ".join(_en_tokenizer.tokenize(text))
        translated = self._model.translate(tokens)
        return translated.replace(' ', '').replace('▁', ' ').strip()
    def _scb_th_en_model_init(self):
        if self._model_name != "scb_1m_th-en_spm":
            self._model_name = "scb_1m_th-en_spm"
            _download_install(self._model_name)
            self._model = TransformerModel.from_pretrained(
                model_name_or_path=_get_translate_path(
                    self._model_name, _TH_EN_FILE_NAME, "models",
                ),
                checkpoint_file="checkpoint.pt",
                data_name_or_path=_get_translate_path(
                    self._model_name, _TH_EN_FILE_NAME, "vocab",
                ),
                bpe="sentencepiece",
                sentencepiece_model=_get_translate_path(
                    self._model_name, _TH_EN_FILE_NAME, "bpe", "spm.th.model",
                ),
            )
    def _scb_th_en_translate(self, text: str) -> str:
        self._scb_th_en_model_init()
        return self._model.translate(text)
    def translate(self, text: str, source: str, target: str) -> str:
        """
        Translate Language

        :param str text: input text in source language
        :param str source: source language ("en" or "th")
        :param str target: target language ("en" or "th")
        
        :return: translated text in target language
        :rtype: str
        """
        translated = None
        if source == "th" and target == "en":
            translated = self._scb_th_en_translate(text)
        elif source == "en" and target == "th":
            translated = self._scb_en_th_translate(text)
        else:
            return ValueError("The combination of the arguments isn't allowed.")
        return translated
