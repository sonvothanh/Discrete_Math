# viết hàm phân tích số 328419349 thành thừa số nguyên tố

def phan_tich_thua_so_nguyen_to(n):
  thua_so = {}
  d = 2
  temp = n
  while d * d <= temp:
    while temp % d == 0:
      thua_so[d] = thua_so.get(d, 0) + 1
      temp //= d
    d += 1
  if temp > 1:
    thua_so[temp] = thua_so.get(temp, 0) + 1
  return thua_so

so_can_phan_tich = 328419349

ket_qua = phan_tich_thua_so_nguyen_to(so_can_phan_tich)

print(f"Phân tích số {so_can_phan_tich} thành thừa số nguyên tố:")

for so, mu in ket_qua.items():
  print(f"{so}^{mu}")
