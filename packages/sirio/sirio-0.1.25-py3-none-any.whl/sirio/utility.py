import mimetypes

def existsJsonPath(document, paths: list):
    esiste = True
    subDocument = document
    for sub in paths:
        if sub in subDocument:
            subDocument = subDocument[sub]
        else:
            esiste = False
            break
    return esiste

def getContentTypeFromName(file_name):
    content_type, _ = mimetypes.guess_type(file_name)
    return content_type or "application/octet-stream"  # valore predefinito