import torch
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset
import pandas as pd
import pickle
import os


class My_dataset(Dataset):
    """
    Dataset Class for any dataset.
    This is a python class object, it inherits functions from 
    the pytorch Dataset object.
    """

    def __init__(self, data_dir, anno_csv) -> object:
        self.anno_data = pd.read_csv(anno_csv)
        self.data_dir = data_dir

    def __len__(self):
        return len(self.anno_data)

    def __getitem__(self, idx):
        data_name = self.anno_data.iloc[idx, 0]
        data_location = os.path.join(self.data_dir, data_name)
        data = np.float32(np.load(data_location))
        # One-hot encoding of the output label
        gt_y = np.float32(np.zeros(10))
        index = self.anno_data.iloc[idx, 1]
        gt_y[index] = 1
        return data, gt_y


def init_weights(device="cpu"): # Init weights using random with a Xavier sigma = sqrt(2/n_input + n_output)
    np.random.seed(42)
    weights = [
        torch.tensor(np.random.randn(784, 100) * np.sqrt(6/(784+100)), dtype=torch.float32, device=device),
        torch.tensor(np.zeros((1, 100)), dtype=torch.float32, device=device),
        torch.tensor(np.random.randn(100, 100) * np.sqrt(6/(100+100)), dtype=torch.float32, device=device),
        torch.tensor(np.zeros((1, 100)), dtype=torch.float32, device=device),
        torch.tensor(np.random.randn(100, 10) * np.sqrt(6/(100+10)), dtype=torch.float32, device=device),
        torch.tensor(np.zeros((1, 10)), dtype=torch.float32, device=device)
    ]

    return weights


def PA2_train():
    # Specifying the training directory and label files
    train_dir = './'
    train_anno_file = './data_prog2Spring24/labels/train_anno.csv'

    # Specifying the device to GPU/CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    MNIST_training_dataset = My_dataset(data_dir=train_dir, anno_csv=train_anno_file)
    lr = .1 
    total_samples = 50000
    batch_size = 50
    total_batch = total_samples // batch_size
    my_max_epoch = 20
    epochs = np.arange(0, my_max_epoch)

    w = init_weights(device=device)
    train_losses = []
    train_errors = []

    for epoch in epochs:
        epoch_loss = 0
        correct = 0
        total = 0

        # mini batch
        indices = np.arange(total_samples)
        np.random.shuffle(indices)
        batches = [indices[i * batch_size:(i + 1) * batch_size] for i in range(total_batch)]

        for b, batch_indices in enumerate(batches):
            batch_data = [MNIST_training_dataset[idx] for idx in batch_indices]
            inputs, labels = zip(*batch_data)
            inputs = torch.tensor(np.array(inputs), dtype=torch.float32, device=device)
            labels = torch.tensor(np.array(labels), dtype=torch.float32, device=device)

            '''Forward pass'''
            Z1 = inputs @ w[0] + w[1]
            H1 = torch.maximum(Z1, torch.tensor(0.0, device=device))  # ReLU
            Z2 = H1 @ w[2] + w[3]
            H2 = torch.maximum(Z2, torch.tensor(0.0, device=device))
            Z3 = H2 @ w[4] + w[5]

            '''Softmax Calculation'''
            exp_Z3 = torch.exp(Z3 - torch.max(Z3, dim=1, keepdim=True)[0])
            softmax = exp_Z3 / torch.sum(exp_Z3, dim=1, keepdim=True)

            batch_size = inputs.shape[0]
            loss = -torch.mean(torch.sum(labels * torch.log(softmax + 1e-9), dim=1))
            epoch_loss += loss.item()

            '''Backprop'''
            dZ3 = (softmax - labels) / batch_size

            # third layer grad
            dW4 = H2.T @ dZ3
            dB4 = torch.sum(dZ3, dim=0, keepdim=True)

            # second layer grad
            dH2 = dZ3 @ w[4].T
            dZ2 = dH2 * (Z2 > 0).float()
            dW2 = H1.T @ dZ2
            dB2 = torch.sum(dZ2, dim=0, keepdim=True)

            # first layer grad
            dH1 = dZ2 @ w[2].T
            dZ1 = dH1 * (Z1 > 0).float()
            dW0 = inputs.T @ dZ1
            dB0 = torch.sum(dZ1, dim=0, keepdim=True)

            '''Update Weights'''
            with torch.no_grad():
                w[0] -= lr * dW0
                w[1] -= lr * dB0
                w[2] -= lr * dW2
                w[3] -= lr * dB2
                w[4] -= lr * dW4
                w[5] -= lr * dB4

            # Calculate accuracy
            predictions = torch.argmax(softmax, dim=1)
            true_labels = torch.argmax(labels, dim=1)
            correct += (predictions == true_labels).sum().item()
            total += true_labels.size(0)

        epoch_loss /= total_batch
        epoch_error = (correct / total) * 100
        train_losses.append(epoch_loss)
        train_errors.append(epoch_error)
        print(f"Epoch {epoch + 1}/{my_max_epoch}, Loss: {epoch_loss:.4f}, Accuracy: {epoch_error:.4f}")

    # save weights
    with open('trained_weights.pkl', 'wb') as f:
        pickle.dump(w, f)

    # Plot training loss and error
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(epochs + 1, train_losses, label='Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training Loss vs Epoch')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(epochs + 1, train_errors, label='Training Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('Training Accuracy vs Epoch')
    plt.legend()
    plt.show()


def PA2_test():
    # Specifying the testing directory and label files
    test_dir = './'
    test_anno_file = './data_prog2Spring24/labels/test_anno.csv'

    # Specifying the device to GPU/CPU
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # load trained weights
    with open('trained_weights.pkl', 'rb') as f:
        w = pickle.load(f)

    MNIST_testing_dataset = My_dataset(data_dir=test_dir, anno_csv=test_anno_file)

    # load all test data
    test_inputs = []
    test_labels = []
    for i in range(len(MNIST_testing_dataset)):
        inputs, labels = MNIST_testing_dataset[i]
        test_inputs.append(inputs)
        test_labels.append(labels)

    # put into torch tensors
    test_inputs = torch.tensor(np.array(test_inputs), dtype=torch.float32, device=device)
    test_labels = torch.tensor(np.array(test_labels), dtype=torch.float32, device=device)

    '''Forward pass'''
    Z1 = test_inputs @ w[0] + w[1]
    H1 = torch.maximum(Z1, torch.tensor(0.0, device=device))  # ReLU
    Z2 = H1 @ w[2] + w[3]
    H2 = torch.maximum(Z2, torch.tensor(0.0, device=device))
    Z3 = H2 @ w[4] + w[5]

    '''Softmax Calculation'''
    exp_Z3 = torch.exp(Z3 - torch.max(Z3, dim=1, keepdim=True)[0])
    softmax = exp_Z3 / torch.sum(exp_Z3, dim=1, keepdim=True)

    # calc acc
    predictions = torch.argmax(softmax, dim=1)
    true_labels = torch.argmax(test_labels, dim=1)
    correct = (predictions == true_labels).sum().item()
    total = true_labels.size(0)

    test_error = 1 - (correct / total)  # class errors
    print(f"Test Classification Error: {test_error:.4f}")

    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    predictions = predictions.cpu().numpy()
    true_labels = true_labels.cpu().numpy()

    # Compute confusion matrix
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    cm = confusion_matrix(true_labels, predictions, labels=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    # Plot confusion matrix
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Confusion Matrix for Test Set")
    plt.show()



if __name__ == "__main__":
    # PA2_train()
    PA2_test()