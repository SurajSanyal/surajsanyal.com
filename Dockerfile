FROM python:3.13.7-slim-trixie
WORKDIR /
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
COPY . .
CMD ["fastapi", "run"]