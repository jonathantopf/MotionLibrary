import os
import re

def new_from_aftereffects_file (file_path):
    animation = Animation ()
    animation.title = (os.path.splitext(os.path.split (file_path)[-1]))[0]
    
    # Open file
    file = open (file_path, "r")

    # Begin itterating

    # FPS
    line = file.readline ()
    while line:
        match = re.search ('\sUnits Per Second\s+(\d+\.?\d*)', line)
        if match:
            animation.fps = float(match.group (1))
            break
        line = file.readline ()

    # Find start of keyframe frame data
    line = file.readline ()
    while line:
        match = re.search ('\sFrame\sX\spixels\sY\spixels\sZ\spixels', line)
        if match:
            break
        line = file.readline ()

    # Keyframe data
    line = file.readline ()
    while line:
        match = re.search ('(\d+)\s(-?\d+\.?\d+)\s(-?\d+\.?\d+)\s(-?\d+\.?\d*)', line)
        if match:
            animation.position_samples.append([float(match.group(2)), float(match.group(3)), float(match.group(4))])
        else:
            break
        line = file.readline ()

    return animation

class Animation ():
    def __init__(self):
        self.title = ""
        self.fps = 30
        self.position_samples = []

    def safe_name (self):
        return self.title.replace (" ", "_").lower ()

    def output_preview_css_animation_file (self, output_directory):

        max_position_component = self.get_max_position_component ()
        min_position_component = self.get_min_position_component ()
        min_position = self.get_min_position ()

        output = "\n"
        output += "@keyframes {0}_animation\n".format(self.safe_name())
        output += "{\n"

        for i, position_sample in enumerate(self.position_samples):

            transformed_sample = [self.position_samples[i][0],self.position_samples[i][1]]

            # Offset animation
            transformed_sample[0] -= min_position[0]
            transformed_sample[1] -= min_position[1]

            # Scale animation to 0-1
            transformed_sample[0] /= max_position_component - min_position_component
            transformed_sample[1] /= max_position_component - min_position_component

            # Scale animation to 0-100
            transformed_sample[0] *= 100
            transformed_sample[1] *= 100

            line = "  {0}%   {{left: {1}%; top: {2}%;}}\n".format(
                float(i * 100) / len(self.position_samples), 
                (transformed_sample[0]), 
                (transformed_sample[1]),
                0)

            output += line

        output += "}\n\n"
        output += ".{0}\n".format (self.safe_name ())
        output += "{\n"
        output += "  animation: {0}_animation {1}s infinite;\n".format(self.safe_name(), self.duration())
        output += "}\n"
        
        if (not os.path.exists (output_directory)):
            os.mkdir (output_directory)

        output_file_path = os.path.join (output_directory, "{0}_preview.css".format(self.safe_name()))
        output_file = open (output_file_path, 'w')
        output_file.write (output.encode ('utf8'))
        output_file.close ()
        return output_file_path

    def get_max_position_component (self):
        max_position_component = self.position_samples[0][0]
        for position_sample in self.position_samples:
            if position_sample[0] > max_position_component:
                max_position_component = position_sample[0]
            if position_sample[1] > max_position_component:
                max_position_component = position_sample[1]
            if position_sample[2] > max_position_component:
                max_position_component = position_sample[2]
        return max_position_component

    def get_min_position (self):
        min_position = self.position_samples[0]
        for position_sample in self.position_samples:
            if position_sample[0] < min_position[0]:
                min_position[0] = position_sample[0]
            if position_sample[1] < min_position[1]:
                min_position[1] = position_sample[1]
            # We dont use Z because its always 0
        return min_position
            
    def get_min_position_component (self):
        min_position = self.get_min_position ()
        if (min_position[0] < min_position[1]):
            return min_position[0]
        return min_position[1]


    def duration (self):
        return len(self.position_samples) / self.fps


