import json
from visualize_app.backend.static import graph_data_path
from manage_app.models import DeviceModel


class NetworkMapper:
    def __init__(self):
        self.device_models = DeviceModel.objects.all()

    def __object_validator(self, device_id):
        validator = False
        for device_node in self.graph_data['nodes']:
            if device_id == device_node['object_id']:
                validator = True
        return validator

    def generate_graph_data(self):
        with open(graph_data_path, 'r') as file_stream:
            self.graph_data = json.loads(file_stream.read())

        for device_model in self.device_models:
            if not self.__object_validator(device_model.id):
                device_name = device_model.system_name.split('.')[0]
                device_type = device_model.device_type
                group = '2' if device_type == 'Router' else '1'
                device_node = {
                    'group': group,
                    'id': device_name,
                    'object_id': device_model.id,

                }
                self.graph_data['nodes'].append(device_node)

        with open(graph_data_path, 'w') as file_stream:
            json.dump(self.graph_data, file_stream)
