from typing import Optional
from datetime import date
from decimal import Decimal
from pydantic import BaseModel
import pandas as pd
from nport.xmltools import child_value, child_text


class BaseInstrument(BaseModel):
    # Elements of C.1
    issuer: Optional[str]
    issuer_lei: Optional[str]
    name: str
    cusip: Optional[str]
    isin: Optional[str]
    ticker: Optional[str]
    other_identifier_name: Optional[str]
    other_identifier: Optional[str]

    # Elements of C.2 and C.3
    balance: Decimal
    value_usd: Decimal
    value_local: Decimal
    price: Decimal
    units: str
    units_description: Optional[str]
    currency: str
    exchange_rate: Optional[Decimal]
    fund_percentage: Decimal
    payoff_profile: Optional[str]

    # Elements of C.4, C.5 and C.6
    asset_type: str
    asset_description: Optional[str]
    issuer_type: str
    issuer_description: Optional[str]
    issuer_country: str
    issuer_country_exposure: Optional[str]
    is_restricted_security: bool

    # Elements of C.7 and C.8
    liquidity: Optional[int]
    fair_value_level: Optional[int]

    # Elements of C.12
    is_cash_collateral_value: bool
    cash_collateral_value: Optional[Decimal]
    is_non_cash_collateral: bool
    non_cash_collateral_value: Optional[Decimal]
    is_on_loan: bool
    on_loan_value: Optional[Decimal]

    # Additional from A.3
    report_date: date

    def __repr__(self):
        return f"{self.name} [{self.issuer}]"

    def __str__(self):
        return self.__repr__()

    @classmethod
    def from_xml(cls, tag, report_date):
        issuer = child_text(tag, "name")
        issuer_lei = child_text(tag, "lei")
        name = child_text(tag, "title")
        cusip = child_text(tag, "cusip")

        identifiers_tag = tag.find("identifiers")
        ticker = child_value(identifiers_tag, "ticker")
        isin = child_value(identifiers_tag, "isin")
        other_identifier_name = child_value(identifiers_tag, "other", "otherDesc")
        other_identifier = child_value(identifiers_tag, "other")

        balance = child_text(tag, "balance")
        value_usd = child_text(tag, "valUSD")
        units = child_text(tag, "units")
        units_description = child_text(tag, "descOthUnits")
        currency = child_text(tag, "curCd")
        exchange_rate = None
        if currency is None:
            currency = child_value(tag, "currencyConditional", "curCd")
            exchange_rate = child_value(tag, "currencyConditional", "exchangeRt")
        fund_percentage = child_text(tag, "pctVal")
        payoff_profile = child_text(tag, "payoffProfile")

        value_local = None
        if currency and currency != "USD" and exchange_rate:
            value_local = Decimal(exchange_rate) * Decimal(value_usd)
        elif currency and currency == "USD":
            value_local = value_usd
        price = Decimal(value_local) / Decimal(balance)
        if units == "PA":
            price = 100 * price
        if payoff_profile == "Short":
            price = -1 * price

        asset_type = child_text(tag, "assetCat")
        asset_description = None
        if asset_type is None:
            asset_type = child_value(tag, "assetConditional", "assetCat")
            asset_description = child_value(tag, "assetConditional", "desc")
        issuer_type = child_text(tag, "issuerCat")
        issuer_description = None
        if issuer_type is None:
            issuer_type = child_value(tag, "issuerConditional", "issuerCat")
            issuer_description = child_value(tag, "issuerConditional", "desc")
        issuer_country = child_text(tag, "invCountry")
        issuer_country_exposure = child_text(tag, "invOthCountry")
        is_restricted_security = child_text(tag, "isRestrictedSec") == "Y"

        liquidity = child_text(tag, "fundCat")
        fair_value_level = child_text(tag, "fairValLevel")

        security_lending_tag = tag.find("securityLending")
        is_cash_collateral_value = child_text(security_lending_tag, "isCashCollateral")
        cash_collateral_value = None
        if is_cash_collateral_value is None:
            is_cash_collateral_value = child_value(security_lending_tag, "cashCollateralCondition", "isCashCollateral")
            cash_collateral_value = child_value(security_lending_tag, "cashCollateralCondition", "cashCollateralVal")
        is_cash_collateral_value = is_cash_collateral_value == "Y"

        is_non_cash_collateral = child_text(security_lending_tag, "isNonCashCollateral")
        non_cash_collateral_value = None
        if is_non_cash_collateral is None:
            is_non_cash_collateral = child_value(security_lending_tag, "nonCashCollateralCondition", "isNonCashCollateral")
            non_cash_collateral_value = child_value(security_lending_tag, "nonCashCollateralCondition", "nonCashCollateralVal")
        is_non_cash_collateral = is_non_cash_collateral == "Y"

        is_on_loan = child_text(security_lending_tag, "isLoanByFund")
        on_loan_value = None
        if is_on_loan is None:
            is_on_loan = child_value(security_lending_tag, "loanByFundCondition", "isLoanByFund")
            on_loan_value = child_value(security_lending_tag, "loanByFundCondition", "loanVal")
        is_on_loan = is_on_loan == "Y"

        return cls(
            issuer=issuer,
            issuer_lei=issuer_lei,
            name=name,
            cusip=cusip,
            isin=isin,
            ticker=ticker,
            other_identifier_name=other_identifier_name,
            other_identifier=other_identifier,
            balance=balance,
            value_usd=value_usd,
            value_local=value_local,
            price=price,
            units=units,
            units_description=units_description,
            currency=currency,
            exchange_rate=exchange_rate,
            fund_percentage=fund_percentage,
            payoff_profile=payoff_profile,
            asset_type=asset_type,
            asset_description=asset_description,
            issuer_type=issuer_type,
            issuer_description=issuer_description,
            issuer_country=issuer_country,
            issuer_country_exposure=issuer_country_exposure,
            is_restricted_security=is_restricted_security,
            liquidity=liquidity,
            fair_value_level=fair_value_level,
            is_cash_collateral_value=is_cash_collateral_value,
            cash_collateral_value=cash_collateral_value,
            is_non_cash_collateral=is_non_cash_collateral,
            non_cash_collateral_value=non_cash_collateral_value,
            is_on_loan=is_on_loan,
            on_loan_value=on_loan_value,
            report_date=report_date
        )

    def to_list(self):
        return pd.Series(
            [
                self.name,
                self.cusip,
                self.isin,
                self.ticker,
                self.other_identifier,
                self.other_identifier_name,
                self.issuer,
                self.issuer_description,
                self.issuer_lei,
                self.issuer_type,
                self.issuer_country,
                self.issuer_country_exposure,
                self.asset_type,
                self.asset_description,
                self.payoff_profile,
                self.currency,
                self.balance,
                self.value_local,
                self.exchange_rate,
                self.price,
                self.fair_value_level
            ],
            index=[
                "Name", "CUSIP", "ISIN", "Ticker", "OtherIdentifier", "OtherIdentifierName", "Issuer",
                "IssuerDescription", "IssuerLEI", "IssuerType", "IssuerCountry", "IssuerCountryExposure",
                "AssetType", "AssetTypeDescription", "PayoffProfile", "Currency", "Balance", "Value", "ExchangeRate",
                "Price", "FairValueLevel"
            ]
        )


