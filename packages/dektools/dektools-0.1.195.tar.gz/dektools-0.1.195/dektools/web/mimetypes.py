from mimetypes import MimeTypes

mimetypes = MimeTypes()

custom_types = {
    'text/javascript': '.js',
    'application/x-javascript': '.js',
    "application/atom+xml": ".xml",
    "application/rdf+xml": ".xml",
    "application/rss+xml": ".xml",
    "application/xhtml+xml": ".html",
    "application/vnd.wap.xhtml+xml": ".html",
    "application/x-json": ".json",
    "application/json-amazonui-streaming": ".json"
}

for k, v in custom_types.items():
    mimetypes.add_type(k, v)
