from typing import Optional
from datetime import date
from pydantic import BaseModel
from nport.xmltools import child_text, child_value


class Registrant(BaseModel):
    # Elements of A.1
    name: str
    file_number: str
    cik: int
    lei: str
    street_address1: str
    street_address2: Optional[str]
    city: str
    state: Optional[str]
    country: Optional[str]
    zip_code: str
    telephone: str

    # Elements of A.2
    series_name: str
    series_edgar_identifier: str
    series_lei: str

    # Elements of A.3 and A.4
    fiscal_year_end: date
    report_date: date
    is_final_filing: bool

    def __repr__(self):
        return f"{self.name} [{self.report_date:%Y-%m-%d}]"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def from_xml(cls, tag):
        name = child_text(tag, "regName")
        file_number = child_text(tag, "regFileNumber")
        cik = child_text(tag, "regCik")
        lei = child_text(tag, "regLei")
        street_address1 = child_text(tag, "regStreet1")
        street_address2 = child_text(tag, "regStreet2")
        city = child_text(tag, "regCity")
        state = child_value(tag, "regStateConditional", "regState")
        country = child_value(tag, "regStateConditional", "regCountry")
        zip_code = child_text(tag, "regZipOrPostalCode")
        telephone = child_text(tag, "regPhone")

        series_name = child_text(tag, "seriesName")
        series_edgar_identifier = child_text(tag, "seriesId")
        series_lei = child_text(tag, "seriesLei")

        fiscal_year_end = child_text(tag, "repPdEnd")
        report_date = child_text(tag, "repPdDate")
        is_final_filing = child_text(tag, "isFinalFiling") == "Y"

        return cls(
            name=name,
            file_number=file_number,
            cik=cik,
            lei=lei,
            street_address1=street_address1,
            street_address2=street_address2,
            city=city,
            state=state,
            country=country,
            zip_code=zip_code,
            telephone=telephone,
            series_name=series_name,
            series_edgar_identifier=series_edgar_identifier,
            series_lei=series_lei,
            fiscal_year_end=fiscal_year_end,
            report_date=report_date,
            is_final_filing=is_final_filing
        )


class PortfolioInterestRisk(BaseModel):
    # Elements of B.3.a and B.3.b
    currency: str
    dv01_3m: float
    dv01_1y: float
    dv01_5y: float
    dv01_10y: float
    dv01_30y: float
    dv100_3m: float
    dv100_1y: float
    dv100_5y: float
    dv100_10y: float
    dv100_30y: float

    @classmethod
    def from_xml(cls, tag):
        currency = child_text(tag, "curCd")
        dv01_3m = child_value(tag, "intrstRtRiskdv01", "period3Mon")
        dv01_1y = child_value(tag, "intrstRtRiskdv01", "period1Yr")
        dv01_5y = child_value(tag, "intrstRtRiskdv01", "period5Yr")
        dv01_10y = child_value(tag, "intrstRtRiskdv01", "period10Yr")
        dv01_30y = child_value(tag, "intrstRtRiskdv01", "period30Yr")
        dv100_3m = child_value(tag, "intrstRtRiskdv100", "period3Mon")
        dv100_1y = child_value(tag, "intrstRtRiskdv100", "period1Yr")
        dv100_5y = child_value(tag, "intrstRtRiskdv100", "period5Yr")
        dv100_10y = child_value(tag, "intrstRtRiskdv100", "period10Yr")
        dv100_30y = child_value(tag, "intrstRtRiskdv100", "period30Yr")

        return cls(
            currency=currency,
            dv01_3m=dv01_3m,
            dv01_1y=dv01_1y,
            dv01_5y=dv01_5y,
            dv01_10y=dv01_10y,
            dv01_30y=dv01_30y,
            dv100_3m=dv100_3m,
            dv100_1y=dv100_1y,
            dv100_5y=dv100_5y,
            dv100_10y=dv100_10y,
            dv100_30y=dv100_30y
        )


