from utilities.models import ConnectionInfo
import requests
def get_options_list(field, **kwargs):
    """
    A working sample that returns a dynamically generated list of options.

    :param field: The field you are generating options for (of type CustomField or its subclass HookInput).

    See the "Generated Parameter Options" section of the docs for more info and the CloudBolt forge
    for more examples: https://github.com/CloudBoltSoftware/cloudbolt-forge/tree/master/actions/cloudbolt_plugins
    """

    # ci = ConnectionInfo.objects.get(name="Digicert API")
    
    # headers = {
    #     'content-Type': 'application/json',
    #     'X-DC-DEVKEY': ci.password
    # }
    
    # response = requests.get(f"{ ci.ip }/organization?filters[status]=active&include_validation=true", headers=headers)
    # result = response.json()
    # options = [item['display_name'] for item in result['organizations'] if 'display_name' in item]
    #   options.insert(0, 'Deutsche Vermögensberatung Aktiengesellschaft DVAG')
    options = []
    options.append("A")
    options.append("B")
    options.append("C")
    options.insert(0, "äöüßÄÖÜ")

    return {
        'options': options,
    }