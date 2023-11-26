
class ResponseProcessor:
    def process_response(self, response_data):
        raise NotImplementedError("Subclasses must implement process_response")


class OpenEiProcessor(ResponseProcessor):
    def process_response(self, response_data):
        # TODO compute avg cost
        # TODO get the most common utility tariff
        # TODO list of utility tariffs to be displayed
        # TODO projection of cost for the first year
        print('>>>>>>>>>>>> test', type(response_data))
        unit = response_data.get('flatdemandunit')
        demands_structure = response_data.get('flatdemandstructure')
        return response_data
