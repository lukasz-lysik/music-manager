import sys
sys.path.insert(0, 'musicbrainzngs\musicbrainzngs')

from Tkinter import *
import ttk
from pymongo import MongoClient
import musicbrainz


class Prezenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def init(self):
        self.view.set_artists(self.model.get_artists())
        self.view.init()


class View:
    def __init__(self):
        self.main_frame = MainFrame()

    def init(self):
        self.main_frame.start()

    def set_artists(self, artists):
        for artist in artists:
            artist_node = self.main_frame.insert_artist(artist['name'])

            if 'albums' not in artist:
                continue

            for album in artist['albums']:
                self.main_frame.insert_album(
                    artist_node,
                    album['name'],
                    album['year'])


class Model:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.music_manager

    def get_artists(self):
        return self.db.artists.find()


class MainFrame(Frame):
    def __init__(self):

        self.parent = Tk()

        self.parent.geometry("250x150+300+300")

        Frame.__init__(self, self.parent)

        self.pack(fill=BOTH, expand=1)

        self.artists_tree = self._init_tree()

    def _init_tree(self):
        tree = ttk.Treeview(self, columns=('year'))

        tree.heading('#0', text='Artist', anchor=W)
        tree.heading('year', text='Year', anchor=W)

        tree.pack(fill=BOTH, expand=1)
        return tree

    def insert_artist(self, name):
        return self.artists_tree.insert('', 'end', text=name)

    def insert_album(self, parent_node, name, year):
        self.artists_tree.insert(parent_node, 'end', text=name, values=[year])

    def start(self):
        self.parent.mainloop()


def main():
    model = Model()
    view = View()
    prezenter = Prezenter(model, view)
    prezenter.init()


if __name__ == '__main__':
    main()
