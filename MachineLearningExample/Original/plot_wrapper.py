#USED IN PLACE of `import matplotlib` etc

#This wraps plotting of a PIL image using Matplotlib because
# my system needs some wrangling to get interactive plots
# On Avon or Sulis set the below parameter to False to
# omit this

_force_tk_back = True

if _force_tk_back:
    import tkinter
    import matplotlib
    matplotlib.use('TkAgg')

    import matplotlib.pyplot as plt
else:
    import matplotlib.pyplot as plt

def plot_image(im, title):
    plt.figure()
    plt.imshow(im)
    plt.title(title)
    plt.show()

