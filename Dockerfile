FROM python:3.12-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
    pip install --requirement /tmp/requirements.txt

COPY src /api/src

WORKDIR /api/src

CMD ["gunicorn", "--bind", "0.0.0.0:8000", \
    "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info", \
    "--access-logformat", "%(t)s \"%(r)s\" %(s)s %(L)s", "core.wsgi"]