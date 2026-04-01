import app
c = app.app.test_client()
t = c.get('/dashboard').data.decode('utf-8', 'ignore')
print('No data marker:', 'No data yet.' in t)
print('Has total label:', 'Total Predictions' in t)
print('Chart null:', 'const chartData = null' in t)
print('Chart object:', 'const chartData = {' in t)