class PortfolioCreditRisk(BaseModel):
    # Elements of B.3.c
    cs01_3m_ig: float
    cs01_1y_ig: float
    cs01_5y_ig: float
    cs01_10y_ig: float
    cs01_30y_ig: float
    cs01_3m_junk: float
    cs01_1y_junk: float
    cs01_5y_junk: float
    cs01_10y_junk: float
    cs01_30y_junk: float

    @classmethod
    def from_xml(cls, tag):
        cs01_3m_ig = child_value(tag, "creditSprdRiskInvstGrade", "period3Mon")
        cs01_1y_ig = child_value(tag, "creditSprdRiskInvstGrade", "period1Yr")
        cs01_5y_ig = child_value(tag, "creditSprdRiskInvstGrade", "period5Yr")
        cs01_10y_ig = child_value(tag, "creditSprdRiskInvstGrade", "period10Yr")
        cs01_30y_ig = child_value(tag, "creditSprdRiskInvstGrade", "period30Yr")
        cs01_3m_junk = child_value(tag, "creditSprdRiskNonInvstGrade", "period3Mon")
        cs01_1y_junk = child_value(tag, "creditSprdRiskNonInvstGrade", "period1Yr")
        cs01_5y_junk = child_value(tag, "creditSprdRiskNonInvstGrade", "period5Yr")
        cs01_10y_junk = child_value(tag, "creditSprdRiskNonInvstGrade", "period10Yr")
        cs01_30y_junk = child_value(tag, "creditSprdRiskNonInvstGrade", "period30Yr")

        return cls(
            cs01_3m_ig=cs01_3m_ig,
            cs01_1y_ig=cs01_1y_ig,
            cs01_5y_ig=cs01_5y_ig,
            cs01_10y_ig=cs01_10y_ig,
            cs01_30y_ig=cs01_30y_ig,
            cs01_3m_junk=cs01_3m_junk,
            cs01_1y_junk=cs01_1y_junk,
            cs01_5y_junk=cs01_5y_junk,
            cs01_10y_junk=cs01_10y_junk,
            cs01_30y_junk=cs01_30y_junk
        )


class Borrower(BaseModel):
    # Elements of B.4.a
    name: str
    lei: Optional[str]
    aggregate_value: float


class NonCashCollateral(BaseModel):
    # Elements of B.4.b
    aggregate_principal: float
    aggregate_value: float
    asset_type: str


class ClassReturn(BaseModel):
    # Elements of B.5.a
    return_month1: float
    return_month2: float
    return_month3: float
    class_identification: str


