# scale_mask

With the recent outbreak of the COVID-19 virus and it becoming a pandemic, a lot of engineering effort is being executed. As a result of this global issue, a facebook group has been created to make relevant engineering efforts open source. Once such effort uncludes 3D printable masks. There are a many good ones posted. In my opinion the following looks quite good and functional:

1) Roomba attachable filter mask by Wally Reene and other members: https://www.thingiverse.com/thing:4243151
2) Ruben Smit: https://www.thingiverse.com/thing:4233428 which was further derived from another person's design listed in the link as well.

I personally printed 10 of the designs from (2) and trialling it out with some medical professionals in NHS. One thing that I learned is that a standardised fitting test needs to happen such that the mask fits snugly with the user. This just means that there is no universal size so someone needs to either:

1) provide the base schematics and one needs to size it appropriatley either by trial and error
OR
2) provide different sizes of the schematics which still doesn't guarantee good fit

This repository provides a script to scale the mask appropirately. At the time of writing this README, I haven't published it in the facebook group so I will need feedback to see if it works. The script is very simple and essentially it does the following things:

1) Gets as input the distance from nose to chin: You need to measure the vertical distance from your chin to the mid part of your nose or where ever you think a mask's top part will fit based on the design. This is in cm btw.
2) Point to a mask schematic.
3) This script then gets a bounding box around the mask and gets the length.
4) Scale the mesh by a factor of your_nose_to_chin_length_in_cm / length_of_bounding_box.
5) Write out the meshes out to a directory. These meshes are essentially your customised mask components.

# How to set up dependencies

I haven't used virtual env yet or pyinstaller but at the moment I am assuming you have some unix setup where you can invoke python and pip. Please follow the steps below:

1) You need to first install pip: Follow this link https://pip.pypa.io/en/stable/installing/
2) Install numpy: ```pip install numpy```
3) Install numpy-stl: ```pip install numpy-stl```

After this you should be good to go and execute the script

# How to use the script

### Basics ###

You need to download any of the schematics for building the mask. You also need to get the measurement from nose to chin as mentioned above. Then you can invoke the following command:

```./scale.py --mask-file=mask/covid_mask.stl --nose-to-chin-in-cm=<measurement>```

Above I am using the mask schematics that are in the repository at ```mask/covid_mask.stl```

### With directory (optional) ###

You can also provide the following options:

```./scale.py --mask-file=mask/covid_mask.stl --nose-to-chin-in-cm=<measurement> --output-dir=<some_output_dir>```

If this option is not provided then the script will create a dated output directory.

### Specify padding (optional) ###

An option for padding can also be provided. I am using a window seal which has 3mm thickness to pad around the insides of the mask. By deafault this script will take that length into account. If you want to add your padding then you can use the following command:

```./scale.py --mask-file=mask/covid_mask.stl --nose-to-chin-in-cm=<measurement> --padding-in-cm=<padding_measurement>```

### Other files to pick (optional) ###

You can also provide a regular expression to parse certain files in the input directory for example:

```./scale.py --mask-file=mask/covid_mask.stl --nose-to-chin-in-cm=<measurement> --output-dir=<some_output_dir> --rest-files-regex="covid.*stl"```

Along with the file pointed to by "--mask-file", this option will provide a regular expression to parse other stl files in the same directory as the input file and write out the scaled version to the output directory. If this option isn't provided then all stl file in the input directory will be picked up.

# Things to improve on

1) I am doing a very simple approach now of scaling a bounding box. There could be much finer grained fitting made but that will have to alter the geometry but also keeping the constraints of an FDM printer as well. This is probably more long term.

2) Provide some parameterisable gap for padding based on either pad length or user provided tolerance (DONE)

3) Take length from image of face: If this script is useful then further looking, my idea was to allow taking measurements from an image. To get proper dimensions, I would require a picture of the face along with something common like a debit/credit card like structure and from that I can get a reference size as I would know the size of the common object. The script won't save any of the images but will only acquire this length metric to calculate the scale factor. Based on this, I can detect where the face is and then where the nose is. After that I can define a recommended length from chin to a certain part of the nose for which the mask fitting will be best fit. This way all sizes will be created in a standard way.
