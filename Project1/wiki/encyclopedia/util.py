import re
import random
import os

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))

def random_entry():
    """
    Retrieves a random encyclopedia entry filename. If no entries exist, the function returns None.
    """
    entries = list_entries()

    if entries:
        random_filename = random.choice(entries)
        return random_filename
    else:
        return None
    

def search_entries(keyword):
    """
    Returns a list of all names of encyclopedia entries that partially contain the given keyword.
    """
    _, filenames = default_storage.listdir("entries")
    
    # Filter entries that contain the partial keyword
    matching_entries = [
        re.sub(r"\.md$", "", filename)
        for filename in filenames
        if filename.lower().endswith(".md") and keyword.lower() in filename.lower()
    ]

    return list(sorted(matching_entries))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
    

    
