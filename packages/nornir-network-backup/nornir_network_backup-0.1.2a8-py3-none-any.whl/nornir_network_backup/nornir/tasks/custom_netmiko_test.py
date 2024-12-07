# direct netmiko connection


def netmiko_direct(task):

    list_of_commands = ["show ip int brief", "show ip arp"]
    # Manually create Netmiko connection
    net_connect = task.host.get_connection("netmiko", task.nornir.config)
    results_dict = {}
    for cmd in list_of_commands:
        output = net_connect.send_command(cmd)
        results_dict[cmd] = output

    # You also could make a more formal Nornir Results object
    return results_dict
