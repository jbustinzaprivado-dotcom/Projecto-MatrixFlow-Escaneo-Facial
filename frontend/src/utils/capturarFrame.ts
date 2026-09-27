/** Convierte el cuadro actual de un <video> en un Blob JPEG, para subir al backend. */
export function capturarFrame(video: HTMLVideoElement): Promise<Blob> {
  const canvas = document.createElement('canvas')
  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  const ctx = canvas.getContext('2d')
  if (!ctx) return Promise.reject(new Error('No se pudo preparar la captura.'))
  ctx.drawImage(video, 0, 0)
  return new Promise((resolve, reject) => {
    canvas.toBlob(
      (blob) => (blob ? resolve(blob) : reject(new Error('No se pudo capturar la imagen.'))),
      'image/jpeg',
      0.9,
    )
  })
}
