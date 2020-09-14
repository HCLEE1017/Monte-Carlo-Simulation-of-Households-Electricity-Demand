import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num
import time
import seaborn as sns
from operator import add
from scipy.ndimage import gaussian_filter1d


getColor = ['black', 'brown', 'red', 'purple', 'blue', 'green', 'orange', 'deeppink', 'dodgerblue']

### Function used to plot the average electricity demand for using each device on working day or weekend
def showGraph (targetTime, result, deviceList, Days, needAll, onlyAll, specifyDevice):

    formatter = mdates.DateFormatter("%H:%M")
    for day in Days:
        fig, ax= plt.subplots()
        ax.xaxis.set_major_formatter(formatter)
        dates = date2num(targetTime)
        if len(specifyDevice) != int(0): specDeviceList = specifyDevice
        else: specDeviceList = deviceList
        ### Plot each curve of the selected device
        if onlyAll == False:
            for i in range(len(specDeviceList)):
                smooth = gaussian_filter1d(result[str(specDeviceList[i]) + '_consumption_' + str(day)], 3)
                ax.plot(dates, smooth, color=str(getColor[i]), label=str(specDeviceList[i]), linestyle='-')
        ### Plot the aggregate curve of all devices
        if needAll == True:
            total = [0]*1440
            for i in range(len(deviceList)):
                total = list( map(add, total, result[str(deviceList[i]) + '_consumption_' + str(day)]))
            smoothTotal = gaussian_filter1d(total, 3)
            ax.plot(dates, smoothTotal, label='All')

        ### Image Setting
        ax.set_title('Average Watt on ' + str(day))
        ax.legend()
        ax.xaxis.set_label_text('Time')
        ax.yaxis.set_label_text('Average Watt')
        figure_name = "AVGfigure_" + str(day) + str(time.time()) + ".png"
        if str(day) == "WorkingDay": workingday_figure = figure_name
        else: weekend_figure = figure_name
        fig.savefig('static/images/' +  figure_name)
        plt.close()
    return workingday_figure, weekend_figure


### Function used to plot probability of watt when using the device
def plotProbDensity(result, deviceList, Days):
    storeImage = []
    for day in Days:
        for i in range(len(deviceList)):
            fig, ax= plt.subplots()
            sns.distplot(result[str(deviceList[i]) + '_probdensity_' + str(day)], hist=True, kde=True, color = getColor[i], hist_kws={'alpha': 0.2}, kde_kws={'linewidth': 1, 'alpha': 1}, label = str(deviceList[i]))
            ax.set_title('Probability Density of Using ' + str(deviceList[i]) + " on " + str(day))
            ax.legend()
            ax.xaxis.set_label_text('Energy (Watt)')
            ax.yaxis.set_label_text('Probability Density')
            figure_name = "PDfigure_" + str(day) + str(time.time()) + str(deviceList[i]) + ".png"
            storeImage.append(figure_name)
            fig.subplots_adjust(left=0.2)
            fig.savefig('static/images/' + figure_name)
            plt.close()
    return storeImage

