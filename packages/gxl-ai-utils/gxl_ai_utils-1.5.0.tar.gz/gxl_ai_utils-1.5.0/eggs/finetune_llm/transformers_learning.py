from transformers import pipeline

import os
import torch
import sys

sys.path.insert(0, '../../')
from gxl_ai_utils.utils import utils_file
from datasets import load_dataset, Audio

os.environ["CUDA_VISIBLE_DEVICES"] = "4"
os.environ['HF_CACHE'] = "./ouput/hf_cache"
os.environ['TRANSFORMERS_CACHE'] = "./ouput/hf_cache"


def learn_pipline():
    classifier = pipeline("sentiment-analysis")
    res = classifier("We are very happy to show you the 🤗 Transformers library.")
    print(res)
    # >>> [{'label': 'POSITIVE', 'score': 0.9997795224189758}]
    # If you have more than one input, pass your inputs as a list to the pipeline()
    results = classifier(["We are very happy to show you the 🤗 Transformers library.", "We hope you don't hate it."])
    for result in results:
        print(f"label: {result['label']}, with score: {round(result['score'], 4)}")


def learn_pipline_2():
    speech_recognizer = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-960h")
    dataset = load_dataset("PolyAI/minds14", name="en-US", split="train")
    dataset = dataset.cast_column("audio", Audio(sampling_rate=speech_recognizer.feature_extractor.sampling_rate))
    result = speech_recognizer(dataset[:4]["audio"])
    print([d["text"] for d in result])


if __name__ == "__main__":
    learn_pipline_2()
