# JsonLLM client

`jsonllm-client` is a Python client library for interacting with the [JsonLLM API](https://jsonllm.com/).

JsonLLM allows you to extract structured data from documents.

`jsonllm-client` allows users to upload documents and delete documents, as well as extract data from said 
documents.

## Installation

`jsonllm-client` is available on PyPI, so it can be installed easily, e.g. using `pip`:

```bash
pip install jsonllm_client
```

## Initialization

You need to create an API key, which you can do [here](https://jsonllm.com/api-keys).

```python
from jsonllm_client import JsonLLM

api_key = "your_api_key_here"
json_llm = JsonLLM(api_key)

```


## Upload document(s)

To upload a document to a project, you need to use the `.upload` method:

```python
from jsonllm_client import JsonLLM

api_key = "your_api_key_here"
jsonllm = JsonLLM(api_key)

jsonllm.upload("invoice", "/home/ubuntu/Invoice_105274235.pdf")
```

To upload multiple documents, simply supply multiple paths:

```python
from jsonllm_client import JsonLLM

api_key = "your_api_key_here"
jsonllm = JsonLLM(api_key)

jsonllm.upload("invoice", ["/home/ubuntu/Invoice_13.pdf", "/home/ubuntu/Invoice_91.pdf"])
```


## Add plain text document(s)

To add a document from plain text, use the `.add_text` method:

```python
from jsonllm_client import JsonLLM

api_key = "your_api_key_here"
jsonllm = JsonLLM(api_key)

jsonllm.add_text("news", "cnn_article.txt", "Tensions rise.")
```

## Extract from document

```python
import json

from jsonllm_client import JsonLLM

api_key = "your_api_key_here"
jsonllm = JsonLLM(api_key)

res = jsonllm.extract(
    project="invoice",
    filename="Invoice_105274235.pdf"
)
print(json.dumps(res, indent=2))
# {
#   "invoice_date": "July 4, 2017",
#   "invoice_id": "105274235",
#   "s3_amount": "0.11",
#   "tax_amount": "0.00",
#   "total_amount": "52.57",
#   "vendor_name": "Amazon Web Services, Inc"
# }

```

## Delete document(s)

To delete a document, use the `.delete_document` method

```python
from jsonllm_client import JsonLLM

api_key = "your_api_key_here"
jsonllm = JsonLLM(api_key)

jsonllm.delete_document("invoice", "/home/ubuntu/Invoice_105274235.pdf")
```