class DebtSecurity(BaseInstrument):
    # Elements of C.9
    maturity_date: date
    coupon_type: Optional[str]
    coupon_rate: Optional[Decimal]
    is_default: bool
    is_deferred_interest: bool
    is_paid_in_kind: bool
    is_mandatory_convertible: Optional[bool]
    is_contingent_convertible: Optional[bool]
    reference_issuer: Optional[str]
    reference_name: Optional[str]
    reference_currency: Optional[str]
    reference_cusip: Optional[str]
    reference_isin: Optional[str]
    reference_ticker: Optional[str]
    reference_other_identifier_name: Optional[str]
    reference_other_identifier: Optional[str]
    conversion_ratio: Optional[Decimal]
    conversion_currency: Optional[str]
    delta: Optional[Decimal]

    @classmethod
    def from_xml(cls, tag, report_date):
        debt_security_tag = tag.find("debtSec")
        maturity_date = child_text(debt_security_tag, "maturityDt")
        coupon_type = child_text(debt_security_tag, "couponKind")
        coupon_rate = child_text(debt_security_tag, "annualizedRt")
        is_default = child_text(debt_security_tag, "isDefault") == "Y"
        is_deferred_interest = child_text(debt_security_tag, "areIntrstPmntsInArrs") == "Y"
        is_paid_in_kind = child_text(debt_security_tag, "isPaidKind")

        is_mandatory_convertible = child_text(debt_security_tag, "isMandatoryConvrtbl")
        if is_mandatory_convertible:
            is_mandatory_convertible = is_mandatory_convertible == "Y"
        is_contingent_convertible = child_text(debt_security_tag, "isContngtConvrtbl")
        if is_contingent_convertible:
            is_contingent_convertible = is_contingent_convertible == "Y"

        reference_issuer = None
        reference_name = None
        reference_currency = None
        reference_cusip = None
        reference_isin = None
        reference_ticker = None
        reference_other_identifier_name = None
        reference_other_identifier = None
        reference_tag = debt_security_tag.find("dbtSecRefInstruments")
        if reference_tag:
            reference_issuer = child_text(reference_tag, "name")
            reference_name = child_text(reference_tag, "title")
            reference_currency = child_text(reference_tag, "curCd")
            reference_identifier_tag = reference_tag.find("identifiers")
            reference_cusip = child_value(reference_identifier_tag, "cusip")
            reference_isin = child_value(reference_identifier_tag, "isin")
            reference_ticker = child_value(reference_identifier_tag, "ticker")
            reference_other_identifier_name = child_value(reference_identifier_tag, "other", "otherDesc")
            reference_other_identifier = child_value(reference_identifier_tag, "other")

        conversion_ratio = None
        conversion_currency = None
        currency_info_tag = debt_security_tag.find("currencyInfos")
        if currency_info_tag:
            conversion_ratio = child_value(currency_info_tag, "currencyInfo", "convRatio")
            conversion_currency = child_value(currency_info_tag, "currencyInfo", "curCd")
        delta = child_text(debt_security_tag, "delta")

        base = BaseInstrument.from_xml(tag, report_date)
        return cls(
            **base.__dict__,
            maturity_date=maturity_date,
            coupon_type=coupon_type,
            coupon_rate=coupon_rate,
            is_default=is_default,
            is_deferred_interest=is_deferred_interest,
            is_paid_in_kind=is_paid_in_kind,
            is_mandatory_convertible=is_mandatory_convertible,
            is_contingent_convertible=is_contingent_convertible,
            reference_issuer=reference_issuer,
            reference_name=reference_name,
            reference_currency=reference_currency,
            reference_cusip=reference_cusip,
            reference_isin=reference_isin,
            reference_ticker=reference_ticker,
            reference_other_identifier_name=reference_other_identifier_name,
            reference_other_identifier=reference_other_identifier,
            conversion_ratio=conversion_ratio,
            conversion_currency=conversion_currency,
            delta=delta
        )


class RepurchasementAgreement(BaseInstrument):
    # Elements of C.10
    agreement_category: str
    is_cleared_by_central_counterparty: bool
    counterparty_name: Optional[str]
    counterparty_lei: Optional[str]
    is_triparty: bool
    repurchase_rate: Decimal
    maturity_date: date
    principal: Decimal
    collateral: Decimal
    collateral_type: str


