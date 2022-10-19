for ((i=1; i<=10; i++))
do
    python3 -m connect4.ConnectFour ai1 ai connect4/initial_states/case4.txt --time 20 
done

for ((i=1; i<=10; i++))
do
    python3 -m connect4.ConnectFour ai ai1 connect4/initial_states/case4.txt --time 20 
done