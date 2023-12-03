
import sys
import subprocess

def run_command_with_output(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(p.stdout.read().decode())

print ("Loading user file...")

userlist = []
with open("/etc/passwd", 'r') as f:
    for line in f:
        userlist.append(line.split(":"))

needuser = False
# this is kind of a pointless variable for now
while needuser == False:
    searchuser = input("Enter the user ID or name to search for: ")
    searchresults = []

    # case-insensitive search
    for idx, u in enumerate(userlist):
        if searchuser.lower() in u[0].lower()  or  searchuser.lower() in u[4].split(',')[0].lower():
                searchresults.append([u[0], u[4].split(',')[0], idx])
    # nothing found
    if len(searchresults) == 0:
        print("Nothing found for " + searchuser)
        continue

    print("Search results: for " + searchuser + "\n")
    for idx, r in enumerate(searchresults):
        print(idx, r[0], r[1])

    selecteduser = input("\nEnter number of user to choose: ")

    #print("You chose", searchresults[int(selecteduser)][0])

    userid = searchresults[int(selecteduser)][0]

    prompt = True
    while prompt == True:
        # print the menu
        print("Job detail 'd <jobnumber>', Current jobs 'c', Job history 'h <days>', Tail job log 't <jobnumber>', WorkDir location 'l <jobnumber>'")
        print("Node detail 'n <nodename>', Show reservations 'r', Down nodes 'dn', Open nodes 'on', Choose new user 'new'")

        userinput = input(" % ").split(' ')

        command = userinput[0]
        output = ""

        if command == "d":
            run_command_with_output("scontrol show job " + userinput[1])
        elif command == "c":
            run_command_with_output("squeue -u " + userid)
        elif command == "h":
            run_command_with_output("sacct -u " + userid + " -S $(date -d '" + userinput[1] +" days ago' +%D-%R) --format=JobID,JobName,Partition,AllocCPUS,State,ExitCode,Start,End")
        elif command == "u":
            print("user detail")
        elif command == "l":
            run_command_with_output("scontrol show job " + userinput[1] + " | sed -n 's/^   WorkDir=//p'")
        elif command == "t":
            run_command_with_output("tail -n 50 $(scontrol show job " + userinput[1] + " | sed -n 's/^   WorkDir=//p')/slurm-" + userinput[1] + ".out")
        elif command == "n":
            run_command_with_output("scontrol show node " + userinput[1])
        elif command == "new":
            prompt = False
            print("quitting")
        else:
            print("Command not found")

