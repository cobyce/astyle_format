
import gi
import subprocess

gi.require_version('Gtk', '3.0')
gi.require_version('Peas', '1.0')

from gi.repository import GObject, Gtk, Peas

STYLE = "java"
STYLES = ["1tbs", "banner", "allman", "gnu", "google", "horstmann", "java",
          "kr", "linux", "lisp", "pico", "stroustrup", "whitesmith"]

ui_str = """
<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_1">
        <menuitem name="AStyleFormat" action="AStyleFormat"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class AStyleFormatPlugin(GObject.Object, Peas.Activatable):
    __gtype_name__ = 'AStyleFormatPlugin'

    object = GObject.Property(type=GObject.Object)

    def __init__(self):
        super().__init__()

    def do_activate(self):
        self.window = self.object
        manager = self.window.get_ui_manager()

        action = Gtk.Action.new('AStyleFormat', _('AStyle Format'))
        #action.connect('activate', lambda a: self.duplicate_line())
        action.connect('activate', lambda action: self.format_code(action))

        self.action_group = Gtk.ActionGroup.new('AStyleFormatPluginActions')
        self.action_group.add_action_with_accel(action, '<Ctrl><Shift>F8')

        manager.insert_action_group(self.action_group, -1)
        self.merge_id = manager.add_ui_from_string(ui_str)

    def do_deactivate(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self.merge_id)
        manager.remove_action_group(self.action_group)
        manager.ensure_update()

    def do_update_state(self):
        pass
    
    def run(self, code):
        global STYLE
        if STYLE is None:
            return code
        view = self.window.get_active_view()
        tabLen = str(view.get_tab_width())
        maxLen = str(view.get_right_margin_position())
        options = "--indent=force-tab --unpad-paren"
        cmd = ["astyle --style="+STYLE+" "+options]

        proc = subprocess.Popen(cmd, shell=True,
                                stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        proc.stdin.write(bytes(code, 'utf-8'))
        proc.stdin.close()
        return proc.stdout.read()

    def format_code(self, action):
        global STYLE
        doc = self.window.get_active_document()
        if not doc:
            return
        start, end = doc.get_bounds()
        code = doc.get_text(start, end, False)
        result = self.run(code)
        doc.set_text(str(result, 'utf-8'))

# vim: ts=4 et

