import dataset as ds
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

scores, type_array = ds.load_data()
a_max_indexes, b_max_indexes = [],[]
with PdfPages('type_b_high_max_index_graphs.pdf') as pdf:
    x = range(0,125)
    for i in range(len(scores)):
        max_val  = max(scores[i])
        max_index = list(scores[i]).index(max_val)

        if type_array[i] == "Type A":
            a_max_indexes.append(max_index)
        elif type_array[i] == "Type B":
            if max_index == 0:
                # plt.plot(range(0,125),scores[i],'r-')
                # plt.axis([0,130,0,1.2])
                # plt.title(type_array[i])
                # plt.show()
                print "skipping one"
            else:
                if max_index >= 100:
                    fig = plt.figure()
                    plt.plot(x,scores[i],'r-')
                    plt.axis([0,130,0,1.2])
                    plt.title(type_array[i])
                    pdf.savefig(fig)
                b_max_indexes.append(max_index)


print "Type A max range: ", min(a_max_indexes) ,max(a_max_indexes)
print "Type B max range: ", min(b_max_indexes) ,max(b_max_indexes)
