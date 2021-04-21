from survey.models import *

data = {
    'password1': 'XJLK2@dX',
    'password2': 'XJLK2@dX'
}

for i in range(10):
    print(i)
    data['email'] = 'a'*(i+1) + '@gmail.com'
    data['username'] = 'u'*(i+1)
    print(data)
    form = UserForm(data)
    u = form.save()
    u.set_password('')
    u.is_active = True
    u.save()