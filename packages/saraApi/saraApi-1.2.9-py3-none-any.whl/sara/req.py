import requests

def get(param):
    """
    @param  Request Parameter
    @return String
    """
    try:
        r = requests.get(f"https://sara-funciones-api.vercel.app/api/category?category={param}").json()
    except Exception as e:
        raise Exception(f"ERROR: > {e}\n\n\nPlease Contact evergaster or Open a Issue in https://github.com/EverGasterXd/sara_api/issues")
    else:
        try:
            return r['url']
        except Exception as e:
            raise Exception(f"ERROR: > {e}\n\n\nPlease Contact evergaster or Open a Issue in https://github.com/EverGasterXd/sara_api/issues")