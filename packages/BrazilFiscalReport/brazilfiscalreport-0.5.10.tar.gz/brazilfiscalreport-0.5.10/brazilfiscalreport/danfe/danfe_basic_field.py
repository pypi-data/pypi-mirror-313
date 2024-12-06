from typing import Optional

from fpdf import FPDF
from fpdf.enums import MethodReturnValue

from brazilfiscalreport.pdf_element import Element

from .danfe_conf import (
    DEFAULT_FIELD_HEIGHT,
    DEFAULT_HEIGHT_FONT_CONTENT,
)

FONT_SIZE_DESC = 5
H_FONT_DESC = 2.8
FONT_SIZE_CONT = 7


class DanfeBasicField(Element):
    def __init__(
        self,
        description: str,
        content: str,
        pdf: FPDF,
        type: Optional[str] = "",
        border: str = "0",
        new_x: str = "RIGHT",
        new_y: str = "TOP",
        w: float = None,
        h: float = None,
        x: float = None,
        y: float = None,
    ) -> None:
        h = h if h else DEFAULT_FIELD_HEIGHT
        super().__init__(
            w=w, h=h, pdf=pdf, border=border, new_x=new_x, new_y=new_y, x=x, y=y
        )
        self.description = description
        self.content = content
        self.type = type if type is not None else ""
        self._content_lines = []
        self._max_content_lines = 0

    def get_content_lines(self):
        return self._content_lines

    def get_max_content_lines(self):
        return self._max_content_lines

    def render(self):
        super().render()
        pdf = self.pdf

        pdf.set_xy(x=self.x, y=self.y)

        # Description Cell
        pdf.set_font(pdf.default_font, "", FONT_SIZE_DESC)
        pdf.cell(
            w=self.w,
            h=H_FONT_DESC,
            text=self.description,
            new_x="LEFT",
            new_y="NEXT",
            align="L",
        )

        if self.type in ["protocolo", "chave_acesso"]:
            pdf.set_font(pdf.default_font, "B", FONT_SIZE_CONT)
            align = "C"
        else:
            pdf.set_font(pdf.default_font, "", FONT_SIZE_CONT)
            align = "R" if self.type == "number" else "L"
        self._content_lines = pdf.multi_cell(
            w=self.w,
            h=DEFAULT_HEIGHT_FONT_CONTENT,
            text=self.content or "",
            align=align,
            output=MethodReturnValue.LINES,
        )
        content_height = self.h - H_FONT_DESC
        self._max_content_lines = int(content_height // DEFAULT_HEIGHT_FONT_CONTENT)
