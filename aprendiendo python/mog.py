#!/usr/bin/env python
# coding: utf-8

# In[22]:


import random


def stringmogolic(string):

    i = 0
    res = ""
    while i < len(string):
        if random.randint(0, 1) == 0:
            res = res + string[i].upper()
        else:
            res = res + string[i].lower()
        i=i+1

    res = res.replace("!", "a", 3)
    print(res)

stringmogolic("por que usas el nombre de dios? si vos no crees en el !!1!1")

# In[ ]:


# In[ ]:


# In[ ]:


# In[ ]:
