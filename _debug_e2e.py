import io
import app

c = app.app.test_client()
with open('TestReviews.csv', 'rb') as f:
    data = {'file': (io.BytesIO(f.read()), 'TestReviews.csv')}
    up = c.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)

text = up.data.decode('utf-8', 'ignore')
print('status:', up.status_code)
print('on dashboard:', '<title>Dashboard</title>' in text)
print('has summary label:', 'Total Predictions' in text)
print('has no-data marker:', 'No data yet.' in text)
print('has chart object:', 'const chartData = {' in text)
