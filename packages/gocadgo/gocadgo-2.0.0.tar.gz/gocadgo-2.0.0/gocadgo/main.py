from gocadgo.network import Network
from helper import set_boundary, set_initial
from plotter import show_fields

def main():
    # scaling size 400 for mesh. Create mesh and run network:
    from_task = Network('from_task.json')

    # re-run with new mesh size finding k_t and k_p.
    actual_size = Network('actual_size.json', from_task.k)

    # display fields of interest on network hot or cold network:
    show_fields(actual_size.hnet, 'T', title = "T plot for Hot Network")
    show_fields(actual_size.cnet, 'T',  title = "T plot for Cold Network")
    show_fields(actual_size.hnet, 'P', title = "P plot for Hot Network")
    show_fields(actual_size.cnet, 'P',  title = "P plot for Cold Network")

if __name__ == "__main__":
    main()