class Derivative(BaseInstrument):
    # Elements of C.11
    derivative_type: str
    derivative_type_description: Optional[str]
    counterparty_name: Optional[str]
    counterparty_lei: Optional[str]


    @classmethod
    def from_xml(cls, tag, report_date):
        derivative_tag = tag.find("derivativeInfo")
        base = BaseInstrument.from_xml(tag, report_date)

        counterparty_tag = derivative_tag.find("counterparties")
        counterparty_name = child_text(counterparty_tag, "counterpartyName")
        counterparty_lei = child_text(counterparty_tag, "counterpartyLei")

        derivative_type_description = None
        if derivative_tag.find("fwdDeriv"):
            forward_tag = derivative_tag.find("fwdDeriv")

            if forward_tag.find("payOffProf"):
                derivative_type = "Forward"
                base.payoff_profile = child_text(forward_tag, "payOffProf")

                reference_instrument_tag = forward_tag.find("descRefInstrmnt")
                reference_instrument = None
                if reference_instrument_tag:
                    if reference_instrument_tag.find("indexBasketInfo"):
                        reference_instrument = ReferenceIndex.from_xml(reference_instrument_tag.find("indexBasketInfo"))
                    elif reference_instrument_tag.find("nestedDerivInfo"):
                        reference_instrument = ReferenceDerivative.from_xml(
                            reference_instrument_tag.find("nestedDerivInfo"))
                    else:
                        reference_instrument = ReferenceOther.from_xml(reference_instrument_tag.find("otherRefInst"))

                maturity = child_text(forward_tag, "expDate")
                notional = child_text(forward_tag, "notionalAmt")
                derivative_currency = child_text(forward_tag, "curCd")
                unrealized_appreciation = child_text(forward_tag, "unrealizedAppr")
                return ForwardFuture(
                    **base.__dict__,
                    derivative_type=derivative_type,
                    derivative_type_description=derivative_type_description,
                    counterparty_name=counterparty_name,
                    counterparty_lei=counterparty_lei,
                    reference_instrument=reference_instrument,
                    maturity=maturity,
                    notional=notional,
                    derivative_currency=derivative_currency,
                    unrealized_appreciation=unrealized_appreciation
                )

            else:
                derivative_type = "FX Forward"
                currency_amount_sold = child_text(forward_tag, "amtCurSold")
                currency_sold = child_text(forward_tag, "curSold")
                currency_amount_purchased = child_text(forward_tag, "amtCurPur")
                currency_purchased = child_text(forward_tag, "curPur")
                settlement = child_text(forward_tag, "settlementDt")
                unrealized_appreciation = child_text(forward_tag, "unrealizedAppr")
                return FXForwardOrSwap(
                    **base.__dict__,
                    derivative_type=derivative_type,
                    derivative_type_description=derivative_type_description,
                    counterparty_name=counterparty_name,
                    counterparty_lei=counterparty_lei,
                    currency_amount_sold=currency_amount_sold,
                    currency_sold=currency_sold,
                    currency_amount_purchased=currency_amount_purchased,
                    currency_purchased=currency_purchased,
                    settlement=settlement,
                    unrealized_appreciation=unrealized_appreciation
                )

        elif derivative_tag.find("futrDeriv"):
            derivative_type = "Future"
            future_tag = derivative_tag.find("futrDeriv")
            base.payoff_profile = child_text(future_tag, "payOffProf")

            reference_instrument_tag = future_tag.find("descRefInstrmnt")
            reference_instrument = None
            if reference_instrument_tag:
                if reference_instrument_tag.find("indexBasketInfo"):
                    reference_instrument = ReferenceIndex.from_xml(reference_instrument_tag.find("indexBasketInfo"))
                elif reference_instrument_tag.find("nestedDerivInfo"):
                    reference_instrument = ReferenceDerivative.from_xml(
                        reference_instrument_tag.find("nestedDerivInfo"))
                else:
                    reference_instrument = ReferenceOther.from_xml(reference_instrument_tag.find("otherRefInst"))

            maturity = child_text(future_tag, "expDate")
            notional = child_text(future_tag, "notionalAmt")
            derivative_currency = child_text(future_tag, "curCd")
            unrealized_appreciation = child_text(future_tag, "unrealizedAppr")
            return ForwardFuture(
                **base.__dict__,
                derivative_type=derivative_type,
                derivative_type_description=derivative_type_description,
                counterparty_name=counterparty_name,
                counterparty_lei=counterparty_lei,
                reference_instrument=reference_instrument,
                maturity=maturity,
                notional=notional,
                derivative_currency=derivative_currency,
                unrealized_appreciation=unrealized_appreciation
            )

        elif derivative_tag.find("swapDeriv"):
            swap_tag = derivative_tag.find("swapDeriv")

            if derivative_tag.find("swapFlag"):
                derivative_type = "Swap"
                swap_flag = child_text(swap_tag, "swapFlag") == "Y"
                maturity = child_text(swap_tag, "terminationDt")

                reference_instrument_tag = swap_tag.find("descRefInstrmnt")
                reference_instrument = None
                if reference_instrument_tag:
                    if reference_instrument_tag.find("indexBasketInfo"):
                        reference_instrument = ReferenceIndex.from_xml(reference_instrument_tag.find("indexBasketInfo"))
                    elif reference_instrument_tag.find("nestedDerivInfo"):
                        reference_instrument = ReferenceDerivative.from_xml(
                            reference_instrument_tag.find("nestedDerivInfo"))
                    else:
                        reference_instrument = ReferenceOther.from_xml(reference_instrument_tag.find("otherRefInst"))

                payment_index = None
                payment_rate = None
                payment_description = None
                payment_currency = None
                payment_amount = None
                if swap_tag.find("fixedPmntDesc"):
                    payment_type = child_value(swap_tag, "fixedPmntDesc", "fixedOrFloating")
                    payment_rate = child_value(swap_tag, "fixedPmntDesc", "fixedRt")
                    payment_currency = child_value(swap_tag, "fixedPmntDesc", "curCd")
                    payment_amount = child_value(swap_tag, "fixedPmntDesc", "amount")
                elif swap_tag.find("floatingPmntDesc"):
                    payment_type = child_value(swap_tag, "floatingPmntDesc", "fixedOrFloating")
                    payment_rate = child_value(swap_tag, "floatingPmntDesc", "floatingRtSpread")
                    payment_index = child_value(swap_tag, "floatingPmntDesc", "floatingRtIndex")
                    payment_currency = child_value(swap_tag, "floatingPmntDesc", "curCd")
                    payment_amount = child_value(swap_tag, "floatingPmntDesc", "pmntAmt")
                elif swap_tag.find("otherPmntDesc"):
                    payment_type = child_value(swap_tag, "otherPmntDesc", "fixedOrFloating")
                    payment_description = child_text(swap_tag, "otherPmntDesc")

                receipt_index = None
                receipt_rate = None
                receipt_description = None
                receipt_currency = None
                receipt_amount = None
                if swap_tag.find("fixedRecDesc"):
                    receipt_type = child_value(swap_tag, "fixedRecDesc", "fixedOrFloating")
                    receipt_rate = child_value(swap_tag, "fixedRecDesc", "fixedRt")
                    receipt_currency = child_value(swap_tag, "fixedRecDesc", "curCd")
                    receipt_amount = child_value(swap_tag, "fixedRecDesc", "amount")
                elif swap_tag.find("floatingRecDesc"):
                    receipt_type = child_value(swap_tag, "floatingRecDesc", "fixedOrFloating")
                    receipt_rate = child_value(swap_tag, "floatingRecDesc", "floatingRtSpread")
                    receipt_index = child_value(swap_tag, "floatingRecDesc", "floatingRtIndex")
                    receipt_currency = child_value(swap_tag, "floatingRecDesc", "curCd")
                    receipt_amount = child_value(swap_tag, "floatingRecDesc", "pmntAmt")
                elif swap_tag.find("otherRecDesc"):
                    receipt_type = child_value(swap_tag, "otherRecDesc", "fixedOrFloating")
                    receipt_description = child_text(swap_tag, "otherRecDesc")

                upfront_payment = child_text(swap_tag, "upfrontPmnt")
                upfront_payment_currency = child_text(swap_tag, "pmntCurCd")
                upfront_receipts = child_text(swap_tag, "upfrontRcpt")
                upfront_receipts_currency = child_text(swap_tag, "rcptCurCd")
                notional = child_text(swap_tag, "notionalAmt")
                derivative_currency = child_text(swap_tag, "curCd")
                unrealized_appreciation = child_text(swap_tag, "unrealizedAppr")
                return Swap(
                    **base.__dict__,
                    derivative_type=derivative_type,
                    derivative_type_description=derivative_type_description,
                    counterparty_name=counterparty_name,
                    counterparty_lei=counterparty_lei,
                    reference_instrument=reference_instrument,
                    swap_flag=swap_flag,
                    maturity=maturity,
                    payment_type=payment_type,
                    payment_description=payment_description,
                    payment_rate=payment_rate,
                    payment_index=payment_index,
                    payment_currency=payment_currency,
                    payment_amount=payment_amount,
                    receipt_type=receipt_type,
                    receipt_description=receipt_description,
                    receipt_rate=receipt_rate,
                    receipt_index=receipt_index,
                    receipt_currency=receipt_currency,
                    receipt_amount=receipt_amount,
                    upfront_payment=upfront_payment,
                    upfront_payment_currency=upfront_payment_currency,
                    upfront_receipts=upfront_receipts,
                    upfront_receipts_currency=upfront_receipts_currency,
                    notional=notional,
                    derivative_currency=derivative_currency,
                    unrealized_appreciation=unrealized_appreciation
                )
            else:
                derivative_type = "FX Swap"
                currency_amount_sold = child_text(swap_tag, "amtCurSold")
                currency_sold = child_text(swap_tag, "curSold")
                currency_amount_purchased = child_text(swap_tag, "amtCurPur")
                currency_purchased = child_text(swap_tag, "curPur")
                settlement = child_text(swap_tag, "settlementDt")
                unrealized_appreciation = child_text(swap_tag, "unrealizedAppr")
                return FXForwardOrSwap(
                    **base.__dict__,
                    derivative_type=derivative_type,
                    derivative_type_description=derivative_type_description,
                    counterparty_name=counterparty_name,
                    counterparty_lei=counterparty_lei,
                    currency_amount_sold=currency_amount_sold,
                    currency_sold=currency_sold,
                    currency_amount_purchased=currency_amount_purchased,
                    currency_purchased=currency_purchased,
                    settlement=settlement,
                    unrealized_appreciation=unrealized_appreciation
                )

        elif derivative_tag.find("optionSwaptionWarrantDeriv"):
            option_tag = derivative_tag.find("optionSwaptionWarrantDeriv")
            derivative_type = {"OPT": "Option", "SWO": "Swaption", "WAR": "Warrant"}.get(
                child_value(derivative_tag, "optionSwaptionWarrantDeriv", "derivCat")
            )
            option_type = child_text(option_tag, "putOrCall")
            option_payoff = child_text(option_tag, "writtenOrPur")

            reference_instrument_tag = option_tag.find("descRefInstrmnt")
            reference_instrument = None
            if reference_instrument_tag:
                if reference_instrument_tag.find("indexBasketInfo"):
                    reference_instrument = ReferenceIndex.from_xml(reference_instrument_tag.find("indexBasketInfo"))
                elif reference_instrument_tag.find("nestedDerivInfo"):
                    reference_instrument = ReferenceDerivative.from_xml(
                        reference_instrument_tag.find("nestedDerivInfo"))
                else:
                    reference_instrument = ReferenceOther.from_xml(reference_instrument_tag.find("otherRefInst"))

            shares = child_text(option_tag, "shareNo")
            notional = child_text(option_tag, "principalAmt")
            derivative_currency = child_text(option_tag, "curCd")
            exercise_price = child_text(option_tag, "exercisePrice")
            exercise_currency = child_text(option_tag, "exercisePriceCurCd")
            exercise_date = child_text(option_tag, "expDt")
            delta = child_text(option_tag, "delta")
            unrealized_appreciation = child_text(option_tag, "unrealizedAppr")
            return Option(
                **base.__dict__,
                derivative_type=derivative_type,
                derivative_type_description=derivative_type_description,
                counterparty_name=counterparty_name,
                counterparty_lei=counterparty_lei,
                option_type=option_type,
                option_payoff=option_payoff,
                reference_instrument=reference_instrument,
                shares=shares,
                notional=notional,
                derivative_currency=derivative_currency,
                exercise_price=exercise_price,
                exercise_currency=exercise_currency,
                exercise_date=exercise_date,
                delta=delta,
                unrealized_appreciation=unrealized_appreciation
            )

        elif derivative_tag.find("othDeriv"):
            derivative_type = "Other"
            derivative_type_description = child_value(derivative_tag, "othDeriv", "othDesc")
            other_derivative_tag = derivative_tag.find("othDeriv")

            reference_instrument_tag = other_derivative_tag.find("descRefInstrmnt")
            reference_instrument = None
            if reference_instrument_tag:
                if reference_instrument_tag.find("indexBasketInfo"):
                    reference_instrument = ReferenceIndex.from_xml(reference_instrument_tag.find("indexBasketInfo"))
                elif reference_instrument_tag.find("nestedDerivInfo"):
                    reference_instrument = ReferenceDerivative.from_xml(reference_instrument_tag.find("nestedDerivInfo"))
                else:
                    reference_instrument = ReferenceOther.from_xml(reference_instrument_tag.find("otherRefInst"))

            maturity = child_text(other_derivative_tag, "terminationDt")
            notional_tag = other_derivative_tag.find("notionalAmts")
            notional = [el.attrs.get("amt") for el in notional_tag.find_all("notionalAmt")]
            notional_currency = [el.attrs.get("curCd") for el in notional_tag.find_all("notionalAmt")]
            delta = child_text(other_derivative_tag, "delta")
            unrealized_appreciation = child_text(other_derivative_tag, "unrealizedAppr")
            return OtherDerivative(
                **base.__dict__,
                derivative_type=derivative_type,
                derivative_type_description=derivative_type_description,
                counterparty_name=counterparty_name,
                counterparty_lei=counterparty_lei,
                reference_instrument=reference_instrument,
                maturity=maturity,
                notional=notional,
                notional_currency=notional_currency,
                delta=delta,
                unrealized_appreciation=unrealized_appreciation
            )


