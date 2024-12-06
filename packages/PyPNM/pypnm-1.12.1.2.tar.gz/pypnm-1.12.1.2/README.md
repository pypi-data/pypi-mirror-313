# PyPNM - PPM and PGM image files reading and writing

## Justification and Overview

PPM and PGM (particular cases on PNM format group) are simplest file formats for RGB and L images, correspondingly. This simplicity lead to some consequences:

- lack of strict official specification. Instead, you may find words like "usual" in format description. Surely, there is someone who implement this part of image format in unprohibited, yet a totally unusual way.

- unwillingness of many software developers to provide any good support to for simple and open format. It took years for almighty Adobe Photoshop developers to include PNM module in distribution rather than count on third-party developers, and surely (see above) they used this chance to implement their own unusual separator scheme nobody else uses. What as to PNM support in Python, say, Pillow... sorry, I promised not to mention Pillow anywhere ladies and children are allowed to read it.

As a result, novice Python user (like me) may find it difficult to get reliable input/output modules for PPM and PGM image formats; therefore current PyPNM package was developed, combining input/output functions for 8-bits and 16-bits per channel binary and ascii PGM and PPM files, i.e. P2, P5, P3 and P6 PNM file types.

## Target Image representation

Is seems logical to represent e.g. an RGB image as nested 3D structure - X, Y-sized matrix of three-component RGB vectors. Since in Python list seem to be about the only variant for mutable structures like that, it is suitable to represent image as list(list(list(int))) structure. Therefore, it would be convenient to have module read/write image data to/from such a structure.

## pnmlpnm.py

Module **pnmlpnm.py** contains 100% pure Python implementation of everything one may need to read/write a variety of PGM and PPM files. I/O functions are written as functions/procedures, as simple as possible, and listed below:

- **pnm2list**  - reading binary or ascii RGB PPM or L PGM file and returning image data as ints and nested list.
- **list2bin**  - getting image data as ints and nested list and creating binary PPM (P6) or PGM (P5) data structure in memory. Suitable for generating data to display with Tkinter.
- **list2pnm**  - writing data created with list2bin to file.
- **list2pnmascii** - alternative function to write ASCII PPM (P3) or PGM (P2) files.
- **create_image** - creating empty nested 3D list for image representation. Not used within this particular module but often needed by programs this module is supposed to be used with.

Detailed functions arguments description is provided below as well as in docstrings, but in general looks simple like that - you feed the function with your image data list and a filename, and get PNM file with that name written.

### pnm2list

`X, Y, Z, maxcolors, image3D = pnmlpnm.pnm2list(in_filename)`

read data from PPM/PGM file, where:

- `X, Y, Z`   - image sizes (int);
- `maxcolors` - number of colors per channel for current image (int);
- `image3D`   - image pixel data as list(list(list(int)));
- `in_filename` - PPM/PGM file name (str).

### list2bin

`image_bytes = pnmlpnm.list2bin(image3D, maxcolors)`

Convert nested image data list to PGM P5 or PPM P6 (binary) data structure in memory, where:

- `image3D`   - `Y*X*Z` list (image) of lists (rows) of lists (pixels) of ints (channels);
- `maxcolors` - number of colors per channel for current image (int).
- `image_bytes` - PNM-structured binary data.

### list2pnm

`pnmlpnm.list2pnm(out_filename, image3D, maxcolors)` where:

- `image3D`   - `Y*X*Z` list (image) of lists (rows) of lists (pixels) of ints (channels);
- `maxcolors` - number of colors per channel for current image (int).
- `out_filename` - PNM file name.

### list2pnmascii

Similar to `list2pnm` above but creates ascii pnm file instead of binary.

`pnmlpnm.list2pnmascii(out_filename, image3D, maxcolors)` where:

- `image3D`   - `Y*X*Z` list (image) of lists (rows) of lists (pixels) of ints (channels);
- `maxcolors` - number of colors per channel for current image (int).
- `out_filename` - PNM file name.

### create_image

Create empty 3D nested list of `X*Y*Z` sizes.

### References

[Netpbm file formats description](https://netpbm.sourceforge.net/doc/)

[PyPNM page](https://dnyarri.github.io/pypnm.html) - contains example application of using `list2bin` to produce data for Tkinter `PhotoImage(data=...)` to display.
