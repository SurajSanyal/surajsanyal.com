This is an example project intended to jumpstart a personal site using FastAPI.

# Setup

## Environment

From the terminal, create a virtual environment and activate it:

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Linux/MacOS
source venv/bin/activate
```

Then install all requirements:
```bash
python -m pip install -r requirements.txt
```

## Running the server

To start the webserver, run the following in a terminal:
```bash
fastapi run
```

This will serve the website on `http://localhost:8000` by default. Optionally specify a port:

```bash
fastapi run --port <port>
```

# Project basics

This project is built using FastAPI for serving webpages and Jinja for templating.

## Project structure
The bulk of this project is located in `website/`.

- `content/`: Contains Markdown and a Markdown-parsing module. Out-of-the-box, the Markdown-parsing module will only recognize Markdown files suffixed with `.md` that are not placed in further subdirectories.
- `static/`: Files to be served statically by the webserver. This includes images, Javascript, fonts, and CSS.
- `templates/`: HTML template files.
- `config.py`: A configuration module. This can contain any configuration you need. Starts only with `CONTENT_PATH` to point the Markdown-parsing module to the correct directory.
- `server.py`: Contains the FastAPI app and all routes.

## Jinja
There are a couple of key Jinja patterns to be aware of when building out page templates.


### Variables
To insert a variable called `var_name` into the template:
```html
<p>You can insert a variable like this: {{ var_name | safe }}</p>
```
The pipe `|` denotes a Jinja filter; these are special functions available to the Jinja templating engine. This particular filter `safe` is used to turn text into HTML-safe text.

For example if you had a variable `raw_html = "<p>This is some raw HTML.</p>"` and you tried to inject this into a template, it would *text insert* everything including the HTML tags. The desired behavior, to signal to the browser to *render* the HTML content, is accomplished using the `safe` filter. This is also used to HTML-escape Unicode characters like "é".

The rule of thumb is: if the variable is intended to be displayed, use `safe`.

Variables can be used *anywhere* in a template, so long as the compiled output is still valid HTML. Let's say there were a variable `color = "#aaaaaa"`. We can inject that color as a tag-level HTML style:
```html
<p style="color: {{ color }};">This will now be styled.</p>
```

### Loops and conditionals

To iterate over a list:
```html
{% for e in example_list %}
    <p>{{ e | safe }}</p>
    <p>{{ loop.index0 | safe }} will get you the index of the loop starting from 0.</p>
{% endfor %}
```

And to use a conditional:
```html
{% if e.some_property %}
    <p>The business is true.</p>
{% else %}
    <p>Not true.</p>
{% endif %}
```
These are cases in which the `safe` filter wouldn't be used, since these variables in the conditional syntax are being *evaluated* rather than displayed. But notice in the for-loop, when the variables are being tucked into `<p>` tags, that `safe` is used since these will actually display on the page.

## Applying styles
To style webpages, modify the CSS file at `website/static/styles.css`.

### Markdown pages

Unlike the HTML templates, which can have manually-specified classes and IDs, Markdown-parsed HTML inside of an HTML template cannot be directly modified (without Javascript). This is a limitation of Markdown.

Because of this, it's *highly* recommended to place your Markdown content in a `<div>` with an appropriate ID. That way, Markdown tag selectors in your CSS can be nested under an ID without modifying higher-level styles.

```html
<h1>This header is outside of the Markdown content. It will be affected by the top-level h1 selector.</h1>
<div id="markdown-content">
    {{ markdown.content | safe }}
</div>
```

```css
h1 {
    font-size: 32pt;
}

#markdown-content {
    h1 {
        /*
        The <h1> outside of markdown-content will be unaffected by this rule. 
        
        Markdown will automatically generate an <h1> for every "# Top level header" in the document,
        an <h2> for every "## Second level header", a <code> for every `code block`, etc.
        */
        font-size: 16pt;
    }
}
```

# Deploying to the Internet

This section is closer to webmastering than web development, but will give a general sense of what needs to happen for a production-level deployment of your site.

## Docker
This project comes with a `Dockerfile` and a `docker-compose.yaml`. These can be used to run this server in a Docker container serving at `http://localhost:8000`. The port can be specified using a `.env` file, see `.env.example` for details.

To run this webserver in Docker:
```bash
docker compose up -d
```

## Exposing the site to the Internet

This is typically done with a reverse proxy; I recommend [Caddy](https://caddyserver.com/docs/) for its automatic TLS registration. If you have a domain already, Caddy will automatically grab certificates and enable HTTPS on this site.

This requires:
- An `A` record for `*` in your domain registrar pointing to the external IP address of the server host.
- Ports 80 and 443 forwarded to Caddy's HTTP and HTTPS ports on your router.
- Ports 80 and 443 open in your host's firewall.

An example Caddyfile might look like this:
```
{
        http_port 80
        https_port 443
        admin :2019
        email <your-email>
}

(protect) {
        @external {
                not remote_ip 192.168.1.0/24
        }
        respond @external 403
}

https://your-domain.com {
        reverse_proxy <your-host-ip>:<service-port>
}
```

## Static file management

Ideally, you don't want to package static images, videos, fonts, etc. in your Docker container, you want to reference them dynamically from the file system. That way, making a new static resource available to your website is as simple as dragging and dropping a file into a folder. Styling adjustments can be propagated to the container automatically.

`docker-compose.yaml` makes use of a Docker *volume* to make a software link between your filesystem and the Docker container. In this case, `website/static/` in the project will correspond to `website/static/` in the container.

This setup is pretty robust for the most part. The most ideal situation would be to have an entirely separate web server for static resources, such as S3 or MinIO.