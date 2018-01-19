# lists
arr = ['a', 'b', 'c']
print(type(arr)) # => list
print(arr[0])    # => 'a'

#--
#Dict
d = {'foo': 'bar'}

print(type(d)) # => dict
print(d['foo']) # => 'bar'
print(d.get('foo')) # => 'bar'
print(d.get('xxx', 'fallback')) # => 'fallback'

#--
#Tuple
t = 'a', 'b', 'c'

print(type(t)) # => tuple
print(t) # => ('a', 'b', 'c')
print(t[0]) # => 'a'

#--
#Set
s = set('foo')
print(type(s)) # => set
print(s)# => {'f', 'o'}