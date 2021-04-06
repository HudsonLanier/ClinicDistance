import urllib
from urllib import request

my_bing_key ='Aubd9H_Chw0zhNdONq22LAVjFVTnlwVeAXgl-QLwQKtQzXb67PF5Hh1dyRhMgdep'

#http://dev.virtualearth.net/REST/v1/Routes?wayPoint.1={wayPoint1}&viaWaypoint.2={viaWaypoint2}&waypoint.3={waypoint3}&wayPoint.n={waypointN}&heading={heading}&optimize={optimize}&avoid={avoid}&distanceBeforeFirstTurn={distanceBeforeFirstTurn}&routeAttributes={routeAttributes}&timeType={timeType}&dateTime={dateTime}&maxSolutions={maxSolutions}&tolerances={tolerances}&distanceUnit={distanceUnit}&key={BingMapsKey}
#http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0=london&wp.1=leeds&avoid=minimizeTolls&key=my_bing_key

sample_coordinates1 = (51.0665226, -114.2094385)
sample_coordinates2 = (39.16301429732479, -75.52250481727634)

def make_url_ready_coords(some_coordinates):
    cleaned_up_coords = str(some_coordinates[0]) + ',' + str(some_coordinates[1])
    return cleaned_up_coords

# start_location = make_url_ready_coords(sample_coordinates1)
# end_location = make_url_ready_coords(sample_coordinates2)

# a working link:
#http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0=london&wp.1=leeds&avoid=minimizeTolls&key=Aubd9H_Chw0zhNdONq22LAVjFVTnlwVeAXgl-QLwQKtQzXb67PF5Hh1dyRhMgdep

#a test
#http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0=51.0665226,-114.2094385&wp.1=39.16301429732479,-75.52250481727634&avoid=minimizeTolls&key=Aubd9H_Chw0zhNdONq22LAVjFVTnlwVeAXgl-QLwQKtQzXb67PF5Hh1dyRhMgdep




#url_string = f"http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0={start_location}&wp.1={end_location}&avoid=minimizeTolls&key=Aubd9H_Chw0zhNdONq22LAVjFVTnlwVeAXgl-QLwQKtQzXb67PF5Hh1dyRhMgdep"
#test = request.urlopen(url_string)

def get_data_from_bing(starting_point, ending_point):
    start_location =  make_url_ready_coords(starting_point)
    end_location = make_url_ready_coords(ending_point)
    url_string = f"http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0={start_location}&wp.1={end_location}&avoid=minimizeTolls&key={my_bing_key}"
    bing_info = request.urlopen(url_string)
    data = bing_info.read()
    xml = data.decode("UTF-8")
    start_travel_dist_index = xml.index('<TravelDistance>') + 16
    end_travel_dist_index = xml.index('</TravelDistance>')
    travel_distance = xml[start_travel_dist_index:end_travel_dist_index]
    start_travel_time_index = xml.index('<TravelDuration') +16
    end_travel_time_index = xml.index('</TravelDuration>')
    travel_time= xml[start_travel_time_index: end_travel_time_index]
    patient_hospital_dict = {'travel_distance': travel_distance,
                             'travel_time': travel_time}
    return patient_hospital_dict



