import tkinter as tk
class TextPeer(tk.Text):
    """A peer of an existing text widget"""
    count = 0
    def __init__(self, master, cnf={}, **kw):
        TextPeer.count += 1
        parent = master.master
        peerName = "peer-{}".format(TextPeer.count)
        if str(parent) == ".":
            peerPath = ".{}".format(peerName)
        else:
            peerPath = "{}.{}".format(parent, peerName)

        # Create the peer
        master.tk.call(master, 'peer', 'create', peerPath, *self._options(cnf, kw))

        # Create the tkinter widget based on the peer
        # We can't call tk.Text.__init__ because it will try to
        # create a new text widget. Instead, we want to use
        # the peer widget that has already been created.
        tk.BaseWidget._setup(self, parent, {'name': peerName})