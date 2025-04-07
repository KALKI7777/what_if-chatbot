# --- knowledge_base.py ---
# Simulate a very simple knowledge base for audiobooks.
# In a real application, this would be a complex system, likely involving
# vector databases, text chunking, and retrieval mechanisms.

SIMULATED_KB = {
    "audiobook_123": {
        "title": "The Mystery of the Clockwork Dragon",
        "summary": "A thrilling adventure where heroes chase a mechanical dragon across continents.",
        "characters": ["Professor Alistair", "Eliza the Explorer", "Clockwork Dragon"],
        "plot_points": [
            "Dragon stolen from the inventor's workshop.",
            "Chase leads through London, Cairo, and hidden jungle temples.",
            "Dragon's power source is a rare crystal.",
            "Heroes deactivate the dragon and confront the villain."
        ],
        "themes": ["Technology vs. Nature", "The thrill of discovery"]
    },
    "audiobook_456": {
        "title": "Whispers in the Starlight Cafe",
        "summary": "A cozy mystery set in a cafe where secrets are spilled like coffee.",
        "characters": ["Barista Ben", "Detective Miller", "Regulars"],
        "plot_points": [
            "A valuable locket goes missing during closing time.",
            "Ben overhears snippets of conversations.",
            "Detective Miller interviews the quirky regulars.",
            "The locket is found hidden in a sugar dispenser."
        ],
        "themes": ["Observation", "Community secrets", "Everyday mysteries"]
    }
}

def get_book_details(book_id):
    """Retrieves details for a specific book ID from the simulated KB."""
    return SIMULATED_KB.get(book_id, None)
