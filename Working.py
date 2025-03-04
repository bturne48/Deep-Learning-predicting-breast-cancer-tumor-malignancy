import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn import metrics
from sklearn.metrics import confusion_matrix
import itertools

np.set_printoptions(threshold=np.inf)

def plotCf(a,b,t):
    cf =confusion_matrix(a,b)
    plt.imshow(cf,cmap=plt.cm.Blues,interpolation='nearest')
    plt.colorbar()
    plt.title(t)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    tick_marks = np.arange(len(set(a))) # length of classes
    class_labels = ['0','1']
    plt.xticks(tick_marks,class_labels)
    plt.yticks(tick_marks,class_labels)
    thresh = cf.max() / 2.
    for i,j in itertools.product(range(cf.shape[0]),range(cf.shape[1])):
        plt.text(j,i,format(cf[i,j],'d'),horizontalalignment='center',color='white' if cf[i,j] >thresh else 'black')
    plt.show();


def Sigmoid(Z):
    return 1 / (1 + np.exp(-Z))


def Relu(Z):
    return np.maximum(0, Z)


def dRelu2(dZ, Z):
    dZ[Z <= 0] = 0
    return dZ


def dRelu(x):
    x[x <= 0] = 0
    x[x > 0] = 1
    return x


def dSigmoid(Z):
    s = 1 / (1 + np.exp(-Z))
    dZ = s * (1 - s)
    return dZ


class dlnet:
    def __init__(self, x, y):
        self.debug = 0;
        self.X = x
        self.Y = y
        self.Yh = np.zeros((1, self.Y.shape[1]))
        self.L = 2
        self.dims = [9, 15, 1]
        self.param = {}
        self.ch = {}
        self.grad = {}
        self.loss = []
        self.lr = 0.003
        self.sam = self.Y.shape[1]
        self.threshold = 0.5

    def nInit(self):
        np.random.seed(1)
        self.param['W1'] = np.random.randn(self.dims[1], self.dims[0]) / np.sqrt(self.dims[0])
        self.param['b1'] = np.zeros((self.dims[1], 1))
        self.param['W2'] = np.random.randn(self.dims[2], self.dims[1]) / np.sqrt(self.dims[1])
        self.param['b2'] = np.zeros((self.dims[2], 1))
        return

    def forward(self):
        Z1 = self.param['W1'].dot(self.X) + self.param['b1']
        A1 = Relu(Z1)
        self.ch['Z1'], self.ch['A1'] = Z1, A1

        Z2 = self.param['W2'].dot(A1) + self.param['b2']
        A2 = Sigmoid(Z2)
        self.ch['Z2'], self.ch['A2'] = Z2, A2

        self.Yh = A2
        loss = self.nloss(A2)
        return self.Yh, loss

    def nloss(self, Yh):
        loss = (1. / self.sam) * (-np.dot(self.Y, np.log(Yh).T) - np.dot(1 - self.Y, np.log(1 - Yh).T))
        return loss

    def backward(self):
        dLoss_Yh = - (np.divide(self.Y, self.Yh) - np.divide(1 - self.Y, 1 - self.Yh))

        dLoss_Z2 = dLoss_Yh * dSigmoid(self.ch['Z2'])
        dLoss_A1 = np.dot(self.param["W2"].T, dLoss_Z2)
        dLoss_W2 = 1. / self.ch['A1'].shape[1] * np.dot(dLoss_Z2, self.ch['A1'].T)
        dLoss_b2 = 1. / self.ch['A1'].shape[1] * np.dot(dLoss_Z2, np.ones([dLoss_Z2.shape[1], 1]))

        dLoss_Z1 = dLoss_A1 * dRelu(self.ch['Z1'])
        dLoss_A0 = np.dot(self.param["W1"].T, dLoss_Z1)
        dLoss_W1 = 1. / self.X.shape[1] * np.dot(dLoss_Z1, self.X.T)
        dLoss_b1 = 1. / self.X.shape[1] * np.dot(dLoss_Z1, np.ones([dLoss_Z1.shape[1], 1]))

        self.param["W1"] = self.param["W1"] - self.lr * dLoss_W1
        self.param["b1"] = self.param["b1"] - self.lr * dLoss_b1
        self.param["W2"] = self.param["W2"] - self.lr * dLoss_W2
        self.param["b2"] = self.param["b2"] - self.lr * dLoss_b2

        return

    def pred(self, x, y):
        self.X = x
        self.Y = y
        comp = np.zeros((1, x.shape[1]))
        pred, loss = self.forward()

        for i in range(0, pred.shape[1]):
            if pred[0, i] > self.threshold:
                comp[0, i] = 1
            else:
                comp[0, i] = 0

        print("Acc: " + str(np.sum((comp == y) / x.shape[1])))

        return comp

    def gd(self, X, Y, iter=3000):
        np.random.seed(1)

        self.nInit()

        for i in range(0, iter):
            Yh, loss = self.forward()
            self.backward()

            if i % 500 == 0:
                print("Cost after iteration %i: %f" % (i, loss))
                self.loss.append(loss)

        plt.plot(np.squeeze(self.loss))
        plt.ylabel('Loss')
        plt.xlabel('Iter')
        plt.title("Lr =" + str(self.lr))
        plt.show()

        return
