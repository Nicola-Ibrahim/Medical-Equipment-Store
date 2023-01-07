from .profiles import Section, Service

def validate_sections(values: list):
    """Validate inserted sections values

    Args:
        values (list): list of sections
    """
    def get_id(value: int|str|Section):
        """Get section id

        Args:
            value (int | str | Section): section value

        Returns:
            id (int): The returned id of a section
        """
        match value:
            case int():
                return value

            case Section():
                id = Section.objects.get(name=value).pk
        
            case str():
                id = Section.objects.get(name=value).pk

        return id

    print(values)

    id_values = list(map(get_id, values))
    return id_values
        
def validate_services(values: list):
    """Validate inserted services values

    Args:
        values (list): list of services
    """
    def get_id(instance: int|str|Service):
        """Get service id

        Args:
            value (int | str | Section): service value

        Returns:
            id: The returned id of a service
        """
        match instance:
            case int():
                return id
            case Service():
                id = Service.objects.get(name=instance).pk
        
            case str():
                id = Service.objects.get(name=instance).pk

        return id

    id_values = list(map(get_id, values))
    return id_values