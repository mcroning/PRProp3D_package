import Ipywidgets as wg
import Ipython.display
name = wg.Text (value = ‘Name’)
age = wg.IntSlider (description = ‘Age: ’)
display (name, age)
print (name.value + ‘ is already ‘+ str (age.value) + ‘ now ’)