class ForwardFuture(Derivative):
    reference_instrument: Optional[object]
    maturity: Optional[date]
    notional: Optional[Decimal]
    derivative_currency: Optional[str]
    unrealized_appreciation: Optional[Decimal]


class Swap(Derivative):
    reference_instrument: Optional[object]
    swap_flag: bool
    maturity: date
    payment_type: str
    payment_description: Optional[str]
    payment_rate: Optional[Decimal]
    payment_index: Optional[str]
    payment_currency: Optional[str]
    payment_amount: Optional[Decimal]
    receipt_type: str
    receipt_description: Optional[str]
    receipt_rate: Optional[Decimal]
    receipt_index: Optional[str]
    receipt_currency: Optional[str]
    receipt_amount: Optional[Decimal]
    upfront_payment: Decimal
    upfront_payment_currency: str
    upfront_receipts: Decimal
    upfront_receipts_currency: str
    notional: Decimal
    derivative_currency: str
    unrealized_appreciation: Optional[Decimal]


class FXForwardOrSwap(Derivative):
    currency_amount_sold: Optional[Decimal]
    currency_sold: Optional[str]
    currency_amount_purchased: Optional[Decimal]
    currency_purchased: Optional[str]
    settlement: Optional[date]
    unrealized_appreciation: Optional[Decimal]