class Fund(BaseModel):
    # Elements of B.1
    total_assets: float
    total_liabilities: float
    net_assets: float

    # Elements of B.2
    misc_assets: float
    controlled_foreign_corporation_assets: float
    borrowings_short_bank: float
    borrowings_short_companies: float
    borrowings_short_affiliates: float
    borrowings_short_others: float
    borrowings_medium_bank: float
    borrowings_medium_companies: float
    borrowings_medium_affiliates: float
    borrowings_medium_others: float
    payables_delayed: float
    payables_standby: float
    liquidation_preference: float
    cash: float

    # Elements of B.3
    interest_risk: list[PortfolioInterestRisk]
    credit_risk: Optional[PortfolioCreditRisk]

    # Elements of B.4
    borrowers: list[Borrower]
    is_non_cash_collateral: bool
    non_cash_collateral: list[NonCashCollateral]

    # Elements of B.5
    class_returns: list[ClassReturn]

    def __repr__(self):
        return f"Net Assets: ${self.net_assets:,.2f}"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def from_xml(cls, tag):
        total_assets = child_text(tag, "totAssets")
        total_liabilities = child_text(tag, "totLiabs")
        net_assets = child_text(tag, "netAssets")

        misc_assets = child_text(tag, "assetsAttrMiscSec")
        controlled_foreign_corporation_assets = child_text(tag, "assetsInvested")
        borrowings_short_bank = child_text(tag, "amtPayOneYrBanksBorr")
        borrowings_short_companies = child_text(tag, "amtPayOneYrCtrldComp")
        borrowings_short_affiliates = child_text(tag, "amtPayOneYrOthAffil")
        borrowings_short_others = child_text(tag, "amtPayOneYrOther")
        borrowings_medium_bank = child_text(tag, "amtPayAftOneYrBanksBorr")
        borrowings_medium_companies = child_text(tag, "amtPayAftOneYrCtrldComp")
        borrowings_medium_affiliates = child_text(tag, "amtPayAftOneYrOthAffil")
        borrowings_medium_others = child_text(tag, "amtPayAftOneYrOther")
        payables_delayed = child_text(tag, "delayDeliv")
        payables_standby = child_text(tag, "standByCommit")
        liquidation_preference = child_text(tag, "liquidPref")
        cash = child_text(tag, "cshNotRptdInCorD")

        interest_risk = []
        interest_risks_tag = tag.find("CurMetrics")
        if interest_risks_tag:
            for interest_risk_tag in interest_risks_tag.find_all("curMetric"):
                interest_risk.append(PortfolioInterestRisk.from_xml(interest_risk_tag))

        credit_risk = None
        if tag.find("creditSprdRiskInvstGrade") or tag.find("creditSprdRiskNonInvstGrade"):
            credit_risk = PortfolioCreditRisk.from_xml(tag)

        borrowers = []
        borrowers_tag = tag.find("borrowers")
        if borrowers_tag:
            for borrower_tag in borrowers_tag.find_all("borrower"):
                borrowers.append(Borrower(
                    name=borrower_tag.attrs.get("name"),
                    lei=borrower_tag.attrs.get("lei"),
                    aggregate_value=borrower_tag.attrs.get("aggrVal")
                ))

        is_non_cash_collateral = child_text(tag, "isNonCashCollateral") == "Y"
        non_cash_collateral = []
        non_cash_collaterals_tag = tag.find("aggregateInfos")
        if non_cash_collaterals_tag:
            is_non_cash_collateral = True
            for non_cash_collateral_tag in non_cash_collaterals_tag.find_all("aggregateInfo"):
                non_cash_collateral.append(NonCashCollateral(
                    aggregate_principal=non_cash_collateral_tag.attrs.get("amt"),
                    aggregate_value=non_cash_collateral_tag.attrs.get("collatrl"),
                    asset_type=child_text(non_cash_collateral_tag, "invstCat")
                ))

        class_returns = []
        return_info_tag = tag.find("returnInfo")
        total_return_infos_tag = return_info_tag.find("monthlyTotReturns")
        for total_return_info_tag in total_return_infos_tag.find_all("monthlyTotReturn"):
            class_returns.append(ClassReturn(
                return_month1=total_return_info_tag.attrs.get("rtn1"),
                return_month2=total_return_info_tag.attrs.get("rtn2"),
                return_month3=total_return_info_tag.attrs.get("rtn3"),
                class_identification=total_return_info_tag.attrs.get("classId")
            ))

        return cls(
            total_assets=total_assets,
            total_liabilities=total_liabilities,
            net_assets=net_assets,
            misc_assets=misc_assets,
            controlled_foreign_corporation_assets=controlled_foreign_corporation_assets,
            borrowings_short_bank=borrowings_short_bank,
            borrowings_short_companies=borrowings_short_companies,
            borrowings_short_affiliates=borrowings_short_affiliates,
            borrowings_short_others=borrowings_short_others,
            borrowings_medium_bank=borrowings_medium_bank,
            borrowings_medium_companies=borrowings_medium_companies,
            borrowings_medium_affiliates=borrowings_medium_affiliates,
            borrowings_medium_others=borrowings_medium_others,
            payables_delayed=payables_delayed,
            payables_standby=payables_standby,
            liquidation_preference=liquidation_preference,
            cash=cash,
            interest_risk=interest_risk,
            credit_risk=credit_risk,
            borrowers=borrowers,
            is_non_cash_collateral=is_non_cash_collateral,
            non_cash_collateral=non_cash_collateral,
            class_returns=class_returns
        )
