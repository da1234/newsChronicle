from theguardian import theguardian_content


headers = {
            "q":"NHS AND Tory AND Labour AND Keir Starmer AND Brexit AND EU AND Seumas Milne AND UK AND Corbyn",
            "order-by": "newest",
            "from-date": "2012-01-01",
            "section": "politics"
    }

# create content
content = theguardian_content.Content(api='test', **headers)

# gets raw_response
raw_content = content.get_request_response()
print("Request Response status code {status}." .format(status=raw_content.status_code))

### content
print("Content Response headers {}." .format(content.response_headers()))
no_pages = content.response_headers()['pages']

### get all results from all pages
for page in range(1,no_pages+1):
    print("Current page:{}".format(content.response_headers()['currentPage']))
    json_content = content.get_content_response(headers={"page":page})
    all_results = content.get_results(json_content)
    for res in all_results:
        print(" result title {}.".format(res['webTitle']))
