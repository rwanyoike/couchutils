# couchutils Documentation

To use couchutils in a project:

```python
>>> from couchutils import <METHOD>
```

## Table of Contents

- [Build CouchDB Documents from a Directory](#build-couchdb-documents-from-a-directory)

## Build CouchDB Documents from a Directory

```python
>>> from couchutils import compile_doc
>>> compile_doc.compile_docs("<DOC_DIR>")
{...}
```

E.g. If passed a directory tree with:

```shell
.
├── example1
│   ├── _id
│   ├── language
│   └── views
│       └── numbers
│           ├── map.js
│           └── reduce
├── example2
│   └── _id
└── ignored.txt
```

The compiled output would be:

```python
>>> compile_doc.compile_docs(".")
{
    "_design/example1": {"_id": "_design/minimal"},
    "_design/example2": {
        "views": {
            "numbers": {
                "reduce": "_count",
                "map": "function (doc) {\n  if (doc.name) {\n    emit(doc.name, null);\n  }\n}",
            }
        },
        "_id": "_design/basic",
        "language": "javascript",
    },
}
```

Ref: [../tests/fixtures/compile_docs](../tests/fixtures/compile_docs)