# (683, 11) (9, 500) (1, 500) (9, 182) (1, 182)
# df = pd.read_csv('wisconsin-cancer-dataset.csv',header=None)
# df = df[~df[6].isin(['?'])]
# df = df.astype(float)
# df.iloc[:,10].replace(2, 0,inplace=True)
# df.iloc[:,10].replace(4, 1,inplace=True)
#
# df.head(3)
# scaled_df=df
# names = df.columns[0:10]
# scaler = MinMaxScaler()
# scaled_df = scaler.fit_transform(df.iloc[:,0:10])
# scaled_df = pd.DataFrame(scaled_df, columns=names)
# x=scaled_df.iloc[0:500,1:10].values.transpose()
# y=df.iloc[0:500,10:].values.transpose()
#
# xval=scaled_df.iloc[501:683,1:10].values.transpose()
# yval=df.iloc[501:683,10:].values.transpose()

#print(df.shape, x.shape, y.shape, xval.shape, yval.shape)

#nn = dlnet(x,y)
#nn.lr=0.07
#nn.dims = [9, 15, 1]




df = pd.read_csv('wdbc.data',header=None)
df.iloc[:,1].replace('B', 0,inplace=True)
df.iloc[:,1].replace('M', 1,inplace=True)
df = df.astype(float)

df.head(3)
scaled_df=df
names = df.columns[1:13]
scaler = MinMaxScaler()
scaled_df = scaler.fit_transform(df.iloc[:,1:13])
#print(scaled_df)
scaled_df = pd.DataFrame(scaled_df, columns=names)

x=scaled_df.iloc[0:500,2:13].values.transpose()
y=df.iloc[0:500,1].values.transpose()
y = np.array([y])


xval=scaled_df.iloc[501:,2:13].values.transpose()
print(xval.shape)
yval=df.iloc[501:,1].values.transpose()
yval = np.array([yval])

print(df.shape, x.shape, y.shape, xval.shape, yval.shape)

nn = dlnet(x,y)
nn.lr=0.01
nn.dims = [10, 15, 1]

nn.gd(x, y, iter = 40000)

pred_train = nn.pred(x, y)
pred_test = nn.pred(xval, yval)

nn.threshold=0.5

nn.X,nn.Y=x, y
target=np.around(np.squeeze(y), decimals=0).astype(np.int)
predicted=np.around(np.squeeze(nn.pred(x,y)), decimals=0).astype(np.int)
plotCf(target,predicted,'Cf Training Set')

nn.X,nn.Y=xval, yval
target=np.around(np.squeeze(yval), decimals=0).astype(np.int)
predicted=np.around(np.squeeze(nn.pred(xval,yval)), decimals=0).astype(np.int)
plotCf(target,predicted,'Cf Validation Set')


loo.get_n_splits(x)

preds = []#

for train_index, test_index in loo.split(x):
    nn = dlnet(x,y)
    nn.lr = 0.01
    nn.dims = [10, 15, 15, 1]
    #print(train_index, test_index)
    x_train, x_test = x[train_index], x[test_index]
    y_train, y_test = y[train_index], y[test_index]
    #print(x_train)
    x_train = x_train.transpose()
    y_train = np.array([y_train.transpose()])
    x_test = x_test.transpose()
    y_test = np.array([y_test.transpose()])
    print(f" x_train.shape: {x_train.shape}, y_train.shape: {y_train.shape}, x_test.shape: {x_test.shape}, y_test.shape: {y_test.shape}")

    nn.gd(x_train, y_train, iter=40000)