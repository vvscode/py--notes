# from matplotlib import pyplot
#
#
# x = [1,2,3,4,5,6,7,8,9,10]
# y = [4,5,6,7,5,4,3,5,6,7]
#
#
# fig = pyplot.figure()
# ax = fig.add_subplot()
# ax.grid(True)
# ax.plot(x, y, color='red')
#
# pyplot.show()


from pandas import read_csv
from matplotlib import pyplot


data = read_csv('graph.csv', sep=";")

data.plot.area()

pyplot.show()
