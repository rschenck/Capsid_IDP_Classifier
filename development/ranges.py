import dataset as ds
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

scores, type_array = ds.load_data()
a_max_indexes, b_max_indexes = [],[]
gt_75_arr =  []
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
                if max_index > 75 or max_index <= 26:
                    fig = plt.figure()
                    plt.plot(x,scores[i],'r-')
                    plt.axis([0,130,0,1.2])
                    plt.title(type_array[i] + " - max index: " + str(max_index) + " - entry #" + str(i))
                    pdf.savefig(fig)
                if max_index > 75:
                    gt_75_arr.append(i)
                b_max_indexes.append(max_index)

print "Type B's greater than 75: ", len(gt_75_arr)
print "indexes for above: ", gt_75_arr
print "Type A max range: ", min(a_max_indexes) ,max(a_max_indexes)
print "Type B max range: ", min(b_max_indexes) ,max(b_max_indexes)

problem_indexes = [13, 26, 31, 42, 45, 76, 80, 81, 141, 217, 218, 219, 220, 221, 258, 287, 288, 300, 301, 307, 308, 328, 329, 330, 343, 361, 366, 375, 380]
with PdfPages('problem_children.pdf') as pdf2:
    for i in range(len(scores)):
        max_val  = max(scores[i])
        max_index = list(scores[i]).index(max_val)
        if problem_indexes.count(i) != 0:
            fig = plt.figure()
            plt.plot(x,scores[i],'r-')
            plt.axis([0,130,0,1.2])
            plt.title(type_array[i] + " - max index: " + str(max_index) + " - entry #" + str(i))
            pdf2.savefig(fig)
