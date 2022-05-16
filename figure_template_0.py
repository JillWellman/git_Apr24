# patches example

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# The image
X = np.arange(16).reshape(4, 4)

# highlight some feature in the
# middle boxes.
fig = plt.figure()

ax = fig.add_subplot(111)
# grid of gray rectangles
ax.imshow(X, cmap = plt.cm.gray,  # cm = colormap
		interpolation ='nearest')

# green rectangle
ax.add_patch( Rectangle((0.5, 0.5),
						2, 2,
						fc ='none',
						ec ='g',
						lw = 10) )

plt.show()

