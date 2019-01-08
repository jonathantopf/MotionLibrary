import os
from distutils.dir_util import copy_tree
from jinja2 import Template
import Animation


TITLE = "The Rose Parade"
SAFE_TITLE = "TheRoseParade"

OUTPUT_SITE_ROOT = "../"
STATIC_SOURCES_DIR = "./src"
TEMPLATE_DIR = "./Templates"
AFTEREFFECTS_ENTRIES_DIR = "./Entries/AfterEffects"

RESOLVED_OUTPUT_SITE_ROOT = "file://" + os.path.abspath (OUTPUT_SITE_ROOT)
SOURCES_OUTPUT_DESTINATION = os.path.join (OUTPUT_SITE_ROOT, "src")

index_page_template = Template (open (os.path.join (TEMPLATE_DIR, "index.html")).read ())
library_card_template = Template (open (os.path.join (TEMPLATE_DIR, "library-card.html")).read ())


def copy_static_sources ():
    copy_tree (STATIC_SOURCES_DIR, SOURCES_OUTPUT_DESTINATION)


class Library ():
    def __init__ (self):
        self.entries = []

    def populate (self):
        for aftereffects_entry_file_name in os.listdir (AFTEREFFECTS_ENTRIES_DIR):
            if (not aftereffects_entry_file_name.startswith(".")):
                self.entries.append (LibraryEntry (Animation.new_from_aftereffects_file (os.path.join (AFTEREFFECTS_ENTRIES_DIR, aftereffects_entry_file_name))))

    def output_htm (self):
        library_card_htms = []
        preview_css_paths = []

        for entry in self.entries:
            library_card_htms.append (entry.output_htm ())
            preview_css_paths.append (os.path.relpath (entry.output_preview_css_animation_file (), OUTPUT_SITE_ROOT))

        htm = index_page_template.render (
            preview_css_paths=preview_css_paths,
            library_card_htms=library_card_htms)

        return htm;

    def output_htm_file (self):
        output_file_path = os.path.join (OUTPUT_SITE_ROOT, "index.html")
        output_file = open (output_file_path, 'w')
        output_file.write (self.output_htm().encode ('utf8'))
        output_file.close ()


class LibraryEntry ():
    def __init__ (self, animation):
        self.animation = animation

    def output_htm (self):
        htm = library_card_template.render (
            preview_class_name=self.animation.safe_name(),
            title=self.animation.title)
        return htm;

    def output_preview_css_animation_file (self):
        return self.animation.output_preview_css_animation_file (os.path.join (SOURCES_OUTPUT_DESTINATION, "css", "animation-previews"))


def main ():
    copy_static_sources ()
    library = Library ()
    library.populate ()

    library.output_htm_file ()

main ()
