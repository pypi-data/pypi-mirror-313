This is neural network training library
#######################################
Examples:
#######################################
#       Example 1 - N+1               #
#######################################
import neuralcat
import numpy as np

inputs=np.array([[1],[2]])
outputs=np.array([[2],[3]])
model=neuralcat.Model()
model.add(neuralcat.layers.MRELU(16))
model.train(inputs, outputs, True,optim=neuralcat.optimize.Adam(0.01), loss=neuralcat.losses.MSE(),epochs=500,logging=False)
pred=model(np.array([[1]]]))
answer=''
for i in pred:
	answer=i[0]
print(answer)
#######################################