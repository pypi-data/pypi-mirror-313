from brazilfiscalreport.dacce import DaCCe
from tests.conftest import assert_pdf_equal, get_pdf_output_path


def test_dacce(tmp_path, load_xml, logo_path):
    emitente = {
        "nome": "EMPRESA LTDA",
        "end": "AV. TEST, 100",
        "bairro": "TEST",
        "cep": "88888-88",
        "cidade": "SÃO PAULO",
        "uf": "SP",
        "fone": "(11) 1234-5678",
    }
    xm_content = load_xml("xml_cce_1.xml")

    pdf_cce = DaCCe(xml=xm_content, emitente=emitente, image=logo_path)
    pdf_path = get_pdf_output_path("dacce", "cce")
    assert_pdf_equal(pdf_cce, pdf_path, tmp_path)
