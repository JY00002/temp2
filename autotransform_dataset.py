import h5py
import numpy as np
 
mods = ['32PSK','16APSK','32QAM','FM','GMSK','32APSK','OQPSK','8ASK','BPSK','8PSK','AM-SSB-SC','4ASK','16PSK','64APSK','128QAM','128APSK','AM-DSB-SC','AM-SSB-WC','64QAM','QPSK','256QAM','AM-DSB-WC','OOK','16QAM']
mods_filt=['BPSK','QPSK','8PSK','GMSK','16APSK','64APSK','16QAM','64QAM','AM-DSB-WC','FM']


snr_range=[-8,8]
snrs=np.array(range(snr_range[0],snr_range[1]+1,2))
mods=np.array(mods)
mods_filt=np.array(mods_filt)

file_name = 'dataset/2018.01/GOLD_XYZ_OSC.0001_1024.hdf5'
Xd = h5py.File(file_name, 'r')

frame_length=64

data = np.empty((0,frame_length,2))
mod_label = []
snr_label = []

for ind in range(0,len(Xd['X'])):
    mod=mods[np.argmax(np.array(Xd['Y'][ind]))]
    snr=Xd['Z'][ind]
    
    if mod in mods_filt and snr in snrs:
        temp=np.array(Xd['X'][ind])
        temp1=np.split(temp,(1024/frame_length),axis=0)
        data=np.concatenate((data,temp1),axis=0)
        for i in range(0,(1024/frame_length)):
                 mod_label.append(Xd['Y'][ind])
                 snr_label.append(Xd['Z'][ind])

del Xd

data_file = h5py.File('dataset/RML2018_selected_data.hdf5', 'w')
data_file.create_dataset('data', data=data)
data_file.create_dataset('mod_label', data=np.array(mod_label))
data_file.create_dataset('snr_label', data=np.array(snr_label))

data_file.close()
