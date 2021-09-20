
FROM gcr.io/deeplearning-platform-release/tf2-gpu.2-6

WORKDIR /

# Copies the trainer code to the docker image.
COPY builder /builder

RUN pip install -r builder/requirements.txt

# Sets up the entry point to invoke the trainer.
ENTRYPOINT ["python", "-m", "builder.task"]
