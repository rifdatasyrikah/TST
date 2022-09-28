API untuk menerima data dalam format JSON

dictionary data mahasiswa :
 {
    "nim" : int
    "nama" : str
 }

Cara menjalankan API
1. aktivasi virtual environment
ketik source venvTugas1/bin/activat

2. jalankan api
ketik uvicorn simpleAPI:app --port 8000 --reload

3. Buka terminal lain dan kirim request misalnya ketik
curl -X 'POST' \
  'http://127.0.0.1:8000/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "nim": 11122333,
  "nama": "contoh data"
}'
