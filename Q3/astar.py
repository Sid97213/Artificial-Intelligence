"""
Parth Krishna Sharma : 2017B3A70907H
Siddhi Burse : 2017B3A70972H
Piyush Phatak : 2017B3A70425H
Keshav Pandya : 2017A3PS0399H

"""


# OpenStreetAPI is used to fetch the coordinates of townships(localities) in latitude 
# and longitude from the source to the destination. There are 40 locations considered in 
# the map. The picture of the hand drawn map is also submitted. The edge weights between the 
# different map points are calculated as the duration it takes to move along the edge 
# using the distance metric API of google-maps. The heuristic function used is the
# time it takes to reach the destination from each point in the
# map (again calculated using google's distance metric api)

# The heuristic function used in the A* algorithm is
# f(n) = g(n) + h(n)

from tkinter import *
from tkinter import messagebox as mb 
import urllib.request
import json
import webbrowser
import sys
import pandas

def dura(src_lat, src_lng, dest_lat, dest_lng):
    endpoint = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&'
    api_key = 'AIzaSyAMWJctuV0azNvNCm6zS9ASEZj_xn-dbIM'
    nav_request = 'origins={}&destinations={}&key={}'.format(src_lat+','+src_lng,dest_lat+','+dest_lng,api_key)
    request = endpoint + nav_request
    response = urllib.request.urlopen(request).read()
    duration = json.loads(response)
    duration = duration['rows'][0]['elements'][0]['duration']['value']
    duration = float(duration/60)
    return duration


def func(start, end):
	df = pandas.read_csv('coordinates.csv')

	df2 = pandas.read_csv('places.csv')

	NOP_coordinate = {}

	cnt=0
	for i in df2['Locations']:
	    NOP_coordinate[i] = (float(df['Latitude'][cnt]),float(df['Longitude'][cnt]))
	    cnt+=1


	#Dictionary 2 : NOP -> [list of (NOP,edge_weight) to which it goes]

	df3 = pandas.read_csv('edge_with_weights.csv')



	# making adjacency list
	Edges = {}

	for i in range(41):
	    Edges[df2['Locations'][i]] = []

	for i in range(68):
	    Edges[df3['Source'][i]].append((df3['Destination'][i],df3['Weight'][i]))
	    Edges[df3['Destination'][i]].append((df3['Source'][i],df3['Weight'][i]))
	    

	# Implementing A*
	# start = input("Enter Source: ")
	# end = input("Enter Destination: ")

	argumentList = sys.argv
	# print(argumentList)

	# start = sys.argv[1]
	# end = sys.argv[2]
	# print(start)
	# print(end)
	# print('\n')

	#Dictionary 3 : NOP -> Heuristic Value

	Heuristic = {}
	    
	df4 = pandas.read_csv('places.csv')

	for i in range(41):
	    s1 = df4['Locations'][i]
	    s2 = end
	    #storing time required to reach destination from each node
	    Heuristic[s1] = dura(str(NOP_coordinate[s1][0]),str(NOP_coordinate[s1][1]),str(NOP_coordinate[s2][0]),str(NOP_coordinate[s2][1]))


	#making the open list for A* algo, which will store the (f(n), NOP)
	open_list = [(0+Heuristic[start],start)]  #we initialised the open list with our source location
	parent = {} #parent list

	f_n = {} #f(n) value for the nth node.

	for i in df2['Locations']:
	    f_n[i] = 1000000000   #initialising the f(n) value for all nodes with a max value

	mx = 1000000000
	closed=[] #defining a closed list
	f_n[start] = Heuristic[start]



	# end when open_list is empty or when we have reached goal and there is 
	# no shorter path.
	while( (len(open_list) > 0) and (mx > open_list[0][0])):
	    # print(open_list)
	    next_closest = open_list[0] # picking node for traversal from the open list
	    # deleting the traversed node from open list and putting into closed.
	    del(open_list[0])
	    closed.append(next_closest[1])
	    # print(next_closest[1])
	    # print("++++++++++")
	    # print(Edges[next_closest[1]])
	    # print("$$$$$$$$$$$$$$$$$$")
	    
	    # stop if we have reached the destination
	    if(next_closest[1] == end):
	        mx = next_closest[0]


	    # else check all the edges of current node to find the next stop
	    for i in Edges[next_closest[1]]:
	        # print("Next closest[0] =====  ", next_closest[0])
	        # print("Heuristic[next_closest[1]]  =====  ", Heuristic[next_closest[1]])

	        # calculate heuristic value for the current node via current path

	        f = next_closest[0] - Heuristic[next_closest[1]] + Heuristic[i[0]] + i[1]
	        # if this heauristc value is lesser than the previous stored, that means this is the optimal value.
	        if f < f_n[i[0]]:
	            t = (f_n[i[0]],i[0])
	            parent[i[0]] = next_closest[1]
	            #updating f(n) value if node is in open list
	            if (t in open_list):
	                open_list.remove(t)
	                open_list.append((f,i[0]))
	                f_n[i[0]] = f
	            #updating f(n) value if node is in closed list
	            elif i[0] in closed:
	                closed.remove(i[0])
	                open_list.append((f,i[0]))
	                f_n[i[0]] = f
	            else:
	                open_list.append((f,i[0]))
	                f_n[i[0]] = f

	node = end
	path = []
	coordinates = []


	#finding the path
	while(node != start):
	    path.append(node)
	    node = parent[node]
	    
	path.append(start)

	path.reverse()

	for node in path:
	    c = []
	    c.append(NOP_coordinate[node][0])
	    c.append(NOP_coordinate[node][1])
	    coordinates.append(c)

	# print("The most optimal Path is ----------->")
	# print()
	# print(path)
	# print()
	# print("Coordinates of the points are -------------> ")
	# print()
	# print(coordinates)
	# print()
	# print("Optimal duration of the journey is -------->")
	opti_duration = f_n[end]
	# print(f_n[end], " minutes.")

	#print('\n')

	url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Road/Routes?"
	for i in range(len(coordinates)):
	    url = url + "wp."+str(i)+"="+str(coordinates[i][0])+","+str(coordinates[i][1])+"&"
	url = url + "key=AlHaFbrw006PkrgcKFwhW_fO8mpDq5w8gZc47tAfnRfVZj1gmTg6fq3y0n9m-ZIB"

	# print("Bing Map Url is :\n")
	# print(url)
	# print('\n')
	webbrowser.open(url)


	# print("To see a better view on google map, just copy-paste the coordinates from the terminal to",end=" ")
	# print("the google_map_path.html file and see the html file on the browser !")

	#print('\n')


	return path, coordinates, opti_duration

