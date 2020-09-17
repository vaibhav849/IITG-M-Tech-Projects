#include<stdio.h> 
#include<stdlib.h> 
#include<unistd.h> 
#include<sys/types.h> 
#include<string.h> 
#include<sys/wait.h> 
#include<time.h>

int main(int argc, char **argv){
	
    int N,P;
    
    //N is the size of grid in 2nd command line argument
    N = atoi(argv[1]);
    
    //P is the number of players in 3rd command line argument
    P = atoi(argv[2]);
    
    //Creating arrays to store information about snakes and ladders
    int ladders[N + 1], snakes[N + 1];
    
    //Initializing snakes and ladders
    for(int i = 0; i <= N; i++){
		
        snakes[i] = -1;
        ladders[i] = -1;
        
    }
    
    //Creating variables which will be used during parsing of input file
    int start,end;
    char what;
    
    //Creating file pointer to parse information of snakes and ladders from file
    FILE *fp = fopen(argv[3],"r");
    
    //Parsing file to update positions of snakes and ladders
    while(fscanf(fp, "%c %d %d ",&what, &start, &end) != EOF){
		
		//checking for snake
        if(what == 'S'){
			
			//In case of snake start index should be greater than end index 
            if(start > end && start >= 1 && end <= N && end >= 1 && start <= N){
				
				//Updating position of snake
                snakes[start] = end;
                
            }
        }
        
        //checking for ladder
        else if(what == 'L'){
			
			//In case of ladder start index should be less than end index 
            if(start < end && start >= 1 && end <= N && end >= 1 && start <= N){
				
				//updating position of ladder
                ladders[start] = end;
                
            }          
        }        
    }
	
	//Creating pipes for communication between players(child processes) and gameboard(parent) 
	//Gameboard(parent) will write on pp and players(child processes) will write on cp
    int pp[2*P],cp[2*P];
    
    //Initializing all pipes
	for(int i = 0; i < P; i++){
		
		pipe(&pp[2*i]);
		pipe(&cp[2*i]);
		
	}
	
	//Creating array to store process id of players(child processes) 
    int players[P];
    
    //spawning required number of players(child processes) 
    for(int i = 0; i < P; i++){
		
			//Creating players(child processes) 
			int pid = fork();

			//Players(child processes) will run this code
			if(pid == 0){
				
				//Setting seed so that rand() generate more random numbers 
				srand(time(NULL)+i);
				
				while(1){
					
					int id = -1,num;
					
					//Closing writing end of pp as it only wants to read from pp
					close(pp[2*i + 1]);
					
					//Closing reading end of cp as it only wants to write on cp
					close(cp[2*i]);
					
					//Reading id from pp pipe
					read(pp[2*i], &id, sizeof(id));
						
					//Player(child) will write on pipe only when it receives its id from parent
					if(id == getpid()){
						
						//Player is generating random number(1 - 6)
						num = rand()%6 + 1;
						
						printf("Number Generated = %d\tPlayer Id = %d\n", num, i+1);
						fflush(stdout);
						
						//Writing random number(1 - 6) on the cp pipe
						write(cp[2*i + 1], &num, sizeof(num));
						
					}	
				}
			}
			
			//Gameboard(parent) will run this code
			else{
				
				//Storing proceess ids of players(child processs)
				players[i] = pid;
					
			}
    }
    
    //Creating array to store positions of all players
    int positions[P];
    
    //Setting starting positions of players as 0
    for(int i = 0; i < P; i++){
		
        positions[i] = 0;
        
    }
	
	int i, current;
	
	//Setting seed so that rand() generate more random numbers 
	srand(time(NULL));
	
	//Giving first chance to a random player
    i = rand() % P;
    
    //Setting position of current player as 0
    current = 0;
    
    //Loop will run untill any player crosses the last square of grid
    while(current <= N){
		
        int id,random,winner = -1;
        printf("\n");
        
        //giving chance to the respective player
        id = players[i];
        
        //Closing writing end of cp as it only wants to read from cp
        close(cp[2*i + 1]);
        
        //Closing reading end of pp as it only wants to write on pp
        close(pp[2*i]);
        
        //Writing process id of respective player
        write(pp[2*i + 1], &id, sizeof(id));
        
        //Reading random number(1 - 6) received from respective player
        read(cp[2*i], &random, sizeof(random));
     
        //If random number is less than 6
        if(random < 6){
			
			//Increasing position of respective player by adding number transmitted by player
            positions[i]+=random;
            
            //Checking for snake if position of player did'nt crossed the last square grid
            if(positions[i] <= N && snakes[positions[i]] != -1){
				
				//Updating new position if there is a snake
                positions[i] = snakes[positions[i]];
                
            }
            
            //Checking for ladder if position of player did'nt crossed the last square grid
            else if(positions[i] <= N && ladders[positions[i]] != -1){
				
				//Updating new position if there is a ladder
                positions[i] = ladders[positions[i]];
                
            }
            
            //Setting current as position of current player
            current = positions[i];
            
            //If current has crossed the square grid then setting winner
            if(current > N){
				
				//Some index balancing
                winner = i + 1;
                
            }
            
            //Giving chance to the next player
            i++;
            
            //Making sure that i should be in range(0 - P - 1)
            i = i % P;
            
        }
        
        //If random number equals to 6
        else{
			
			//Increasing position of respective player by adding number transmitted by player
            positions[i]+=random;
            
            //Checking for snake if position of player did'nt crossed the last square grid
            if(positions[i] <= N && snakes[positions[i]] != -1){
				
				//Updating new position if there is a snake
                positions[i] = snakes[positions[i]];
                
            }
            
            //Checking for ladder if position of player did'nt crossed the last square grid
            else if(positions[i] <= N && ladders[positions[i]] != -1){
				
				//Updating new position if there is a ladder
                positions[i] = ladders[positions[i]];
                
            }
            
            //Setting current as position of current player
            current = positions[i];
            
            //If current has crossed the square grid then setting winner
            if(current > N){
				
				//Some index balancing
                winner = i + 1;
                
            }
            
            //No i++ as same player will get the chance again as it got 6 in previous chance
        }
        
        //Printing positions of all players after each chance(iteration)
        for(int j = 0; j < P; j++){
			
            printf("Position of Player %d : %d\n", j+1, positions[j]);
            
        }
        
        //Repeating with same player if it got 6 in this chance and iff there are more than 1 players in the game
        if(random == 6 && current <= N && P != 1){

			printf("\nRepeating with same Player as it got 6 in previous chance\n");
		}
        
        //Printing the name of winner if position of current player is crossed last square grid
        if(winner != -1){
		
            printf("\nPlayer %d is Winner!\n", winner);
            break;
            
        }
        
    }
   
	//Killing all the players(child processes) and closing both ends of all the pipes as game has ended
    for(int k = 0; k < P; k++){
		
		kill(players[k], SIGKILL);
		close(pp[2*k]);
		close(pp[2*k + 1]);
		close(cp[2*k]);
		close(cp[2*k + 1]);
		
	}
	
	//Printing exit message after completion of Game
	printf("Game has been ended Successfully!\n");
	
    return 0;
}
