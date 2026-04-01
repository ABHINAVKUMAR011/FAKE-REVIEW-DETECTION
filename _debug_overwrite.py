import io
import re
import app

c = app.app.test_client()

csv1 = b"review\nthis is great\nawful scam buy now!!!\n"
csv2 = b"review\njust okay\n"

r1 = c.post('/upload', data={'file': (io.BytesIO(csv1), 'a.csv')}, content_type='multipart/form-data', follow_redirects=True)
t1 = r1.data.decode('utf-8','ignore')

m1 = re.search(r'Total Predictions</div>\s*<div class="v">(\d+)</div>', t1)
print('after upload1 total=', m1.group(1) if m1 else 'missing')

r2 = c.post('/upload', data={'file': (io.BytesIO(csv2), 'b.csv')}, content_type='multipart/form-data', follow_redirects=True)
t2 = r2.data.decode('utf-8','ignore')

m2 = re.search(r'Total Predictions</div>\s*<div class="v">(\d+)</div>', t2)
print('after upload2 total=', m2.group(1) if m2 else 'missing')

rd = c.get('/dashboard')
td = rd.data.decode('utf-8','ignore')
md = re.search(r'Total Predictions</div>\s*<div class="v">(\d+)</div>', td)
print('dashboard refresh total=', md.group(1) if md else 'missing')
