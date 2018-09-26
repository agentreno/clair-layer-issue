FROM nginx:1.12.0

RUN apt remove -y --purge libtiff5
