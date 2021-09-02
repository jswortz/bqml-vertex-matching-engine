
FROM gcr.io/deeplearning-platform-release/tf2-gpu.2-5

WORKDIR /

# Copies the trainer code to the docker image.
COPY trainer /trainer

RUN pip install -r trainer/requirements.txt

# Sets up the entry point to invoke the trainer.
ENTRYPOINT ["python", "-m", "trainer.task"]
