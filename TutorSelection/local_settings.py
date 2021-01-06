LOCAL_APP_CODE = "tutor_selection"
LOCAL_SECRET_KEY = "111"
LOCAL_DATABASE = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': LOCAL_APP_CODE,
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'post': 3306,
        },
    }
PASSWORD_KEY = ""
TOKEN_KEY = ""