# Import necessary modules
import os
import eyed3
import yaml
import datetime

# Function to write data to a YAML file
def write_to_yaml(audio_files):
  # Create a dictionary with the data to be written to the YAML file
  data = {
    'title': 'The Future in Tech',
    'subtitle': 'Powered by LinkedIn Learning',
    'author': 'Ray Villalobos',
    'description': 'Conversations with leaders building next generation techology tools.',
    'image': '/images/artwork.jpg',
    'language': 'en-us',
    'category': 'Technology',
    'format': 'audio/mpeg',
    'item': audio_files  # The audio files data will be written under the 'item' key
  }
  # Open the YAML file in write mode and dump the data into it
  with open('episodes.yaml', 'w') as file:
    yaml.dump(data, file)

# Function to get audio files data
def get_audio_files():
  # Use a list comprehension to create a list of dictionaries, each containing data for one audio file
  audio_files = [{
    'title': audiofile.tag.title,
    'description': ', '.join(comment.text for comment in audiofile.tag.comments),
    'published': audiofile.tag.release_date,
    'file': '/audio/' + file,
    'duration': str(datetime.timedelta(seconds=int(audiofile.info.time_secs))),
    'length': "{:,}".format(os.path.getsize(os.path.join('audio', file)))
  } for file in os.listdir('audio') if file.endswith('.mp3') for audiofile in [eyed3.load(os.path.join('audio', file))]]
  return audio_files

# Function to prevent YAML from sorting the data
def noalias_dumper(dumper, data):
  return dumper.represent_mapping(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, data.items(), flow_style=False)

# Register the function as a representer for dictionaries
yaml.add_representer(dict, noalias_dumper)

# Get the audio files data
audio_files = get_audio_files()
# Write the data to the YAML file
write_to_yaml(audio_files)