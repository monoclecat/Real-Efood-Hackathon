########### Python 3.6 #############
try:
  import unzip_requirements
except ImportError:
  pass

import http.client, urllib.request, urllib.parse, urllib.error, base64, json, re
import requests
from operator import itemgetter
from copy import deepcopy


def parse_receipt(base64_data):
    # Replace the subscription_key string value with your valid subscription key.
    subscription_key = '1ffc58cd61754f34abe6f8581f507885'

    # Replace or verify the region.
    #
    # You must use the same region in your REST API call as you used to obtain your subscription keys.
    # For example, if you obtained your subscription keys from the westus region, replace
    # "westcentralus" in the URI below with "westus".
    #
    # NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
    # a free trial subscription key, you should not need to change this region.
    uri_base = 'westcentralus.api.cognitive.microsoft.com'

    headers = {
        # Request headers.
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters. The language setting "unk" means automatically detect the language.
        'language': 'unk',
        'detectOrientation ': 'true',
    })


    image = base64.b64decode(base64_data)

    # In[16]:


    try:
        response = requests.post(url='https://'+uri_base+'/vision/v1.0/ocr',
                                 headers=headers,
                                 params=params,
                                 data=image)

        parsed = response.json()
        print("Response:")
        print(json.dumps(parsed, sort_keys=True, indent=2))

    except Exception as e:
        print('Error:')
        print(e)
        return {'ResponseCode': 500, 'Result': {'Errormessage': "Communication with API server caused an error."}}

    if parsed['regions'] == []:
        # Recognition failed
        return {'ResponseCode': 500, 'Result': {'Errormessage': "Image recognition API failed to see text."}}

    def get_elements_at_y(y, parsed):
        try:
            for region in parsed['regions']:
                for box in region['lines']:
                    print(box)
                    print("--")
        except ValueError:
            return {'ResponseCode': 500, 'Result': {'Errormessage': "Getting elements at a specific y value caused a ValueError."}}

    def get_y(box):
        # box must be dict with 'boundingbox' key in top level
        # "boundingBox": "X,Y,width,height"
        coords_string = box['boundingBox']
        coords = coords_string.split(',')
        return int(coords[1])

    def get_x(box):
        # box must be dict with 'boundingbox' key in top level
        # "boundingBox": "X,Y,width,height"
        coords_string = box['boundingBox']
        coords = coords_string.split(',')
        return int(coords[0])

    def get_height(box):
        # box must be dict with 'boundingbox' key in top level
        # "boundingBox": "X,Y,width,height"
        coords_string = box['boundingBox']
        coords = coords_string.split(',')
        return int(coords[3])

    line_heights = []
    try:
        for region in parsed['regions']:
            for line in region['lines']:
                line_heights.append(get_height(line))
        line_height = line_heights[int(line_heights.__len__() / 2)]
    except ValueError:
        print("Getting median line height failed.")
        return {'ResponseCode': 500, 'Result': {'Errormessage': "Getting median line height caused an error."}}

    receipt_lines = []  # [ [{'boundingBox': '...', 'words': [{...}]}], ...]
    # "boundingBox": "X,Y,width,height"
    try:
        for region in parsed['regions']:
            for box in region['lines']:
                if receipt_lines != []:
                    for line in receipt_lines:
                        if get_y(box) < get_y(line[0]) + line_height / 2 and get_y(box) > get_y(line[0]) - line_height / 2:
                            for word in box['words']:
                                word['x-coord'] = get_x(box)
                                line.append(word)
                            break
                    else:
                        append_to_receipt = []
                        for word in box['words']:
                            word['x-coord'] = get_x(box)
                            append_to_receipt.append(word)
                        receipt_lines.append(append_to_receipt)
                else:
                    append_to_receipt = []
                    for word in box['words']:
                        word['x-coord'] = get_x(box)
                        append_to_receipt.append(word)
                    receipt_lines.append(append_to_receipt)
    except ValueError:
        print("Sorting by lines failed.")
        return {'ResponseCode': 500, 'Result': {'Errormessage': "Sorting lines caused an error."}}

    x_coord_sorter_array = []
    for line in receipt_lines:
        x_coord_sorter_array.append(sorted(line, key=itemgetter('x-coord')))

    receipt_lines = x_coord_sorter_array

    print(json.dumps(receipt_lines, sort_keys=True, indent=2))

    # In[18]:


    y_and_text = []
    try:
        for line in receipt_lines:
            y_and_text_entry = {'y-coord': int(get_y(line[0]))}
            y_and_text_string = ""
            for box in line:
                if y_and_text_string != "":
                    if box['text'][0] == ',' or box['text'][0] == '.' or y_and_text_string[
                                                                         -2:] == ", " or y_and_text_string[-2:] == ". ":
                        y_and_text_string = y_and_text_string[:-1]
                y_and_text_string += box['text'] + " "
            y_and_text_string = y_and_text_string[:-1]
            y_and_text_entry['text'] = y_and_text_string
            y_and_text.append(y_and_text_entry)
    except ValueError:
        return {'ResponseCode': 500, 'Result': {'Errormessage': "Joining line strings failed."}}

    y_and_text = sorted(y_and_text, key=itemgetter('y-coord'))

    print(json.dumps(y_and_text, sort_keys=True, indent=2))

    # In[22]:

    parsed_receipt = {'DateTime': "", 'Position': "", 'TotalPrice': 0, 'Items': {}}

    y_and_text_copy = deepcopy(y_and_text)

    receipt_head = []
    city_prog = re.compile("(\s|\A)(?P<plz>\d\d\d\d\d)\s(?P<city>[a-zA-Z]+)(\s|\Z|\D)")
    plz_prog = re.compile("(\s|\A)(?P<plz>\d\d\d\d\d)(\s|\Z|\D)")
    address_prog = re.compile("(\s|\A)(?P<address>[a-zA-Z]+\.+\d+)(\s|\Z|\D)")

    receipt_body = []
    product_prog = re.compile("(?P<name>(\S\S\S+\s*)+)\s(?P<price>\d?\d(\.|\,)\d\d)")
    real_product_amount_prog = re.compile("(?P<amount>\d+)\sx\s\d?\d(\.|\,)\d\d")

    receipt_foot = []
    datetime_prog = re.compile("(?P<day>\d?\d)(\.|\,)(?P<month>\d?\d)(\.|\,)(?P<year>\d\d)\s(?P<time>\d\d\:\d\d)")

    state = 1  # 1: head 2: body 3: foot
    for line in y_and_text:
        if state == 1:
            if product_prog.search(line['text']) is None:
                receipt_head.append(line)
            else:
                state = 2
        if state == 2:
            if "summe" not in line['text'].lower():
                receipt_body.append(line)
            else:
                state = 3
        if state == 3:
            receipt_foot.append(line)

    this_iteration = {}
    next_iteration = {}

    receipt_address = ["", "", ""]  # [Address,PLZ,City]
    for line in receipt_head:
        if "Tel" not in line['text']:
            found = plz_prog.search(line['text'])
            if found is not None:
                receipt_address[1] = found.group('plz')
            found = address_prog.search(line['text'])
            if found is not None:
                receipt_address[0] = found.group('address')
            else:
                found = city_prog.search(line['text'])
                if found is not None:
                    receipt_address[2] = found.group('city')
    parsed_receipt['Position'] = " ".join(receipt_address)

    for line in receipt_body:
        found = real_product_amount_prog.search(line['text'])
        if found is not None:
            next_iteration['Amount'] = found.group('amount')
        else:
            found = product_prog.search(line['text'])
            if found is not None:
                product_price = int(re.sub('[,\.]', '', found.group('price')))
                parsed_receipt['TotalPrice'] += product_price
                if found.group('name') not in parsed_receipt['Items']:
                    append_to_product = {'Price': product_price}
                    if 'Amount' in this_iteration:
                        append_to_product['Amount'] = this_iteration['Amount']
                    else:
                        append_to_product['Amount'] = 1
                    parsed_receipt['Items'][found.group('name')] = append_to_product
                else:
                    amount_now = int(parsed_receipt['Items'][found.group('name')]['Amount'])
                    if 'Amount' in this_iteration:
                        amount_now += int(this_iteration['Amount'])
                    else:
                        amount_now += 1
                    parsed_receipt['Items'][found.group('name')]['Amount'] = str(amount_now)
                    parsed_receipt['Items'][found.group('name')]['Price'] = \
                        parsed_receipt['Items'][found.group('name')]['Price'] + product_price

        this_iteration = {}
        this_iteration = deepcopy(next_iteration)
        next_iteration = {}

    for line in receipt_foot:
        found = datetime_prog.search(line['text'])
        if found is not None:
            receipt_year = found.group('year')
            receipt_year = '20' + receipt_year

            receipt_month = found.group('month')
            if receipt_month.__len__() == 1:
                receipt_month = "0" + receipt_month

            receipt_day = found.group('day')
            if receipt_day.__len__() == 1:
                receipt_day = "0" + receipt_day

            parsed_receipt['DateTime'] = receipt_year + "-" + receipt_month + "-" + receipt_day + " " + found.group(
                'time') + ":00"

    # print(json.dumps(parsed_receipt, sort_keys=True, indent=2))
    return {'ResponseCode': 200, 'Result': parsed_receipt}

