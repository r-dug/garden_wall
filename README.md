# Overview

This project is an effort to protect my garden from chipmunks and squirrels who surrepticiously pilfer ripe tomatoes and cucumbers, only to discard them after taking a single bite. They seem to remember after digging into them *"YUCK! Why's it so sweet and savory at the SAME TIME!?!?"*. Building this has been a fun way to learn about object detection, play more with Raspberry Pis, and configure client-server communication on my local network. It serves as inspo for future endeavors (eg. a local streaming platform on our home network using music we OWN).

I wanted to try to solve this problem economically, so price of materials was a major consideration. I also wanted fairly low latency for the response to detected vermin (sorry rodent lovers - I acknowledge chipmunks' cuteness but don't want them in my garden).

## Setup

The Software components for this project are really pretty simplistic: a client to send a video feed, and a server to receive and process the feed via a YOLO object detection model, and a some conditional logic to open a solenoid valve. Balancing budget concerns with sourcing adequate hardware was probably the trickiest part. 

### Hardware

#### PI

Raspberry Pi is so awesome. They're cheap, easy to work with for those accustom to linux, and can do SO MUCH! Honestly, I'm very impressed with the PI for how accessible it is. Although I used a seperate machine with vastly more compute to run inferences for the pi last grow season, I will experiment this winter with running inferences on the PI itself. 

The most crutial considerations for this project were weatherproofing and poweringthe pi. I used a cheap j-box I found on amazon to protect electronics from the rain, and heat sinks to disipate the... well... heat. The heat of the growing season here in Kentucky, however, WAS problematic. The PI would essentially just stop working if it got too hot. The location of the PI was something I experimented quite a lot with. When the PI was indoors, no problem. However, when it was, the webcam could not be placed in an ideal location to monitor the garden. For that reason, I may opt for wi-fi capable, solar powered cameras in the future... And might outfit the property with security while I'm at it.

#### Camera

I used a cheap logitec webcam as the RGB sensor to provide a feed of images on which to run inference. Other potential options included wi-fi capable security cameras, which seem like a reasonably good solution, but are often expensive... The logitec webcam seemed a suitable option for its price and versatility outside of this particular project.

Location was obviously important. I tried extending the webcam's cabled connection with CAT/USB adapters, but the conversion resulted in serious degredation of the feed's quality. Apparently some adapters exist that won't degrade the quality but I'm unwilling at this time to put the money towards experimenting with them, and returned the ones I did try to Amazon. USB extensions were either too expensive, or too short. Consequently, I needed to place the housing for the PI close enough to an appropriate location for the camera.

#### WiFi card

I needed to use a wifi card to enable the PI, since the model I had on hand was not wifi capable. 'Twas cheap and worked.

#### Sprinkler System

- **Solenoid Valve**
  - I found a pretty cheap chinese model on Amazon. I wired it through a relay with power boost to the PI with AWG wire (doorbell wire, because it was CHEAP!). 
- **"Plumbing"**
  - Uhhhhmm... I just burried a gardsen hose. We'll call this a beta version this year.... though I might consider PVC for a more permenant installation, particularly if I use the same irrigation for my drip issigation system.
- **Sprinklers**
  - I used in-ground, pop-up springler heads from [Rain Bird](https://store.rainbird.com/)
    - This was *the* choice, because it was discrete and could stay where it was even if someone was mowing the lawn or whatever.

### Software

#### Flask API

Flask is a simple, high level python framework to maintain a stream between the PI and the server. I only needed some very simple functions from flask to create an API. It was very easy.

#### YOLO!

Object detection out of the box. Pretty neat! Only thing is... the pretrained YOLO model has no class for squirrels or chipmunks, at least not the one I was using (I think trained on COCO but it's been a while). Cats were a decently effective class label, as it turns out. However, my german shepherd dog was sometimes labeled a cat... sorry buddy.  Consequently, I thought transfer learning / fine-tuning would be a good option (and it may well be). However, I need to find better methods for dataset creation. Tools exist to add bounding boxes to image sets so they might be used in object detection, but doing this manually is tedious ad infinitum. I'm not working on this project right now though... maybe later.

