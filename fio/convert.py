import os
import gzip
import uuid

replacements = {'test': 'one', 'temp': 'tmp'}

files = [f for f in os.listdir('./rawfiles/') if str(f).endswith('.gz')]
for f in files:

    with gzip.open('./rawfiles/' + f) as zfile:

        filename = str(uuid.uuid4()).upper()
        filename = filename.translate(None, '-') + '.log'

        with open('./logfiles/' + filename, 'w') as outfile:

            for line in zfile:
                for src, target in replacements.iteritems():
                    line = line.replace(src, target)
                outfile.write(line)
