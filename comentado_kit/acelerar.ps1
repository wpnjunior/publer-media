# PASSO FINAL do carrossel comentado, obrigatório antes de postar: acelerar 1.1x.
# Wagner aprovou esse ritmo em 15/08/2026 (a voz sai a 124 palavras/min, devagar demais).
# atempo preserva o tom da voz (não vira chipmunk) e setpts mantém tudo em sincronia —
# slides e b-roll aceleram junto.
#
# Uso:  .\acelerar.ps1                      -> reel_comentado.mp4 a 1.1x
#       .\acelerar.ps1 -Velocidade 1.2      -> outra velocidade, se pedirem
param(
  [string]$Entrada = "reel_comentado.mp4",
  [double]$Velocidade = 1.1
)

$v = $Velocidade
$saida = [IO.Path]::GetFileNameWithoutExtension($Entrada) + "_FINAL.mp4"

ffmpeg -y -loglevel error -i $Entrada `
  -filter_complex "[0:v]setpts=PTS/$v[v];[0:a]atempo=$v[a]" `
  -map "[v]" -map "[a]" -r 30 `
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k $saida

if (Test-Path $saida) {
  $d = [double](ffprobe -v error -show_entries format=duration -of csv=p=0 $saida)
  $mm = [math]::Floor($d / 60); $ss = [math]::Round($d % 60)
  Write-Output "PRONTO PARA POSTAR: $saida | ${v}x | $([math]::Round($d,1))s (${mm}min${ss})"
} else {
  Write-Output "FALHOU ao acelerar $Entrada"
}
