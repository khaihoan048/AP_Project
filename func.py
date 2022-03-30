from requests import post
import smtplib
import unidecode
# Module variables to connect to moodle api
KEY = "308d28b425ba110ff98ef6b8e1ee5ab2"
URL = "http://e-learning.hcmut.edu.vn/"
ENDPOINT="/webservice/rest/server.php"
EMAIL="bkelupdate@gmail.com"
PASSWORD="Kh04082002"

def courseRetrieve(id):
    enrolled=call('core_enrol_get_users_courses',userid=id)
    dict={}
    for course in enrolled:
        if course['shortname'].endswith('HK212'):
            dict[course['id']]=unidecode.unidecode(course['fullname'])
    return dict

def rest_api_parameters(in_args, prefix='', out_dict=None):
    """Transform dictionary/array structure to a flat dictionary, with key names
    defining the structure.

    Example usage:
    >>> rest_api_parameters({'courses':[{'id':1,'name': 'course1'}]})
    {'courses[0][id]':1,
     'courses[0][name]':'course1'}
    """
    if out_dict==None:
        out_dict = {}
    if not type(in_args) in (list,dict):
        out_dict[prefix] = in_args
        return out_dict
    if prefix == '':
        prefix = prefix + '{0}'
    else:
        prefix = prefix + '[{0}]'
    if type(in_args)==list:
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif type(in_args)==dict:
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict

def call(fname, **kwargs):
    """Calls moodle API function with function name fname and keyword arguments.

    Example:
    >>> call_mdl_function('core_course_update_courses',
                           courses = [{'id': 1, 'fullname': 'My favorite course'}])
    """
    parameters = rest_api_parameters(kwargs)
    parameters.update({"wstoken": KEY, 'moodlewsrestformat': 'json', "wsfunction": fname})
    response = post(URL+ENDPOINT, parameters)
    response = response.json()
    if type(response) == dict and response.get('exception'):
        raise SystemError("Error calling Moodle API\n", response)
    return response
def send_email(msg, toAdress):
    try:
        server=smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(EMAIL,PASSWORD)
        subject="You got updates of courses from BKEL!"
        message='Subject:{}\n\n{}'.format(subject,msg)
        server.sendmail(EMAIL,toAdress,unidecode.unidecode(message))
        print("Sucess!")
    except:
        print (message)
 