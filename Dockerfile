FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MCP_TRANSPORT=sse
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=7860
ENV PROPOSITION_WORK_DIR=/tmp/proposition-sessions

EXPOSE 7860

CMD ["python", "server.py"]
