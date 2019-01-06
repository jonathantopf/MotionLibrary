import os
from distutils.dir_util import copy_tree
from jinja2 import Template


TITLE = "The Rose Parade"
SAFE_TITLE = "TheRoseParade"

GENERATED_SITE_ROOT = "../"
GENERATED_SITE_STATIC_SOURCES = "./src"
GENERATED_SITE_TEMPLATE_DIR = "./Templates"

GENERATED_SITE_RESOLVED_DIR = "file://" + os.path.abspath (GENERATED_SITE_ROOT)
GENERATED_SITE_STATIC_SOURCES_DESTINATION = os.path.join (GENERATED_SITE_ROOT, "src")

index_page_template = Template (open (os.path.join (GENERATED_SITE_TEMPLATE_DIR, "index.html")).read ())
library_card_template = Template (open (os.path.join (GENERATED_SITE_TEMPLATE_DIR, "library-card.html")).read ())


def copy_static_sources ():
    copy_tree (GENERATED_SITE_STATIC_SOURCES, GENERATED_SITE_STATIC_SOURCES_DESTINATION)


class Library ():
    entries = []
    def __init__ (self):
        pass

    def populate (self):
        self.entries.append (LibraryEntry ("Foo"))
        self.entries.append (LibraryEntry ("Long title goes here"))
        self.entries.append (LibraryEntry ("Bar"))
        self.entries.append (LibraryEntry ("Test"))
        self.entries.append (LibraryEntry ("Lorem ipsum dolar si amet"))

    def output_html (self):
        library_cards_data = []

        for library_card in self.entries:
            library_cards_data.append (library_card.output_html ())

        html_data = index_page_template.render (
            library_cards=library_cards_data)

        return html_data;


class LibraryEntry ():
    title = ""
    def __init__ (self, title):
        self.title = title

    def output_html (self):
        html_data = library_card_template.render (
            title = self.title)

        return html_data;


def main ():
    copy_static_sources ()
    library = Library ()
    library.populate ()

    html_data = library.output_html ()



    output_file_path = os.path.join (GENERATED_SITE_ROOT, "index.html")
    output_file = open (output_file_path, 'w')
    output_file.write (html_data.encode ('utf8'))
    output_file.close ()

main ()
