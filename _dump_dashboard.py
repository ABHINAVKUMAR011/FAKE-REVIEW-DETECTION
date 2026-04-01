import app
c = app.app.test_client()
html = c.get('/dashboard').data.decode('utf-8','ignore')
open('_dashboard_rendered.html','w',encoding='utf-8').write(html)
print('saved _dashboard_rendered.html, length=', len(html))
