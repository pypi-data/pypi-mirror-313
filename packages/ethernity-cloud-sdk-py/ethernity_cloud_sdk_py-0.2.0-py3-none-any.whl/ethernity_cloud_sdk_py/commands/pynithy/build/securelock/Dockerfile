# FROM registry.scontain.com:5050/sconecuratedimages/apps:python3.10.5-alpine3.15-scone5.8-pre-release as release
FROM registry.ethernity.cloud:443/debuggingdelight/ethernity-cloud-sdk-registry/etny-pynithy-testnet/python3.10.5-alpine3.15-scone5.8-pre-release AS release

RUN apk update

RUN cd /
RUN apk add bash openrc bind-tools sudo npm binutils curl binutils gcc g++ git openblas-dev
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install python-dotenv
RUN pip3 install web3==5.31.0
RUN pip3 install cryptography==42.0.7
RUN pip3 install ecdsa
RUN pip3 install pyasn1
RUN pip3 install tinyec
RUN pip3 install minio
RUN pip3 install pynacl
RUN pip3 install pytest
RUN pip3 install numpy
RUN pip3 install scipy
RUN pip3 install hypothesis
RUN pip3 install pooch
RUN pip3 install ipywidgets
RUN pip3 install pyinstaller
RUN pip3 install requests
RUN CMAKE_ARGS="-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python

#RUN pip3 install requests
#RUN pip3 install beautifulsoup4
#RUN pip3 install tokenizers
#RUN pip3 install transformers
#RUN pip3 install tensorflow


ENV ENCLAVE_NAME_SECURELOCK=ec_sdk_py_win_06_SECURELOCK_V3_testnet_v1
ENV BUCKET_NAME=etny-pynithy-testnet-v3
ENV SMART_CONTRACT_ADDRESS=0x02882F03097fE8cD31afbdFbB5D72a498B41112c
ENV IMAGE_REGISTRY_ADDRESS=0x15D73a742529C3fb11f3FA32EF7f0CC3870ACA31
ENV RPC_URL=https://core.bloxberg.org
ENV CHAIN_ID=8995
ENV TRUSTED_ZONE_IMAGE=etny-pynithy-testnet


RUN mkdir binary-fs-dir

COPY ./src /etny-securelock/
COPY ./scripts/* /etny-securelock/

RUN /etny-securelock/binary-fs-build.sh

FROM registry.ethernity.cloud:443/debuggingdelight/ethernity-cloud-sdk-registry/sconecuratedimages/crosscompilers AS build

COPY --from=release /binary-fs-dir /.

RUN scone gcc ./binary_fs_blob.s ./libbinary_fs_template.a -shared -o /libbinary-fs.so

FROM registry.ethernity.cloud:443/debuggingdelight/ethernity-cloud-sdk-registry/etny-pynithy-testnet/python3.10.5-alpine3.15-scone5.8-pre-release

COPY --from=build /usr/local/bin/scone /usr/local/bin/scone

#RUN scone cas attest scone-cas.cf 3061b9feb7fa67f3815336a085f629a13f04b0a1667c93b14ff35581dc8271e4 -GCS --only_for_testing-debug --only_for_testing-ignore-signer

COPY --from=build /libbinary-fs.so /lib/libbinary-fs.so

RUN openssl genrsa -3 -out /enclave-key.pem 3072


ENV SCONE_HEAP=1024M
ENV SCONE_LOG=FATAL
ENV SCONE_STACK=4M
ENV SCONE_ALLOW_DLOPEN=1
ENV SCONE_EXTENSIONS_PATH=/lib/libbinary-fs.so

# Disabled production mode for testnet
# RUN scone-signer sign --key=/enclave-key.pem --env --production /usr/local/bin/python3

RUN rm -rf /enclave-key.pem


ENTRYPOINT ["/usr/local/bin/python", "/etny-securelock/securelock.py"]
