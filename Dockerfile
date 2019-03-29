FROM python:3.6-stretch
LABEL maintainer="Derek DiCillo <dddicillo@gmail.com>"

COPY requirements.txt ./
RUN /usr/local/bin/pip install -r requirements.txt

COPY conf ./conf
COPY eternal_twitch /usr/local/lib/python3.6/site-packages/eternal_twitch/

CMD ["/usr/local/bin/python", "-m", "eternal_twitch"]
