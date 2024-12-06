from dataclasses import dataclass, field
from enum import Enum
from io import BytesIO
from numbers import Number
from typing import Union


class TaxConfiguration(Enum):
    STANDARD_ICMS_IPI = "Standard ICMS and IPI"
    ICMS_ST = "ICMS ST only"
    WITHOUT_IPI = "Without IPI fields"


class InvoiceDisplay(Enum):
    DUPLICATES_ONLY = "Duplicatas Only"
    FULL_DETAILS = "Full Details"


class FontType(Enum):
    COURIER = "Courier"
    TIMES = "Times"


@dataclass
class Margins:
    top: Number = 5
    right: Number = 5
    bottom: Number = 5
    left: Number = 5


@dataclass
class DecimalConfig:
    price_precision: int = 4
    quantity_precision: int = 4


class ReceiptPosition(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"


@dataclass
class ProductDescriptionConfig:
    display_branch: bool = False
    branch_info_prefix: str = ""
    display_additional_info: bool = True


@dataclass
class DanfeConfig:
    logo: Union[str, BytesIO, bytes] = None
    margins: Margins = field(default_factory=Margins)
    receipt_pos: ReceiptPosition = ReceiptPosition.TOP
    decimal_config: DecimalConfig = field(default_factory=DecimalConfig)
    tax_configuration: TaxConfiguration = TaxConfiguration.STANDARD_ICMS_IPI
    invoice_display: InvoiceDisplay = InvoiceDisplay.FULL_DETAILS
    font_type: FontType = FontType.TIMES
    display_pis_cofins: bool = False
    product_description_config: ProductDescriptionConfig = field(
        default_factory=ProductDescriptionConfig
    )
