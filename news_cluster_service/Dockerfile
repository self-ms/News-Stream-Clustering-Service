FROM python3.8:AI-Torch11-GPU

RUN apt-get update && apt-get -y install netcat && apt-get clean

RUN apt-get -y install nano
RUN apt-get -y install supervisor
RUN apt-get -y install cpulimit

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y install zsh
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true
RUN export SHELL=/usr/bin/zsh

WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python3 -m nltk.downloader punkt

CMD ["supervisord","-c","/app/supervisor/services.conf"]