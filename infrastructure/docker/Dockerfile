FROM python:3.14.3-slim-trixie AS app-build

WORKDIR /app 

ARG APP_UID=1000 
ARG APP_GID=1000 

RUN apt-get update \ 
    && apt-get install -y --no-install-recommends \ 
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \ 
    && apt-get clean \ 
    && groupadd -g "${APP_GID}" appuser \ 
    && useradd --create-home --no-log-init -u "${APP_UID}" -g "${APP_GID}" appuser \ 
    && chown appuser:appuser -R /app 
    
COPY --from=ghcr.io/astral-sh/uv:0.8.17 /uv /uvx /bin/ 

USER appuser 

COPY --chown=appuser:appuser /postapi/pyproject.toml /postapi/uv.lock* . 

ENV PYTHONDONTWRITEBYTECODE=1 \ 
    PYTHONUNBUFFERED=1 \ 
    UV_COMPILE_BYTECODE=1 \ 
    UV_LINK_MODE=copy \ 
    UV_PROJECT_ENVIRONMENT="/home/appuser/.local" \ 
    UV_PYTHON=python3.14 \ 
    PATH="${PATH}:/home/appuser/.local/bin" \ 
    USER="appuser" 

RUN --mount=type=cache,target=/app/.cache/uv \ 
    uv sync --frozen --no-install-project 
    
CMD ["bash"] 



########################################################################################## 



FROM python:3.14.2-slim-trixie AS app-final

WORKDIR /app 

ARG APP_UID=1000 
ARG APP_GID=1000 

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \ 
    && apt-get clean \ && groupadd -g "${APP_GID}" appuser \ 
    && useradd --create-home --no-log-init -u "${APP_UID}" -g "${APP_GID}" appuser \ 
    && chown appuser:appuser -R /app 

USER appuser

ENV UV_PROJECT_ENVIRONMENT="/home/appuser/.local" \ 
    UV_PYTHON=python3.14 \ 
    PATH="${PATH}:/home/appuser/.local/bin" \ 
    USER="appuser" 
    
COPY --chown=appuser:appuser --from=app-build /home/appuser/.local /home/appuser/.local
COPY --chown=appuser:appuser /postapi . 

EXPOSE 8000 
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.app:create_app()"]
