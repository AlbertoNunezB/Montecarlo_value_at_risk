import random
import numpy as np
import matplotlib.pyplot as plt

class Montecarlo_value_at_risk():
    raw_data    =   [] #list of tuples: (lower_likelihood_limit , upper_likelihood_limit , cost, currency). Currency shall be unique for every row

    def __init__(self,raw_data):
        self.raw_data   =   raw_data
        self.graph_x    =   []
        self.graph_y    =   []
        self.currency   =   None
    def value_at_risk(self,num_iterations):
        #check currency is unique
        for current_risk_row in self.raw_data:
            current_risk_currency   =   current_risk_row[3]
            if(self.currency==None):
                self.currency = current_risk_currency
            elif(self.currency != current_risk_currency):
                raise Exception('Multicurrency detected')
        value_at_risk_list  =   []
        for current_iteration_number in range(0,num_iterations):
            probability_risk_acum       =   0.0
            for current_risk_row in self.raw_data:
                current_risk_lower                  =   current_risk_row[0]
                current_risk_upper                  =   current_risk_row[1]
                current_risk_cost                   =   current_risk_row[2]
                current_risk_currency               =   current_risk_row[3]

                current_risk_assigned_probability   =   random.uniform(current_risk_lower,current_risk_upper)/100
                current_risk_probability_cost       =   current_risk_cost * current_risk_assigned_probability
                probability_risk_acum               +=  current_risk_probability_cost
            value_at_risk_list.append(probability_risk_acum)

        numpy_array             =   np.array(value_at_risk_list)
        mean                    =   np.mean(numpy_array,axis=0)
        std_deviation           =   np.std(numpy_array,axis=0)
        percentiles_1_to_100    =   []
        for i in range(1,101):
            percentiles_1_to_100.append(np.percentile(numpy_array,i))
        #print('mean   '+str(mean))
        #print('stddev '+str(std_deviation))
        #for i in range(1,101):
        #    print('p%'+str(i)+'  '+str(percentiles_1_to_100[i-1]))

        absolute_freqs              =   []
        values, absolute_freqs      =   np.unique(np.round(np.sort(numpy_array),0), return_counts=True)
        relative_freqs              =   [x/len(value_at_risk_list) for x in absolute_freqs]
        accumulative_freqs          =   []
        acum                        =   0
        for i in relative_freqs:
            acum+=i
            accumulative_freqs.append(acum)
        self.graph_x    =   values
        self.graph_y    =   accumulative_freqs
        return (self.graph_x,self.graph_x)
    def plot(self):
        plt.plot(self.graph_x,self.graph_y)
        plt.ticklabel_format(useOffset=False, style='plain')
        plt.xticks(rotation=45)
        plt.ylabel('Accumulative probability')
        plt.xlabel('Risk in '+self.currency)
        plt.show()

