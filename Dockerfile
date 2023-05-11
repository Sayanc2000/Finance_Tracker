FROM python:3.9-slim

WORKDIR /server/app

RUN pip3 install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install

COPY  . .

#CMD ["hypercorn", "app.main:app", "--bind", "0.0.0.0:8000", "--access-logformat", "{'address': '%(h)s', 'method': '%(m)s', 'path': '%(Uq)s', 'status': %(s)s, 'referer': '%(f)s'}", "--access-logfile", "-"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]