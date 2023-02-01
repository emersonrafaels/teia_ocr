from UTILS.image_ocr import ocr_functions


def execute_ocr(image_input: str, view_image: bool) -> str:
    """

    INSTANCIA A CLASSE QUE EXECUTA O OCR SOBRE UMA ÚNICA IMAGEM.

    DEVE RECEBER UMA IMAGEM (FILEPATH) E RETORNAR
    UM TEXTO (OCR) OBTIDO

    # Arguments
        image_input            - Required : Imagem que o OCR será aplicado (Path)

    # Returns
        result_ocr            - Required : Texto de resultado (PIL)

    """


    # INSTANCIANDO A CLASSE E OBTENDO O RESULTADO DO OCR
    result_ocr = ocr_functions().orchestra_execute_ocr(image=image_input, view_image=view_image)

    return result_ocr
