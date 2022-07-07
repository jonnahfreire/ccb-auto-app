# ------------------------------------
class BaseModel:

    def __init__(self) -> None:
        self.type: str = None
        self.num: str = None
        self.date: list = []
        self.emitter: str = None
        self.value: str = None
        self.expenditure: str = None
        self.hist1: str = None
        self.hist2: str = None
        self.cost_center: str = None
        self.cost_account: str = "1000"
        self.payment_form: str = "DINHEIRO"
        self.file_name: str = None
        self.check_num: str = None
        self.doc_num: str = None
        self.file_type: str = None
        self.insert_type: str = "DEBT"
        self.location: str = None

    def get_mapped_data(self) -> dict:
        return {
            "type": self.type,
            "num": self.num,
            "date": self.date,
            "value": self.value,
            "emitter": self.emitter,
            "expenditure": self.expenditure,
            "hist-1": self.hist1,
            "hist-2": self.hist2,
            "cost-center": self.cost_center,
            "cost-account": self.cost_account,
            "payment-form": self.payment_form,
            "file-name": self.file_name,
            "check-num": self.check_num,
            "doc-num": self.doc_num,
            "file-type": self.file_type,
            "insert-type": self.insert_type,
            "location": self.location
        }


# ----------------------------------
# RECEITAS
class Model1415:
    """Movimentação Interna"""

    def __init__(self) -> None:
        self.type: str = "SAQ"
        self.date: list = []
        # se a forma de transferência for com CHEQUE, 
        # inserir o favorecido como Congregação Cristã no Brasil
        self.transform: str = None
        self.doc_num: str = None
        self.value: str = None
        self.orig_account: str = None
        self.dest_account: str = None
        self.receiver: str = None
        self.hist: str = None
        self.complement: str = None
        self.file_name: str = None
        self.file_type: str = None
        self.insert_type: str = "MOVINT"
        self.location: str = None

    def get_mapped_data(self) -> dict:
        return {
            "type": self.type,
            "date": self.date,
            "transform": self.transform,
            "doc-num": self.doc_num,
            "value": self.value,
            "orig-account": self.orig_account,
            "dest-account": self.dest_account,
            "receiver": self.receiver,
            "hist": self.hist,
            "complement": self.complement,
            "file-name": self.file_name,
            "file-type": self.file_type,
            "insert-type": self.insert_type,
            "location": self.location
        }


class Model1835(Model1415):
    """Receitas em geral"""

    def __init__(self) -> None:
        super().__init__()


# FIM - RECEITAS
# ----------------------------------
# DESPESAS

class Model002(Model1415):

    def __init__(self) -> None:
        super().__init__()
        self.type: str = "APLICACAO"
        self.transform: str = "TRANSF. BANCARIA"
        self.hist: str = "002"
        self.orig_account: str = "1010"
        self.dest_account: str = "1033"
        self.file_type: str = "pdf"
        self.receiver: str = None
        self.complement: str = None


# ----------------------------------
class Model1120(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "1120"


# ----------------------------------
class Model3006(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3006"


# ----------------------------------
class Model3007(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3007"


# ----------------------------------
class Model3008(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3008"


# ----------------------------------
class Model3010(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3010"


# ----------------------------------
class Model3011(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3011"


# ----------------------------------
class Model3014(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3014"


# ----------------------------------
class Model3016(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3016"


# ----------------------------------
class Model3020(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3020"


# ----------------------------------
class Model3021(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3021"


# ----------------------------------
class Model3023(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3023"


# ----------------------------------
class Model3026(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3026"


# ----------------------------------
class Model3027(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3027"


# ----------------------------------
class Model3030(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.type: str = "RECIBO"
        self.expenditure: str = "3030"
        self.hist1: str = "012"
        self.emitter = "CAIXA ECONOMICA FEDERAL"
        self.hist2: str = "012"
        self.cost_center: str = "ADM"
        self.cost_account: str = "1010"
        self.payment_form: str = "DEBITO AUTOMATICO"
        self.file_type: str = "pdf"
        self.insert_type: str = "DEBT"


# ----------------------------------
class Model3300(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3300"


# ----------------------------------
class Model3301(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3301"


# ----------------------------------
class Model3302(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3302"


# ----------------------------------
class Model11101(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "11101"


# ----------------------------------
class Model11102(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "11102"
