import os, subprocess, dot.dot, target_dir.moving_file, sys
import  target_dir.package.nested_moving_file
import target_dir.package.nested_moving_file2
import target_dir.package as p

target_dir.moving_file.test()
       '' target_dir.moving_file.test()  c

target_dir.package.nested_moving_file.hi()
target_dir.package.nested_moving_file2.hello()
p.nested_moving_file.hi()

