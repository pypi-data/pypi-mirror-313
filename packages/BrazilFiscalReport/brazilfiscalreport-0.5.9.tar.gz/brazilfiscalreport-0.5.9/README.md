[![image](https://github.com/engenere/BrazilFiscalReport/workflows/tests/badge.svg)](https://github.com/Engenere/BrazilFiscalReport/actions)
[![image](https://codecov.io/gh/engenere/BrazilFiscalReport/branch/main/graph/badge.svg)](https://app.codecov.io/gh/Engenere/BrazilFiscalReport)
[![image](https://img.shields.io/github/languages/top/Engenere/brazilfiscalreport)](https://pypi.org/project/BrazilFiscalReport/)
[![image](https://img.shields.io/pypi/v/brazilfiscalreport.svg)](https://pypi.org/project/BrazilFiscalReport/)
[![image](https://img.shields.io/pypi/l/brazilfiscalreport)](https://github.com/Engenere/BrazilFiscalReport/blob/main/LICENSE)
![beta](https://img.shields.io/badge/status-beta-orange)
# Brazil Fiscal Report

Python library for generating Brazilian auxiliary fiscal documents in PDF from XML documents.

## Supported Documents 📄

- **DANFE** - Documento Auxiliar da Nota Fiscal Eletrônica (NF-e)
- **DACCe** - Documento Auxiliar da Carta de Correção Eletrônica (CC-e)
- **DACTE** - Documento Auxiliar do Conhecimento de Transporte Eletrônico (CT-e)
- **DAMDFE** - Documento Auxiliar do Manifesto Eletrônico de Documentos Fiscais (MDF-e)

## Beta Stage Notice 🚧

This library is currently in the beta stage of development. While it has many of the intended features implemented, it is still undergoing testing and improvements. Users should note that during this phase, functionality may change and some instability may occur. We welcome feedback on any issues or suggestions for enhancements. Use in production environments should be approached with caution.

Check the [documentation](https://engenere.github.io/BrazilFiscalReport/) for more ✨✨✨

## Dependencies 🛠️

- [FPDF2](https://github.com/py-pdf/fpdf2) - PDF creation library for Python
- phonenumbers
- python-barcode
- qrcode (only required for DACTE)

## To install 🔧

```bash
pip install brazilfiscalreport
```

## Installing DACTE with Dependencies
If you specifically need the DACTE functionality, you can install it along with its required dependencies using:

```bash
pip install brazilfiscalreport[dacte]
```

### Installing CLI with Dependencies
If you specifically need the CLI functionality, you can install it along with its required dependencies using:

```bash
pip install brazilfiscalreport[cli]
```

## Credits 🙌
This is a fork of the [nfe_utils](https://github.com/edsonbernar/nfe_utils) project, originally created by [Edson Bernardino](https://github.com/edsonbernar).

## Maintainer 🛠️
[![Engenere](https://storage.googleapis.com/eng-imagens/logo-fundo-preto.webp)]([#](https://engenere.one/))
