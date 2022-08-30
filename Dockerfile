FROM python:3

WORKDIR /workspace/llvd
COPY ./ ./
RUN python setup.py install

WORKDIR /courses

ENTRYPOINT [ "llvd" ]
CMD [ "--help" ]