class Option(Derivative):
    option_type: str
    option_payoff: str
    reference_instrument: Optional[object]
    shares: Optional[Decimal]
    notional: Optional[Decimal]
    derivative_currency: Optional[str]
    exercise_price: Decimal
    exercise_currency: str
    exercise_date: date
    delta: Optional[Decimal]
    unrealized_appreciation: Optional[Decimal]


class OtherDerivative(Derivative):
    reference_instrument: Optional[object]
    maturity: date
    notional: list[Decimal]
    notional_currency: list[str]
    delta: Optional[Decimal]
    unrealized_appreciation: Optional[Decimal]


class ReferenceDerivative(BaseModel):
    derivative_type: str
    derivative_type_description: Optional[str]
    counterparty_name: Optional[str]
    counterparty_lei: Optional[str]

    @classmethod
    def from_xml(cls, tag):
        counterparty_tag = tag.find("counterparties")
        counterparty_name = child_text(counterparty_tag, "counterpartyName")
        counterparty_lei = child_text(counterparty_tag, "counterpartyLei")

        derivative_type_description = None
        if tag.find("fwdDeriv"):
            forward_tag = tag.find("fwdDeriv")

            if forward_tag.find("payOffProf"):
                derivative_type = "Forward"
                payoff_profile = child_text(forward_tag, "payOffProf")

                reference_instrument_tag = forward_tag.find("descRefInstrmnt")
                reference_instrument = None
                if reference_instrument_tag:
                    if reference_instrument_tag.find("indexBasketInfo"):
                        reference_instrument = ReferenceIndex.from_xml(reference_instrument_tag.find("indexBasketInfo"))
                    elif reference_instrument_tag.find("nestedDerivInfo"):
                        reference_instrument = ReferenceDerivative.from_xml(reference_instrument_tag.find("nestedDerivInfo"))
                    else:
                        reference_instrument = ReferenceOther.from_xml(reference_instrument_tag.find("otherRefInst"))

                maturity = child_text(forward_tag, "expDate")
                notional = child_text(forward_tag, "notionalAmt")
                derivative_currency = child_text(forward_tag, "curCd")
                return ReferenceForwardFuture(
                    derivative_type=derivative_type,
                    derivative_type_description=derivative_type_description,
                    counterparty_name=counterparty_name,
                    counterparty_lei=counterparty_lei,
                    payoff_profile=payoff_profile,
                    reference_instrument=reference_instrument,
                    maturity=maturity,
                    notional=notional,
                    derivative_currency=derivative_currency
                )

            else:
                derivative_type = "FX Forward"
                currency_amount_sold = child_text(forward_tag, "amtCurSold")
                currency_sold = child_text(forward_tag, "curSold")
                currency_amount_purchased = child_text(forward_tag, "amtCurPur")
                currency_purchased = child_text(forward_tag, "curPur")
                settlement = child_text(forward_tag, "settlementDt")
                return ReferenceFXForwardOrSwap(
                    derivative_type=derivative_type,
                    derivative_type_description=derivative_type_description,
                    counterparty_name=counterparty_name,
                    counterparty_lei=counterparty_lei,
                    currency_amount_sold=currency_amount_sold,
                    currency_sold=currency_sold,
                    currency_amount_purchased=currency_amount_purchased,
                    currency_purchased=currency_purchased,
                    settlement=settlement
                )

        elif tag.find("futrDeriv"):
            derivative_type = "Future"
            future_tag = tag.find("futrDeriv")
            payoff_profile = child_text(future_tag, "payOffProf")

            reference_instrument_tag = future_tag.find("descRefInstrmnt")
            reference_instrument = None
            if reference_instrument_tag:
                if reference_instrument_tag.find("indexBasketInfo"):
                    reference_instrument = ReferenceIndex.from_xml(reference_instrument_tag.find("indexBasketInfo"))
                elif reference_instrument_tag.find("nestedDerivInfo"):
                    reference_instrument = ReferenceDerivative.from_xml(
                        reference_instrument_tag.find("nestedDerivInfo"))
                else:
                    reference_instrument = ReferenceOther.from_xml(reference_instrument_tag.find("otherRefInst"))

            maturity = child_text(future_tag, "expDate")
            notional = child_text(future_tag, "notionalAmt")
            derivative_currency = child_text(future_tag, "curCd")
            return ReferenceForwardFuture(
                derivative_type=derivative_type,
                derivative_type_description=derivative_type_description,
                counterparty_name=counterparty_name,
                counterparty_lei=counterparty_lei,
                payoff_profile=payoff_profile,
                reference_instrument=reference_instrument,
                maturity=maturity,
                notional=notional,
                derivative_currency=derivative_currency
            )

        elif tag.find("swapDeriv"):
            swap_tag = tag.find("swapDeriv")

            if tag.find("swapFlag"):
                derivative_type = "Swap"
                swap_flag = child_text(swap_tag, "swapFlag") == "Y"
                maturity = child_text(swap_tag, "terminationDt")

                reference_instrument_tag = swap_tag.find("descRefInstrmnt")
                reference_instrument = None
                if reference_instrument_tag:
                    if reference_instrument_tag.find("indexBasketInfo"):
                        reference_instrument = ReferenceIndex.from_xml(reference_instrument_tag.find("indexBasketInfo"))
                    elif reference_instrument_tag.find("nestedDerivInfo"):
                        reference_instrument = ReferenceDerivative.from_xml(
                            reference_instrument_tag.find("nestedDerivInfo"))
                    else:
                        reference_instrument = ReferenceOther.from_xml(reference_instrument_tag.find("otherRefInst"))

                payment_index = None
                payment_rate = None
                payment_description = None
                payment_currency = None
                payment_amount = None
                if swap_tag.find("fixedPmntDesc"):
                    payment_type = child_value(swap_tag, "fixedPmntDesc", "fixedOrFloating")
                    payment_rate = child_value(swap_tag, "fixedPmntDesc", "fixedRt")
                    payment_currency = child_value(swap_tag, "fixedPmntDesc", "curCd")
                    payment_amount = child_value(swap_tag, "fixedPmntDesc", "amount")
                elif swap_tag.find("floatingPmntDesc"):
                    payment_type = child_value(swap_tag, "floatingPmntDesc", "fixedOrFloating")
                    payment_rate = child_value(swap_tag, "floatingPmntDesc", "floatingRtSpread")
                    payment_index = child_value(swap_tag, "floatingPmntDesc", "floatingRtIndex")
                    payment_currency = child_value(swap_tag, "floatingPmntDesc", "curCd")
                    payment_amount = child_value(swap_tag, "floatingPmntDesc", "pmntAmt")
                elif swap_tag.find("otherPmntDesc"):
                    payment_type = child_value(swap_tag, "otherPmntDesc", "fixedOrFloating")
                    payment_description = child_text(swap_tag, "otherPmntDesc")

                receipt_index = None
                receipt_rate = None
                receipt_description = None
                receipt_currency = None
                receipt_amount = None
                if swap_tag.find("fixedRecDesc"):
                    receipt_type = child_value(swap_tag, "fixedRecDesc", "fixedOrFloating")
                    receipt_rate = child_value(swap_tag, "fixedRecDesc", "fixedRt")
                    receipt_currency = child_value(swap_tag, "fixedRecDesc", "curCd")
                    receipt_amount = child_value(swap_tag, "fixedRecDesc", "amount")
                elif swap_tag.find("floatingRecDesc"):
                    receipt_type = child_value(swap_tag, "floatingRecDesc", "fixedOrFloating")
                    receipt_rate = child_value(swap_tag, "floatingRecDesc", "floatingRtSpread")
                    receipt_index = child_value(swap_tag, "floatingRecDesc", "floatingRtIndex")
                    receipt_currency = child_value(swap_tag, "floatingRecDesc", "curCd")
                    receipt_amount = child_value(swap_tag, "floatingRecDesc", "pmntAmt")
                elif swap_tag.find("otherRecDesc"):
                    receipt_type = child_value(swap_tag, "otherRecDesc", "fixedOrFloating")
                    receipt_description = child_text(swap_tag, "otherRecDesc")

                upfront_payment = child_text(swap_tag, "upfrontPmnt")
                upfront_payment_currency = child_text(swap_tag, "pmntCurCd")
                upfront_receipts = child_text(swap_tag, "upfrontRcpt")
                upfront_receipts_currency = child_text(swap_tag, "rcptCurCd")
                notional = child_text(swap_tag, "notionalAmt")
                derivative_currency = child_text(swap_tag, "curCd")
                return ReferenceSwap(
                    derivative_type=derivative_type,
                    derivative_type_description=derivative_type_description,
                    counterparty_name=counterparty_name,
                    counterparty_lei=counterparty_lei,
                    reference_instrument=reference_instrument,
                    swap_flag=swap_flag,
                    maturity=maturity,
                    payment_type=payment_type,
                    payment_description=payment_description,
                    payment_rate=payment_rate,
                    payment_index=payment_index,
                    payment_currency=payment_currency,
                    payment_amount=payment_amount,
                    receipt_type=receipt_type,
                    receipt_description=receipt_description,
                    receipt_rate=receipt_rate,
                    receipt_index=receipt_index,
                    receipt_currency=receipt_currency,
                    receipt_amount=receipt_amount,
                    upfront_payment=upfront_payment,
                    upfront_payment_currency=upfront_payment_currency,
                    upfront_receipts=upfront_receipts,
                    upfront_receipts_currency=upfront_receipts_currency,
                    notional=notional,
                    derivative_currency=derivative_currency
                )
            else:
                derivative_type = "FX Swap"
                currency_amount_sold = child_text(swap_tag, "amtCurSold")
                currency_sold = child_text(swap_tag, "curSold")
                currency_amount_purchased = child_text(swap_tag, "amtCurPur")
                currency_purchased = child_text(swap_tag, "curPur")
                settlement = child_text(swap_tag, "settlementDt")
                return ReferenceFXForwardOrSwap(
                    derivative_type=derivative_type,
                    derivative_type_description=derivative_type_description,
                    counterparty_name=counterparty_name,
                    counterparty_lei=counterparty_lei,
                    currency_amount_sold=currency_amount_sold,
                    currency_sold=currency_sold,
                    currency_amount_purchased=currency_amount_purchased,
                    currency_purchased=currency_purchased,
                    settlement=settlement
                )

        elif tag.find("optionSwaptionWarrantDeriv"):
            option_tag = tag.find("optionSwaptionWarrantDeriv")
            derivative_type = {"OPT": "Option", "SWO": "Swaption", "WAR": "Warrant"}.get(
                child_value(tag, "optionSwaptionWarrantDeriv", "derivCat")
            )
            option_type = child_text(option_tag, "putOrCall")
            option_payoff = child_text(option_tag, "writtenOrPur")

            reference_instrument_tag = option_tag.find("descRefInstrmnt")
            reference_instrument = None
            if reference_instrument_tag:
                if reference_instrument_tag.find("indexBasketInfo"):
                    reference_instrument = ReferenceIndex.from_xml(reference_instrument_tag.find("indexBasketInfo"))
                elif reference_instrument_tag.find("nestedDerivInfo"):
                    reference_instrument = ReferenceDerivative.from_xml(
                        reference_instrument_tag.find("nestedDerivInfo"))
                else:
                    reference_instrument = ReferenceOther.from_xml(reference_instrument_tag.find("otherRefInst"))

            shares = child_text(option_tag, "shareNo")
            notional = child_text(option_tag, "principalAmt")
            derivative_currency = child_text(option_tag, "curCd")
            exercise_price = child_text(option_tag, "exercisePrice")
            exercise_currency = child_text(option_tag, "exercisePriceCurCd")
            exercise_date = child_text(option_tag, "expDt")
            delta = child_text(option_tag, "delta")
            return ReferenceOption(
                derivative_type=derivative_type,
                derivative_type_description=derivative_type_description,
                counterparty_name=counterparty_name,
                counterparty_lei=counterparty_lei,
                option_type=option_type,
                option_payoff=option_payoff,
                reference_instrument=reference_instrument,
                shares=shares,
                notional=notional,
                derivative_currency=derivative_currency,
                exercise_price=exercise_price,
                exercise_currency=exercise_currency,
                exercise_date=exercise_date,
                delta=delta
            )

        elif tag.find("othDeriv"):
            derivative_type = "Other"
            derivative_type_description = child_value(tag, "othDeriv", "othDesc")
            other_derivative_tag = tag.find("othDeriv")

            reference_instrument_tag = other_derivative_tag.find("descRefInstrmnt")
            reference_instrument = None
            if reference_instrument_tag:
                if reference_instrument_tag.find("indexBasketInfo"):
                    reference_instrument = ReferenceIndex.from_xml(reference_instrument_tag.find("indexBasketInfo"))
                elif reference_instrument_tag.find("nestedDerivInfo"):
                    reference_instrument = ReferenceDerivative.from_xml(
                        reference_instrument_tag.find("nestedDerivInfo"))
                else:
                    reference_instrument = ReferenceOther.from_xml(reference_instrument_tag.find("otherRefInst"))

            maturity = child_text(other_derivative_tag, "terminationDt")
            notional_tag = other_derivative_tag.find("notionalAmts")
            notional = [el.attrs.get("amt") for el in notional_tag.find_all("notionalAmt")]
            notional_currency = [el.attrs.get("curCd") for el in notional_tag.find_all("notionalAmt")]
            delta = child_text(other_derivative_tag, "delta")
            return ReferenceOtherDerivative(
                derivative_type=derivative_type,
                derivative_type_description=derivative_type_description,
                counterparty_name=counterparty_name,
                counterparty_lei=counterparty_lei,
                reference_instrument=reference_instrument,
                maturity=maturity,
                notional=notional,
                notional_currency=notional_currency,
                delta=delta,
                unrealized_appreciation=None
            )


