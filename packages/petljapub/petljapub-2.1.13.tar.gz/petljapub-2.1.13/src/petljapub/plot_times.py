import matplotlib.pyplot as plt

def plot_times(times, langs=[], sol=None):
    fig, ax = plt.subplots()    
    width = 0.35
    i = 0
    for s in times["times"].keys():
        if sol and sol != s:
            continue
        for l in times["times"][s].keys():
            if langs and lang not in langs:
                continue
            y = [times["times"][s][l][test] for test in times["times"][s][l].keys()]
            n = len(times["times"][s][l].keys())
            x = list(map(lambda x: x + i*width, range(n)))
            rects = ax.bar(x, y, width, label=s + "-" + l)
            ax.set_xticks(range(n))
            ax.set_xticklabels(times["times"][s][l].keys())
            ax.bar_label(rects, padding=3)            
            i += 1
    ax.legend()
    ax.set_ylabel("miliseconds")
    fig.suptitle('Execution time', fontsize=16)
    fig.tight_layout()
    plt.show()
    
