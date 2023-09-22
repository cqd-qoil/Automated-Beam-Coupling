#######################################################################################################################
#######################################################################################################################
#Database Libraries
#Modelling Libraries 
import matplotlib.pyplot as plt
#######################################################################################################################
#######################################################################################################################

class Database:
    """
    Class for tracking data through experiment and modelling when completed
    """
    def __init__(self):
        self.templist = []
        self.energylist = []
        self.solutions = []

    def addData(self, temp, energy, solution):
        self.addtemp(temp)
        self.addenergy(energy)
        self.addsolution(solution)

    def addtemp(self, temp):
        self.templist.append(temp)
    def addenergy(self, energy):
        self.energylist.append(energy)
    def addsolution(self, solution):
        self.solutions.append(solution)

    def print(self):
        for i in range(len(self.solutions)):
            print("Solution: ", i, self.solutions[i])

        for i in range(len(self.energylist)):
            print("Energy: ", i, self.energylist[i])

        for i in range(len(self.templist)):
            print("Temp: ", i, self.templist[i])

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
        axs[0, 0].scatter(x1_steps, self.energylist, color='black')
        axs[0, 0].set_title('x1 vs Count')

        # scatter plot x0 against p1
        axs[0, 1].scatter(y1_steps, self.energylist, color='black')
        axs[0, 1].set_title('y1 vs Count')

        # scatter plot x1 against p0
        axs[1, 0].scatter(x2_steps, self.energylist, color='black')
        axs[1, 0].set_title('x2 vs Count')

        # scatter plot x1 against p1
        axs[1, 1].scatter(y2_steps, self.energylist, color='black')
        axs[1, 1].set_title('y2 vs Count')

        # adjust spacing between subplots
        plt.subplots_adjust(wspace=0.3, hspace=0.5)

        # add caption to the figure
        fig.text(0.5, 0.01, 'Axis coordinate vs Normalised Photon Counts (#).', ha='center')

        # display the plot
        plt.show()
    
    def modelCountVsTime(self):      
        """
        Models Photon count achieved vs iteration 

        Takes no inputs
        """       
        #Plot for energy (coupling) vs solution coordinates
        fig, ax = plt.subplots()
        time = range(len(self.energylist))
        ax.plot(time, self.energylist, color='black')

        best_coupling = max(self.energylist)  # Corrected line
        best_coupling_str = str(round(best_coupling, 4))

        ax.set_title('Coupling vs Optimsation iteration (steps)')
        ax.set_xlabel('Time [Iteration #]')
        ax.set_ylabel('Normalised Photon Counts [#]')
        caption = '\n\n\n\nConvergence is achieved at a coupling of ' + best_coupling_str + ' counts.'
        ax.text(0.5, -0.1, caption, ha='center', va='center', transform=ax.transAxes)

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