try:
    from RPA.Robocorp.WorkItems import WorkItems

    work_items = WorkItems()
    work_items.get_input_work_item()
    work_item = work_items.get_work_item_variables()
    variables = work_item.get("variables", dict())
    metadata = work_item.get("metadata", dict())
except (ImportError, KeyError):
    variables = {}
    metadata = {}
