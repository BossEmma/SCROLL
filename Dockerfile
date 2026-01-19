FROM ubuntu:20.04

ADD dependencies /
RUN ["chmod", "+x", "dependencies"]
RUN /dependencies

RUN ["mkdir", "output"]
RUN ["mkdir", "background_music"]

RUN ["python3 -m -venv venv"]
RUN ["source venv/bin/activate"]
RUN ["pip install -r requirements.txt"]
RUN ["python3 -m piper.download_voices en_US-hfc_male-medium"]

RUN ["git clone https://github.com/ggml-org/whisper.cpp.git"]
WORKDIR /whisper.cpp
RUN ["sh ./models/download-ggml-model.sh large-v3-turbo"]
RUN ["cmake -B build"]
RUN ["cmake --build build -j --config Release"]


CMD ["python", "scripts/main.py"]



