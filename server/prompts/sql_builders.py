TransactionModel = """
class Kind(str, Enum):
    Credit = "Credit"
    Debit = "Debit"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.now)
    user = Column(String, index=True)
    kind = Column(SQLEnum(Kind), nullable=False)
    value = Column(DECIMAL, nullable=False)
    reason = Column(String, index=True)
"""

FREE_PROMPT = f"""
    Você é um analista de dados.
    Você terá acesso ao meu banco de dados que é um sqlite3 com uma tabela chamada transactions.
    Nome da tabela no banco: transactions
    Schema da tabela: {TransactionModel}
    Dados da table: {all_data}
    Sua tarefa é retonar a consulta que o usuário solicitou.

    Exemplo:
      - Entrada: "Quanto eu fiquei no banco?"
      - Saída: "Você está com R$ 1000,00 (soma de todos os valores)"

    Outro exemplo: 
      - Entrada: ""
      - Saída: ""

"""