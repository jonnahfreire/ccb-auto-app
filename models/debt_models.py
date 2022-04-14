
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
        self.expenditure: str = "3030"


#----------------------------------
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

