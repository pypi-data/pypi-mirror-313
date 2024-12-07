# Tyba API Client

## Examples
For examples see [https://github.com/Tyba-Energy/tyba-client-notebooks](https://github.com/Tyba-Energy/tyba-client-notebooks).
The script examples in tyba-python-client/examples will be deprecated eventually.

## Development
### Docs
We use [`sphinx`](https://github.com/sphinx-doc/sphinx) to manage the documentation for the client.
Source .rst files can be found in docs/source. We use the
[`intersphinx`](https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#) extension to manage links
between the client docs and the docs of [`generation_models`](https://github.com/Tyba-Energy/generation/) (the model
schema for the client). Make sure you understand how these links are defined based on the `intersphinx_mapping`
variable in docs/source/conf.py to avoid any gotchas.  

To generate/update documentation for the Tyba client, `cd` into the docs directory and run the makefile that generates
the HTML documentation
```bash
# Assuming you are already in the tyba-python-client directory
$ cd docs
$ poetry run make html
```
The HTML documentation can be found in docs/build/html.

Once it's been reviewed, this HTML documentation needs to be uploaded to s3, so it
can be served at [https://docs.tybaenergy.com/api/](https://docs.tybaenergy.com/api/). We have a python script to do
this
```bash
poetry run python upload_to_s3.py
```



