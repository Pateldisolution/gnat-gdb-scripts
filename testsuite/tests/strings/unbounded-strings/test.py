from support.build import gnatmake
from support.gdb import GDBSession


gnatmake('foo')
gdb = GDBSession('foo')
gdb.run_to(gdb.find_loc('foo.adb', 'BREAK'))

gdb.execute('set corrupted_string.reference := 0x1')

gdb.print_expr('empty_string', 'Unbounded_String ("")')
gdb.print_expr('some_string', 'Unbounded_String ("Hello, world!")')
gdb.print_expr('binary_string', 'Unbounded_String ("b["00"]""["ff"]")')
gdb.print_expr('corrupted_string', 'Unbounded_String ([Invalid])')

gdb.test('python'
         ' s = gdb.parse_and_eval("binary_string");'
         ' v = gnatdbg.strings.UnboundedString(s);'
         ' string = v.get_string("ascii", errors="ignore");'
         ' print(gnatdbg.utils.ada_string_repr(string))',

         '"b["00"]"""')
