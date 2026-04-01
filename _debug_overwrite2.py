import io
import app

c = app.app.test_client()

csv1 = b"review\nthis is great\nawful scam buy now!!!\n"
r1 = c.post('/upload', data={'file': (io.BytesIO(csv1), 'a.csv')}, content_type='multipart/form-data', follow_redirects=True)
text = r1.data.decode('utf-8','ignore')
print('status', r1.status_code)
print('is_dashboard', '<title>Dashboard</title>' in text)
print('is_index', 'AI-Based Fake Review Detection' in text)
print('has_error_card', 'Dashboard Error' in text)
print(text[:500])
