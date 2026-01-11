def create_diagram():
    from .styles import PRIMARY_COLOR, SECONDARY_COLOR, BACKGROUND_COLOR

    # Dummy content for the diagram outline
    diagram_outline = {
        "title": "Sample Diagram",
        "elements": [
            {
                "type": "rectangle",
                "color": PRIMARY_COLOR,
                "label": "Main Component"
            },
            {
                "type": "circle",
                "color": SECONDARY_COLOR,
                "label": "Sub Component"
            }
        ],
        "background": BACKGROUND_COLOR
    }

    return diagram_outline