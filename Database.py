#######################################################################################################################
#######################################################################################################################
#Database Libraries
#Modelling Libraries 
import matplotlib.pyplot as plt
#######################################################################################################################
#######################################################################################################################

#Stefan looking for comparitor boards 

class Database:
    """
    Class for tracking data through experiment and modelling when completed
    """
    def __init__(self):
        self.countlist = []
        self.solutions = []
        self.method = 'Not Set'
        self.est_maximum = 0

    def addData(self, count, solution):
        # print("ADDING TO DATABASE: ", count, " ", solution)
        self.addcount(count)
        self.addsolution(solution)

    def addcount(self, count):
        self.countlist.append(count)
        # print(self.countlist)

    def addsolution(self, solution):
        self.solutions.append(solution)
        # print(self.solutions)
        
    def setMethod(self, method):
        self.method = method

    def set_est_max(self, max):
        self.est_maximum = max

    def print(self):
        # print("TRIAL SOLUTIONS:\n")
        for i in range(len(self.solutions)):
            print("Solution: ", i, " ", self.solutions[i])

        for i in range(len(self.countlist)):
            print("Count: ", i," ", self.countlist[i])
    #Change in srep size vs power
    
    def modelCountVsAxis(self):
        """
        Models Photon count vs Solution steps 

        Takes no inputs
        """
        #get each axis steps list 
        x1_steps = []
        y1_steps = []
        x2_steps = []
        y2_steps = []

        for i in range(len(self.solutions)):
            # extract data from solutions list
            x1_steps.append(self.solutions[i][0])
            y1_steps.append(self.solutions[i][1])
            x2_steps.append(self.solutions[i][2])
            y2_steps.append(self.solutions[i][3])

        # create subplots
        fig, axs = plt.subplots(2, 2)

        # scatter plot x0 against p0
        axs[0, 0].scatter(x1_steps, range(len(self.solutions)), color='black')
        axs[0, 0].set_title('x1 vs Count')

        # scatter plot x0 against p1
        axs[0, 1].scatter(y1_steps, range(len(self.solutions)), color='black')
        axs[0, 1].set_title('y1 vs Count')

        # scatter plot x1 against p0
        axs[1, 0].scatter(x2_steps, range(len(self.solutions)), color='black')
        axs[1, 0].set_title('x2 vs Count')

        # scatter plot x1 against p1
        axs[1, 1].scatter(y2_steps, range(len(self.solutions)), color='black')
        axs[1, 1].set_title('y2 vs Count')

        # adjust spacing between subplots
        plt.subplots_adjust(wspace=0.3, hspace=0.5)

        # add caption to the figure
        fig.text(0.5, 0.01, 'Axis coordinate vs Normalised Photon Counts (#).' + self.method, ha='center')

        # display the plot
        plt.show()
    
    def modelCountVsTime(self):      
        """
        Models Photon count achieved vs iteration 

        Takes no inputs
        """       
        #Plot for energy (coupling) vs solution coordinates
        fig, ax = plt.subplots()
        time = range(len(self.countlist))
        ax.plot(time, self.countlist, color='black')

        # best_coupling = max(self.countlist)
        # best_coupling_str = str(round(best_coupling, 4))

        ax.set_title('Coupling vs Optimsation iteration (steps) for ' + self.method + ' method')
        ax.set_xlabel('Time [Iteration #]')
        ax.set_ylabel('Normalised Photon Counts [#]')
        # caption = '\n\n\n\nConvergence is achieved at a coupling of ' + best_coupling_str + ' counts.'
        # ax.text(0.5, -0.1, caption, ha='center', va='center', transform=ax.transAxes)

        # Show the plot
        plt.show()

def modelTimeVsAxis(self):
        """
        Models Photon count vs Solution steps 

        Takes no inputs
        """
        #get each axis steps list 
        x1_steps = []
        y1_steps = []
        x2_steps = []
        y2_steps = []

        time = range(len(self.solutions))

        for i in range(len(self.solutions)):
            # extract data from solutions list
            x1_steps.append(self.solutions[i][0])
            y1_steps.append(self.solutions[i][1])
            x2_steps.append(self.solutions[i][2])
            y2_steps.append(self.solutions[i][3])

        # create subplots
        fig, axs = plt.subplots(2, 2)

        # scatter plot x0 against p0
        axs[0, 0].scatter( time, x1_steps, color='black')
        axs[0, 0].set_title('x1 vs Time')

        # scatter plot x0 against p1
        axs[0, 1].scatter( time, y1_steps,color='black')
        axs[0, 1].set_title('y1 vs Time')

        # scatter plot x1 against p0
        axs[1, 0].scatter( time, x2_steps,color='black')
        axs[1, 0].set_title('x2 vs Time')

        # scatter plot x1 against p1
        axs[1, 1].scatter(time,y2_steps, color='black')
        axs[1, 1].set_title('y2 vs Time')

        # adjust spacing between subplots
        plt.subplots_adjust(wspace=0.3, hspace=0.5)

        # add caption to the figure
        fig.text(0.5, 0.01, 'Axis coordinate vs Normalised Photon Counts (#).', ha='center')

        # display the plot
        plt.show()