#path, coordinates, opti_duration = func("Uppal", "RGIA")
#print(path)

def show():
    src = src_loc.get()[2:-3]
    dest = dest_loc.get()[2:-3]
    path, coordinates, opti_duration = func(src,dest)
    opti_path.delete(0.0,END)
    opti_path.insert(END,path)
    coords.delete(0.0,END)
    coords.insert(END,coordinates)
    time.delete(0.0,END)
    time.insert(END,opti_duration)

master = Tk()
master.geometry("900x570")
backgrnd_colr = "lemon chiffon"
master.configure(background=backgrnd_colr)
master.title('A* Algorithm Navigation')

#Label
Label (master,text="Enter Source: ",bg=backgrnd_colr,fg="black",font="none 14 bold").place(x=150,y=50)
Label (master,text="Enter Destination: ",bg=backgrnd_colr,fg="black",font="none 14 bold").place(x=150,y=80)
Label (master,text="Most Optimal path: ",bg=backgrnd_colr,fg="black",font="none 14 bold").place(x=90,y=160)
Label (master,text="Coordinates of the points are: ",bg=backgrnd_colr,fg="black",font="none 14 bold").place(x=90,y=300)
Label (master,text="Optimal Duration of the journey: ",bg=backgrnd_colr,fg="black",font="none 14 bold").place(x=90,y=450)
Label (master,text="minutes",bg=backgrnd_colr,fg="black",font="none 14 bold").place(x=630,y=450)

#DropDown list
df_temp = pandas.read_csv('places.csv')
options = df_temp.values.tolist()
options.sort()
src_loc = StringVar()
src_loc.set(options[0])
dest_loc = StringVar()
dest_loc.set(options[1])
drop1 = OptionMenu(master,src_loc,*options)
drop1.configure(bg="snow",fg="black",font="none 13 bold",width=22)
drop1.place(x=400,y=40)
drop1 = OptionMenu(master,dest_loc,*options)
drop1.configure(bg="snow",fg="black",font="none 13 bold",width=22)
drop1.place(x=400,y=80)

#Button
bttn_clr = "tan1"
Button (master,text="ENTER",bg=bttn_clr,fg="black",font="none 13 bold",width=6,height=1,command=show).place(x=720,y=60)
Button (master,text="STOP",bg=bttn_clr,fg="black",font="none 13 bold",width=6,height=1,command=master.destroy).place(x=760,y=510)

#TextBox
opti_path = Text (master,fg="black",font="none 13 bold",width=68,height=5)
opti_path.place(x=80,y=195)
coords = Text (master,fg="black",font="none 13 bold",width=68,height=5)
coords.place(x=80,y=335)
time = Text (master,fg="black",font="none 14 bold",width=10,height=1)
time.place(x=500,y=450)
mainloop()
