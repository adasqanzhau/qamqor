if [ -z "$OPENAI_API_KEY" ]; then
    export OPENAI_API_KEY="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"
fi
exec gunicorn --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --bind 0.0.0.0:$PORT run:app
