from cloudcix.client import Client


class Support:
    """
    The Support application is both a ticketing system, and a returns management system
    """
    _application_name = 'support'

    iris_condition = Client(
        _application_name,
        'iris_condition/',
    )
    iris_condition_translation = Client(
        _application_name,
        'iris_condition/{iris_condition_id}/translation/',
    )
    iris_defect = Client(
        _application_name,
        'iris_defect/',
    )
    iris_defect_translation = Client(
        _application_name,
        'iris_defect/{iris_defect_id}/translation/',
    )
    iris_extended_condition = Client(
        _application_name,
        'iris_extended_condition/',
    )
    iris_extended_condition_translation = Client(
        _application_name,
        'iris_extended_condition/{iris_extended_condition_id}/translation/',
    )
    iris_ntf = Client(
        _application_name,
        'iris_ntf/',
    )
    iris_ntf_translation = Client(
        _application_name,
        'iris_ntf/{iris_ntf_id}/translation/',
    )
    iris_repair = Client(
        _application_name,
        'iris_repair/',
    )
    iris_repair_translation = Client(
        _application_name,
        'iris_repair/{iris_repair_id}/translation/',
    )
    iris_section = Client(
        _application_name,
        'iris_section/',
    )
    iris_section_translation = Client(
        _application_name,
        'iris_section/{iris_section_id}/translation/',
    )
    iris_symptom = Client(
        _application_name,
        'iris_symptom/',
    )
    iris_symptom_translation = Client(
        _application_name,
        'iris_symptom/{iris_symptom_id}/translation/',
    )
    item = Client(
        _application_name,
        'ticket/{transaction_type_id}/{tsn}/item/',
    )
    item_history = Client(
        _application_name,
        'ticket/{transaction_type_id}/{tsn}/item/{item_id}/history/',
    )
    item_status = Client(
        _application_name,
        'item_status/',
    )
    part_used = Client(
        _application_name,
        'ticket/{transaction_type_id}/{tsn}/item/{item_id}/part_used/',
    )
    reason_for_return = Client(
        _application_name,
        'reason_for_return/',
    )
    reason_for_return_translation = Client(
        _application_name,
        'reason_for_return/{reason_for_return_id}/translation/',
    )
    service_centre_logic = Client(
        _application_name,
        'service_centre_logic/',
    )
    service_centre_warrantor = Client(
        _application_name,
        'service_centre/{address_id}/warrantor/',
    )
    status = Client(
        _application_name,
        'status/',
    )
    summary_support_ticket = Client(
        _application_name,
        'summary_support_ticket/',
    )
    ticket = Client(
        _application_name,
        'ticket/{transaction_type_id}/',
    )
    ticket_history = Client(
        _application_name,
        'ticket/{transaction_type_id}/{tsn}/history/',
    )
    ticket_question = Client(
        _application_name,
        'ticket_question/',
    )
    ticket_type = Client(
        _application_name,
        'ticket_type/',
    )
    warrantor_logic = Client(
        _application_name,
        'warrantor_logic/',
    )
    warrantor_service_centre = Client(
        _application_name,
        'warrantor/{address_id}/service_centre/',
    )
