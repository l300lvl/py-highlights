# Hexchat Metadata
__module_name__ = "PyHighlights" 
__module_version__ = "v0.3.3" 
__module_description__ = "Script to shove highlights into another window." 

# Imports
import urllib2
import urllib
import xchat

class PyHighlights:
    def __init__(self):
        """Inits the PyHighlights Object, and includes the config.
        Yes, config inside here is rubbish, but it's an IRC script."""
        
        # Config
        self._key = "" # Insert here.
        self._name = "IRC Highlights"
        self._window = "highlights"
        self.url = "https://www.notifymyandroid.com/publicapi/notify"
        
        # Holds State
        self.nma = True # set false if you dont have NMA.
        self.active = True
        
        # Init
        context = xchat.get_context()
        xchat.command("QUERY {}".format(self._window))
        context.set()
        
        # Highlights window.
        self._context = xchat.find_context(channel=self._window)
    
    def nma_push(self, channel, nick, message):
        if not self.nma return
        events = {
            "apikey" : self._key,
            "event" : u"Highlight from {0} in {1}".format(nick, channel),
            "description" : message,
            "application" : self._name
        }
        req = urllib2.Request(self.url, urllib.urlencode(events))
        urllib2.urlopen(req) # can't be bothered to read response.
                             # If it gets there, it gets there.    
    
    def print_highlight(self, context, channel, nick, message):
        self._context.emit_print("Private Message to Dialog",
            nick,"({0}): {1}".format(channel, message))
        context.set() # return to normal window
        self.nma_push(nick, channel, message) # totally not pythonic.
        return xchat.EAT_NONE
    
    def main(self, word, word_eol, userdata):
        context = xchat.get_context()
        channel = context.get_info("channel")
        nick = word[0]
        message = word[1]
        self.print_highlight(context, channel, nick, message)
        return xchat.EAT_NONE
    
    def unloaded(self, userdata):
        print "Hilights Unloaded."
        return xchat.EAT_NONE
    
    def disable_nma(self, word, word_eol, userdata):
        self.nma = False if self.nma else True
        return xchat.EAT_XCHAT # prevent "not a command" error

p = PyHighlights()

# Hooks
xchat.hook_print("Channel Msg Hilight", p.main)
xchat.hook_unload(p.unloaded)
xchat.hook_command("nma", p.disable_nma)

print "Hilights loaded."
