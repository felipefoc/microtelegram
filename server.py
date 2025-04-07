import json
from fastapi import FastAPI, Depends, Response, Body
from pydantic import BaseModel
from server.database import engine, Base, get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from server.models.balance import Transaction
from server.schema.balance import ExpenseInput
from server.ai import TogetherAI, UtilsForSQL
from server.prompts.formatters import CHECK_INPUT_PROMPT

app = FastAPI()
TogetherClient = TogetherAI()
UtilsForSQL = UtilsForSQL()
Base.metadata.create_all(bind=engine)

balance_prefix = "/expense"
@app.post(balance_prefix + "/add")
def add_expense(data: ExpenseInput, db: Session = Depends(get_db)):
    print("WITHOUT RESPONSE")
    transaction = Transaction(
        user=data.user,
        value=data.value,
        reason=data.reason
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return {
        "status": "success", 
        "id": transaction.id,
        "user": transaction.user,
        "value": transaction.value,
        "reason": transaction.reason,
        "created_at": transaction.created_at
    }

@app.delete(balance_prefix + "/delete/{id}")
def delete_transaction(id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == id).first()
    if transaction is None:
        return {"status": "error", "message": "Transaction not found"}

    db.delete(transaction)
    db.commit()
    return {"status": "success"}


# @app.get("/list")
# async def list_transactions(db: Session = Depends(get_db)):
#     transactions = db.query(Transaction).all()
#     return format_data([t.__dict__ for t in transactions])


# @app.get("/list_raw")
# async def list_transactions_raw(db: Session = Depends(get_db)):
#     transactions = db.query(Transaction).all()
#     return [x.__dict__ for x in transactions]

class CheckInputRequest(BaseModel):
    text: str

@app.post("/freedbconsulting")
def free_llm_consulting(request: CheckInputRequest):
    response = UtilsForSQL.ask_to_db(question=request.text)
    return response


@app.post("/checkinput/")
def check_input(request: CheckInputRequest, db: Session = Depends(get_db)):
    raw = TogetherClient.get_response_from_ai_with_template_prompt(
        message=request.text,
        template=CHECK_INPUT_PROMPT
    )
    res = json.loads(raw)
    if res.get("error"):
        return Response(
            content=json.dumps(res),
            status_code=400,
            media_type="application/json"
        )
    return res

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)