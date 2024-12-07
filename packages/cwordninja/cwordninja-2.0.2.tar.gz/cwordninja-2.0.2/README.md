![image](https://user-images.githubusercontent.com/2049665/29219793-b4dcb942-7e7e-11e7-8785-761b0e784e04.png)

C Word Ninja
==========

Slice your munged together words!  Seriously, Take anything, `'imateapot'` for example, would become `['im', 'a', 'teapot']`.  Useful for humanizing stuff (like database tables when people don't like underscores).

This project is repackaging the excellent work from here: http://stackoverflow.com/a/11642687/2449774

cwordninja is rewritten using cython based on wordninja.

Usage
-----
```
$ python
>>> import cwordninja
>>> cwordninja.split('derekanderson')
['derek', 'anderson']
>>> cwordninja.split('imateapot')
['im', 'a', 'teapot']
>>> cwordninja.split('heshotwhointhewhatnow')
['he', 'shot', 'who', 'in', 'the', 'what', 'now']
>>> cwordninja.split('thequickbrownfoxjumpsoverthelazydog')
['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog']
```

Performance
-----------
It's super fast!

Code:

```
import cwordninja
import wordninja
import timeit

def a():
    cwordninja.split("derek anderson")

c_time = int(timeit.timeit(a, number=10000) * 1000)
print("cwordninja:", c_time, "ms")

def b():
    wordninja.split("derek anderson")

r_time = int(timeit.timeit(b, number=10000) * 1000)
print("wordninja:", r_time, "ms")

print(int(r_time / c_time), "x")
```

Result:
```
cwordninja: 2 ms
wordninja: 1507 ms
753 x
```

It can handle long strings:
```
>>> cwordninja.lsplit('wethepeopleoftheunitedstatesinordertoformamoreperfectunionestablishjusticeinsuredomestictranquilityprovideforthecommondefencepromotethegeneralwelfareandsecuretheblessingsoflibertytoourselvesandourposteritydoordainandestablishthisconstitutionfortheunitedstatesofamerica')
['we', 'the', 'people', 'of', 'the', 'united', 'states', 'in', 'order', 'to', 'form', 'a', 'more', 'perfect', 'union', 'establish', 'justice', 'in', 'sure', 'domestic', 'tranquility', 'provide', 'for', 'the', 'common', 'defence', 'promote', 'the', 'general', 'welfare', 'and', 'secure', 'the', 'blessings', 'of', 'liberty', 'to', 'ourselves', 'and', 'our', 'posterity', 'do', 'ordain', 'and', 'establish', 'this', 'constitution', 'for', 'the', 'united', 'states', 'of', 'america']
```
And scales well.  (This string takes ~0.1ms to compute.) 

How to Install
--------------

```
pip3 install cwordninja
```

Custom Language Models
----------------------
#1 most requested feature!  If you want to do something other than english (or want to specify your own model of english), this is how you do it.

```
>>> lm = cwordninja.LanguageModel('my_lang.txt.gz')
>>> lm.split('derek')
['der','ek']
```

Language files must be gziped text files with one word per line in decreasing order of probability.

If you want to make your model the default, set:

```
cwordninja.DEFAULT_LANGUAGE_MODEL = wordninja.LanguageModel('my_lang.txt.gz')
```
