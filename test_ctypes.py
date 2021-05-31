from ctypes import *


my_buffer = create_unicode_buffer("1", 10)
# print "1 ==> "
# print my_buffer.raw
print "2 ==> "
print my_buffer.value
print "3 ==> "
print repr(my_buffer.value)
print "4 ==> "
print bytes(my_buffer.value)
# print "5 ==> "
# print repr(my_buffer.raw)
# print "6 ==> "
# print bytes(my_buffer.raw)
print "7 ==> "
print bytes(len(my_buffer))
print bytes(my_buffer.__getitem__(0))