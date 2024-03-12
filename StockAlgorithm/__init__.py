"""
    STOCK ALGORITHM
    Made by Monnapse
"""

import math

def calculate_angle(x1, y1, x2, y2):
    # Calculate the angle between two points relative to the horizontal axis
    return math.atan2(y2 - y1, x2 - x1)

def average_angle(points):
    # Calculate the total sum of sine and cosine components of all angles
    sin_sum = 0
    cos_sum = 0
    
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        angle = calculate_angle(x1, y1, x2, y2)
        sin_sum += math.sin(angle)
        cos_sum += math.cos(angle)
    
    # Calculate the average angle from the sum of sine and cosine components
    avg_angle = math.atan2(sin_sum / len(points), cos_sum / len(points))
    
    return avg_angle

def should_buy(price_points: list):
    #stock_points = [(1000, 10), (2000, 20), (3000, 30), (4000, 40), (5000, 50)]  # Example stock points (timestamp in milliseconds, price)
    avg_angle = average_angle(price_points) - math.pi/2
    print('Average Angle:', math.degrees(avg_angle))
    return False