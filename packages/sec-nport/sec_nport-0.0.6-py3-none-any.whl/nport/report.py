import os.path

from pydantic import BaseModel
from bs4 import BeautifulSoup
import pandas as pd
import xmlschema
from nport.fund import Registrant, Fund
from nport.instruments import BaseInstrument, DebtSecurity, Derivative


PATH, _ = os.path.split(__file__)


class NPORT(BaseModel):
    registrant: Registrant
    fund: Fund
    securities: list[BaseInstrument | DebtSecurity | Derivative]

    def __repr__(self):
        return f"{self.registrant.name} [{self.registrant.report_date:%Y-%m-%d}]"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def from_file(cls, path: str, **kwargs):
        with open(path, "r") as file:
            xml = file.read()

        validate = kwargs.get("validate", True)
        if validate:
            schema = xmlschema.XMLSchema(os.path.join(PATH, "..", "schema", "nport", "eis_NPORT_Filer.xsd"))
            try:
                xmlschema.validate(xml, schema)
            except xmlschema.XMLSchemaDecodeError:
                pass

        root = BeautifulSoup(xml, features="xml")
        return cls.from_xml(root)

    @classmethod
    def from_str(cls, xml: str, **kwargs):
        validate = kwargs.get("validate", True)
        if validate:
            schema = xmlschema.XMLSchema(os.path.join(PATH, "..", "schema", "nport", "eis_NPORT_Filer.xsd"))
            try:
                xmlschema.validate(xml, schema)
            except xmlschema.XMLSchemaDecodeError:
                pass

        root = BeautifulSoup(xml, features="xml")
        return cls.from_xml(root)

    @classmethod
    def from_xml(cls, root):
        form_tag = root.find("formData")

        registrant_tag = form_tag.find("genInfo")
        registrant = Registrant.from_xml(registrant_tag)

        fund_tag = form_tag.find("fundInfo")
        fund = Fund.from_xml(fund_tag)

        securities_tag = form_tag.find("invstOrSecs")
        securities = []
        for security_tag in securities_tag.find_all("invstOrSec"):
            if security_tag.find("debtSec"):
                securities.append(DebtSecurity.from_xml(security_tag, registrant.report_date))
            elif security_tag.find("derivativeInfo"):
                securities.append(Derivative.from_xml(security_tag, registrant.report_date))
            else:
                securities.append(BaseInstrument.from_xml(security_tag, registrant.report_date))

        return cls(
            registrant=registrant,
            fund=fund,
            securities=securities
        )

    def export_prices(self):
        price_list = [security.to_list() for security in self.securities]
        return pd.DataFrame(price_list)