class ReferenceForwardFuture(ReferenceDerivative):
    derivativepayoff_profile: Optional[str]
    reference_instrument: Optional[object]
    maturity: Optional[date]
    notional: Optional[Decimal]
    derivative_currency: Optional[str]


class ReferenceSwap(ReferenceDerivative):
    reference_instrument: Optional[object]
    swap_flag: bool
    maturity: date
    payment_type: str
    payment_description: Optional[str]
    payment_rate: Optional[Decimal]
    payment_index: Optional[str]
    payment_currency: Optional[str]
    payment_amount: Optional[Decimal]
    receipt_type: str
    receipt_description: Optional[str]
    receipt_rate: Optional[Decimal]
    receipt_index: Optional[str]
    receipt_currency: Optional[str]
    receipt_amount: Optional[Decimal]
    upfront_payment: Decimal
    upfront_payment_currency: str
    upfront_receipts: Decimal
    upfront_receipts_currency: str
    notional: Decimal
    derivative_currency: str


class ReferenceFXForwardOrSwap(ReferenceDerivative):
    currency_amount_sold: Optional[Decimal]
    currency_sold: Optional[str]
    currency_amount_purchased: Optional[Decimal]
    currency_purchased: Optional[str]
    settlement: Optional[date]


class ReferenceOption(ReferenceDerivative):
    option_type: str
    option_payoff: str
    reference_instrument: Optional[object]
    shares: Optional[Decimal]
    notional: Optional[Decimal]
    derivative_currency: Optional[str]
    exercise_price: Decimal
    exercise_currency: str
    exercise_date: date
    delta: Optional[Decimal]


