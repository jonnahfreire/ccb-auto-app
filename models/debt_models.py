
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
        self.cost_account: str = None
        self.payment_form: str = None
        self.file_name: str = None
        self.check_num: str = None
        self.doc_num: str = None

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
            "doc-num": self.doc_num
        }


# ----------------------------------
class Model11102(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "11102"


# ----------------------------------
class Model3026(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3026"
        self.cost_center: str = "ADM"
        self.cost_account: str = "1000"
        self.payment_form: str = "DINHEIRO"


# ----------------------------------
class Model3008(Model3026):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3008"


# ----------------------------------
class Model3006(Model3026):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3006"


# ----------------------------------
class Model3014(Model3026):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3014"


# ----------------------------------
class Model3030(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.cost_center: str = "ADM"
        self.expenditure: str = "3030"


# ----------------------------------
class Model3301(BaseModel):

    def __init__(self) -> None:
        super().__init__()
        self.cost_center: str = "ADM"
        self.expenditure: str = "3301"
