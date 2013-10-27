from Tkinter import *
import ttk
from pymongo import MongoClient

class MusicManagerApp(Frame):
    def __init__(self, parent):
        parent.geometry("250x150+300+300")

        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def initUI(self):
        self.pack(fill=BOTH, expand=1)

        tree = ttk.Treeview(self, columns=('year'))

        tree.heading('#0', text='Artist', anchor=W)
        tree.heading('year', text='Year', anchor=W)

        tree.pack(fill=BOTH, expand=1)

        client = MongoClient('localhost', 27017)
        db = client.music_manager
        artists = db.artists

        for artist in artists.find():
            artist_node = tree.insert('', 'end', text=artist['name'])

            if 'albums' not in artist:
                continue

            for album in artist['albums']:
                tree.insert(artist_node, 'end', text=album['name'], values=[album['year']])

    def start(self):
        self.parent.mainloop()

def main():
    root = Tk()
    app = MusicManagerApp(root)
    app.start()

if __name__ == '__main__':
    main()