## Install CBR Community

Here is how to run "The Cyber Boardroom Community Edition" site on a laptop or docker environment

### Python

1) install the package

```
pip install cbr_website_beta
```

2) start site

```
'python -m cbr_website_beta'
```

### Docker

1) pull image

```
docker pull --platform linux/amd64  diniscruz/cbr_website_beta:latest
```

2) start container (when using ollama)

docker run -it --rm -p 5115:3000 --platform linux/amd64  diniscruz/cbr_website_beta

2) start container (when using other platforms)

<pre>
export GROQ_API_KEY={your key}
export OPEN_AI__API_KEY={your key}
export OPEN_ROUTER_API_KEY={your key}
docker run -it --rm -p 5115:3000 --platform linux/amd64  -e GROQ_API_KEY=$GROQ_API_KEY -e OPEN_AI__API_KEY=$OPEN_AI__API_KEY -e OPEN_ROUTER_API_KEY=$OPEN_ROUTER_API_KEY  diniscruz/cbr_website_beta
</pre>
