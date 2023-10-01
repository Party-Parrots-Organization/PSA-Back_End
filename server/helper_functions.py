import port_distance_client

def calculate_accumulated_distance(port_list):
    total_distance = 0
    for i in range(0,len(port_list)-2):
        port_pair = sorted([port_list[i], port_list[i+1]])
        distance = port_distance_client.get_route_distance(port_pair[0], port_pair[1])
        total_distance += distance
    return total_distance