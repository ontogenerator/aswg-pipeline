FROM ubuntu:20.04
ENV http_proxy http://proxy.charite.de:8080
ENV https_proxy http://proxy.charite.de:8080
RUN apt-get update \
    && DEBIAN_FRONTEND="noninteractive" apt-get -y install \
        python3.8 \
        openjdk-17-jre \
        python3-pip \
        poppler-utils \
        libpoppler-cpp-dev \
        r-cran-littler \
        libcurl4-gnutls-dev \
        libxml2-dev \
        libssl-dev \
        libgit2-dev \
        curl \
        libfontconfig1-dev \
        libharfbuzz-dev \
        libfribidi-dev \
        libtiff5-dev \
    && ln -s $(which python3.8) /usr/bin/python
RUN python3.8 -m pip install --upgrade pip \
    && python3.8 -m pip install --no-cache-dir \
        numpy==1.22.2 \
        psycopg2-binary \
        requests \
        beautifulsoup4 \
        requests-oauthlib \
        fasttext \
        spacy==2.2.4 \
        Pillow \
        pandas \
        scikit-learn==0.22 \
        scikit-image \
        colorspacious \
        fastai==2.5.3 \
        importlib_resources \
        unidecode \
        fastapi \
        uvicorn \
        python-multipart \
        weasyprint
RUN Rscript \
    -e 'install.packages("devtools")' \
    -e 'install.packages("tidyverse")' \
    -e 'devtools::install_github("quest-bih/oddpub")' \
    -e 'devtools::install_github("serghiou/rtransparent@edb1eb9f4628fe372b9850a893bb70ba6e58f673")' \
    -e 'devtools::install_github("maia-sh/ctregistries")'

COPY . .

COPY Renviron.site usr/local/lib/R/etc/Renviron.site

CMD uvicorn api:app --host 0.0.0.0
