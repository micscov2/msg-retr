#/bin/bash

# Loading other scripts
. utils.sh

# Global variables
declare -A servers

echo "+-------------------------------------------+"
echo "| -- Welcome to Py-IRC Command Line: ZYNC --|"
echo "+-------------------------------------------+"

start_server()
{
    echo -n "Please enter name of server: "
    read server_name
    echo -n "   Please enter port number: "
    read port_num
    ./start.sh $port_num $server_name & &> debug.log
    print_empty_line
    if [ $? == 0 ]; then
        echo "Server $server_name started successfully on $port_num :)"
    else
        echo "Errors occurred while starting server"
    fi
    servers[$server_name]=$!
    print_empty_line
}

stop_server()
{
    echo -n "Please enter server name: "
    read server_name
    server_pid=${servers[$server_name]}
    kill -9 $server_pid
    print_empty_line
    if [ $? == 0 ]; then
        echo "Server $server_name stopped successfully"
    else
        echo "Errors occured while stopping server"
    fi
    print_empty_line
}

list_servers()
{
    print_empty_line
    echo "Servers List"
    for item in "${!servers[@]}"; do
        echo "-> " $item
    done
    print_empty_line
}

start_cache_server()
{
    print_empty_line
    echo "Starting cache server..."
    print_empty_line
}

check_performance_stats()
{
    print_empty_line
    echo "Computing performance stats..."
    for item in "${!servers[@]}"; do
        echo "For server: $item"
        res=$(grep "PERF" "server_"$item".log" | tail -n 2 | awk '{print $6}')
        groups=$(echo $res | cut -f1 -d" ")
        clients=$(echo $res | cut -f2 -d" ")
        echo "  Number of groups -> $groups"
        echo " Number of clients -> $clients"
    done
    print_empty_line
}

while [ 1 ]; do
    echo "Press 1: Start a new server"
    echo "Press 2: Stop a server"
    echo "Press 3: List all servers"
    echo "Press 4: Start cache server"
    echo "Press 5: See performance stats"
    echo -n "  Input: "
    read option_selected
    print_empty_line

    case $option_selected in
        1) start_server ;;
        2) stop_server ;;
        3) list_servers ;;
        4) start_cache_server ;;
        5) check_performance_stats ;;
    esac
done
