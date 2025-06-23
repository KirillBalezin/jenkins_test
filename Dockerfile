FROM bellsoft/liberica-openjre-alpine:17

ENV TZ=Europe/Moscow \
    PORT=9000

RUN apk upgrade --update --no-cache && \
    apk add --no-cache curl

COPY bspb /app

WORKDIR /app

RUN chmod 755 start.sh

HEALTHCHECK --interval=10s --timeout=10s --start-period=3m \
    CMD sh -c 'curl -f http://localhost:${PORT} || exit 1'

CMD ["./start.sh"]
