FROM redis:6-alpine
EXPOSE 6379
COPY ./docker_config/redis/redis.conf /usr/local/etc/redis/redis.conf
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