class ReferenceOtherDerivative(ReferenceDerivative):
    reference_instrument: Optional[object]
    maturity: date
    notional: list[Decimal]
    notional_currency: list[str]
    delta: Optional[Decimal]


class ReferenceIndexComponents(BaseModel):
    name: str
    cusip: Optional[str]
    isin: Optional[str]
    ticker: Optional[str]
    other_identifier_name: Optional[str]
    other_identifier: Optional[str]
    balance: Decimal
    currency: Optional[str]
    issue_currency: str
    value: Decimal

    @classmethod
    def from_xml(cls, tag):
        name = child_text(tag, "othIndName")
        identifiers_tag = tag.find("identifiers")
        cusip = child_text(identifiers_tag, "cusip")
        isin = child_text(identifiers_tag, "isin")
        ticker = child_text(identifiers_tag, "ticker")
        other_identifier_name = child_value(identifiers_tag, "other", "otherDesc")
        other_identifier = child_value(identifiers_tag, "other", "value")
        balance = child_text(tag, "othIndNotAmt")
        currency = child_text(tag, "othIndCurCd")
        value = child_text(tag, "othIndValue")
        issue_currency = child_text(tag, "othIndIssCurCd")
        if currency is None:
            currency = issue_currency
        return cls(
            name=name,
            cusip=cusip,
            isin=isin,
            ticker=ticker,
            other_identifier_name=other_identifier_name,
            other_identifier=other_identifier,
            balance=balance,
            currency=currency,
            value=value,
            issue_currency=issue_currency
        )


