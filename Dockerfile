FROM rocker/r-ubuntu:22.04

ENV http_proxy http://proxy.charite.de:8080
ENV https_proxy http://proxy.charite.de:8080

RUN apt-get update \
    && DEBIAN_FRONTEND="noninteractive" apt-get -y install \
        python3.10 \
        openjdk-17-jre \
        python3-pip \
        libpoppler-cpp-dev \
        poppler-utils \
        libcurl4-gnutls-dev \
        libxml2-dev \
        libssl-dev \
        libgit2-dev \
        curl \
        libfontconfig1-dev \
        libharfbuzz-dev \
        libfribidi-dev \
        libtiff5-dev \
        && ln -s $(which python3.10) /usr/bin/python \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

RUN Rscript \
    -e 'install.packages("devtools", dependencies = TRUE, repos = "http://cran.us.r-project.org")' \
    -e 'install.packages("pdftools", dependencies = TRUE, repos = "http://cran.us.r-project.org")' \
    -e 'install.packages("tidyverse", dependencies = TRUE)' \
    -e 'devtools::install_github("quest-bih/oddpub")' \
    -e 'devtools::install_github("maia-sh/ctregistries")' \
    -e 'devtools::install_github("serghiou/rtransparent@edb1eb9f4628fe372b9850a893bb70ba6e58f673")'

RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install --no-cache-dir --use-deprecated=legacy-resolver \
        numpy==1.25.0 \
        psycopg2-binary \
        requests \
        beautifulsoup4 \
        requests-oauthlib \
        fasttext \
        spacy \
        pymupdf \
	    Pillow \
        pandas==2.2.2 \
        scikit-learn \
        scikit-image \
        colorspacious \
        fastai==2.7.13 \
        importlib_resources \
        unidecode \
        uvicorn \
        python-multipart \
        fastapi \
        weasyprint \
        torch==2.4.0 \
        torchvision==0.15.0

COPY . .

COPY Renviron.site usr/local/lib/R/etc/Renviron.site


CMD uvicorn api:app --host 0.0.0.0
