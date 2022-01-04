# Get the last python image version and update all the repositories
FROM python:3.10
RUN apt-get update && apt-get install -y wget make gettext && apt-get clean
RUN apt-get autoclean

# Install dockerize to avoid startup problems (waiting for DB to start)
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz -O - | tar -C /usr/local/bin -xzv

# Set the external path for the docker container
ARG PROJECT_EXTERNAL_PATH=src/

# Prepare work directory
RUN mkdir -p src
WORKDIR src

# Install all the requirements
RUN pip install poetry
ADD ${PROJECT_EXTERNAL_PATH}/poetry.lock /src/
ADD ${PROJECT_EXTERNAL_PATH}/pyproject.toml /src/
RUN poetry config virtualenvs.create false && poetry install

# Load source code from the repository or local to the container
COPY ${PROJECT_EXTERNAL_PATH}/ /src/

# Load executors
COPY docker/src/post_deploy.sh /src/
COPY docker/src/run_worker.sh /src/
COPY docker/src/run_beat.sh /src/

# Add terminal colors
COPY docker/src/.bashrc /root/

# Ipython config
RUN mkdir -p /root/.ipython/profile_default/
COPY docker/src/ipython-config.py /root/.ipython/profile_default/ipython_config.py
