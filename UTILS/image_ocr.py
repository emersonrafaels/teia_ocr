"""

    FUNÇÕES PARA REALIZAÇÃO DE OCR DE UMA IMAGEM.
    O OCR PERMITIRÁ TRANSCREVER A IMAGEM.
    CONVERSÃO IMAGEM PARA TEXTO.

    # Arguments
        object                  - Required : Imagem para aplicação do OCR (String | Object)
    # Returns
        texto_obtido            - Required : Texto obtido após aplicação da técnica de OCR (String)

"""

__version__ = "1.0"
__author__ = """Emerson V. Rafael (EMERVIN)"""
__data_atualizacao__ = "28/10/2021"


from inspect import stack

import cv2
import pandas as pd
import pytesseract
from dotenv import load_dotenv

# LOADING ENV FILE
load_dotenv()

from dynaconf import settings

from UTILS.generic_functions import converte_int
from UTILS.image_view import image_view_functions
from UTILS.image_convert_format import orchestra_read_image
from UTILS import execute_log


class ocr_functions:

    """

    FUNÇÕES PARA REALIZAÇÃO DE OCR DE UMA IMAGEM.
    O OCR PERMITIRÁ TRANSCREVER A IMAGEM.
    CONVERSÃO IMAGEM PARA TEXTO.

    # Arguments

        imagem_atual                          - Required : Imagem para aplicação do OCR (String | Object)
        lang_padrao                           - Optional : Linguagem que será utilizada no OCR (String)
        config_tesseract_psm                  - Optional : Configuração do tesseract.
                                                           É possível passar um valor
                                                           específico de PSM. (String | Integer)
        config_tesseract_oem                  - Optional : Configuração do tesseract.
                                                           É possível passar um valor
                                                           específico de OEM. (String | Integer)
        tipo_retorno_ocr_input                - Optional : Tipo de retorno do ocr desejado (String)
        tipo_output_type_image_data           - Optional : Tipo de formato do output do ocr completo (String)

    # Returns
        texto_ocr                             - Required : Texto obtido após aplicação da técnica de OCR (String)

    """

    def __init__(
        self,
        lang_tesseract_default=settings.TESSERACT_LANG,
        config_tesseract_psm=settings.TESSERACT_PSM,
        config_tesseract_oem=settings.TESSERACT_OEM,
        type_return_ocr_input=settings.TYPE_OCR,
        view_ocr_complete=settings.VIEW_OCR_COMPLETE,
        type_output_image_data=settings.OUTPUT_TYPE_IMAGE_DATA,
    ):
        # 1 - LINGUAGEM PADRÃO DO OCR
        self.lang_tesseract_default = lang_tesseract_default

        # 2 - CONFIG PSM DO TESSERACT
        self.config_tesseract_psm = config_tesseract_psm

        # 3 - CONFIG OEM DO TESSERACT
        self.config_tesseract_oem = config_tesseract_oem

        # 4 - LISTA DE TIPOS DE RETORNO DO OCR
        self.list_types_return_ocr = ["TEXTO", "COMPLETO"]

        # 5 - TIPO DE RETORNO DO OCR SELECIONADA
        self.return_type_ocr = str(type_return_ocr_input).upper()
        self.view_ocr_complete = view_ocr_complete

        # 6 - TIPO DE FORMATO DO OUTPUT QUANDO UTILIZADO OCR COMPLETO
        self.OUTPUT_TYPE_IMAGE_DATA = str(type_output_image_data).upper()

    def tesseract_lang_availables(self):
        """

        OBTÉM A LISTA DE LINGUAGENS DISPONÍVEIS.
        UTILIZA TESSERACT - GET LANGUAGES

        # Arguments

        # Returns
            validator                        - Required : validator de execução da função (Boolean)
            list_tesseract_langs       - Required : Lista de lang disponíveis (List)

        """

        # INICIANDO O validator
        validator = False

        # INICIANDO A VARIÁVEL DE LINGUAGENS DISPONÍVEIS
        list_tesseract_langs = []

        try:
            list_tesseract_langs = pytesseract.get_languages(config="")

            validator = True

        except Exception as ex:
            print("A LINGUAGEM SELECIONADA NÃO ESTÁ DISPONÍVEL")
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return list_tesseract_langs

    @staticmethod
    def get_tesseract_psm_oem(value_config_psm, value_config_oem):
        """
        Modos de segmentação de página:
           0 Orientação e detecção de script (OSD) apenas.
           1 Segmentação de página automática com OSD.
           2 Segmentação automática de página, mas sem OSD ou OCR.
           3 Segmentação de página totalmente automática, mas sem OSD. (Padrão)
           4 Considere uma única coluna de texto de tamanhos variáveis.
           5 Considere um único bloco uniforme de texto alinhado verticalmente.
           6 Considere um único bloco de texto uniforme.
           7 Trate a imagem como uma única linha de texto.
           8 Trate a imagem como uma única palavra.
           9 Trate a imagem como uma única palavra em um círculo.
          10 Trate a imagem como um único caractere.
          11 Texto esparso. Encontre o máximo de texto possível em nenhuma ordem específica.
          12 Texto esparso com OSD.
          13 Linha bruta. Trate a imagem como uma única linha de texto,
             contornando hacks que são específicos do Tesseract.
        """

        """
        Modo do motor:
            0 Legacy Engine somente
            1 Neural Nets LSTM Engine somente
            2 Legacy + LSTM engines
            3 Padrão, o que estiver disponível
        """

        # INICIANDO O validator
        validator = False

        # INICIANDO A VARIÁVEL DE CONFIG PSM
        value_psm_oem_tesseract = "tessdata"

        # CONVERTENDO OS VALORES PARA INT

        try:
            # VERIFICANDO SE O VALOR DE PSM E OEM ENCONTRA-SE DENTRE AS CONFIGS
            if converte_int(value_config_psm) in range(14) and converte_int(
                value_config_oem
            ) in range(4):
                # CONVERTENDO O VALOR DO ARGUMENTO (INT) PARA
                # FORMA ESPERADA PELO TESSERACT

                value_psm_oem_tesseract = "tessdata --psm {} --oem {}".format(
                    str(value_config_psm), str(value_config_oem)
                )

                validator = True

        except Exception as ex:
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return value_psm_oem_tesseract

    @staticmethod
    def get_tesseract_output_type_image_data(value_config_output_type_image_data):
        """

        EXISTEM DUAS PRINCIPAIS FORMAS DE OUTPUT:
            1) DATAFRAME
            2) DICT

        """

        # INICIANDO O validator
        validator = False

        # INICIANDO A VARIÁVEL DE OUTPUT DO IMAGE DATA
        value_output_type_image_data = pytesseract.Output.DATAFRAME

        try:
            # VERIFICANDO SE O VALOR DE PSM E OEM ENCONTRA-SE DENTRE AS CONFIGS
            if value_config_output_type_image_data == "DATAFRAME":
                value_output_type_image_data = pytesseract.Output.DATAFRAME
            elif value_config_output_type_image_data == "DICT":
                value_output_type_image_data = pytesseract.Output.DICT
            else:
                value_output_type_image_data = pytesseract.Output.DATAFRAME

                validator = True

        except Exception as ex:
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return value_output_type_image_data

    def get_image_orientation(self, image_dir=None):
        """

        DETECTA E RETORNA A ORIENTAÇÃO DA IMAGEM.


        # Arguments
            image_dir                   - Required : Caminho da imagem atual (String)
        # Returns
            validator                   - Required : validator de execução da função (Boolean)
            orientation_value            - Required : Propriedades de orientação da imagem (String)

        """

        """ Page number,
            Orientation in degrees,
            Rotate,
            Orientation confidence,
            Script,
            Script confidence
        """

        # INICIANDO O validator
        validator = False

        # INICIANDO A VARIÁVEL QUE ARMAZENARÁ A ORIENTAÇÃO
        orientation_value = {}

        # VERIFICANDO SE UMA NOVA IMAGEM FOI PASSADA COMO ARGUMENTO DA CHAMADA DA FUNÇÃO
        if image_dir is None:
            image_dir = self.image_ocr

        try:
            # ORQUESTRANDO A LEITURA DA IMAGEM
            image_ocr = orchestra_read_image(image_dir)

            orientation_value = pytesseract.image_to_osd(image_ocr)
            validator = True

        except Exception as ex:
            print("NÃO FOI POSSÍVEL DETECTAR A ORIENTAÇÃO DA PÁGINA")
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return validator, orientation_value

    def set_config_tesseract(self):
        """

        CONFIGURA AS OPÇÕES DE PSM E OEM PARA O USO DO TESSERACT


        # Arguments

        # Returns
            validator                   - Required : validator de execução da função (Boolean)

        """

        # INICIANDO O validator
        validator = False

        try:
            # VERIFICANDO SE A LINGUAGEM SELECIONADA, ESTÁ DISPONÍVEL
            if (
                self.lang_tesseract_default
                not in ocr_functions.tesseract_lang_availables(self)
            ):
                # COMO A LINGUAGEM SELECIONADA NÃO ESTÁ DISPONÍVEL
                # UTILIZAREMOS A VERSÃO ENGLISH
                self.lang_tesseract_default = "eng"

            # VERIFICANDO A CONFIGURAÇÃO PSM - OEM
            self.config_tesseract_psm_oem = ocr_functions.get_tesseract_psm_oem(
                self.config_tesseract_psm, self.config_tesseract_oem
            )

            validator = True

        except Exception as ex:
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return validator

    @staticmethod
    def convert_result_ocr_complete(input_result_ocr):
        """

        APÓS A REALIZAÇÃO DO OCR COMPLETO (POR BOUNDING BOX),
        ESSA FUNÇÃO CONCATENA O TEXTO, RESULTANDO EM UMA ÚNICA STRING.

        CONVERTE O RESULTADO DO OCR COMPLETO (IMAGE DATA)
        EM UM FORMATO LEGÍVEL:
            1) TEXT: STRING CONTENDO O TEXTO DO OCR OBTIDO
            2) INFOS_OCR: DATAFRAME CONTENDO AS INFORMAÇÕES DO OCR (IMAGE_DATA)

        # Arguments
            input_result_ocr              - Required : Informações obtidas no OCR (DataFrame | Dict)
        # Returns
            list_result                   - Required : Texto resultante (List)
            text_result                   - Required : Texto resultante (String)
            infos_ocr                     - Required : Informações obtidas no OCR (DataFrame)

        """

        # INICIANDO AS VARIÁVEIS QUE ARMAZENARÃO O RESULTADO FINAL
        string_atual = ""
        list_result = []
        infos_ocr = pd.DataFrame()

        # VERIFICANDO QUAL O TIPO DE DADO DO INPUT DE RESULTADO DO OCR
        if isinstance(input_result_ocr, pd.DataFrame):
            # O INPUT É UM DATAFRAME
            result_ocr = " ".join(list(input_result_ocr["text"].fillna(" ")))

            # MANTEMOS O INFO_OCR COMO DATAFRAME
            infos_ocr = input_result_ocr
        else:
            # O INPUT É UM DATAFRAME
            result_ocr = " ".join(input_result_ocr["text"])

            # CONVERTEMOS O INFO_OCR PARA DATAFRAME
            infos_ocr = pd.DataFrame(input_result_ocr)

        # PERCORRENDO O TEXTO CONCATENADO E REALIZANDO AS QUEBRAS DE LINHA
        for value in str(result_ocr).strip().split(" "):
            text_valid = False

            if str(value).strip() != "":
                string_atual = string_atual + " " + value
                text_valid = True
            else:
                text_valid = False
                list_result.append(str(string_atual).strip())
                string_atual = ""

        if list_result:
            # FORMATANDO PARA RESULTADO EM FORMATO TEXTO
            text_result = "\n".join(list_result)
        else:
            # FORMATANDO PARA RESULTADO EM FORMATO TEXTO
            text_result = "\n".join(string_atual)

        # RETORNANDO O RESULTADO DO OCR
        # LISTA CONTENDO CADA UM DOS TEXTOS
        # TEXTO CONTENDO O TEXTO COM QUEBRA DE LINHAS
        # DATAFRAME COMPLETO CONTENDO AS INFORMAÇÕES DO OCR
        return list_result, text_result, infos_ocr

    def view_bounding_box_ocr_complete(self, image, info_ocr):
        """

        FUNÇÃO PARA VISUALIZAR OS BOUNDING BOX E TEXTOS OBTIDOS
        APÓS A APLICAÇÃO DO OCR COMPLETO(image_to_data).

        # Arguments
            image                   - Required : Imagem para visualização do ocr (Object)
            info_ocr                - Required : Informações obtidas no OCR (Dict | DataFrame)

        # Returns

        """

        try:
            # CRIANDO UMA CÓPIA DA IMAGEM
            img_copy = image.copy()

            for i in range(len(info_ocr["text"])):
                # DEFININDO A FONTE A SER UTILIZADA
                font = "UTILS/FONTS/calibri.ttf"

                # REALIZANDO A CRIAÇÃO DA CAIXA DE TEXTO SOBRE O TEXTO
                x, y, img_copy = image_view_functions.create_bounding_box(
                    img=img_copy, bounding_positions=info_ocr.iloc[i]
                )

                # INSERINDO O TEXTO SOBRE A CAIXA RETANGULAR (TOP - 10)
                img_copy = image_view_functions.put_text_image(
                    img=img_copy,
                    text=info_ocr["text"][i],
                    x_position=x + 20,
                    y_position=y + 20,
                    font=font,
                )

            image_view_functions.view_image(img_copy)

        except Exception as ex:
            print(ex)

    def execute_ocr_return_complete(self, image):
        """

        OBTÉM AS INFORMAÇÕES DA IMAGEM APÓS APLICAÇÃO DO OCR.
        ESSA FUNÇÃO TRAZ TODAS AS INFORMAÇÕES CONTIDAS NO TEXTO ABAIXO.
        POSIÇÕES DOS TEXTOS ENCONTRATOS, NÍVEL DE CONFIANÇA E TEXTOS.


        # Arguments
            image                       - Required : Imagem para aplicação do ocr (Object)

        # Returns
            validator                   - Required : validator de execução da função (Boolean)
            infos_ocr                   - Required : Informações obtidas no OCR (Dict | DataFrame)

        """

        """
        - lock_num = Número do bloco atual. Quando o tesseract faz o OCR,
        ele divide a imagem em várias regiões, o que pode variar de
        acordo com os parametros do PSM e também outros critérios próprios do algoritmo.
        Cada bloco é uma região

        - conf = confiança da predição (de 0 a 100. -1 significa que não foi reconhecido texto)

        - height = altura do bloco de texto detectada (ou seja, da caixa delimitadora)

        - left = coordenada x onde inicia a caixa delimitadora

        - level = o level (nível) corresponde à categoria do bloco detectado. são 5 valores possiveis:
          1. página
          2. bloco
          3. parágrafo
          4. linha
          5. palavra

        Portanto, se foi retornado o valor 5 significa que o bloco detectado é texto, se foi 4 significa que o que foi detectado é uma linha

        - line_num = número da linha do que foi detectado (inicia com 0)

        - page_num = o índice da página onde o item foi detectado. Na maioria dos casos sempre haverá uma página só

        - text = o resultado do reconhecimento

        - top = coordenada y onde a caixa delimitadora começa

        - width = largura do bloco de texto atual detectado

        - word_num = numero da palavra (indice) dentro do bloco atual"""

        # INICIANDO O validator
        validator = False

        # INICIANDO A VARIÁVEL INFORMAÇÕES DE OCR
        infos_ocr = {}

        # OBTENDO A CONFIG DE FORMATO DO OUTPUT
        self.OUTPUT_TYPE_IMAGE_DATA = (
            ocr_functions.get_tesseract_output_type_image_data(
                self.OUTPUT_TYPE_IMAGE_DATA
            )
        )

        try:
            # REALIZANDO O OCR SOBRE A IMAGEM
            infos_ocr = pytesseract.image_to_data(
                image,
                lang=self.lang_tesseract_default,
                config=self.config_tesseract_psm,
                output_type=self.OUTPUT_TYPE_IMAGE_DATA,
            )

            validator = True

        except Exception as ex:
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return validator, infos_ocr

    def execute_ocr_return_text(self, image):
        """
        REALIZA A APLICAÇÃO DE OCR SOBRE UMA IMAGEM.
        O OCR PERMITIRÁ TRANSCREVER A IMAGEM.
        CONVERSÃO IMAGEM PARA TEXTO.

        # Arguments
            image                       - Required : Imagem para aplicação do ocr (Object)

        # Returns
            validator                   - Required : validator de execução da função (Boolean)
            texto                       - Required : Texto obtido (String)
        """

        # INICIANDO O validator
        validator = False

        # INICIANDO A VARIÁVEL TEXTO
        result_text = ""

        try:
            # REALIZANDO O OCR SOBRE A IMAGEM
            result_text = pytesseract.image_to_string(
                image,
                lang=self.lang_tesseract_default,
                config=self.config_tesseract_psm,
            )

            validator = True

        except Exception as ex:
            print("ERRO NA FUNÇÃO: {} - {}".format(stack()[0][3], ex))

        return validator, result_text

    def orchestra_type_ocr(self, imagem_rgb):
        """

        ORQUESTRA A APLICAÇÃO DE OCR SOBRE UMA IMAGEM.
        SELECIONA QUAL FUNÇÃO SERÁ UTILIZADA.
        UMA OPÇÃO RETORNARÁ APENAS O RESULTADO TEXTUAL DO OCR.
        OUTRA OPÇÃO RETORNARÁ TODAS AS INFORMAÇÕES DO OCR.


        # Arguments
            imagem_rgb                  - Required : Imagem para aplicação do ocr (Object)

        # Returns
            validator                   - Required : validator de execução da função (Boolean)
            retorno_ocr                 - Required : Retorno do OCR (String | Dict)

        """

        # INICIANDO AS VARIÁVEIS DE RETORNO
        validator = False
        retorno_ocr = None

        if self.return_type_ocr == self.list_types_return_ocr[0]:
            # O RETORNO SERÁ APENAS O TEXTUAL
            validator, retorno_ocr = ocr_functions.execute_ocr_return_text(
                self, imagem_rgb
            )

        elif self.return_type_ocr == self.list_types_return_ocr[1]:
            # O RETORNO SERÁ UM DICT CONTENDO TODAS AS INFORMAÇÕES
            validator, retorno_ocr = ocr_functions.execute_ocr_return_complete(
                self, imagem_rgb
            )

        else:
            print("NÃO FOI INFORMADA NENHUMA OPÇÃO VÁLIDA DE RETORNO DO OCR")

        return validator, retorno_ocr

    def orchestra_execute_ocr(self, image, view_image=False):
        # INICIANDO O validator
        validator = False

        # OBTENDO A ORIENTAÇÃO DA IMAGEM
        # validator, resultado_orientacao = ocr_functions.obtem_orientacao_imagem(self, image)

        # REALIZANDO A LEITURA DA IMAGEM
        img_ocr = orchestra_read_image(image)

        if view_image:
            image_view_functions.view_image_with_coordinates(img_ocr)

        # DEFININDO AS CONFIGURAÇÕES DO OCR - TESSERACT
        validator = ocr_functions.set_config_tesseract(self)

        validator, retorno_ocr = ocr_functions.orchestra_type_ocr(self, img_ocr)

        if validator and self.return_type_ocr == "COMPLETO" and self.view_ocr_complete:
            ocr_functions.view_bounding_box_ocr_complete(
                self, image=img_ocr, info_ocr=retorno_ocr
            )

        if validator is False:
            execute_log.error("NÃO FOI POSSÍVEL APLICAR O OCR")
        else:
            execute_log.info("OCR EXECUTADO COM SUCESSO")

        return retorno_ocr
