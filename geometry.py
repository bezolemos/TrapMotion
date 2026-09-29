from PIL import Image
import cv2
import numpy as np
from scipy import ndimage


def criar_mascara(caminho_imagem, largura, altura):

    # ---------------------------------------------------------
    # 1. Abre a imagem usando Pillow
    # ---------------------------------------------------------

    imagem_pillow = Image.open(caminho_imagem)

    # Converte para escala de cinza
    imagem_cinza = imagem_pillow.convert("L")

    # Transforma a imagem em uma matriz NumPy
    matriz = np.array(imagem_cinza)

    # ---------------------------------------------------------
    # 2. Converte a matriz para uma imagem colorida
    #    para utilizar o GrabCut do OpenCV
    # ---------------------------------------------------------

    imagem = cv2.cvtColor(
        matriz,
        cv2.COLOR_GRAY2BGR
    )

    altura_imagem, largura_imagem = imagem.shape[:2]

    # ---------------------------------------------------------
    # 3. Converte para LAB
    # ---------------------------------------------------------

    imagem_lab = cv2.cvtColor(
        imagem,
        cv2.COLOR_BGR2LAB
    )

    imagem_lab = imagem_lab.astype(np.float32)

    # ---------------------------------------------------------
    # 4. Detecta a cor do fundo pelas bordas
    # ---------------------------------------------------------

    margem = max(
        5,
        int(min(altura_imagem, largura_imagem) * 0.03)
    )

    borda_superior = imagem_lab[:margem, :]
    borda_inferior = imagem_lab[-margem:, :]
    borda_esquerda = imagem_lab[:, :margem]
    borda_direita = imagem_lab[:, -margem:]

    pixels_fundo = np.concatenate([
        borda_superior.reshape(-1, 3),
        borda_inferior.reshape(-1, 3),
        borda_esquerda.reshape(-1, 3),
        borda_direita.reshape(-1, 3)
    ])

    cor_fundo = np.median(
        pixels_fundo,
        axis=0
    )

    # ---------------------------------------------------------
    # 5. Calcula a diferença em relação ao fundo
    # ---------------------------------------------------------

    distancia_fundo = np.linalg.norm(
        imagem_lab - cor_fundo,
        axis=2
    )

    distancia_fundo = np.clip(
        distancia_fundo,
        0,
        255
    ).astype(np.uint8)

    # ---------------------------------------------------------
    # 6. Threshold automático
    # ---------------------------------------------------------

    _, mascara_inicial = cv2.threshold(
        distancia_fundo,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    mascara_inicial = mascara_inicial > 0

    # ---------------------------------------------------------
    # 7. Limpeza inicial
    # ---------------------------------------------------------

    kernel = np.ones(
        (9, 9),
        np.uint8
    )

    mascara_inicial = cv2.morphologyEx(
        mascara_inicial.astype(np.uint8),
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2
    )

    # ---------------------------------------------------------
    # 8. Prepara o GrabCut
    # ---------------------------------------------------------

    mascara_grabcut = np.full(
        (altura_imagem, largura_imagem),
        cv2.GC_PR_BGD,
        dtype=np.uint8
    )

    area_provavel = cv2.dilate(
        mascara_inicial,
        np.ones((21, 21), np.uint8),
        iterations=1
    )

    mascara_grabcut[
        area_provavel > 0
    ] = cv2.GC_PR_FGD

    mascara_grabcut[
        mascara_inicial > 0
    ] = cv2.GC_FGD

    # Bordas são consideradas fundo
    margem_borda = 10

    mascara_grabcut[
        :margem_borda, :
    ] = cv2.GC_BGD

    mascara_grabcut[
        -margem_borda:, :
    ] = cv2.GC_BGD

    mascara_grabcut[
        :, :margem_borda
    ] = cv2.GC_BGD

    mascara_grabcut[
        :, -margem_borda:
    ] = cv2.GC_BGD

    # ---------------------------------------------------------
    # 9. Executa o GrabCut
    # ---------------------------------------------------------

    modelo_fundo = np.zeros(
        (1, 65),
        np.float64
    )

    modelo_objeto = np.zeros(
        (1, 65),
        np.float64
    )

    cv2.grabCut(
        imagem,
        mascara_grabcut,
        None,
        modelo_fundo,
        modelo_objeto,
        5,
        cv2.GC_INIT_WITH_MASK
    )

    mask = (
        (mascara_grabcut == cv2.GC_FGD) |
        (mascara_grabcut == cv2.GC_PR_FGD)
    )

    # ---------------------------------------------------------
    # 10. Limpeza da máscara
    # ---------------------------------------------------------

    mask = cv2.morphologyEx(
        mask.astype(np.uint8),
        cv2.MORPH_CLOSE,
        np.ones((7, 7), np.uint8),
        iterations=1
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        np.ones((3, 3), np.uint8),
        iterations=1
    )

    # ---------------------------------------------------------
    # 11. Mantém o maior objeto
    # ---------------------------------------------------------

    numero_objetos, rotulos, estatisticas, _ = (
        cv2.connectedComponentsWithStats(
            mask,
            connectivity=8
        )
    )

    if numero_objetos > 1:

        maior_objeto = 1 + np.argmax(
            estatisticas[1:, cv2.CC_STAT_AREA]
        )

        mask = rotulos == maior_objeto

    else:

        mask = mask > 0

    # ---------------------------------------------------------
    # 12. Preenche buracos
    # ---------------------------------------------------------

    mask = ndimage.binary_fill_holes(mask)

    # ---------------------------------------------------------
    # 13. Redimensionamento sem distorcer
    # ---------------------------------------------------------

    altura_mask, largura_mask = mask.shape

    escala_largura = largura / largura_mask
    escala_altura = altura / altura_mask

    escala = min(
        escala_largura,
        escala_altura
    )

    nova_largura = max(
        1,
        round(largura_mask * escala)
    )

    nova_altura = max(
        1,
        round(altura_mask * escala)
    )

    mask_redimensionada = cv2.resize(
        mask.astype(np.uint8),
        (nova_largura, nova_altura),
        interpolation=cv2.INTER_NEAREST
    )

    # ---------------------------------------------------------
    # 14. Cria a área final
    # ---------------------------------------------------------

    mask_final = np.zeros(
        (altura, largura),
        dtype=np.uint8
    )

    # ---------------------------------------------------------
    # 15. Centraliza sem deformar
    # ---------------------------------------------------------

    pos_x = (
        largura - nova_largura
    ) // 2

    pos_y = (
        altura - nova_altura
    ) // 2

    mask_final[
        pos_y:pos_y + nova_altura,
        pos_x:pos_x + nova_largura
    ] = mask_redimensionada

    mask = mask_final > 0

    # ---------------------------------------------------------
    # 16. Salva a máscara para visualização
    # ---------------------------------------------------------

    mask_imagem = np.where(
        mask,
        255,
        0
    ).astype(np.uint8)

    cv2.imwrite(
        "mascara.png",
        mask_imagem
    )

    return mask


# =============================================================
# TESTE DO PROGRAMA
# =============================================================

if __name__ == "__main__":

    caminho = input(
        "Digite o caminho da imagem: "
    )

    mask = criar_mascara(
        caminho,
        100,
        100
    )