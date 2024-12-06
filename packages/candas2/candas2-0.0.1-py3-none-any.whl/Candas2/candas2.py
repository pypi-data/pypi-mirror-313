import pandas as pd
import can


class Candas:

    def __init__(self, blf_file):
        self.blf_file = blf_file
        with can.BLFReader(self.blf_file) as log:
            data = [(msg.timestamp,
                     hex(msg.arbitration_id),
                     msg.is_rx,
                     msg.dlc,
                     msg.data.hex(),
                     msg.channel)for msg in log if not msg.is_error_frame]
                                                
        self.df = pd.DataFrame(data, columns = ['Timestamp',
                                                'Arbitration_ID',
                                                'Is_Rx',
                                                'DLC',
                                                'Data',
                                                'Channel'])
        self.df['Miliseconds'] = (self.df['Timestamp'] - self.df['Timestamp'].min()) * 1000

    def id_filtering(self, id_filter):
        
        self.id_df = self.df.loc[(self.df['Arbitration_ID'] == id_filter)].copy()
        self.id_df['Time_dif'] = self.id_df['Miliseconds'].diff()


    def time_rev(self, period_time, tolerance):
        
        min_time = period_time - ((period_time*tolerance)/100)
        max_time = period_time + ((period_time*tolerance)/100)
        
        self.id_df['Time_Jud'] = (self.id_df['Time_dif'] >= min_time & self.id_df['Time_dif'] <= max_time)
        time_jud = self.id_df['Time_Jud'].copy()
        false_indices = time_jud.index[time_jud[0:] == False]
        if len(false_indices) > 1:
            return False
        else:
            return True
        
if __name__ == '__main__':
    blf = Candas(r'C:\Users\Folder\file.blf')