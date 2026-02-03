from pydantic import BaseModel

class DocumentOutput(BaseModel):
    author: str | None = None
    doc_num: str | None = None
    sender: str | None = None
    date: str | None = None
    receiver: str | None = None
    context: str | None = None
    address: str | None = None
    phone_number: str | None = None
    email: str | None = None
    summary: str | None = None
    code_doc: str | None = None
