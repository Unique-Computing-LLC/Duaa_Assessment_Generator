FROM python:3.10-slim

WORKDIR /app

# Install git and other required tools
RUN apt-get update && apt-get install -y git bash coreutils && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY ./install_github_package.py .

ENV PYTHONUNBUFFERED=1

# Use Docker BuildKit secrets for sensitive data (pass each secret individually)
# Example usage:
# DOCKER_BUILDKIT=1 docker build \
#   --secret id=AWS_ACCESS_KEY_ID,env=AWS_ACCESS_KEY_ID \
#   --secret id=AWS_SECRET_ACCESS_KEY,env=AWS_SECRET_ACCESS_KEY \
#   --secret id=AWS_REGION,env=AWS_REGION \
#   --secret id=DUAA_EDTOOLS_SECRET_NAME,env=DUAA_EDTOOLS_SECRET_NAME \
#   -t your-image-name .

RUN --mount=type=secret,id=AWS_ACCESS_KEY_ID,required=true \
    --mount=type=secret,id=AWS_SECRET_ACCESS_KEY,required=true \
    --mount=type=secret,id=AWS_REGION,required=true \
    --mount=type=secret,id=DUAA_EDTOOLS_SECRET_NAME,required=true \
    export AWS_ACCESS_KEY_ID=$(cat /run/secrets/AWS_ACCESS_KEY_ID) && \
    export AWS_SECRET_ACCESS_KEY=$(cat /run/secrets/AWS_SECRET_ACCESS_KEY) && \
    export AWS_REGION=$(cat /run/secrets/AWS_REGION) && \
    export DUAA_EDTOOLS_SECRET_NAME=$(cat /run/secrets/DUAA_EDTOOLS_SECRET_NAME) && \
    python install_github_package.py

CMD ["python","-m", "src.main"]