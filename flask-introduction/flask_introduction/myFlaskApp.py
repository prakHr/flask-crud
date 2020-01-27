import os

#from library._01_simple import app
#from library._02_html_inside_view import app
#from library._03_template_str_inside_view import app
#from library._03_01_template_str_inside_view_with_database import app
#from library._04_template_outside_view import app
from library._05_database_app_template_eng import app

if __name__ == '__main__':
    app.debug = True
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))
    app.run(host=host, port=port)
