class InputController:
    def __init__(self, view, shopping_list_controller):
        self.view = view
        self.shopping_list_controller = shopping_list_controller

    def add_product(self):
        name, duration, price = self.view.get_input_values()
        message = self.shopping_list_controller.add_product(name, duration, price)
        self.view.clear_inputs()
        return message