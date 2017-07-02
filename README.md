pip install pip-tools

requirements.in are the base packages

create installable requirements.txt file

``` 
pip-compile --output-file requirements.txt

```

the gutenberg package will download the rdf tar file
extract the rdf files and insert into cache.
this process can take a long time.  the first time
once cache is generated you can just read from it.
