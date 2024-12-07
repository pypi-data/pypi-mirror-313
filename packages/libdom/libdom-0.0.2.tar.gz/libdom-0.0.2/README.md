# LibDOM

LibDOM is a Python library that abstracts all modern (non-obsolete) HTML tags, allowing you to create dynamic HTML documents in a simple and programmatic way. With LibDOM, you can generate HTML structures entirely in Python, bringing clarity and flexibility to web development.

## Key Features

- **Complete Abstraction**: Supports all modern HTML tags.
- **Flexibility**: Ideal for creating dynamic web pages that require frequent updates.
- **Productivity**: Reduces repetitive code, simplifies maintenance, and accelerates development.

## Example

```py
from libdom import Html, Body, Div, P

# Creating a dynamic HTML page
page = Html(
    Body(
        Div(
            P("Hello, LibDOM! Building dynamic HTML with Python.", style="margin: none;"),
            class_="div",
            id="div"
        )
    )
)

print(page)
# Return <html><body><div class="div" id="div" ><p style="margin: none;" >Hello, LibDOM! Building dynamic HTML with Python.</p></div></body></html>
```