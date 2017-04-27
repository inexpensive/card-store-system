def is_basic_land(card_name):
    basic_lands = (
        "Plains",
        "Island",
        "Swamp",
        "Mountain",
        "Forest",
    )
    return card_name in basic_lands