class ReferenceIndex(BaseModel):
    name: Optional[str]
    identifier: Optional[str]
    description: Optional[str]
    components: Optional[list[ReferenceIndexComponents]]

    @classmethod
    def from_xml(cls, tag):
        name = child_text(tag, "indexName")
        identifier = child_text(tag, "indexIdentifier")
        description = child_text(tag, "narrativeDesc")
        components = None
        component_tag = tag.find("components")
        if component_tag:
            components = [ReferenceIndexComponents.from_xml(instrument_tag) for instrument_tag in component_tag.find_all("component")]
        return cls(
            name=name,
            identifier=identifier,
            description=description,
            components=components
        )


class ReferenceOther(BaseModel):
    issuer: Optional[str]
    name: Optional[str]
    cusip: Optional[str]
    isin: Optional[str]
    ticker: Optional[str]
    other_identifier_name: Optional[str]
    other_identifier: Optional[str]

    @classmethod
    def from_xml(cls, tag):
        issuer = child_text(tag, "issuerName")
        name = child_text(tag, "issueTitle")
        identifier_tag = tag.find("identifiers")
        cusip = child_text(identifier_tag, "cusip")
        isin = child_text(identifier_tag, "isin")
        ticker = child_text(identifier_tag, "ticker")
        other_identifier_name = child_value(identifier_tag, "other", "otherDesc")
        other_identifier = child_value(identifier_tag, "other")
        return cls(
            issuer=issuer,
            name=name,
            cusip=cusip,
            isin=isin,
            ticker=ticker,
            other_identifier_name=other_identifier_name,
            other_identifier=other_identifier
        )
