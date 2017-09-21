from theguardian import theguardian_content


headers = {
##            "q":" mps AND issues AND corbyns AND election AND party AND labour AND meeting AND partys AND brexit AND leaked",

##            "q" :" north AND nuclear AND south AND taking AND pressure AND weapons AND korea AND donald AND korean AND bait AND sanctions AND trump AND koreas AND region ",
##    "q":"theresa AND think AND ambition AND capture AND heartlands AND labour AND lays AND corbyn AND harehills AND leeds AND country AND election AND voters AND traditional AND bare AND vote",
            "q":"NHS AND Tory AND Labour AND Keir Starmer AND Brexit AND EU AND Seumas Milne AND UK AND Corbyn",
            "order-by": "newest",
            "from-date": "2012-01-01",
##            "section": "politics",
    }



# create content
content = theguardian_content.Content(api='test', **headers)

# gets raw_response
raw_content = content.get_request_response()
print("Request Response status code {status}." .format(status=raw_content.status_code))


### content
print("Content Response headers {}." .format(content.response_headers()))
no_pages = content.response_headers()['pages']
##
### get all results from all pages


for page in range(1,no_pages+1):

    print("Current page:{}".format(content.response_headers()['currentPage']))

    json_content = content.get_content_response(headers={"page":page})
    all_results = content.get_results(json_content)

    for res in all_results:
        print(" result title {}.".format(res['webTitle']))                                                



##for i in all_results:
##
##    print(" results title {}." .format(i['webTitle']))
