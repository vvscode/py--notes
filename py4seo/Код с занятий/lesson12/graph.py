from pandas import read_csv
from matplotlib import pyplot

data = read_csv('graph.csv', sep=";")

data.plot.area()

pyplot.show()

# breakpoint()

# xdata = [x for x in range(200)]
# ydata = [x**3 for x in xdata]
#
#
# with open('graph.csv', 'w') as f:
#     f.write('x_data;y_data\n')
#     for x in xdata:
#         f.write(f'{x};{x**3}\n')

print(type(data.x_data))

fig = pyplot.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(data.x_data, data.y_data, color='tab:blue')

# pyplot.show()
