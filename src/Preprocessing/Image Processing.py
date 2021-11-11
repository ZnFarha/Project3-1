

import numpy as np
import cv2
import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')
# if you are running this code in Jupyter notebook

img = cv2.imread('C:/Users/as/Desktop/333.png', 0) 
# cv2.imshow('image',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# In[25]:


# Median filtering


# In[26]:


median = cv2.medianBlur(img, 5)
compare = np.concatenate((img, median), axis=1) #side by side comparison
cv2.imshow('img', compare)
cv2.waitKey(0)
cv2.destroyAllWindows


# In[10]:


# Gaussian filtering


# In[27]:


median = cv2.medianBlur(img, 5)
gauss = cv2.GaussianBlur(img, (5,5), 0)

images = np.concatenate((median, gauss), axis=1)

cv2.imshow('img', images)
cv2.waitKey(0)
cv2.destroyAllWindows


# In[13]:


# Brightness


# In[14]:


import PIL
from PIL import ImageEnhance


# In[30]:


img = PIL.Image.open('C:/Users/as/Desktop/333.png')
converter = ImageEnhance.Brightness(img)
img2 = converter.enhance(0.5)
img3 = converter.enhance(2)
plt.imshow(img3)
cv2.waitKey(0)
cv2.destroyAllWindows


# In[38]:


# Sharpness


# In[33]:


img = PIL.Image.open('C:/Users/as/Desktop/333.png')
converter = ImageEnhance.Sharpness(img)
img2 = converter.enhance(0.5)
img3 = converter.enhance(2)
plt.imshow(img3)
cv2.waitKey(0)
cv2.destroyAllWindows


# In[41]:


# Contrast


# In[35]:


img = PIL.Image.open('C:/Users/as/Desktop/333.png')
converter = ImageEnhance.Contrast(img)
img2 = converter.enhance(0.5)
img3 = converter.enhance(2)
plt.imshow(img3)
cv2.waitKey(0)
cv2.destroyAllWindows


# In[ ]:


# Saturation


# In[36]:


img = PIL.Image.open('C:/Users/as/Desktop/333.png')
converter = ImageEnhance.Color(img)
img2 = converter.enhance(0.5)
img3 = converter.enhance(2)
plt.imshow(img3)
cv2.waitKey(0)
cv2.destroyAllWindows


# In[ ]:




