# objexp

objexp is a util to check what members in a object or Class or module imported.


## Installation

You can install objexp from [PyPI](https://pypi.org/project/objexp/):

```bash
pip install objexp
```

The reader is supported on Python 3.7 and above. 

## How to use

There is only 1 function: ox(), with 2 parameters, `savefile`, `ifprint`

if you want to save the result to a txt file, give the string of file path to save to parameter `savefile`, which defult value is `None`.

if you dont want to output result on screen, you could give a `false` value to `ifprint`, which defult value is `true`.


```python
from objexp import ox
ox(print)

```
It will output the members of function `print` on the screen as below:

```
_________________________

<class 'builtin_function_or_method'>

<built-in function print>
_________________________

<class 'NoneType'>
__text_signature__,

<class 'builtin_function_or_method'>
__dir__, __format__, __init_subclass__, __new__, __reduce__, __reduce_ex__, __sizeof__, __subclasshook__,

<class 'method-wrapper'>
__call__, __delattr__, __eq__, __ge__, __getattribute__, __gt__, __hash__, __init__, __le__, __lt__, __ne__, __repr__, __setattr__, __str__,

<class 'module'>
__self__,

<class 'str'>
__doc__, __module__, __name__, __qualname__,

<class 'type'>
__class__,

"\n_________________________\n\n<class 'builtin_function_or_method'>\n\n<built-in function print>\n_________________________\n\n<class 'NoneType'>\n__text_signature__, \n\n<class 'builtin_function_or_method'>\n__dir__, __format__, __init_subclass__, __new__, __reduce__, __reduce_ex__, __sizeof__, __subclasshook__, \n\n<class 'method-wrapper'>\n__call__, __delattr__, __eq__, __ge__, __getattribute__, __gt__, __hash__, __init__, __le__, __lt__, __ne__, __repr__, __setattr__, __str__, \n\n<class 'module'>\n__self__, \n\n<class 'str'>\n__doc__, __module__, __name__, __qualname__, \n\n<class 'type'>\n__class__, \n"

```