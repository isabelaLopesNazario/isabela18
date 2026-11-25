"""Afasta a foto (zoom out) aumentando a parede lisa em volta: replica a borda, suaviza só a parte nova e funde."""
import sys, cv2, numpy as np
src, dst, frac = sys.argv[1], sys.argv[2], float(sys.argv[3])   # frac = largura da foto no quadro final
im = cv2.imread(src); H, W = im.shape[:2]
CW = int(round(W / frac)); CH = int(round(CW * 1350 / 1080))
lado = (CW - W) // 2; topo = CH - H
ext = cv2.copyMakeBorder(im, topo, 0, lado, CW - W - lado, cv2.BORDER_REPLICATE)
suave = cv2.GaussianBlur(ext, (0, 0), 25 * W / 1086)
m = np.zeros((CH, CW), np.float32); m[topo:, lado:lado + W] = 1
m = cv2.GaussianBlur(cv2.erode(m, np.ones((int(61 * W / 1086),) * 2)), (0, 0), 18 * W / 1086)[..., None]
out = (ext * m + suave * (1 - m)).astype(np.uint8)
# leve granulado na parte nova para não ficar lisa demais
ruido = np.random.default_rng(1).normal(0, 2.2, out.shape).astype(np.float32)
out = np.clip(out + ruido * (1 - m), 0, 255).astype(np.uint8)
cv2.imwrite(dst, out); print(dst, out.shape)
