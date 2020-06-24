#!/usr/bin/env python
"""
Showcases basic features of PyPDF.
"""
from __future__ import print_function

from os import pardir
from os.path import abspath, basename, dirname, join
from sys import argv, path, stderr

from PyPDF4.pdf import PdfFileReader, PdfFileWriter

SAMPLE_CODE_ROOT = dirname(__file__)
SAMPLE_PDF_ROOT = join(SAMPLE_CODE_ROOT, "pdfsamples")

path.append(abspath(join(SAMPLE_CODE_ROOT, pardir)))


FLAG_HELP = {"-h", "--help"}
USAGE = """\
Showcases basic features of PyPDF.

%(progname)s: <input file> [output file]
%(progname)s: [-h | --help]
""" % {
    "progname": argv[0]
}


def main():
    pagesRequired = 5
    output = "PyPDF-Features-Output.pdf"

    if set(argv) & FLAG_HELP:
        print(USAGE)
        exit(0)
    elif len(argv) < 2:
        print(USAGE)
        exit(1)
    else:
        inputpath = argv[1].strip()
        filename = basename(inputpath)

        if len(argv) > 2:
            output = argv[2].strip()

    # We can instantiate a PdfFileReader/Writer by giving in a stream object
    # or a path string
    reader = PdfFileReader(open(inputpath, "rb"))
    writer = PdfFileWriter(output)

    # Check that the PDF file has the required number of pages
    if reader.numPages < pagesRequired:
        print(
            "We require a document with %d pages at least, %s has %d"
            % (pagesRequired, filename, reader.numPages),
            file=stderr,
        )
        exit(1)
    else:
        print("'%s' has %d pages... OK" % (filename, reader.numPages))

    # Add page 1 from reader to output document, unchanged
    writer.addPage(reader.getPage(0))

    # Add page 2 from reader, but rotated clockwise 90 degrees
    writer.addPage(reader.getPage(1).rotateClockwise(90))

    # Add page 3 from reader, rotated the other way:
    writer.addPage(reader.getPage(2).rotateCounterClockwise(90))
    # Alt.: writer.addPage(reader.getPage(2).rotateClockwise(270))

    # Add page 4 from reader, but first add a watermark from another PDF:
    page4 = reader.getPage(3)
    watermark = PdfFileReader(open(join(SAMPLE_PDF_ROOT, "AutoCad_Diagram.pdf"), "rb"))
    page4.mergePage(watermark.getPage(0))
    writer.addPage(page4)

    # Add page 5 from reader, but crop it to half size:
    page5 = reader.getPage(4)
    page5.mediaBox.upperRight = (
        page5.mediaBox.getUpperRight_x() / 2,
        page5.mediaBox.getUpperRight_y() / 2,
    )
    writer.addPage(page5)

    # Add some Javascript to launch the print window on opening this PDF.
    # The password dialog may prevent the print dialog from being shown.
    # Comment the encrypted lines, if that's the case, to try this out
    writer.addJS("this.print({bUI:true,bSilent:false,bShrinkToFit:true});")

    # Encrypt your new PDF and add a password
    password = "secret"
    writer.encrypt(password)

    # Finally, write the resulting PDF document to ``output``
    writer.write()

    print("Output successfully written to", output)

    reader.close()
    writer.close()


if __name__ == "__main__":
    main()
