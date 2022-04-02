# ----------------------------------
class Model3026:

    def __init__(self) -> None:
        self.type: str = None
        self.num: str = None
        self.date: list = []
        self.emitter: str = None
        self.value: str = None
        self.expenditure: str = None
        self.hist1: str = "021"
        self.hist2: str = "023"
        self.cost_center: str = "ADM"
        self.cost_account: str = "1000"
        self.bill_form: str = "DINHEIRO"
        self.file_name: str = None

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
            "bill-form": self.bill_form, 
            "file-name": self.file_name
        }


# ----------------------------------
class Model3008(Model3026):

    def __init__(self) -> None:
        super().__init__()
        self.expenditure: str = "3008"


# ----------------------------------
class Model3014(Model3026):

    def __init__(self) -> None:
        super().__init__()
        self.check_num: str = None
        self.expenditure: str = "3008"
        self.cost_account: str = "1010"


# ----------------------------------