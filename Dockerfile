FROM ubuntu

#Check for Ubuntu update, Install Sudo 
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    curl

#Install Sudo and Git
RUN apt-get -y install sudo
RUN sudo apt-get -y install git
RUN sudo apt -y install nodejs npm

#Install Python and Rust
RUN apt-get install -y python3 python3-pip
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
RUN pip install flask
RUN pip install Gunicorn

ENV PATH="/root/.cargo/bin:${PATH}"
ENV APP_HOME /APP_HOMEWORKDIR $APP_HOME
ENV PORT=8080
EXPOSE 8080

WORKDIR /usr/src/app
COPY . .

RUN ./run install
ENV GIT_PYTHON_REFRESH=quiet

# Probably needs to be revisited
ENV GITHUB_TOKEN=${GITHUB_TOKEN} 

RUN ./run build


CMD ./run showscore ShortSample.txt
