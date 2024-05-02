from django.forms.models import model_to_dict


class ModelToDictionary:
    """Adds a function that converts model to dictionary"""

    def to_dict(self):
        """Converts model to dictionary"""
        return model_to_dict(self)
